#!/usr/bin/env python
import sys
import numpy as np
import os
import glob
import json
from netCDF4 import Dataset
from file_to_radar_object import file_to_radar_object
from calculate_dbz95 import calculate_dbz95_ppi, calculate_dbz95_hsrhi

"""
baseline.py loops through a day's worth of radar files (specify PPI or HSRHI),
calculates the median daily 95th percentile clutter area reflectivity,
and saves the value to a netcdf as the baseline 95th percentile clutter area reflectivity
"""

if __name__ == "__main__":
    if len(sys.argv) < 7:
        print(
            """ERROR: Arguments are radar file directory path, clutter map netCDF path (include filename), 
            baseline netCDF output directory path, desired baseline date (YYYYMMDD), scan type (ppi or rhi),
            polarization (horizontal or dual)
            """
        )
        sys.exit(0)

    datadir = sys.argv[1]
    cluttermap = sys.argv[2]
    baselinedir = sys.argv[3]
    date = sys.argv[4]
    scantype = sys.argv[5]
    polarization = sys.argv[6]
    print(datadir, cluttermap, baselinedir, date, scantype, polarization)

##############################################
# VARIABLES THAT SHOULD GO IN CONFIG/JSON FILE?
range_limit = 10 000
site = ''
inst = ''
    # could break these into a few recommended defaults for different radar bands and scan types

##############################################

# Read in clutter map netCDF
dataset = Dataset(cluttermap)
if scantype == 'ppi':
    clutter_map_mask_h = dataset.variables["clutter_map_mask_zh"][:, :]
elif scantype == 'rhi':
    clutter_map_mask_h = dataset.variables["clutter_map_mask_zh"][:, :, :]
if polarization == 'dual' and scantype == 'ppi':
    clutter_map_mask_v = dataset.variables["clutter_map_mask_zv"][:, :]
elif polarization == 'dual' and scantype == 'rhi':
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
            dt, d95_h, s_h = calculate_dbz95_rhi(
                                radar,
                                polarization,
                                range_limit,
                                clutter_map_mask_h,
                                clutter_mask_v=None)
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
            baselinedir + "baseline_" + scantype + "_" + site + inst + "_" + date + ".nc",
            "w",
            format="NETCDF4_CLASSIC",
        )
        value = d.createDimension("value", 1)
        dbz95_h_base = d.createVariable("baseline_dbz95_zh", np.float64, ("value",))
        dbz95_h_base.long_name = "Baseline 95th percentile reflectivity (H)"
        dbz95_h_base[:] = dbz95_h_baseline
        d.close()

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
            baselinedir + "baseline_" + scantype + "_" + site + inst + "_" + date + ".nc",
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
    


