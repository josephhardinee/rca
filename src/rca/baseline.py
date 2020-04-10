#!/usr/bin/env python
import numpy as np
import os
import glob
import json
from netCDF4 import Dataset
from .aux.file_to_radar_object import file_to_radar_object
from .aux.get_var_arrays_from_radar_object import get_var_arrays_from_radar_object
from .calculate_dbz95 import calculate_dbz95_ppi, calculate_dbz95_rhi


def baseline(radar_config_file, filters=True):
    """
    baseline loops through a day's worth of radar files (specify PPI or HSRHI),
    calculates the median daily 95th percentile clutter area reflectivity,
    and saves the value to a netCDF as the baseline 95th percentile clutter area reflectivity.
    
    Parameters
    ----------
    radar_config_file: str
        path to JSON file containing specifications: data directory, file extension, clutter map directory, output directory for baseline netCDF, baseline date, scan type, polarization, site, instrument, range limit
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
    if inst == 'kasacr':
        radar_band = 'ka'
    else:
        radar_band = inst[0]

    # Identify which radar band you are using (change if statement as needed)
    # Most important to identify Ka-band radars
    if inst == "kasacr":
        radar_band = "ka"
    else:
        radar_band = inst[0]

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
                    + baseline_date
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
    pass_filter = []

    # Read in each radar file and turn into radar object and use function to
    # calculate 95th percentile clutter area reflectivity
    
    # Will use glob, so grab all files and then sort by datetime
    files = []
    for f in glob.glob(os.path.join(datadir, "*" + baseline_date + ".*.??")):
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

            if filters==True:
                # Read in filters array
                pass_filter.append(total_filter[idx_f])
            
        # Calculate median 95th percentile clutter area reflecitivty from all times in day
        dbz95_h = np.array(dbz95_h)
        if filters==True:
            pass_filter = np.array(pass_filter)
            dbz95_h_baseline = np.nanmedian(dbz95_h[pass_filter > 0])
        else:
            dbz95_h_baseline = np.nanmedian(dbz95_h)

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
            format="NETCDF4",
        )
        value = d.createDimension("value", 1)
        dbz95_h_base = d.createVariable("baseline_dbz95_zh", np.float64, ("value",))
        dbz95_h_base.long_name = "Baseline 95th percentile reflectivity (H)"
        dbz95_h_base[:] = dbz95_h_baseline
        d.close()

        return dbz95_h_baseline

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
            dbz95_v.append(s_v["reflectivity_95"])

            if filters==True:
                # Read in filters array
                pass_filter.append(total_filter[idx_f])

        # Calculate median 95th percentile clutter area reflecitivty from all
        # times in day
        if filters==True:
            dbz95_h_baseline = np.nanmedian(dbz95_h[pass_filter > 0])
            dbz95_v_baseline = np.nanmedian(dbz95_v[pass_filter > 0])
        else:
            dbz95_h_baseline = np.nanmedian(dbz95_h)
            dbz95_v_baseline = np.nanmedian(dbz95_v)

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
            format="NETCDF4",
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
