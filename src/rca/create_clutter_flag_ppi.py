import numpy as np
import pyart
from create_az_mask_ppi import create_az_mask_ppi

def create_clutter_flag_ppi(filename,inst,range_limit,range_shape,z_thresh):
    '''Creates a clutter flag array (precip-free day) to be used for the clutter map creation for PPIs
    and returns the date and time of the file and the clutter flag arrays for Zh and/or Zv'''
    
    ext = filename[-3:]
    if inst == 'kasacr':
        if ext == '.h5':
            radar = pyart.aux_io.read_gamic(filename, file_field_names=True) 
            date_time = radar.time['units'].replace('seconds since ', '')
            r_start_idx = 0
            r_stop_idx = np.where(radar.range['data'] > range_limit)[0][0]
            # Using lowest elevation angle of PPI (0.5 deg)
            sweep_start_idx = radar.sweep_start_ray_index['data'][0]
            sweep_stop_idx = radar.sweep_end_ray_index['data'][0]+1
            r = radar.range['data'][r_start_idx:r_stop_idx]
            theta = radar.azimuth['data'][sweep_start_idx:sweep_stop_idx]
            zh = radar.fields['UZh']['data'][sweep_start_idx:sweep_stop_idx,r_start_idx:r_stop_idx]

        else:
        #elif ext == '.nc':
            radar = pyart.io.cfradial.read_cfradial(filename,delay_field_loading=True)
            date_time = radar.time['units'].replace('seconds since ', '')
            r_start_idx = 0
            r_stop_idx = np.where(radar.range['data'] > range_limit)[0][0]
            # Using lowest elevation angle of PPI (0.5 deg)
            sweep_start_idx = radar.sweep_start_ray_index['data'][0]
            sweep_stop_idx = radar.sweep_end_ray_index['data'][0]+1
            r = radar.range['data'][r_start_idx:r_stop_idx]
            theta = radar.azimuth['data'][sweep_start_idx:sweep_stop_idx]
            zh = radar.fields['reflectivity']['data'][sweep_start_idx:sweep_stop_idx,r_start_idx:r_stop_idx]

        print(zh.shape)
        print(theta.shape, r.shape)
        print(theta)
        print(r)
        theta_list = np.arange(360)
        r_list = np.arange(range_shape)
        clutter_flag_h = np.zeros((len(theta_list),len(r_list)))

        # H POLARIZATION
        for idx_az, az in enumerate(theta_list):        #loop thru each azimuth in list
            az_mask = create_az_mask_ppi(az,theta)              #create mask for desired azimuths
            zh_rays = zh[az_mask,:]            #get Zh values for only the desired elevation and azimuth
            for idx_ra, ra in enumerate(r_list):            #loop thru each range gate in the range grid boxes (len = 80)
                if ra == range_shape:
                    continue                                    #skip the last value in the range grid
                else:
                    zh_ray_list = []
                    for idx_z, z in enumerate(zh_rays[:,idx_ra*10:idx_ra*10+10]):  #loop thru each zh value in chunks of 10 100m range gates (1 km chunks)
                        if np.any(z >= z_thresh):   
                            zh_ray_list.append(z)
                            clutter_flag_h[idx_az,idx_ra] = 1                 #flag the grid box as clutter is any zh in the 1 km chunk is greater than the threshold value
    
        return date_time, clutter_flag_h

    else:
        if ext == '.h5':
            radar = pyart.aux_io.read_gamic(filename, file_field_names=True) 
            date_time = radar.time['units'].replace('seconds since ', '')
            r_start_idx = 0
            r_stop_idx = np.where(radar.range['data'] > range_limit)[0][0]
            # Using lowest elevation angle of PPI (0.5 deg)
            sweep_start_idx = radar.sweep_start_ray_index['data'][0]
            sweep_stop_idx = radar.sweep_end_ray_index['data'][0]+1
            r = radar.range['data'][r_start_idx:r_stop_idx]
            theta = radar.azimuth['data'][sweep_start_idx:sweep_stop_idx]
            zh = radar.fields['UZh']['data'][sweep_start_idx:sweep_stop_idx,r_start_idx:r_stop_idx]
            zv = radar.fields['UZv']['data'][sweep_start_idx:sweep_stop_idx,r_start_idx:r_stop_idx]

        elif ext == '.nc':
            radar = pyart.io.cfradial.read_cfradial(filename,delay_field_loading=True)
            date_time = radar.time['units'].replace('seconds since ', '')
            r_start_idx = 0
            r_stop_idx = np.where(radar.range['data'] > range_limit)[0][0]
            # Using lowest elevation angle of PPI (0.5 deg)
            sweep_start_idx = radar.sweep_start_ray_index['data'][0]
            sweep_stop_idx = radar.sweep_end_ray_index['data'][0]+1
            r = radar.range['data'][r_start_idx:r_stop_idx]
            theta = radar.azimuth['data'][sweep_start_idx:sweep_stop_idx]
            zh = radar.fields['uncorrected_reflectivity_h']['data'][sweep_start_idx:sweep_stop_idx,r_start_idx:r_stop_idx]
            zv = radar.fields['uncorrected_reflectivity_v']['data'][sweep_start_idx:sweep_stop_idx,r_start_idx:r_stop_idx]
            
        elif inst == 'xsaprI4' or inst == 'xsaprI5':
            radar = pyart.io.read(filename)
            date_time = radar.time['units'].replace('seconds since ', '')
            r_start_idx = 0
            r_stop_idx = np.where(radar.range['data'] > range_limit)[0][0]
            # Using lowest elevation angle of PPI (0.5 deg)
            sweep_start_idx = radar.sweep_start_ray_index['data'][0]
            sweep_stop_idx = radar.sweep_end_ray_index['data'][0]+1
            r = radar.range['data'][r_start_idx:r_stop_idx]
            theta = radar.azimuth['data'][sweep_start_idx:sweep_stop_idx]
            zh = radar.fields['reflectivity']['data'][sweep_start_idx:sweep_stop_idx,r_start_idx:r_stop_idx]
            zdr = radar.fields['differential_reflectivity']['data'][sweep_start_idx:sweep_stop_idx,r_start_idx:r_stop_idx]
            zv = 10*np.log10((10**(zh/10))/(zdr))

        theta_list = np.arange(360)
        r_list = np.arange(range_shape)
        clutter_flag_h = np.zeros((len(theta_list),len(r_list)))
        clutter_flag_v = np.zeros((len(theta_list),len(r_list)))

        # H POLARIZATION
        for idx_az, az in enumerate(theta_list):        #loop thru each azimuth in list
            az_mask = create_az_mask_ppi(az,theta)              #create mask for desired azimuths
            zh_rays = zh[az_mask,:]            #get Zh values for only the desired elevation and azimuth
            for idx_ra, ra in enumerate(r_list):            #loop thru each range gate in the range grid boxes (len = 80)
                if ra == range_shape:
                    continue                                    #skip the last value in the range grid
                else:
                    zh_ray_list = []
                    for idx_z, z in enumerate(zh_rays[:,idx_ra*10:idx_ra*10+10]):  #loop thru each zh value in chunks of 10 100m range gates (1 km chunks)
                        if np.any(z >= z_thresh):   
                            zh_ray_list.append(z)
                            clutter_flag_h[idx_az,idx_ra] = 1                 #flag the grid box as clutter is any zh in the 1 km chunk is greater than the threshold value

        # V POLARIZATION
        for idx_az, az in enumerate(theta_list):        #loop thru each azimuth in list
            az_mask = create_az_mask_ppi(az,theta)              #create mask for desired azimuths
            zv_rays = zv[az_mask,:]               #get Zv values for only the desired elevation and azimuth
            for idx_ra, ra in enumerate(r_list):            #loop thru each range gate in the range grid boxes (len = 80)
                if ra == range_shape-1:
                    continue                                    #skip the last value in the range grid
                else:
                    zv_ray_list = []
                    for idx_z, z in enumerate(zv_rays[:,idx_ra*10:idx_ra*10+10]):  #loop thru each zv value in chunks of 10 100m range gates (1 km chunks)
                        if np.any(z >= z_thresh):   
                            zv_ray_list.append(z)
                            clutter_flag_v[idx_az,idx_ra] = 1                 #flag the grid box as clutter is any zh in the 1 km chunk is greater than the threshold value    
    
    
        return date_time, clutter_flag_h, clutter_flag_v
