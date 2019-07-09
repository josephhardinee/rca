#!/usr/bin/env python
import sys
import numpy as np
import pyart
import os
import glob
from netCDF4 import Dataset 
from create_clutter_flag_ppi import create_clutter_flag_ppi

if __name__ == "__main__":
    if len(sys.argv) < 6:
        print(
            "ERROR: Arguments are PPI path, three letter site code (i.e. ena, cor), instrument (i.e. csapr2, xsapr2, kasacr, xsacr), date (YYYYMMDD), output path for netCDF file containing clutter map array"
        )
        sys.exit(0)

    datadir = sys.argv[1]
    site = sys.argv[2]
    inst = sys.argv[3]
    date = sys.argv[4]
    cluttermapdir = sys.argv[5]
    print(datadir, site, inst, date, cluttermapdir)

    # Lists to fill in loops below
    clutter_flag_h = []
    clutter_flag_v = []
    dt = []             # date and time, string

    if inst == 'kasacr':
        range_limit = 10000   # integer in meters
        range_shape = range_limit/1000 
        z_thresh = 10.   # reflectivity threshold, dBZ

        for f in glob.glob(os.path.join(datadir, '*kasacr*'+date+'*.??')):
            print(f)
            DateTime, ClutterFlagH = create_clutter_flag_ppi(f,inst,range_limit,range_shape,z_thresh)
            
            # Append output from each file to lists
            clutter_flag_h.append(ClutterFlagH)
            dt.append(DateTime)

        clutter_flag_h = np.asarray(clutter_flag_h)
    
        # Calculate percentage of "clutter ON" for each grid box in clutter map grid
        pct_h = np.sum(clutter_flag_h,axis=0)/len(clutter_flag_h[:,0,0])
        print('PCT_ON H shape: ',pct_h.shape)

        # Create mask for clutter percentages greater than 50%
        clutter_map_h_mask = pct_h > 0.5

        # Write clutter map arrays to netCDF file
        dataset = Dataset(cluttermapdir+'cluttermap_ppi_'+site+inst+'_'+date+'.nc',
                        'w',format='NETCDF4_CLASSIC')
        azi = dataset.createDimension('azi', 360)
        rang = dataset.createDimension('rang', range_shape)
    
        HPCT_ON = dataset.createVariable('clutter_gate_pcts_zh', np.float64, ('azi','rang'))
        HMASK = dataset.createVariable('clutter_map_mask_zh', 'i1', ('azi','rang'))

        HPCT_ON.long_name = 'Clutter grid gate percentages (Zh)'
        HMASK.long_name = 'Clutter map mask (Zh)'

        HPCT_ON[:,:] = pct_h
        HMASK[:,:] = clutter_map_h_mask

        dataset.close()

    else:
        if inst == 'xsapr2':
            range_limit = 5000   # integer in meters
            range_shape = range_limit/1000 
            z_thresh = 40.   # reflectivity threshold, dBZ

            for f in glob.glob(os.path.join(datadir, '*xsapr*.sec_XSAPR2_'+date+'*.h5')):
                print(f)
                DateTime, ClutterFlagH, ClutterFlagV = create_clutter_flag_ppi(f,inst,range_limit,range_shape,z_thresh)
            
                # Append output from each file to lists
                clutter_flag_h.append(ClutterFlagH)
                clutter_flag_v.append(ClutterFlagV)
                dt.append(DateTime)
                
        elif inst == 'xsaprI4' or inst == 'xsaprI5':
            range_limit = 10000   # integer in meters
            range_shape = range_limit/1000 
            date_mod = date[2:8]
            z_thresh = 40.   # reflectivity threshold, dBZ

            for f in glob.glob(os.path.join(datadir, 'X*'+date_mod+'*.RAW*')):
                print(f)
                DateTime, ClutterFlagH, ClutterFlagV = create_clutter_flag_ppi(f,inst,range_limit,range_shape,z_thresh)
            
                # Append output from each file to lists
                clutter_flag_h.append(ClutterFlagH)
                clutter_flag_v.append(ClutterFlagV)
                dt.append(DateTime)

        elif inst == 'csapr2':
            range_limit = 10000   # integer in meters
            range_shape = range_limit/1000
            z_thresh = 45.   # reflectivity threshold, dBZ

            for f in glob.glob(os.path.join(datadir, '*csapr2*ppi*'+date+'*.nc')):
                print(f)
                DateTime, ClutterFlagH, ClutterFlagV = create_clutter_flag_ppi(f,inst,range_limit,range_shape,z_thresh)
            
                # Append output from each file to lists
                clutter_flag_h.append(ClutterFlagH)
                clutter_flag_v.append(ClutterFlagV)
                dt.append(DateTime)

        clutter_flag_h = np.asarray(clutter_flag_h)
        clutter_flag_v = np.asarray(clutter_flag_v)
    
        # Calculate percentage of "clutter ON" for each grid box in clutter map grid
        pct_h = np.sum(clutter_flag_h,axis=0)/len(clutter_flag_h[:,0,0])
        pct_v = np.sum(clutter_flag_v,axis=0)/len(clutter_flag_v[:,0,0])
        print('PCT_ON H shape: ',pct_h.shape, 'PCT_ON V shape: ',pct_v.shape)

        # Create mask for clutter percentages greater than 50%
        clutter_map_h_mask = pct_h > 0.5
        clutter_map_v_mask = pct_v > 0.5

        # Write clutter map arrays to netCDF file
        dataset = Dataset(cluttermapdir+'cluttermap_ppi_'+site+inst+'_'+date+'.nc',
                        'w',format='NETCDF4_CLASSIC')
        azi = dataset.createDimension('azi', 360)
        rang = dataset.createDimension('rang', range_shape)
    
        HPCT_ON = dataset.createVariable('clutter_gate_pcts_zh', np.float64, ('azi','rang'))
        VPCT_ON = dataset.createVariable('clutter_gate_pcts_zv', np.float64, ('azi','rang'))
        HMASK = dataset.createVariable('clutter_map_mask_zh', 'i1', ('azi','rang'))
        VMASK = dataset.createVariable('clutter_map_mask_zv', 'i1', ('azi','rang'))

        HPCT_ON.long_name = 'Clutter grid gate percentages (Zh)'
        VPCT_ON.long_name = 'Clutter grid gate percentages (Zv)'
        HMASK.long_name = 'Clutter map mask (Zh)'
        VMASK.long_name = 'Clutter map mask (Zv)'

        HPCT_ON[:,:] = pct_h
        VPCT_ON[:,:] = pct_v
        HMASK[:,:] = clutter_map_h_mask
        VMASK[:,:] = clutter_map_v_mask

        dataset.close()
