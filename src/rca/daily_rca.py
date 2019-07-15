#!/usr/bin/env python
import sys
import numpy as np
import os
import glob
import json
from netCDF4 import Dataset
import pandas as pd
from file_to_radar_object import file_to_radar_object
from calculate_dbz95 import calculate_dbz95_ppi, calculate_dbz95_hsrhi

"""
daily_rca.py loops through a day's worth of radar files (specify PPI or HSRHI),
calculates the median daily 95th percentile clutter area reflectivity,
computes the RCA value using the established baseline 95h percentile clutter area reflectivity
and saves the daily median RCA value to a CSV file.
"""

# Get variables from JSON configuration file
date = ' ' # DEAL WITH THIS will be used for looping......
radar_config_file = './kaband_ppi.json'
config_vars = json.load(open(radar_config_file))
datadir = config_vars["data_directory"]
extension = config_vars["file_extension"]
cluttermap = config_vars["cluttermap_path"]
baseline = config_vars["baseline_path"]
dailycsvdir = config_vars["daily_csv_dir"]
scantype = config_vars["scan_type"]
polarization = config_vars["polarization"]
site = config_vars["site_abbrev"]
inst = config_vars["instrument_abbrev"]
range_limit = config_vars["range_limit"]

daily_csv_fullpath = dailycsvdir + "daily_rca_" + scantype + site + inst + ".csv"

# Read in clutter map netCDF and baseline value netCDF
dataset = Dataset(cluttermap)
dataset_b = Dataset(baseline)
if scantype == 'ppi':
    clutter_map_mask_h = dataset.variables["clutter_map_mask_zh"][:, :]
    baseline_dbz95_h = dataset_b.variables["baseline_dbz95_zh"][:]
elif scantype == 'rhi':
    clutter_map_mask_h = dataset.variables["clutter_map_mask_zh"][:, :, :]
    baseline_dbz95_h = dataset_b.variables["baseline_dbz95_zh"][:]
if polarization == 'dual' and scantype == 'ppi':
    clutter_map_mask_v = dataset.variables["clutter_map_mask_zv"][:, :]
    baseline_dbz95_v = dataset_b.variables["baseline_dbz95_zv"][:]
elif polarization == 'dual' and scantype == 'rhi':
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

# Read in each radar file and turn into radar object and use function to
# calculate 95th percentile clutter area reflectivity
for f in glob.glob(os.path.join(datadir, "*" + date + "*.??")):
    print(f)
    radar = file_to_radar_object(f,extension)
    if polarization == 'horizontal':
        if scantype == 'ppi':
            dt, d95_h, s_h = calculate_dbz95_ppi(
                                radar,
                                polarization,
                                range_limit,
                                clutter_map_mask_h,
                                clutter_mask_v=None)
            date_time.append(dt)
            dbz95_h.append(d95_h)
            stats_h.append(s_h)
        elif scantype == 'rhi':
            dt, d95_h, s_h = calculate_dbz95_hsrhi(
                                radar,
                                polarization,
                                range_limit,
                                clutter_map_mask_h,
                                clutter_mask_v=None)
            date_time.append(dt)
            dbz95_h.append(d95_h)
            stats_h.append(s_h)
        # Calculate median 95th percentile clutter area reflecitivty from all times in day
        dbz95_h_mean = np.nanmedian(dbz95_h)
        # Calculate RCA
        rca_h = baseline_dbz95_h[0] - dbz95_h_mean
        yr = date[0:4]
        mon = date[4:6]
        day = date[6:]
        base = 0  # set to 0 for daily RCA, set to 1 when calculating for baseline
        date = yr + "-" + mon + "-" + day
        # Create dictionary and dataframe
        csv_frame = pd.read_csv(dailycsvdir + "daily_rca_" + scantype + "_" + site + "_" + inst + ".csv")
        rca_dict = {"DATE": date, "RCA_H": rca_h, "RCA_V": np.nan, "BASELINE": base}
        csv_frame = csv_frame.append(rca_dict, ignore_index=True)
        csv_frame.set_index("DATE")
        csv_frame.to_csv(daily_csv_fullpath, index=False)

    elif polarization == 'dual':
        if scantype == 'ppi':
            dt, d95_h, d95_v, s_h, s_v = calculate_dbz95_ppi(
                                            radar,
                                            polarization,
                                            range_limit,
                                            clutter_map_mask_h,
                                            clutter_mask_v=clutter_map_mask_v)
            date_time.append(dt)
            dbz95_h.append(d95_h)
            stats_h.append(s_h)
            dbz95_v.append(d95_v)
            stats_v.append(s_v)
        elif scantype == 'rhi':
            dt, d95_h, d95_v, s_h, s_v = calculate_dbz95_hsrhi(
                                            radar,
                                            polarization,
                                            range_limit,
                                            clutter_map_mask_h,
                                            clutter_mask_v=clutter_map_mask_v)
            date_time.append(dt)
            dbz95_h.append(d95_h)
            stats_h.append(s_h)
            dbz95_v.append(d95_v)
            stats_v.append(s_v)
        # Calculate median 95th percentile clutter area reflecitivty from all times in day
        dbz95_h_mean = np.nanmedian(dbz95_h)
        dbz95_v_mean = np.nanmedian(dbz95_v)
        # Calculate RCA
        rca_h = baseline_dbz95_h[0] - dbz95_h_mean
        rca_v = baseline_dbz95_v[0] - dbz95_v_mean
        yr = date[0:4]
        mon = date[4:6]
        day = date[6:]
        base = 0  # set to 0 for daily RCA, set to 1 when calculating for baseline
        date = yr + "-" + mon + "-" + day
        # Create dictionary and dataframe
        csv_frame = pd.read_csv(dailycsvdir + "daily_rca_" + scantype + "_" + site + "_" + inst + ".csv")
        rca_dict = {"DATE": date, "RCA_H": rca_h, "RCA_V": rca_v, "BASELINE": base}
        csv_frame = csv_frame.append(rca_dict, ignore_index=True)
        csv_frame.set_index("DATE")
        csv_frame.to_csv(daily_csv_fullpath, index=False)