#!/usr/bin/env python
import sys
import numpy as np
import pyart
import os
import glob
import json
from netCDF4 import Dataset
from create_clutter_flag import create_clutter_flag_ppi, create_clutter_flag_hsrhi

if __name__ == "__main__":
    if len(sys.argv) < 6:
        print(
            """ERROR: Arguments are radar file directory path, clutter map netCDF output directory path,
            date (YYYYMMDD), scan type (ppi or rhi), polarization (horizontal or dual)
            """
        )
        sys.exit(0)

    datadir = sys.argv[1]
    cluttermapdir = sys.argv[2]
    date = sys.argv[3]
    scantype = sys.argv[4]
    polarization = sys.argv[5]
    print(datadir, cluttermapdir, date, scantype, polarization)

##############################################
# VARIABLES THAT SHOULD GO IN CONFIG/JSON FILE?
range_limit = 10000
site = ''
inst = ''
z_thresh = 40. 
    # could break these into a few recommended defaults for different radar bands and scan types

##############################################

# Lists to fill in loops below
clutter_flag_h = []
clutter_flag_v = []
date_time = []  # date and time, string

for f in glob.glob(os.path.join(datadir, "*" + date + "*.??")):
    print(f)
    radar = file_to_radar_object(f,extension)
    if polarization == 'horizontal':
        if scantype == 'ppi':
            dt, cflag_h = create_clutter_flag_ppi(
                            radar,
                            polarization,
                            range_limit,
                            z_thresh)
            clutter_flag_h.append(cflag_h)
            date_time.append(dt)

            
        elif scantype == 'rhi':
            dt, cflag_h = create_clutter_flag_hsrhi(
                            radar,
                            polarization,
                            range_limit,
                            z_thresh)
            clutter_flag_h.append(cflag_h)
            date_time.append(dt)

        

    elif polarization == 'dual':
        if scantype == 'ppi':
        
        elif scantype == 'rhi':