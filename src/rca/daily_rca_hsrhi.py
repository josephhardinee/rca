#!/usr/bin/env python
import sys
import numpy as np
import pyart
import os
import glob
import pandas as pd
from netCDF4 import Dataset 
from calculate_dbz95_hsrhi import calculate_dbz95_hsrhi

if __name__ == "__main__":
    if len(sys.argv) < 9:
        print(
            "ERROR: Arguments are HSRHI path, three letter site code (i.e. ena, cor), instrument (i.e. csapr2, xsapr2, kasacr, xsacr), date (YYYYMMDD), path to netCDF file containing clutter map, path to netCDF containing baseline information, baseline date (YYYYMMDD), path to output CSV file"
        )
        sys.exit(0)

    datadir = sys.argv[1]
    site = sys.argv[2]
    inst = sys.argv[3]
    date = sys.argv[4]
    cluttermapdir = sys.argv[5]
    baselinedir = sys.argv[6]
    baseline_date = sys.argv[7]
    csvdir = sys.argv[8]
    print(datadir, site, inst, date, cluttermapdir, baselinedir, baseline_date, csvdir)

    csv_filepath = csvdir+'daily_rcavalues_hsrhi_'+site+inst+'.csv'

    # Empty lists to fill in loops below
    dt = []        # date and time strings
    dbz95_h = []   # 95th percentile reflectivity in H
    dbz95_v = []   # 95th percentile reflectivity in V
    sh = []        # dictionary of statistics in H
    sv = []        # dictionary of statistics in V

    # Different range limits for different radar bands, in meters
    c_range = 40000
    x_range = 20000
    ka_range = 20000

    if inst == 'csapr2':
        # Import clutter map information
        dataset = Dataset(cluttermapdir+'cluttermap_hsrhi_'+site+inst+'_composite.nc')
        clutter_map_mask_h = dataset.variables['clutter_map_mask_zh'][:,:,:]
        clutter_map_mask_v = dataset.variables['clutter_map_mask_zv'][:,:,:]
        dataset.close()

        # Import 95th percentile reflectivity values
        dataset1 = Dataset(baselinedir+'baseline_hsrhi_'+site+inst+'_'+baseline_date+'.nc')
        baseline_dbz95_h = dataset1.variables['baseline_dbz95_zh'][:]
        baseline_dbz95_v = dataset1.variables['baseline_dbz95_zv'][:]
        dataset1.close()

        range_limit = c_range

        for f in glob.glob(os.path.join(datadir, '*csapr2*hsrhi*' + date + '*.??')):
            print(f)   # helpful for identifying which file causes a problem, may comment out if desired
            try:
                DateTime, DBZ95H, DBZ95V, SH, SV = calculate_dbz95_hsrhi(
                f, inst, range_limit, clutter_map_mask_h, clutter_mask_v = clutter_map_mask_v
            )
            except IndexError or OSError:
                print('Error here')
                pass

            # Append output from each file to lists
            dt.append(DateTime)
            dbz95_h.append(DBZ95H)
            dbz95_v.append(DBZ95V)
            sh.append(SH)
            sv.append(SV)

        # Daily 95th percentile reflectivity value calculated as mean value of 95th percentile reflectivity from all times in day            
        dbz95_h_mean = np.nanmedian(dbz95_h)
        dbz95_v_mean = np.nanmedian(dbz95_v)

        rca_h = baseline_dbz95_h[0] - dbz95_h_mean
        rca_v = baseline_dbz95_v[0] - dbz95_v_mean

        print('RCA H: ',rca_h, 'RCA V: ',rca_v)

        yr = date[0:4]
        mon = date[4:6]
        day = date[6:]

        base = 0  # set to 0 for daily RCA, set to 1 when calculating for baseline
        date = yr + "-" + mon + "-" + day

        # Create dictionary and dataframe
        csv_frame = pd.read_csv(csv_filepath)
        #import pdb; pdb.set_trace()

        rca_dict = {
            "DATE": date, "RCA_H": rca_h, "RCA_V": rca_v, "BASELINE": base
            }
        csv_frame = csv_frame.append(rca_dict, ignore_index=True)
        csv_frame.set_index('DATE')
        csv_frame.to_csv(csv_filepath , index=False)

    elif inst == 'xsacr':
        # Import clutter map information
        dataset = Dataset(cluttermapdir+'cluttermap_hsrhi_'+site+inst+'_composite.nc')
        clutter_map_mask_h = dataset.variables['clutter_map_mask_zh'][:,:,:]
        clutter_map_mask_v = dataset.variables['clutter_map_mask_zv'][:,:,:]
        dataset.close()

        # Import 95th percentile reflectivity values
        dataset1 = Dataset(baselinedir+'baseline_hsrhi_'+site+inst+'_'+baseline_date+'.nc')
        baseline_dbz95_h = dataset1.variables['baseline_dbz95_zh'][:]
        baseline_dbz95_v = dataset1.variables['baseline_dbz95_zv'][:]
        dataset1.close()

        range_limit = x_range
        
        for f in glob.glob(os.path.join(datadir, '*xsacr*hsrhi*' + date + '*.??')):
            print(f)
            try:
                DateTime, DBZ95H, DBZ95V, SH, SV = calculate_dbz95_hsrhi(
                f, inst, range_limit, clutter_map_mask_h, clutter_mask_v = clutter_map_mask_v
            )
                # Append output from each file to lists
                dt.append(DateTime)
                dbz95_h.append(DBZ95H)
                dbz95_v.append(DBZ95V)
                sh.append(SH)
                sv.append(SV)
            except IndexError:# or OSError:
                print('Error here')
                pass

            # Append output from each file to lists
            #dt.append(DateTime)
            #dbz95_h.append(DBZ95H)
            #dbz95_v.append(DBZ95V)
            #sh.append(SH)
            #sv.append(SV)

        # Daily 95th percentile reflectivity value calculated as mean value of 95th percentile reflectivity from all times in day            
        dbz95_h_mean = np.nanmedian(dbz95_h)
        dbz95_v_mean = np.nanmedian(dbz95_v)

        rca_h = baseline_dbz95_h[0] - dbz95_h_mean
        rca_v = baseline_dbz95_v[0] - dbz95_v_mean

        print('RCA H: ',rca_h, 'RCA V: ',rca_v)

        yr = date[0:4]
        mon = date[4:6]
        day = date[6:]

        base = 0  # set to 0 for daily RCA, set to 1 when calculating for baseline
        date = yr + "-" + mon + "-" + day

        # Create dictionary and dataframe
        csv_frame = pd.read_csv(csv_filepath)
        #import pdb; pdb.set_trace()

        rca_dict = {
            "DATE": date, "RCA_H": rca_h, "RCA_V": rca_v, "BASELINE": base
            }
        csv_frame = csv_frame.append(rca_dict, ignore_index=True)
        csv_frame.set_index('DATE')
        csv_frame.to_csv(csv_filepath , index=False)

    if inst == 'kasacr':
        # Import clutter map information
        dataset = Dataset(cluttermapdir+'cluttermap_hsrhi_'+site+inst+'_composite.nc')
        #dataset = Dataset(cluttermapdir+'cluttermap_hsrhi_'+site+inst+'_20190306.nc')
        clutter_map_mask_h = dataset.variables['clutter_map_mask_zh'][:,:,:]
        dataset.close()

        # Import 95th percentile reflectivity values
        dataset1 = Dataset(baselinedir+'baseline_hsrhi_'+site+inst+'_'+baseline_date+'.nc')
        baseline_dbz95_h = dataset1.variables['baseline_dbz95_zh'][:]
        dataset1.close()

        range_limit = ka_range

        for f in glob.glob(os.path.join(datadir, '*kasacr*hsrhi*'+date+'*.??')):
            print(f)
            try:
                DateTime, DBZ95H, SH = calculate_dbz95_hsrhi(
                f, inst, range_limit, clutter_map_mask_h, clutter_mask_v = None
            )
            except IndexError or OSError:
                print('Error here')
                pass

            # Put all PPI times into a list
            dt.append(DateTime)
            dbz95_h.append(DBZ95H)
            sh.append(SH)
        
        # Daily 95th percentile reflectivity value calculated as mean value of 95th percentile reflectivity from all times in day        
        dbz95_h_mean = np.nanmedian(dbz95_h)

        rca_h = baseline_dbz95_h[0] - dbz95_h_mean

        print('RCA H: ',rca_h)

        yr = date[0:4]
        mon = date[4:6]
        day = date[6:]

        base = 0  # set to 0 for daily RCA, set to 1 when calculating for baseline
        date = yr + "-" + mon + "-" + day

        # Create dictionary and dataframe
        csv_frame = pd.read_csv(csv_filepath)
        #import pdb; pdb.set_trace()

        rca_dict = {
            "DATE": date, "RCA_H": rca_h, "RCA_V": np.nan, "BASELINE": base
            }
        csv_frame = csv_frame.append(rca_dict, ignore_index=True)
        csv_frame.set_index('DATE')
        csv_frame.to_csv(csv_filepath , index=False)          
