import numpy as np
import pyart
import os
import glob
import json
from netCDF4 import Dataset
from rca.modules.create_clutter_flag import (
    create_clutter_flag_ppi,
    create_clutter_flag_hsrhi,
)
from rca.modules.file_to_radar_object import file_to_radar_object
from rca.modules.get_var_arrays_from_radar_object import (
    get_var_arrays_from_radar_object,
)


def clutter_map(radar_config_file, date):
    """
    clutter_map loops through a day's worth of radar files (specify PPI or HSRHI, dual or horizontal polarization)
    utilizes the create_clutter_flag function to flag clutter points for each scan. If more than 50% of the day's 
    scans have a gate identified, it is considered a clutter point and saved to the resulting clutter map.
    The clutter map (array) is written to a netCDF.
    
    Parameters:
    --------------
    radar_config_file: str
                path to JSON file containing specifications:
                    data directory
                    file extension
                    output directory for clutter map
                    date of clutter map
                    scan type
                    polarization
                    site
                    instrument
                    range limit
                    reflectivity threshold
    date: str
        date used for clutter map day
        in YYYYMMDD format (overrides what's in config file)
                    
    Returns:
    --------------
    (no specific return)
    however, a netCDF file is written out
    
    """
    config_vars = json.load(open(radar_config_file))
    datadir = config_vars["data_directory"]
    extension = config_vars["file_extension"]
    cluttermap_dir = config_vars["cluttermap_directory"]
    cluttermap_date = config_vars["cluttermap_date"]
    scantype = config_vars["scan_type"]
    polarization = config_vars["polarization"]
    site = config_vars["site_abbrev"]
    inst = config_vars["instrument_abbrev"]
    range_limit = config_vars["range_limit"]
    z_thresh = config_vars["z_threshold"]

    cluttermap_date = date

    # Lists to fill in loops below
    clutter_flag_h = []
    clutter_flag_v = []
    date_time = []  # date and time, string

    if polarization == "horizontal" and scantype == "ppi":
        for f in glob.glob(os.path.join(datadir, "*" + cluttermap_date + "*.??")):
            print(f)
            radar = file_to_radar_object(f, extension)
            var_dict = get_var_arrays_from_radar_object(radar, radar_config_file)
            dt, cflag_h = create_clutter_flag_ppi(
                var_dict, polarization, range_limit, z_thresh
            )
            clutter_flag_h.append(cflag_h)
            date_time.append(dt)
        # Calculate percentage of "clutter ON" for each grid box in clutter map grid
        clutter_flag_h = np.asarray(clutter_flag_h)
        pct_h = np.sum(clutter_flag_h, axis=0) / len(clutter_flag_h[:, 0, 0])
        # Create mask for clutter percentages greater than 50%
        clutter_map_h_mask = pct_h > 0.5
        # Write clutter map arrays to netCDF file
        dataset = Dataset(
            cluttermap_dir
            + "cluttermap_"
            + scantype
            + "_"
            + site
            + inst
            + "_"
            + cluttermap_date
            + ".nc",
            "w",
            format="NETCDF4_CLASSIC",
        )
        azi = dataset.createDimension("azi", 360)
        rang = dataset.createDimension("rang", range_limit / 1000)

        HPCT_ON = dataset.createVariable(
            "clutter_gate_pcts_zh", np.float64, ("azi", "rang")
        )
        HMASK = dataset.createVariable("clutter_map_mask_zh", "i1", ("azi", "rang"))
        HPCT_ON.long_name = "Clutter grid gate percentages (Zh)"
        HMASK.long_name = "Clutter map mask (Zh)"
        HPCT_ON[:, :] = pct_h
        HMASK[:, :] = clutter_map_h_mask
        dataset.close()

    elif polarization == "horizontal" and scantype == "rhi":
        for f in glob.glob(os.path.join(datadir, "*" + cluttermap_date + "*.??")):
            print(f)
            radar = file_to_radar_object(f, extension)
            var_dict = get_var_arrays_from_radar_object(radar, radar_config_file)
            dt, cflag_h = create_clutter_flag_hsrhi(
                var_dict, polarization, range_limit, z_thresh
            )
            clutter_flag_h.append(cflag_h)
            date_time.append(dt)
        # Calculate percentage of "clutter ON" for each grid box in clutter map grid
        clutter_flag_h = np.asarray(clutter_flag_h)
        pct_h = np.sum(clutter_flag_h, axis=0) / len(clutter_flag_h[:, 0, 0, 0])
        # Create mask where clutter percentages are greater than 50%
        clutter_map_h_mask = pct_h > 0.5
        # Write clutter map arrays to netCDF file
        dataset = Dataset(
            cluttermap_dir
            + "cluttermap_"
            + scantype
            + "_"
            + site
            + inst
            + "_"
            + cluttermap_date
            + ".nc",
            "w",
            format="NETCDF4_CLASSIC",
        )
        azi = dataset.createDimension("azi", 6)
        ele = dataset.createDimension("ele", 10)
        rang = dataset.createDimension("rang", range_limit / 1000)

        HPCT_ON = dataset.createVariable(
            "clutter_gate_pcts_zh", np.float64, ("azi", "ele", "rang")
        )
        HMASK = dataset.createVariable(
            "clutter_map_mask_zh", "i1", ("azi", "ele", "rang")
        )
        HPCT_ON.long_name = "Clutter grid gate percentages (Zh)"
        HMASK.long_name = "Clutter map mask (Zh)"
        HPCT_ON[:, :, :] = pct_h
        HMASK[:, :, :] = clutter_map_h_mask
        dataset.close()

    elif polarization == "dual" and scantype == "ppi":
        for f in glob.glob(os.path.join(datadir, "*" + cluttermap_date + "*.??")):
            print(f)
            radar = file_to_radar_object(f, extension)
            var_dict = get_var_arrays_from_radar_object(radar, radar_config_file)
            dt, cflag_h, cflag_v = create_clutter_flag_ppi(
                var_dict, polarization, range_limit, z_thresh
            )
            clutter_flag_h.append(cflag_h)
            clutter_flag_v.append(cflag_v)
            date_time.append(dt)
        # Calculate percentage of "clutter ON" for each grid box in clutter map grid
        clutter_flag_h = np.asarray(clutter_flag_h)
        clutter_flag_v = np.asarray(clutter_flag_v)
        pct_h = np.sum(clutter_flag_h, axis=0) / len(clutter_flag_h[:, 0, 0])
        pct_v = np.sum(clutter_flag_v, axis=0) / len(clutter_flag_v[:, 0, 0])
        # Create mask for clutter percentages greater than 50%
        clutter_map_h_mask = pct_h > 0.5
        clutter_map_v_mask = pct_v > 0.5
        # Write clutter map arrays to netCDF file
        dataset = Dataset(
            cluttermap_dir
            + "cluttermap_"
            + scantype
            + "_"
            + site
            + inst
            + "_"
            + cluttermap_date
            + ".nc",
            "w",
            format="NETCDF4_CLASSIC",
        )
        azi = dataset.createDimension("azi", 360)
        rang = dataset.createDimension("rang", range_limit / 1000)

        HPCT_ON = dataset.createVariable(
            "clutter_gate_pcts_zh", np.float64, ("azi", "rang")
        )
        VPCT_ON = dataset.createVariable(
            "clutter_gate_pcts_zv", np.float64, ("azi", "rang")
        )
        HMASK = dataset.createVariable("clutter_map_mask_zh", "i1", ("azi", "rang"))
        VMASK = dataset.createVariable("clutter_map_mask_zv", "i1", ("azi", "rang"))
        HPCT_ON.long_name = "Clutter grid gate percentages (Zh)"
        VPCT_ON.long_name = "Clutter grid gate percentages (Zv)"
        HMASK.long_name = "Clutter map mask (Zh)"
        VMASK.long_name = "Clutter map mask (Zv)"
        HPCT_ON[:, :] = pct_h
        VPCT_ON[:, :] = pct_v
        HMASK[:, :] = clutter_map_h_mask
        VMASK[:, :] = clutter_map_v_mask
        dataset.close()

    elif polarization == "dual" and scantype == "rhi":
        for f in glob.glob(os.path.join(datadir, "*" + cluttermap_date + "*.??")):
            print(f)
            radar = file_to_radar_object(f, extension)
            var_dict = get_var_arrays_from_radar_object(radar, radar_config_file)
            dt, cflag_h, cflag_v = create_clutter_flag_hsrhi(
                var_dict, polarization, range_limit, z_thresh
            )
            clutter_flag_h.append(cflag_h)
            clutter_flag_v.append(cflag_v)
            date_time.append(dt)
        # Calculate percentage of "clutter ON" for each grid box in clutter map grid
        clutter_flag_h = np.asarray(clutter_flag_h)
        clutter_flag_v = np.asarray(clutter_flag_v)
        pct_h = np.sum(clutter_flag_h, axis=0) / len(clutter_flag_h[:, 0, 0, 0])
        pct_v = np.sum(clutter_flag_v, axis=0) / len(clutter_flag_v[:, 0, 0, 0])
        # Create mask where clutter percentages are greater than 50%
        clutter_map_h_mask = pct_h > 0.5
        clutter_map_v_mask = pct_v > 0.5
        # Write clutter map arrays to netCDF file
        dataset = Dataset(
            cluttermap_dir
            + "cluttermap_"
            + scantype
            + "_"
            + site
            + inst
            + "_"
            + cluttermap_date
            + ".nc",
            "w",
            format="NETCDF4_CLASSIC",
        )
        azi = dataset.createDimension("azi", 6)
        ele = dataset.createDimension("ele", 10)
        rang = dataset.createDimension("rang", range_limit / 1000)

        HPCT_ON = dataset.createVariable(
            "clutter_gate_pcts_zh", np.float64, ("azi", "ele", "rang")
        )
        VPCT_ON = dataset.createVariable(
            "clutter_gate_pcts_zv", np.float64, ("azi", "ele", "rang")
        )
        HMASK = dataset.createVariable(
            "clutter_map_mask_zh", "i1", ("azi", "ele", "rang")
        )
        VMASK = dataset.createVariable(
            "clutter_map_mask_zv", "i1", ("azi", "ele", "rang")
        )
        HPCT_ON.long_name = "Clutter grid gate percentages (Zh)"
        VPCT_ON.long_name = "Clutter grid gate percentages (Zv)"
        HMASK.long_name = "Clutter map mask (Zh)"
        VMASK.long_name = "Clutter map mask (Zv)"
        HPCT_ON[:, :, :] = pct_h
        VPCT_ON[:, :, :] = pct_v
        HMASK[:, :, :] = clutter_map_h_mask
        VMASK[:, :, :] = clutter_map_v_mask
        dataset.close()
