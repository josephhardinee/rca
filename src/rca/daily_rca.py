#!/usr/bin/env python
import numpy as np
import os
import glob
import json
from netCDF4 import Dataset
import pandas as pd
from .aux.file_to_radar_object import file_to_radar_object
from .aux.get_var_arrays_from_radar_object import get_var_arrays_from_radar_object
from .calculate_dbz95 import calculate_dbz95_ppi, calculate_dbz95_rhi


def daily_rca(radar_config_file, date, filters=True):
    """
    daily_rca loops through a day's worth of radar files (specify PPI or HSRHI, dual or horizontal polarization),
    calculates the median daily 95th percentile clutter area reflectivity,
    computes the RCA value using the established baseline 95h percentile clutter area reflectivity.
    
    A running CSV is ammended to include the daily median RCA values.
    
    Parameters
    ----------
    radar_config_file: str
        path to JSON file containing specifications: data directory, file extension, clutter map directory, baseline directory, baseline date, daily CSV directory, scan type, polarization, site, instrument, range limit
    date: str
        YYYYMMDD specifying date of interest
    filters: boolean
        Include IAH and RH filters
                    
    """

    config_vars = json.load(open(radar_config_file))
    datadir = config_vars["data_directory"]
    extension = config_vars["file_extension"]
    cluttermap_dir = config_vars["cluttermap_directory"]
    baseline_dir = config_vars["baseline_directory"]
    baseline_date = config_vars["baseline_date"]
    dailycsvdir = config_vars["daily_csv_dir"]
    scantype = config_vars["scan_type"]
    polarization = config_vars["polarization"]
    site = config_vars["site_abbrev"]
    inst = config_vars["instrument_abbrev"]
    range_limit = config_vars["range_limit"]

    # Identify which radar band you are using (change if statement as needed)
    # Most important to identify Ka-band radars
    if inst == "kasacr":
        radar_band = "ka"
    else:
        radar_band = inst[0]

    daily_csv_fullpath = (
        dailycsvdir + "daily_rca_" + scantype + "_" + site + inst + ".csv"
    )

    hourly_csv_fullpath = (
        dailycsvdir + "hourlies/"  + "hourly_rca_" + scantype + "_" + site + inst + "_" + date + ".csv"
    )

    # Read in clutter map netCDF and baseline value netCDF
    dataset = Dataset(
        cluttermap_dir
        + "cluttermap_"
        + scantype
        + "_"
        + site
        + inst
        + "_"
        + "composite"
        + ".nc"
    )
    dataset_b = Dataset(
        baseline_dir
        + "baseline_"
        + scantype
        + "_"
        + site
        + inst
        + "_"
        + baseline_date
        + ".nc"
    )
    if scantype == "ppi":
        clutter_map_mask_h = dataset.variables["clutter_map_mask_zh"][:, :]
        baseline_dbz95_h = dataset_b.variables["baseline_dbz95_zh"][:]
    elif scantype == "rhi":
        clutter_map_mask_h = dataset.variables["clutter_map_mask_zh"][:, :, :]
        baseline_dbz95_h = dataset_b.variables["baseline_dbz95_zh"][:]
    if polarization == "dual" and scantype == "ppi":
        clutter_map_mask_v = dataset.variables["clutter_map_mask_zv"][:, :]
        baseline_dbz95_v = dataset_b.variables["baseline_dbz95_zv"][:]
    elif polarization == "dual" and scantype == "rhi":
        clutter_map_mask_v = dataset.variables["clutter_map_mask_zv"][:, :, :]
        baseline_dbz95_v = dataset_b.variables["baseline_dbz95_zv"][:]
    dataset.close()
    dataset_b.close()

    # Prep for filters, if argument is set to True (read in and grab variables)
    if filters==True:
        dataset_f = Dataset(
                    dailycsvdir+"/filters/"
                    + "filters_"
                    + scantype
                    + "_"
                    + site
                    + inst
                    + "_"
                    + date
                    + ".nc"
        )

        total_filter = dataset_f.variables["iah_and_rh_filter"][:]
        rh_value = dataset_f.variables["rh_value"][:]
        #datetime = dataset_f.variables["datetime"][:]
        dataset_f.close()

    # Empty lists to fill in loops below
    date_time = []  # date and time strings
    dbz95_h = []  # 95th percentile reflectivity in H
    dbz95_v = []  # 95th percentile reflectivity in V
    num_pts_h = []
    num_pts_v = []
    pass_filter = []

    # Read in each radar file and turn into radar object and use function to
    # calculate 95th percentile clutter area reflectivity

    # Will use glob, so grab all files and then sort by datetime
    files = []
    for f in glob.glob(os.path.join(datadir, "*" + date + "*.??")):
        files.append(f)
    files.sort()

    if polarization == "horizontal":
        for idx_f, f in enumerate(files):
            print(f)
            radar = file_to_radar_object(f, extension)
            var_dict = get_var_arrays_from_radar_object(radar, radar_config_file)
            if scantype == "ppi":
                dt, s_h = calculate_dbz95_ppi(
                    var_dict,
                    polarization,
                    range_limit,
                    radar_band,
                    clutter_map_mask_h,
                    clutter_mask_v=None,
                )
            elif scantype == "rhi":
                dt, s_h = calculate_dbz95_rhi(
                    var_dict,
                    polarization,
                    range_limit,
                    radar_band,
                    clutter_map_mask_h,
                    clutter_mask_v=None,
                )
            date_time.append(dt[0:19])
            dbz95_h.append(s_h["reflectivity_95"])
            num_pts_h.append(s_h["num_points"])

            if filters==True:
                # Read in filters array
                pass_filter.append(total_filter[idx_f])
            
            # Calculate RCA for the file
            rca_h_file = baseline_dbz95_h[0] - s_h["reflectivity_95"]
            print(dt[0:19],rca_h_file)

            # Create dictionary and dataframe for hourly CSV
            csv_frame = pd.read_csv(hourly_csv_fullpath)
            if filters==True:
                rca_dict = {
                    "DATE": dt[0:19],
                    "RCA_H": rca_h_file,
                    "RCA_V": np.nan, 
                    "NUM_PTS": s_h['num_points'], 
                    "NUM_PTS_V": np.nan,
                    "PASS_FILTER": total_filter[idx_f],
                    "RH": rh_value[idx_f]
                }
            else:
                rca_dict = {
                    "DATE": dt[0:19],
                    "RCA_H": rca_h_file,
                    "RCA_V": np.nan, 
                    "NUM_PTS": s_h['num_points'],
                    "NUM_PTS_V": np.nan
                }
            csv_frame = csv_frame.append(rca_dict, ignore_index=True)
            csv_frame.set_index("DATE")
            csv_frame.to_csv(hourly_csv_fullpath, index=False)

        # Calculate median 95th percentile clutter area reflecitivty from all times in day
        # and total the number of points from files
        dbz95_h = np.array(dbz95_h)
        num_pts_h = np.array(num_pts_h)
        if filters==True:
            pass_filter = np.array(pass_filter)
            dbz95_h_mean = np.nanmedian(dbz95_h[pass_filter > 0])
            total_num_pts_h = np.nansum(num_pts_h[pass_filter > 0])
        else:
            dbz95_h_mean = np.nanmedian(dbz95_h)
            total_num_pts_h = np.nansum(num_pts_h)

        # Calculate RCA
        rca_h = baseline_dbz95_h[0] - dbz95_h_mean
        yr = date[0:4]
        mon = date[4:6]
        day = date[6:]
        date = yr + "-" + mon + "-" + day

        # Create dictionary and dataframe for daily CSV
        csv_frame = pd.read_csv(daily_csv_fullpath)
        rca_dict = {
            "DATE": date,
            "RCA_H": rca_h,
            "RCA_V": np.nan,
            "NUM_PTS_H": total_num_pts_h,
            "NUM_PTS_V": np.nan
        }
        csv_frame = csv_frame.append(rca_dict, ignore_index=True)
        csv_frame.set_index("DATE")
        csv_frame.to_csv(daily_csv_fullpath, index=False)

    elif polarization == "dual":
        for idx_f, f in enumerate(files):
            print(f)
            radar = file_to_radar_object(f, extension)
            var_dict = get_var_arrays_from_radar_object(radar, radar_config_file)
            if scantype == "ppi":
                dt, s_h, s_v = calculate_dbz95_ppi(
                    var_dict,
                    polarization,
                    range_limit,
                    radar_band,
                    clutter_map_mask_h,
                    clutter_mask_v=clutter_map_mask_v,
                )
            elif scantype == "rhi":
                dt, s_h, s_v = calculate_dbz95_rhi(
                    var_dict,
                    polarization,
                    range_limit,
                    radar_band,
                    clutter_map_mask_h,
                    clutter_mask_v=clutter_map_mask_v,
                )
            date_time.append(dt)
            dbz95_h.append(s_h["reflectivity_95"])
            num_pts_h.append(s_h["num_points"])
            dbz95_v.append(s_v["reflectivity_95"])
            num_pts_v.append(s_v["num_points"])

            if filters==True:
                # Read in filters array
                pass_filter.append(total_filter[idx_f])
                rh.append(rh_values[idx_f])

            # Calculate RCA for the file
            rca_h_file = baseline_dbz95_h[0] - s_h["reflectivity_95"]
            rca_v_file = baseline_dbz95_v[0] - s_v["reflectivity_95"]

            # Create dictionary and dataframe for hourly CSV
            csv_frame = pd.read_csv(hourly_csv_fullpath)
            if filters==True:
                rca_dict = {
                    "DATE": dt[0:19],
                    "RCA_H": rca_h_file,
                    "RCA_V": rca_v_file, 
                    "NUM_PTS": s_h['num_points'], 
                    "NUM_PTS_V": s_v['num_points'],
                    "PASS_FILTER": total_filter[idx_f],
                    "RH": rh_values[idx_f]
                }
            else:
                rca_dict = {
                    "DATE": dt[0:19],
                    "RCA_H": rca_h_file,
                    "RCA_V": rca_v_file, 
                    "NUM_PTS": s_h['num_points'],
                    "NUM_PTS_V": s_h['num_points']
                }
            csv_frame = csv_frame.append(rca_dict, ignore_index=True)
            csv_frame.set_index("DATE")

        # Calculate median 95th percentile clutter area reflecitivty from all times in day
        dbz95_h = np.array(dbz95_h)
        dbz95_v = np.array(dbz95_v)
        num_pts_h = np.array(num_pts_h)
        num_pts_v = np.array(num_pts_v)
        if filters==True:
            pass_filter = np.array(pass_filter)
            dbz95_h_mean = np.nanmedian(dbz95_h[pass_filter > 0])
            dbz95_v_mean = np.nanmedian(dbz95_v[pass_filter > 0])
            # Total up the number of points from all files
            total_num_pts_h = np.nansum(num_pts_h[pass_filter > 0])
            total_num_pts_v = np.nansum(num_pts_v[pass_filter > 0])
        else:
            dbz95_h_mean = np.nanmedian(dbz95_h)
            dbz95_v_mean = np.nanmedian(dbz95_v)
            # Total up the number of points from all files
            total_num_pts_h = np.nansum(num_pts_h)
            total_num_pts_v = np.nansum(num_pts_v)

        # Calculate RCA
        rca_h = baseline_dbz95_h[0] - dbz95_h_mean
        rca_v = baseline_dbz95_v[0] - dbz95_v_mean
        yr = date[0:4]
        mon = date[4:6]
        day = date[6:]
        date = yr + "-" + mon + "-" + day

        # Create dictionary and dataframe
        csv_frame = pd.read_csv(daily_csv_fullpath)
        rca_dict = {
            "DATE": date,
            "RCA_H": rca_h,
            "RCA_V": rca_v,
            "NUM_PTS_H": total_num_pts_h,
            "NUM_PTS_V": total_num_pts_v,
        }
        csv_frame = csv_frame.append(rca_dict, ignore_index=True)
        csv_frame.set_index("DATE")
        csv_frame.to_csv(daily_csv_fullpath, index=False)
