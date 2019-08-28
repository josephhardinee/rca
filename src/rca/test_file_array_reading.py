#!/usr/bin/env python
from file_to_radar_object import file_to_radar_object
from get_var_arrays_from_radar_object import get_var_arrays_from_radar_object
from calculate_dbz95 import calculate_dbz95_ppi, calculate_dbz95_hsrhi

radar_config_file = '/Users/hunz743/projects/github/rca/src/rca/cband_ppi.json'
file = file = '/Users/hunz743/projects/rca_auxillary/datafiles/data/corcsapr2cfrppiM1.a1.20181215.000003.nc'
extension = '.nc'
radar = file_to_radar_object(file,extension)
var_dict = get_var_arrays_from_radar_object(radar,radar_config_file)