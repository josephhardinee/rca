import xarray as xr
import glob
import numpy as np
import pandas as pd
import os
import json
from netCDF4 import Dataset, stringtochar
from .aux.file_to_radar_object import file_to_radar_object
from .aux.get_var_arrays_from_radar_object import get_var_arrays_from_radar_object
from .iah_filter import iah_filter_ppi, iah_filter_rhi
from .rh_filter import rh_filter

# filters.py

# create filters for a day using all day filters
# use functions: iah_filter, rh_filter

def filters(radar_config_file, date, met_path):
    """
    filters loops through a day's worth of radar files (specify PPI or HSRHI, dual or horizontal polarization),
    and calculates IAH and RH filters (if desired) for every file in a day.
    
    A netCDF for each day with a filter-passing array is stored.
    
    Parameters
    ----------
    radar_config_file: str
        path to JSON file containing specifications: data directory, file extension, clutter map directory, baseline directory, baseline date, daily CSV directory, scan type, polarization, site, instrument, range limit
    date: str
        YYYYMMDD specifying date of interest
    met_path: str
        path to cormet files                
    """

    os.environ['HDF5_USE_FILE_LOCKING'] = 'FALSE'
    print(date)

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

    # Get all the cormet files for a specified day
    met_files = glob.glob(met_path+'*'+date+'*.cdf')
    met_files.sort()
    met = xr.open_mfdataset(met_files)
    met = met.to_dataframe()

    # Set RH (%) threshold
    rh_thresh = 90

    # Get all files in a day
    day_files = []
    #for f in glob.glob(os.path.join(datadir, "*" + date + ".*.??")):
    for f in glob.glob(os.path.join(datadir, "*" + date + ".20*.??")):
        day_files.append(f)
    
    # Sort files chronologically
    day_files.sort()

    # For each time file, calculate filters
    iah_filter_list = []
    rh_filter_list = []
    rh_list = []
    datetime_list = []
    for idx_f, f in enumerate(day_files):
    #    print(f)
        extension = f[-3:]
        radar = file_to_radar_object(f, extension)
        var_dict = get_var_arrays_from_radar_object(radar, radar_config_file)
        date_time_iah, pass_filter_iah = iah_filter_rhi(var_dict,
                                                        polarization,
                                                        range_limit,
                                                        radar_band,
                                                        clutter_map_mask_h,
                                                        clutter_mask_v=None
                                                        )
        iah_filter_list.append(pass_filter_iah)
        date_time_rh, rh, pass_filter_rh = rh_filter(date,
                                                    var_dict,
                                                    met,
                                                    rh_thresh
                                                    )
        datetime_list.append(date_time_iah[0:19])
        rh_list.append(rh)
        rh_filter_list.append(pass_filter_rh)
    
    # Convert lists to arrays
    #datetime_array = np.asarray(datetime_list)
    #rh_array = np.array(rh_list)
    iah_filter_array = np.array(iah_filter_list)
    rh_filter_array = np.array(rh_filter_list)

    filter_array = np.zeros(iah_filter_array.shape, dtype=int)

    iah_pass = iah_filter_array > 0
    rh_pass = rh_filter_array > 0
    pass_filter = np.logical_and(iah_pass,rh_pass)

    filter_array[pass_filter] = 1

    print(type(rh_filter_array), type(iah_filter_array), type(filter_array))
    print(rh_filter_array.dtype, iah_filter_array.dtype, filter_array.dtype)
    print(filter_array.dtype.str)

    # Convert date_time string to character
    #date_time_str_out = stringtochar(datetime_array, 'S18')

    # Write filter arrays to netCDF
    d = Dataset(
        dailycsvdir+'/filters/'
        + "filters_"
        + scantype
        + "_"
        + site
        + inst
        + "_"
        + date
        + ".nc",
        "w",
        format="NETCDF4",
    )

    print(d.data_model)
    print(len(filter_array))
    arr_len = d.createDimension("len",len(filter_array))
    print(d.dimensions)
    #scalar_example = d.createVariable("scalar","")
    total_filter = d.createVariable("iah_and_rh_filter",np.int64,("len",))
    #total_filter = d.createVariable("iah_and_rh_filter",rh_filter_array.dtype.str,("len",))
    #print(total_filter)
    print(type(filter_array), filter_array.dtype)
    d.close()

    #arr_len = d.createDimension("arr_len", len(filter_array))
    #str_len = d.createDimension("nchar", len(datetime_array))

    #total_filter = d.createVariable("iah_and_rh_filter", 'f4', ("arr_len",))
    #iah_fil = d.createVariable("iah_filter", 'f4', ("arr_len",))
    #rh_fil = d.createVariable("rh_filter", 'f4', ("arr_len",))
    #rh_value = d.createVariable("rh_value", 'f4', ("arr_len",))
    #datetime = d.createVariable("datetime", 'S4', ("arr_len",))

    #total_filter.long_name = "Combined filter using IAH and RH filters"
    #iah_fil.long_name = "IAH filter"
    #rh_fil.long_name = "RH filter"
    #rh_value.long_name = "RH value"
    #datetime.long_name = "Datetime"
    
    #print(type(filter_array), type(datetime_array))
    #print(filter_array.dtype, datetime_array.dtype)
    
    #total_filter[:] = filter_array
    #iah_fil[:] = iah_filter_array
    #rh_fil[:] = rh_filter_array
    #rh_value[:] = rh_array
    #datetime[:] = datetime_array
    #datetime[:] = date_time_str_out

    #d.close()


    
