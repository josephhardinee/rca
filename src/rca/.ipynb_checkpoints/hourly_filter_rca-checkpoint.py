#!/usr/bin/env python
import numpy as np
import os
import glob
import json
from netCDF4 import Dataset
import pandas as pd
from .aux.file_to_radar_object import file_to_radar_object
from .aux.get_var_arrays_from_radar_object import get_var_arrays_from_radar_object
from .calculate_dbz95 import calculate_dbz95_ppi, calculate_dbz95_hsrhi
import matplotlib.pyplot as plt

def hourly_filter_rca(radar_config_file, date):
    """
    hourly_rca loops through a day's worth of radar files (specify PPI or HSRHI,
dual or horizontal polarization),
    computes the RCA value using the established baseline 95h percentile
clutter area reflectivity.
    
    A running CSV is ammended to include the hourly (or each scan time) median RCA values.
    
    Parameters
    ----------
    radar_config_file: str
        path to JSON file containing specifications: data directory, file
extension, clutter map directory, baseline directory, baseline date, daily CSV
directory, scan type, polarization, site, instrument, range limit
    date: str
        YYYYMMDD specifying date of interest
                    
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

    hourly_csv_fullpath = (dailycsvdir + "hourly_rca_" + scantype + "_" + site + inst + "_" + date + "_filter_dropzero.csv")
    #hourly_csv_fullpath = (dailycsvdir + "hourly_rca_" + scantype + "_" + site + inst + "_" + date + "_strictaz.csv")

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
       # + "_strict"
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

    # Empty lists to fill in loops below
    date_time = []  # date and time strings
    dbz95_h = []  # 95th percentile reflectivity in H
    dbz95_v = []  # 95th percentile reflectivity in V
    stats_h = []  # dictionary of statistics in H
    stats_v = []  # dictionary of statistics in V
    az_list = []
    el_list = []
    num_list = []
    # Read in each radar file and turn into radar object and use function to
    # calculate 95th percentile clutter area reflectivity
    if polarization == "horizontal":
        for f in glob.glob(os.path.join(datadir, "*" + date + ".*.??")):
        #for f in glob.glob(os.path.join(datadir, "*" + date + ".18*.??")):
            print(f)
            radar = file_to_radar_object(f, extension)
            var_dict = get_var_arrays_from_radar_object(radar,radar_config_file)
            if scantype == "ppi":
                dt, d95_h, s_h = calculate_dbz95_ppi(
                    var_dict,
                    polarization,
                    range_limit,
                    clutter_map_mask_h,
                    clutter_mask_v=None,
                )
            elif scantype == "rhi":
                dt, d95_h, s_h = calculate_dbz95_hsrhi(
                    var_dict,
                    polarization,
                    range_limit,
                    clutter_map_mask_h,
                    clutter_mask_v=None,
                )
            #az_list.append(az)
            #el_list.append(el)
            #num_list.append(s_h['num_points'])
            #date_time.append(dt)
            #dbz95_h.append(d95_h)
            #stats_h.append(s_h)
        # Calculate median 95th percentile clutter area reflecitivty from all
        # times in day
        #dbz95_h_mean = np.nanmedian(dbz95_h)
        # Calculate RCA
            rca_h = baseline_dbz95_h[0] - d95_h
            yr = date[0:4]
            mon = date[4:6]
            day = date[6:]
            base = 0  # set to 0 for daily RCA, set to 1 when calculating for baseline
            date = yr + "-" + mon + "-" + day
            dt = dt[0:19]
            # Create dictionary and dataframe
            csv_frame = pd.read_csv(hourly_csv_fullpath)
            rca_dict = {"DATE": dt, "RCA_H": rca_h, "RCA_V":np.nan, "NUM_PTS":s_h['num_points'], "PASS_FILTER":s_h['pass_filter']}
            #rca_dict = {"DATE": dt, "RCA_H":rca_h,"RCA_V":np.nan,"BASELINE":base}
            csv_frame = csv_frame.append(rca_dict, ignore_index=True)
            csv_frame.set_index("DATE")
            csv_frame.to_csv(hourly_csv_fullpath, index=False)
            
        
        #fig, ax = plt.subplots(figsize=[8,6])
        #ax = plt.gca()
        #for idx_i,a in enumerate(az_list):
        #    if num_list[idx_i] > 12000:
        #        color = 'red'
        #    else:
        #        color = 'blue'
        #    ax.plot(a, c=color)
        #ax.set_title('Azimuth for KaSACR HSRHIs 2019-01-23 05UTC')
        #ax.set_ylabel('azimuth (deg)')
        #plt.savefig(dailycsvdir+'kasacr_20190123_05_azimuth.png')        
        
        #fig, ax = plt.subplots(figsize=[8,6])
        #ax = plt.gca()
        #for idx_i,e in enumerate(el_list):
        #    if num_list[idx_i] > 12000:
        #        color = 'red'
        #    else:
        #        color = 'blue'
        #    ax.plot(e, c=color)
        #ax.set_title('Elevation for KaSACR HSRHIs 2019-01-23 05UTC')
        #ax.set_ylabel('elevation (deg)')
        #plt.savefig(dailycsvdir+'kasacr_20190123_05_elevation.png')

    elif polarization == "dual":
        for f in glob.glob(os.path.join(datadir, "*" + date + "*.??")):
            print(f)
            radar = file_to_radar_object(f, extension)
            var_dict = get_var_arrays_from_radar_object(radar,radar_config_file)
            if scantype == "ppi":
                dt, d95_h, d95_v, s_h, s_v = calculate_dbz95_ppi(
                    var_dict,
                    polarization,
                    range_limit,
                    clutter_map_mask_h,
                    clutter_mask_v=clutter_map_mask_v,
                )
            elif scantype == "rhi":
                dt, d95_h, d95_v, s_h, s_v = calculate_dbz95_hsrhi(
                    var_dict,
                    polarization,
                    range_limit,
                    clutter_map_mask_h,
                    clutter_mask_v=clutter_map_mask_v,
                )
            #date_time.append(dt)
            #dbz95_h.append(d95_h)
            #stats_h.append(s_h)
            #dbz95_v.append(d95_v)
            #stats_v.append(s_v)

        # Calculate median 95th percentile clutter area reflecitivty from all
        # times in day
        #dbz95_h_mean = np.nanmedian(dbz95_h)
        #dbz95_v_mean = np.nanmedian(dbz95_v)
            # Calculate RCA
            rca_h = baseline_dbz95_h[0] - d95_h
            rca_v = baseline_dbz95_v[0] - d95_v
            yr = date[0:4]
            mon = date[4:6]
            day = date[6:]
            base = 0  # set to 0 for daily RCA, set to 1 when calculating for baseline
            date = yr + "-" + mon + "-" + day
            # Create dictionary and dataframe
            csv_frame = pd.read_csv(hourly_csv_fullpath)
            rca_dict = {"DATE": dt, "RCA_H": rca_h, "RCA_V":rca_v,"NUM_PTS":s_h['num_points'], "NUM_PTS_V":s_v['num_points']}
            csv_frame = csv_frame.append(rca_dict, ignore_index=True)
            csv_frame.set_index("DATE")
            csv_frame.to_csv(hourly_csv_fullpath, index=False)
