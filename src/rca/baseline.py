#!/usr/bin/env python
import numpy as np
import os
import glob
import json
from netCDF4 import Dataset
from file_to_radar_object import file_to_radar_object
from get_var_arrays_from_radar_object import get_var_arrays_from_radar_object
from calculate_dbz95 import calculate_dbz95_ppi, calculate_dbz95_hsrhi


def baseline(radar_config_file):
    """
    baseline.py loops through a day's worth of radar files (specify PPI or HSRHI),
    calculates the median daily 95th percentile clutter area reflectivity,
    and saves the value to a netCDF as the baseline 95th percentile clutter area reflectivity.
    
    Parameters:
    --------------
    radar_config_file: str
                path to JSON file containing specifications:
                    data directory
                    file extension
                    clutter map directory
                    output directory for baseline netCDF
                    baseline date
                    scan type
                    polarization
                    site
                    instrument
                    range limit
                    
    Returns:
    --------------
    (no specific return)
    however, a netCDF file is written out
    """
    config_vars = json.load(open(radar_config_file))
    datadir = config_vars["data_directory"]
    extension = config_vars["file_extension"]
    cluttermap_dir = config_vars["cluttermap_directory"]
    baseline_dir = config_vars["baseline_directory"]
    baseline_date = config_vars["baseline_date"]
    scantype = config_vars["scan_type"]
    polarization = config_vars["polarization"]
    site = config_vars["site_abbrev"]
    inst = config_vars["instrument_abbrev"]
    range_limit = config_vars["range_limit"]

    # Read in clutter map netCDF
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
    if scantype == "ppi":
        clutter_map_mask_h = dataset.variables["clutter_map_mask_zh"][:, :]
    elif scantype == "rhi":
        clutter_map_mask_h = dataset.variables["clutter_map_mask_zh"][:, :, :]
    if polarization == "dual" and scantype == "ppi":
        clutter_map_mask_v = dataset.variables["clutter_map_mask_zv"][:, :]
    elif polarization == "dual" and scantype == "rhi":
        clutter_map_mask_v = dataset.variables["clutter_map_mask_zv"][:, :, :]
    dataset.close()

    # Empty lists to fill in loops below
    date_time = []  # date and time strings
    dbz95_h = []  # 95th percentile reflectivity in H
    dbz95_v = []  # 95th percentile reflectivity in V
    stats_h = []  # dictionary of statistics in H
    stats_v = []  # dictionary of statistics in V

    # Read in each radar file and turn into radar object and use function to
    # calculate 95th percentile clutter area reflectivity
    if polarization == "horizontal":
        for f in glob.glob(os.path.join(datadir, "*" + baseline_date + "*")):
            print(f)
            radar = file_to_radar_object(f, extension)
            var_dict = get_var_arrays_from_radar_object(radar, radar_config_file)
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
            date_time.append(dt)
            dbz95_h.append(d95_h)
            stats_h.append(s_h)
        # Calculate median 95th percentile clutter area reflecitivty from all times in day
        dbz95_h_baseline = np.nanmedian(dbz95_h)
        # Calculate total number of radar gates used in calculation
        total_num_pts_h = []
        for i in range(0, len(stats_h)):
            total_num_pts_h.append(stats_h[i]["num_points"])
        total_num_pts_h = np.sum(total_num_pts_h)
        # Write baseline 95th reflectivity values to a netCDF file
        d = Dataset(
            baseline_dir
            + "baseline_"
            + scantype
            + "_"
            + site
            + inst
            + "_"
            + baseline_date
            + ".nc",
            "w",
            format="NETCDF4_CLASSIC",
        )
        value = d.createDimension("value", 1)
        dbz95_h_base = d.createVariable("baseline_dbz95_zh", np.float64, ("value",))
        dbz95_h_base.long_name = "Baseline 95th percentile reflectivity (H)"
        dbz95_h_base[:] = dbz95_h_baseline
        d.close()
        
        return dbz95_h_baseline

    elif polarization == "dual":
        for f in glob.glob(os.path.join(datadir, "*" + baseline_date + "*")):
            print(f)
            radar = file_to_radar_object(f, extension)
            var_dict = get_var_arrays_from_radar_object(radar, radar_config_file)
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
            date_time.append(dt)
            dbz95_h.append(d95_h)
            stats_h.append(s_h)
            dbz95_v.append(d95_v)
            stats_v.append(s_v)

        # Calculate median 95th percentile clutter area reflecitivty from all times in day
        dbz95_h_baseline = np.nanmedian(dbz95_h)
        dbz95_v_baseline = np.nanmedian(dbz95_v)
        # Calculate total number of radar gates used in calculation
        total_num_pts_h = []
        for i in range(0, len(stats_h)):
            total_num_pts_h.append(stats_h[i]["num_points"])
        total_num_pts_h = np.sum(total_num_pts_h)
        total_num_pts_v = []
        for i in range(0, len(stats_v)):
            total_num_pts_v.append(stats_v[i]["num_points"])
        total_num_pts_v = np.sum(total_num_pts_v)
        # Write baseline 95th reflectivity values to a netCDF file
        d = Dataset(
            baseline_dir
            + "baseline_"
            + scantype
            + "_"
            + site
            + inst
            + "_"
            + baseline_date
            + ".nc",
            "w",
            format="NETCDF4_CLASSIC",
        )
        value = d.createDimension("value", 1)
        dbz95_h_base = d.createVariable("baseline_dbz95_zh", np.float64, ("value",))
        dbz95_v_base = d.createVariable("baseline_dbz95_zv", np.float64, ("value",))
        dbz95_h_base.long_name = "Baseline 95th percentile reflectivity (H)"
        dbz95_v_base.long_name = "Baseline 95th percentile reflectivity (V)"
        dbz95_h_base[:] = dbz95_h_baseline
        dbz95_v_base[:] = dbz95_v_baseline
        d.close()
        
        return dbz95_h_baseline, dbz95_v_baseline
