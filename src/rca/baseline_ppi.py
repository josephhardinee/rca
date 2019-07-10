#!/usr/bin/env python
import sys
import numpy as np
import pyart
import os
import glob
from netCDF4 import Dataset 
from calculate_dbz95_ppi import calculate_dbz95_ppi

"""
baseline_ppi loops through a day's worth of PPI files, calculates the median daily 95th percentile clutter area reflectivity,
and saves the value to a netcdf as the baseline 95th percentile clutter area reflectivity
"""

if __name__ == "__main__":
    if len(sys.argv) < 7:
        print(
            "ERROR: Arguments are PPI path, date (YYYYMMDD), three letter site code (i.e. ena, cor), instrument (i.e. csapr2, xsapr2, kasacr, xsacr), path to netCDF file containing clutter map, path to output netCDF containing baseline information"
        )
        sys.exit(0)

    datadir = sys.argv[1]
    site = sys.argv[2]
    inst = sys.argv[3]
    date = sys.argv[4]
    cluttermapdir = sys.argv[5]
    baselinedir = sys.argv[6]
    print(datadir, site, inst, date, cluttermapdir, baselinedir)

    # Different range limits for different radar bands, in meters
    c_range = 10000
    x_range = 5000
    ka_range = 10000
    
    # Empty lists to fill in loops below
    dt = []        # date and time strings
    dbz95_h = []   # 95th percentile reflectivity in H
    dbz95_v = []   # 95th percentile reflectivity in V
    sh = []        # dictionary of statistics in H
    sv = []        # dictionary of statistics in V
    dbz93_h = []
    dbz97_h = []
    
    if inst == 'kasacr':
        range_limit = ka_range
        # Import clutter map information
        #dataset = Dataset(cluttermapdir+'cluttermap_ppi_'+site+inst+'_composite.nc')
        dataset = Dataset(cluttermapdir+'cluttermap_ppi_'+site+inst+'_'+date+'.nc')
        clutter_map_mask_h = dataset.variables['clutter_map_mask_zh'][:,:]
        dataset.close()

        for f in glob.glob(os.path.join(datadir, '*kasacr*'+date+'*.??')):
            print(f)   # helpful for identifying which file causes a problem, may comment out if desired
            DateTime, DBZ95H, SH = calculate_dbz95_ppi(f,inst,range_limit,clutter_map_mask_h,clutter_mask_v=None)
            # Append output from each file to lists
            dt.append(DateTime)
            dbz95_h.append(DBZ95H)
            sh.append(SH)

        # Baseline 95th percentile reflectivity value calculated as mean value of 95th percentile reflectivity from all times in day     
        dbz95_h_baseline = np.nanmedian(dbz95_h)
        print('DBZ95 H: ',dbz95_h_baseline)
    
        # Calculate total number of radar gates used in calculation
        # H
        total_num_pts_h = []
        for i in range(0,len(sh)):
            total_num_pts_h.append(sh[i]['num_points'])
        total_num_pts_h = np.sum(total_num_pts_h)
        print('Total number of Zh gates flagged in clutter map = ',total_num_pts_h)

        # Write baseline 95th reflectivity values to a netCDF file
        d = Dataset(baselinedir+'baseline_ppi_'+site+inst+'_'+date+'.nc',
                'w', format='NETCDF4_CLASSIC')
        value = d.createDimension('value',1)
        HDBZ95_BASE = d.createVariable('baseline_dbz95_zh', np.float64, ('value',))
        HDBZ95_BASE.long_name = 'Baseline 95th percentile reflectivity (H)'
        HDBZ95_BASE[:] = dbz95_h_baseline
        d.close()

    elif inst == 'xsapr2':
        range_limit = x_range
        # Import clutter map information
        dataset = Dataset(cluttermapdir+'cluttermap_ppi_'+site+inst+'_composite.nc')
        #dataset = Dataset(cluttermapdir+'cluttermap_ppi_'+site+inst+'_'+date'.nc')
        clutter_map_mask_h = dataset.variables['clutter_map_mask_zh'][:,:]
        clutter_map_mask_v = dataset.variables['clutter_map_mask_zv'][:,:]
        dataset.close()

        for f in glob.glob(os.path.join(datadir, '*xsapr*.sec_XSAPR2_'+date+'*.h5')):
            print(f)   # helpful for identifying which file causes a problem, may comment out if desired
            DateTime, DBZ95H, DBZ95V, SH, SV = calculate_dbz95_ppi(f,inst,range_limit,clutter_map_mask_h,clutter_mask_v=clutter_map_mask_v)
            # Append output from each file to lists
            dt.append(DateTime)
            dbz95_h.append(DBZ95H)
            dbz95_v.append(DBZ95V)
            sh.append(SH)
            sv.append(SV)
        
        # Baseline 95th percentile reflectivity value calculated as mean value of 95th percentile reflectivity from all times in day     
        dbz95_h_baseline = np.nanmedian(dbz95_h)
        dbz95_v_baseline = np.nanmedian(dbz95_v)
        print('DBZ95 H: ',dbz95_h_baseline, 'DBZ95 V:',dbz95_v_baseline)
    
        # Calculate total number of radar gates used in calculation
        # H
        total_num_pts_h = []
        for i in range(0,len(sh)):
            total_num_pts_h.append(sh[i]['num_points'])
        total_num_pts_h = np.sum(total_num_pts_h)
        print('Total number of Zh gates flagged in clutter map = ',total_num_pts_h)
        # V
        total_num_pts_v = []
        for i in range(0,len(sv)):
            total_num_pts_v.append(sv[i]['num_points'])
        total_num_pts_v = np.sum(total_num_pts_v)
        print('Total number of Zv gates flagged in clutter map = ',total_num_pts_v)

        # Write baseline 95th reflectivity values to a netCDF file
        d = Dataset(baselinedir+'baseline_ppi_'+site+inst+'_'+date+'.nc',
                'w', format='NETCDF4_CLASSIC')
        value = d.createDimension('value',1)
        HDBZ95_BASE = d.createVariable('baseline_dbz95_zh', np.float64, ('value',))
        VDBZ95_BASE = d.createVariable('baseline_dbz95_zv', np.float64, ('value',))
        HDBZ95_BASE.long_name = 'Baseline 95th percentile reflectivity (H)'
        VDBZ95_BASE.long_name = 'Baseline 95th percentile reflectivity (V)'
        HDBZ95_BASE[:] = dbz95_h_baseline
        VDBZ95_BASE[:] = dbz95_v_baseline
        d.close()
        
    elif inst == 'xsaprI4' or inst == 'xsaprI5':
        range_limit = c_range
        date_mod = date[2:8]
        # Import clutter map information
        dataset = Dataset(cluttermapdir+'cluttermap_ppi_'+site+inst+'_composite.nc')
        #dataset = Dataset(cluttermapdir+'cluttermap_ppi_'+site+inst+'_'+date'.nc')
        clutter_map_mask_h = dataset.variables['clutter_map_mask_zh'][:,:]
        clutter_map_mask_v = dataset.variables['clutter_map_mask_zv'][:,:]
        print(clutter_map_mask_v)
        dataset.close()

        for f in glob.glob(os.path.join(datadir, 'X*'+date_mod+'*.RAW*')):
            print(f)   # helpful for identifying which file causes a problem, may comment out if desired
            DateTime, DBZ95H, DBZ95V, SH, SV = calculate_dbz95_ppi(f,inst,range_limit,clutter_map_mask_h,clutter_mask_v=clutter_map_mask_v)
            # Append output from each file to lists
            dt.append(DateTime)
            dbz95_h.append(DBZ95H)
            dbz95_v.append(DBZ95V)
            sh.append(SH)
            sv.append(SV)
            dbz93_h.append(SH['reflectivity_93'])
            dbz97_h.append(SH['reflectivity_97'])
        
        # Baseline 95th percentile reflectivity value calculated as mean value of 95th percentile reflectivity from all times in day     
        dbz95_h_baseline = np.nanmedian(dbz95_h)
        dbz95_v_baseline = np.nanmedian(dbz95_v)
        dbz93_h_baseline = np.nanmedian(dbz93_h)
        dbz97_h_baseline = np.nanmedian(dbz97_h)
        print('DBZ95 H: ',dbz95_h_baseline, 'DBZ95 V:',dbz95_v_baseline)
    
        # Calculate total number of radar gates used in calculation
        # H
        total_num_pts_h = []
        for i in range(0,len(sh)):
            total_num_pts_h.append(sh[i]['num_points'])
        total_num_pts_h = np.sum(total_num_pts_h)
        print('Total number of Zh gates flagged in clutter map = ',total_num_pts_h)
        # V
        total_num_pts_v = []
        for i in range(0,len(sv)):
            total_num_pts_v.append(sv[i]['num_points'])
        total_num_pts_v = np.sum(total_num_pts_v)
        print('Total number of Zv gates flagged in clutter map = ',total_num_pts_v)

        # Write baseline 95th reflectivity values to a netCDF file
        d = Dataset(baselinedir+'baseline_ppi_'+site+inst+'_'+date+'.nc',
                'w', format='NETCDF4_CLASSIC')
        value = d.createDimension('value',1)
        HDBZ95_BASE = d.createVariable('baseline_dbz95_zh', np.float64, ('value',))
        VDBZ95_BASE = d.createVariable('baseline_dbz95_zv', np.float64, ('value',))
        HDBZ93_BASE = d.createVariable('baseline_dbz93_zh', np.float64, ('value',))
        HDBZ97_BASE = d.createVariable('baseline_dbz97_zh', np.float64, ('value',))
        HDBZ95_BASE.long_name = 'Baseline 95th percentile reflectivity (H)'
        VDBZ95_BASE.long_name = 'Baseline 95th percentile reflectivity (V)'
        HDBZ93_BASE.long_name = 'Baseline 93th percentile reflectivity (H)'
        HDBZ97_BASE.long_name = 'Baseline 97th percentile reflectivity (H)'
        HDBZ95_BASE[:] = dbz95_h_baseline
        VDBZ95_BASE[:] = dbz95_v_baseline
        HDBZ93_BASE[:] = dbz93_h_baseline
        HDBZ97_BASE[:] = dbz97_h_baseline
        d.close()

    elif inst == 'csapr2':
        range_limit = c_range
        # Import clutter map information
        dataset = Dataset(cluttermapdir+'cluttermap_ppi_'+site+inst+'_composite.nc')
        #dataset = Dataset(cluttermapdir+'cluttermap_ppi_'+site+inst+'_'+date'.nc')
        clutter_map_mask_h = dataset.variables['clutter_map_mask_zh'][:,:]
        clutter_map_mask_v = dataset.variables['clutter_map_mask_zv'][:,:]
        dataset.close()
        
        for f in glob.glob(os.path.join(datadir, '*csapr2*ppi*'+date+'*.??')):
            print(f)   # helpful for identifying which file causes a problem, may comment out if desired
            DateTime, DBZ95H, DBZ95V, SH, SV = calculate_dbz95_ppi(f,inst,range_limit,clutter_map_mask_h,clutter_mask_v=clutter_map_mask_v)
            # Append output from each file to lists
            dt.append(DateTime)
            dbz95_h.append(DBZ95H)
            dbz95_v.append(DBZ95V)
            sh.append(SH)
            sv.append(SV)
        
        # Baseline 95th percentile reflectivity value calculated as mean value of 95th percentile reflectivity from all times in day     
        dbz95_h_baseline = np.nanmedian(dbz95_h)
        dbz95_v_baseline = np.nanmedian(dbz95_v)
        print('DBZ95 H: ',dbz95_h_baseline, 'DBZ95 V:',dbz95_v_baseline)
    
        # Calculate total number of radar gates used in calculation
        # H
        total_num_pts_h = []
        for i in range(0,len(sh)):
            total_num_pts_h.append(sh[i]['num_points'])
        total_num_pts_h = np.sum(total_num_pts_h)
        print('Total number of Zh gates flagged in clutter map = ',total_num_pts_h)
        # V
        total_num_pts_v = []
        for i in range(0,len(sv)):
            total_num_pts_v.append(sv[i]['num_points'])
        total_num_pts_v = np.sum(total_num_pts_v)
        print('Total number of Zv gates flagged in clutter map = ',total_num_pts_v)

        # Write baseline 95th reflectivity values to a netCDF file
        d = Dataset(baselinedir+'baseline_ppi_'+site+inst+'_'+date+'.nc',
                'w', format='NETCDF4_CLASSIC')
        value = d.createDimension('value',1)
        HDBZ95_BASE = d.createVariable('baseline_dbz95_zh', np.float64, ('value',))
        VDBZ95_BASE = d.createVariable('baseline_dbz95_zv', np.float64, ('value',))
        HDBZ95_BASE.long_name = 'Baseline 95th percentile reflectivity (H)'
        VDBZ95_BASE.long_name = 'Baseline 95th percentile reflectivity (V)'
        HDBZ95_BASE[:] = dbz95_h_baseline
        VDBZ95_BASE[:] = dbz95_v_baseline
        d.close()

    