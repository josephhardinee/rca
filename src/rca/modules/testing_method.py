#!/usr/bin/env python
import numpy as np
from rca.modules.create_masks import create_az_mask_ppi
from rca.modules.file_to_radar_object import file_to_radar_object
from rca.modules.get_var_arrays_from_radar_object import get_var_arrays_from_radar_object
#from rca.modules.calculate_dbz95 import calculate_dbz95_ppi, calculate_dbz95_hsrhi

radar_config_file = '/Users/hunz743/projects/github/rca/src/rca/cband_ppi.json'
#radar_config_file = '/Users/hunz743/projects/github/rca/src/rca/kaband_rhi.json'
file = '/Users/hunz743/projects/rca_auxillary/datafiles/data/corcsapr2cfrppiM1.a1.20181215.000003.nc'
#file = '/Users/hunz743/projects/rca_auxillary/datafiles/data/corkasacrcfrhsrhiM1.a1.20181215.000309.nc'
extension = '.nc'
radar = file_to_radar_object(file,extension)
var_dict = get_var_arrays_from_radar_object(radar,radar_config_file)

print(var_dict.keys())
print(var_dict['reflectivity_h'].shape)
#print(var_dict['reflectivity_v'].shape)
print(var_dict['range'].shape)
print(var_dict['azimuth'].shape)
print(var_dict['elevation'].shape)
print(var_dict['date_time'])

z_thresh = 45.
range_limit = 10000
theta_list = np.arange(2) #360
range_shape = range_limit / 1000
r_list = np.arange(range_shape) + 1
clutter_flag_h = np.zeros((len(theta_list), len(r_list)))
#clutter_flag_v = np.zeros((len(theta_list), len(r_list)))

date_time = var_dict['date_time']
r = var_dict['range']
theta = var_dict['azimuth']
zh = var_dict['reflectivity_h']

# H POLARIZATION
for idx_az, az in enumerate(theta_list):  # loop thru each azimuth in list
    az_mask = create_az_mask_ppi(az, theta)  # create mask for desired azimuths
    zh_rays = zh[
        az_mask, :
    ]  # get Zh values for only the desired elevation and azimuth
    print(az, zh_rays.shape)
    for idx_ra, ra in enumerate(
        r_list
    ):  # loop thru each range gate in the range grid boxes (len = 80)
        print(ra)
        if ra == range_shape:
            continue  # skip the last value in the range grid
        else:
            zh_ray_list = []
            rstart = np.where(r-(ra*1000.) > 0)[0][0]
            rstop = np.where(r-(r_list[idx_ra+1]*1000.) > 0)[0][0]
            print(ra,idx_ra,rstart,rstop)
            for idx_z, z in enumerate(
                zh_rays[:, rstart : rstop]
            ):  # loop thru each zh value in chunks of 10 100m range gates (1 km chunks)
                if np.any(z >= z_thresh):
                    zh_ray_list.append(z)
                    clutter_flag_h[
                        idx_az, idx_ra
                    ] = (
                        1
                    )  # flag the grid box as clutter is any zh in the 1 km chunk is greater than the threshold value