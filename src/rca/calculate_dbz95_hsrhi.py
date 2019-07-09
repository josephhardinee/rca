import numpy as np
import pyart
from create_az_mask_hsrhi import create_az_mask_hsrhi

def calculate_dbz95_hsrhi(filename,inst,range_limit,clutter_mask_h,clutter_mask_v=None):
    """
    calculate_dbz95_hsrhi calculates the 95th percentile reflectivity for a given HSRHI scan
    using the input HSRHI cluter map masks (H and/or V). Returns the date and time of the file,
    95th percentile reflectivity value for Zh and/or Zv, and dictionaries of statistics,
    including number of points, histogram/PDF, bins, CDF.
    """

    # Use a different reader for different file types (i.e. .h5, .nc)
    ext = filename[-3:]

    if inst == 'kasacr':   #KaSACR is H polarization only
        if ext == '.h5':
            radar = pyart.aux_io.read_gamic(filename, file_field_names=True)
            date_time = radar.time['units'].replace('seconds since ', '')
            r_start_idx = 0
            r_stop_idx = np.where(radar.range['data'] > range_limit)[0][0]
            r = radar.range['data'][r_start_idx:r_stop_idx]
            theta = radar.azimuth['data']
            zh = radar.fields['UZh']['data'][:,r_start_idx:r_stop_idx]
            elev = radar.elevation['data']
        else:
            radar = pyart.io.cfradial.read_cfradial(filename, delay_field_loading=True)
            date_time = radar.time['units'].replace('seconds since ', '')
            r_start_idx = 0
            r_stop_idx = np.where(radar.range['data'] > range_limit)[0][0]
            r = radar.range['data'][r_start_idx:r_stop_idx]
            theta = radar.azimuth['data']
            zh = radar.fields['reflectivity']['data'][:,r_start_idx:r_stop_idx]
            elev = radar.elevation['data']

        range_shape = range_limit/1000
        elev_list = [1,2,3,4,5,175,176,177,178,179]
        theta_list = [0,30,60,90,120,150]
        r_list = np.arange(range_shape)+1

        # Artificially increase/decrease reflectivity values for testing
        #zh = zh-5.

        # H POLARIZATION
        zh_from_mask = []
        for idx_az, az in enumerate(theta_list):
            az_mask = create_az_mask_hsrhi(az,theta)
            for idx_el, el in enumerate(elev_list):
                el_mask = np.abs(elev - el) < .5
                zh_rays = zh[np.logical_and(az_mask,el_mask),:]
                zh_rays = np.ma.getdata(zh_rays)
                zh_list = []
                for idx_ra, ra in enumerate(r_list):
                    if clutter_mask_h[idx_az,idx_el,idx_ra]:
                        zh_list.append(zh_rays[:,idx_ra*10:idx_ra*10+10])
                zh_from_mask.append(zh_list)
        
        all_zh = []
        for i in range(0,len(zh_from_mask)):
            zh_from_mask[i] = np.array(zh_from_mask[i])
            if len(zh_from_mask[i]) != 0:
                for ia,a in enumerate(zh_from_mask[i][:,0,0]):
                    for ib,b in enumerate(zh_from_mask[i][0,:,0]):
                        for ic,c in enumerate(zh_from_mask[i][0,0,:]):
                            all_zh.append(zh_from_mask[i][ia,ib,ic])  

        num_pts_h = len(all_zh)

        hn,hbins=np.histogram(all_zh,bins=525,range=(-40.,65.))
        # Calculate CDF of clutter area reflectivity
        hcdf = np.cumsum(hn)
        hp = hcdf/hcdf[-1]*100
        # Find coefficients of 13th degree polynomial for CDF
        x = np.arange(525)*(1/5)-40
        #hcoeff = np.polyfit(hp,x,13)
        #hpoly_func = np.poly1d(hcoeff)
        # Find the value of reflectivity at the 95th percentile of CDF
        idx95 = (np.abs(hp - 95.)).argmin()
        #dbz95_h = hpoly_func(95.)  
        dbz95_h = x[idx95]

        stats_h = { 'num_points':num_pts_h,
                    'histo_n':hn,
                    'histo_bins':hbins,
                    'cdf':hp,
                    #'polynomial_func':hpoly_func,
                    'reflectivity_95':dbz95_h,
                    }

        del radar

        return date_time, dbz95_h, stats_h

    else:
        if inst == 'xsacr':
            radar = pyart.io.cfradial.read_cfradial(filename, delay_field_loading=True)
            date_time = radar.time['units'].replace('seconds since ', '')
            r_start_idx = 0
            r_stop_idx = np.where(radar.range['data'] > range_limit)[0][0]
            # Get variables (only the rays/gates needed)
            r = radar.range['data'][r_start_idx:r_stop_idx]
            theta = radar.azimuth['data']
            zh = radar.fields['reflectivity']['data'][:,r_start_idx:r_stop_idx]
            #zv = radar.fields['uncorrected_reflectivity_v']['data'][:,r_start_idx:r_stop_idx]
            zdr = radar.fields['differential_reflectivity']['data'][:,r_start_idx:r_stop_idx]            
            elev = radar.elevation['data']
            zv = zh - zdr
        else:        
            if ext == '.h5':
                radar = pyart.aux_io.read_gamic(filename, file_field_names=True)
                date_time = radar.time['units'].replace('seconds since ', '')
                r_start_idx = 0
                r_stop_idx = np.where(radar.range['data'] > range_limit)[0][0]
                # Get variables (only the rays/gates needed)
                r = radar.range['data'][r_start_idx:r_stop_idx]
                theta = radar.azimuth['data']
                zh = radar.fields['UZh']['data'][:,r_start_idx:r_stop_idx]
                zv = radar.fields['UZv']['data'][:,r_start_idx:r_stop_idx]
                elev = radar.elevation['data']
            else:
                radar = pyart.io.cfradial.read_cfradial(filename, delay_field_loading=True)
                date_time = radar.time['units'].replace('seconds since ', '')
                r_start_idx = 0
                r_stop_idx = np.where(radar.range['data'] > range_limit)[0][0]
                # Get variables (only the rays/gates needed)
                r = radar.range['data'][r_start_idx:r_stop_idx]
                theta = radar.azimuth['data']
                zh = radar.fields['uncorrected_reflectivity_h']['data'][:,r_start_idx:r_stop_idx]
                zv = radar.fields['uncorrected_reflectivity_v']['data'][:,r_start_idx:r_stop_idx]
                elev = radar.elevation['data']       

        range_shape = range_limit/1000
        elev_list = [1,2,3,4,5,175,176,177,178,179]
        theta_list = [0,30,60,90,120,150]
        r_list = np.arange(range_shape)+1

        # Artificially increase/decrease reflectivity values for testing
        #zh = zh-5.
        #zv = zv-5.

        # H POLARIZATION
        zh_from_mask = []
        for idx_az, az in enumerate(theta_list):
            az_mask = create_az_mask_hsrhi(az,theta)
            for idx_el, el in enumerate(elev_list):
                el_mask = np.abs(elev - el) < .5
                zh_rays = zh[np.logical_and(az_mask,el_mask),:]
                zh_rays = np.ma.getdata(zh_rays)
                zh_list = []
                for idx_ra, ra in enumerate(r_list):
                    if clutter_mask_h[idx_az,idx_el,idx_ra]:
                        zh_list.append(zh_rays[:,idx_ra*10:idx_ra*10+10])
                zh_from_mask.append(zh_list)

        all_zh = []
        for i in range(0,len(zh_from_mask)):
            zh_from_mask[i] = np.array(zh_from_mask[i])
            if len(zh_from_mask[i]) != 0:
                for ia,a in enumerate(zh_from_mask[i][:,0,0]):
                    for ib,b in enumerate(zh_from_mask[i][0,:,0]):
                        for ic,c in enumerate(zh_from_mask[i][0,0,:]):
                            all_zh.append(zh_from_mask[i][ia,ib,ic])  

        num_pts_h = len(all_zh)

        hn,hbins=np.histogram(all_zh,bins=525,range=(-40.,65.))
        # Calculate CDF of clutter area reflectivity
        hcdf = np.cumsum(hn)
        hp = hcdf/hcdf[-1]*100
        # Find coefficients of 13th degree polynomial for CDF
        x = np.arange(525)*(1/5)-40
        #hcoeff = np.polyfit(hp,x,13)
        #hpoly_func = np.poly1d(hcoeff)
        # Find the value of reflectivity at the 95th percentile of CDF
        idx95 = (np.abs(hp - 95.)).argmin()
        #dbz95_h = hpoly_func(95.)  
        dbz95_h = x[idx95]

        stats_h = { 'num_points':num_pts_h,
                    'histo_n':hn,
                    'histo_bins':hbins,
                    'cdf':hp,
                    #'polynomial_func':hpoly_func,
                    'reflectivity_95':dbz95_h,
                    }

        # V POLARIZATION
        zv_from_mask = []
        for idx_az, az in enumerate(theta_list):
            az_mask = create_az_mask_hsrhi(az,theta)
            for idx_el, el in enumerate(elev_list):
                el_mask = np.abs(elev - el) < .5
                zv_rays = zv[np.logical_and(az_mask,el_mask),:]
                zv_rays = np.ma.getdata(zv_rays)
                zv_list = []
                for idx_ra, ra in enumerate(r_list):
                    if clutter_mask_v[idx_az,idx_el,idx_ra]:
                        zv_list.append(zv_rays[:,idx_ra*10:idx_ra*10+10])
                zv_from_mask.append(zv_list)

        all_zv = []
        for i in range(0,len(zv_from_mask)):
            zv_from_mask[i] = np.array(zv_from_mask[i])
            if len(zv_from_mask[i]) != 0:
                for ia,a in enumerate(zv_from_mask[i][:,0,0]):
                    for ib,b in enumerate(zv_from_mask[i][0,:,0]):
                        for ic,c in enumerate(zv_from_mask[i][0,0,:]):
                            all_zv.append(zv_from_mask[i][ia,ib,ic])    

        num_pts_v = len(all_zv)

        vn,vbins=np.histogram(all_zv,bins=525,range=(-40.,65.))
        # Calculate CDF of clutter area reflectivity
        vcdf = np.cumsum(vn)
        vp = vcdf/vcdf[-1]*100
        # Find coefficients of 13th degree polynomial for CDF
        x = np.arange(525)*(1/5)-40
        #vcoeff = np.polyfit(vp,x,13)
        #vpoly_func = np.poly1d(vcoeff)
        # Find the value of reflectivity at the 95th percentile of CDF
        idx95 = (np.abs(vp - 95.)).argmin()
        #dbz95_v = vpoly_func(95.)  
        dbz95_v = x[idx95]

        stats_v = { 'num_points':num_pts_v,
                    'histo_n':vn,
                    'histo_bins':vbins,
                    'cdf':vp,
                    #'polynomial_func':vpoly_func,
                    'reflectivity_95':dbz95_v,
                    }

        del radar
        
        return date_time, dbz95_h, dbz95_v, stats_h, stats_v
