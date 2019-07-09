import numpy as np
import pyart
from create_az_mask_hsrhi import create_az_mask_hsrhi

def create_clutter_flag_hsrhi(filename,inst,range_limit,range_shape,z_thresh):
    '''Creates a clutter flag array (precip-free day) to be used for the clutter map creation for HSRHIs
    and returns the date and time of the file and the clutter flag arrays for Zh and/or Zv'''
    
    ext = filename[-3:]
    if inst == 'kasacr':   #KaSACR is H pol only
        if ext == '.h5':
            radar = pyart.aux_io.read_gamic(filename, file_field_names=True)
            date_time = radar.time['units'].replace('seconds since ', '')
            r_start_idx = 0
            r_stop_idx = np.where(radar.range['data'] > range_limit)[0][0]
            r = radar.range['data'][r_start_idx:r_stop_idx]
            theta = radar.azimuth['data']
            zh = radar.fields['UZh']['data'][:,r_start_idx:r_stop_idx]
            elev = radar.elevation['data'] 

        #elif ext == '.nc':
        else:
            radar = pyart.io.cfradial.read_cfradial(filename, delay_field_loading=True)
            date_time = radar.time['units'].replace('seconds since ', '')
            r_start_idx = 0
            r_stop_idx = np.where(radar.range['data'] > range_limit)[0][0]
            r = radar.range['data'][r_start_idx:r_stop_idx]
            theta = radar.azimuth['data']
            zh = radar.fields['reflectivity']['data'][:,r_start_idx:r_stop_idx]
            vr = radar.fields['mean_doppler_velocity']['data'][:,r_start_idx:r_stop_idx]            
            elev = radar.elevation['data']

        elev_list = [1,2,3,4,5,175,176,177,178,179]
        theta_list = [0,30,60,90,120,150]
        r_list = np.arange(range_shape)+1
        clutter_flag_h = np.zeros((len(theta_list),len(elev_list),len(r_list)))
        vr_thresh = 0.

        # H POLARIZATION
        for idx_az, az in enumerate(theta_list):        #loop thru each azimuth in list
            az_mask = create_az_mask_hsrhi(az,theta)              #create mask for desired azimuths
            for idx_el, el in enumerate(elev_list):         #loop thru each element in desired elevation grid boxes 
                el_mask = np.abs(elev - el) < .5                #create mask for desired elevations   
                #print(az,el)
                zh_rays = zh[np.logical_and(az_mask,el_mask),:] #get Zh values for only the desired elevation and azimuth
                for idx_ra, ra in enumerate(r_list):            #loop thru each range gate in the range grid boxes (len = 80)
                    if ra == range_shape:
                        continue                                    #skip the last value in the range grid
                    else:
                        zh_ray_list = []
                        for idx_z, z in enumerate(zh_rays[:,idx_ra*10:idx_ra*10+10]):  #loop thru each zh value in chunks of 10 100m range gates (1 km chunks)
                            if np.any(z >= z_thresh):   
                                zh_ray_list.append(z)
                                clutter_flag_h[idx_az,idx_el,idx_ra] = 1                 #flag the grid box as clutter is any zh in the 1 km chunk is greater than the threshold value
    
        del radar

        return date_time, clutter_flag_h

    elif inst == 'xsacr':
        if ext == '.h5':
            radar = pyart.aux_io.read_gamic(filename, file_field_names=True)
            date_time = radar.time['units'].replace('seconds since ', '')
            r_start_idx = 0
            r_stop_idx = np.where(radar.range['data'] > range_limit)[0][0]
            r = radar.range['data'][r_start_idx:r_stop_idx]
            theta = radar.azimuth['data']
            zh = radar.fields['UZh']['data'][:,r_start_idx:r_stop_idx]
            #zv = radar.fields['UZv']['data'][:,r_start_idx:r_stop_idx]
            elev = radar.elevation['data']
        else:
            radar = pyart.io.cfradial.read_cfradial(filename, delay_field_loading=True)
            date_time = radar.time['units'].replace('seconds since ', '')
            r_start_idx = 0
            r_stop_idx = np.where(radar.range['data'] > range_limit)[0][0]
            r = radar.range['data'][r_start_idx:r_stop_idx]
            theta = radar.azimuth['data']
            zh = radar.fields['reflectivity']['data'][:,r_start_idx:r_stop_idx]
            #zv = radar.fields['uncorrected_reflectivity_v']['data'][:,r_start_idx:r_stop_idx]
            zdr = radar.fields['differential_reflectivity']['data'][:,r_start_idx:r_stop_idx]            
            elev = radar.elevation['data']

        zv = zh - zdr
        elev_list = [1,2,3,4,5,175,176,177,178,179]
        theta_list = [0,30,60,90,120,150]
        r_list = np.arange(range_shape)+1
        clutter_flag_h = np.zeros((len(theta_list),len(elev_list),len(r_list)))
        clutter_flag_v = np.zeros((len(theta_list),len(elev_list),len(r_list)))

        # H POLARIZATION
        for idx_az, az in enumerate(theta_list):        #loop thru each azimuth in list
            az_mask = create_az_mask_hsrhi(az,theta)              #create mask for desired azimuths
            for idx_el, el in enumerate(elev_list):         #loop thru each element in desired elevation grid boxes 
                el_mask = np.abs(elev - el) < .5                #create mask for desired elevations   
                #print(az,el)
                zh_rays = zh[np.logical_and(az_mask,el_mask),:] #get Zh values for only the desired elevation and azimuth
                for idx_ra, ra in enumerate(r_list):            #loop thru each range gate in the range grid boxes (len = 80)
                    if ra == range_shape:
                        continue                                    #skip the last value in the range grid
                    else:
                        zh_ray_list = []
                        for idx_z, z in enumerate(zh_rays[:,idx_ra*10:idx_ra*10+10]):  #loop thru each zh value in chunks of 10 100m range gates (1 km chunks)
                            if np.any(z >= z_thresh):
                                zh_ray_list.append(z)
                                clutter_flag_h[idx_az,idx_el,idx_ra] = 1                 #flag the grid box as clutter is any zh in the 1 km chunk is greater than the threshold value

        # V POLARIZATION
        for idx_az, az in enumerate(theta_list):        #loop thru each azimuth in list
            az_mask = create_az_mask_hsrhi(az,theta)              #create mask for desired azimuths
            for idx_el, el in enumerate(elev_list):         #loop thru each element in desired elevation grid boxes 
                el_mask = np.abs(elev - el) < .5                #create mask for desired elevations   
                #print(az,el)
                zv_rays = zv[np.logical_and(az_mask,el_mask),:] #get Zv values for only the desired elevation and azimuth
                for idx_ra, ra in enumerate(r_list):            #loop thru each range gate in the range grid boxes (len = 80)
                    if ra == range_shape:
                        continue                                    #skip the last value in the range grid
                    else:
                        zv_ray_list = []
                        for idx_z, z in enumerate(zv_rays[:,idx_ra*10:idx_ra*10+10]):  #loop thru each zv value in chunks of 10 100m range gates (1 km chunks)
                            if np.any(z >= z_thresh):
                                zv_ray_list.append(z)
                                clutter_flag_v[idx_az,idx_el,idx_ra] = 1                 #flag the grid box as clutter is any zh in the 1 km chunk is greater than the threshold value        
        del radar

        return date_time, clutter_flag_h, clutter_flag_v    
    else:
        if ext == '.h5':
            radar = pyart.aux_io.read_gamic(filename, file_field_names=True)
            date_time = radar.time['units'].replace('seconds since ', '')
            r_start_idx = 0
            r_stop_idx = np.where(radar.range['data'] > range_limit)[0][0]
            r = radar.range['data'][r_start_idx:r_stop_idx]
            theta = radar.azimuth['data']
            zh = radar.fields['UZh']['data'][:,r_start_idx:r_stop_idx]
            zv = radar.fields['UZv']['data'][:,r_start_idx:r_stop_idx]
            elev = radar.elevation['data']
        elif ext == '.nc':
            radar = pyart.io.cfradial.read_cfradial(filename, delay_field_loading=True)
            date_time = radar.time['units'].replace('seconds since ', '')
            r_start_idx = 0
            r_stop_idx = np.where(radar.range['data'] > range_limit)[0][0]
            r = radar.range['data'][r_start_idx:r_stop_idx]
            theta = radar.azimuth['data']
            zh = radar.fields['uncorrected_reflectivity_h']['data'][:,r_start_idx:r_stop_idx]
            zv = radar.fields['uncorrected_reflectivity_v']['data'][:,r_start_idx:r_stop_idx]
            elev = radar.elevation['data']

        elev_list = [1,2,3,4,5,175,176,177,178,179]
        theta_list = [0,30,60,90,120,150]
        r_list = np.arange(range_shape)+1
        clutter_flag_h = np.zeros((len(theta_list),len(elev_list),len(r_list)))
        clutter_flag_v = np.zeros((len(theta_list),len(elev_list),len(r_list)))

        # H POLARIZATION
        for idx_az, az in enumerate(theta_list):        #loop thru each azimuth in list
            az_mask = create_az_mask_hsrhi(az,theta)              #create mask for desired azimuths
            for idx_el, el in enumerate(elev_list):         #loop thru each element in desired elevation grid boxes 
                el_mask = np.abs(elev - el) < .5                #create mask for desired elevations   
                #print(az,el)
                zh_rays = zh[np.logical_and(az_mask,el_mask),:] #get Zh values for only the desired elevation and azimuth
                for idx_ra, ra in enumerate(r_list):            #loop thru each range gate in the range grid boxes (len = 80)
                    if ra == range_shape:
                        continue                                    #skip the last value in the range grid
                    else:
                        zh_ray_list = []
                        for idx_z, z in enumerate(zh_rays[:,idx_ra*10:idx_ra*10+10]):  #loop thru each zh value in chunks of 10 100m range gates (1 km chunks)
                            if np.any(z >= z_thresh):   
                                zh_ray_list.append(z)
                                clutter_flag_h[idx_az,idx_el,idx_ra] = 1                 #flag the grid box as clutter is any zh in the 1 km chunk is greater than the threshold value

        # V POLARIZATION
        for idx_az, az in enumerate(theta_list):        #loop thru each azimuth in list
            az_mask = create_az_mask_hsrhi(az,theta)              #create mask for desired azimuths
            for idx_el, el in enumerate(elev_list):         #loop thru each element in desired elevation grid boxes 
                el_mask = np.abs(elev - el) < .5                #create mask for desired elevations   
                #print(az,el)
                zv_rays = zv[np.logical_and(az_mask,el_mask),:] #get Zv values for only the desired elevation and azimuth
                for idx_ra, ra in enumerate(r_list):            #loop thru each range gate in the range grid boxes (len = 80)
                    if ra == range_shape:
                        continue                                    #skip the last value in the range grid
                    else:
                        zv_ray_list = []
                        for idx_z, z in enumerate(zv_rays[:,idx_ra*10:idx_ra*10+10]):  #loop thru each zv value in chunks of 10 100m range gates (1 km chunks)
                            if np.any(z >= z_thresh):   
                                zv_ray_list.append(z)
                                clutter_flag_v[idx_az,idx_el,idx_ra] = 1                 #flag the grid box as clutter is any zh in the 1 km chunk is greater than the threshold value    
    
        del radar

        return date_time, clutter_flag_h, clutter_flag_v 
