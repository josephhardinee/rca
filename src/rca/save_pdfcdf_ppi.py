#!/usr/bin/env python
import sys
import numpy as np
import pyart
import os
import glob
#import pandas as pd
from netCDF4 import Dataset 
from calculate_dbz95_ppi import calculate_dbz95_ppi

if __name__ == "__main__":
    if len(sys.argv) < 9:
        print(
            "ERROR: Arguments are PPI path, three letter site code (i.e. ena, cor), instrument (i.e. csapr2, xsapr2, kasacr, xsacr), date (YYYYMMDD), path to netCDF file containing clutter map, path to netCDF containing baseline information, baseline date (YYYYMMDD), path to output CSV file"
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

    #csv_filepath = csvdir+'daily_rcavalues_hsrhi_'+site+inst+'.csv'
    outdir = baselinedir+'figures/'

    # Empty lists to fill in loops below
    # dt = []        # date and time strings
    # dbz95_h = []   # 95th percentile reflectivity in H
    # dbz95_v = []   # 95th percentile reflectivity in V
    # sh = []        # dictionary of statistics in H
    # sv = []        # dictionary of statistics in V

    # Import clutter map information
    dataset = Dataset(cluttermapdir+'cluttermap_ppi_'+site+inst+'_composite.nc')
    clutter_map_mask_h = dataset.variables['clutter_map_mask_zh'][:,:]
    clutter_map_mask_v = dataset.variables['clutter_map_mask_zv'][:,:]
    dataset.close()

    # Import 95th percentile reflectivity values
    dataset1 = Dataset(baselinedir+'baseline_ppi_'+site+inst+'_'+baseline_date+'.nc')
    baseline_dbz95_h = dataset1.variables['baseline_dbz95_zh'][:]
    baseline_dbz95_v = dataset1.variables['baseline_dbz95_zv'][:]
    dataset1.close()

    range_limit = 5000   # integer in meters

    for f in glob.glob(os.path.join(datadir, '*xsapr*' + date + '.*.h5')):
        print(f)   # helpful for identifying which file causes a problem, may comment out if desired
        try:
            DateTime, DBZ95H, DBZ95V, SH, SV = calculate_dbz95_ppi(
            f, range_limit, clutter_map_mask_h, clutter_map_mask_v
            )
            print(DateTime)
            #print(SH)
            # Get PDF, CDF, dbz95 from the dictionaries
            pdf_h = SH['histo_n']
            cdf_h = SH['cdf']
            d95_h = SH['reflectivity_95']
            bin_h = SH['histo_bins']
            pdf_v = SV['histo_n']
            cdf_v = SV['cdf']
            d95_v = SV['reflectivity_95']
            bin_v = SV['histo_bins']

            #print(len(pdf_h),len(cdf_h),len(bin_h))#len(d95_h),len(bin_h))
            #print(f[-20:-6])
            # Create a netCDF to save to for each datetime
            d = Dataset(outdir+'pdf_ppi_'+site+inst+'_'+f[-20:-6]+'.nc',
                    'w', format='NETCDF4_CLASSIC')

            value = d.createDimension('value',1)
            stats = d.createDimension('stats',len(pdf_h))
            bins = d.createDimension('bins',len(bin_h))

            HDBZ95 = d.createVariable('dbz95_zh', np.float64, ('value',))
            VDBZ95 = d.createVariable('dbz95_zv', np.float64, ('value',))
            HPDF = d.createVariable('pdf_zh', np.float64, ('stats',))
            VPDF = d.createVariable('pdf_zv', np.float64, ('stats',))
            HCDF = d.createVariable('cdf_zh', np.float64, ('stats',))
            VCDF = d.createVariable('cdf_zv', np.float64, ('stats',))
            HBIN = d.createVariable('bin_zh', np.float64, ('bins',))
            VBIN = d.createVariable('bin_zv', np.float64, ('bins',))

            HDBZ95.long_name = 'Baseline 95th percentile reflectivity (H)'
            VDBZ95.long_name = 'Baseline 95th percentile reflectivity (V)'
            HPDF.long_name = 'PDF (H)'
            VPDF.long_name = 'PDF (V)'
            HCDF.long_name = 'CDF (H)'
            VCDF.long_name = 'CDF (V)'
            HBIN.long_name = 'Bins (H)'
            VBIN.long_name = 'Bins (V)'

            HDBZ95[:] = d95_h
            VDBZ95[:] = d95_v
            HPDF[:] = pdf_h
            VPDF[:] = pdf_v
            HCDF[:] = cdf_h
            VCDF[:] = cdf_v
            HBIN[:] = bin_h
            VBIN[:] = bin_v

            d.close()
        except IndexError or OSError:
            print('Error here')
            pass

# Sort the dates and sort the sh/sv accordingly

# Get the PDF and CDF from sh, sv and
