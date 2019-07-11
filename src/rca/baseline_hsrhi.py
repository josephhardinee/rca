#!/usr/bin/env python
import sys
import numpy as np
import pyart
import os
import glob
from netCDF4 import Dataset
from calculate_dbz95_hsrhi import calculate_dbz95_hsrhi

"""
baseline_hsrhi loops through a day's worth of HSRHI files, calculates the median daily 95th percentile clutter area reflectivity,
and saves the value to a netcdf as the baseline 95th percentile clutter area reflectivity
"""

if __name__ == "__main__":
    if len(sys.argv) < 7:
        print(
            "ERROR: Arguments are HSRHI path, three letter site code (i.e. ena, cor), instrument (i.e. csapr2, xsapr2, kasacr, xsacr), date (YYYYMMDD), path to netCDF file containing clutter map, path to output netCDF containing baseline information"
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
    c_range = 40000
    x_range = 20000
    ka_range = 20000

    # Empty lists to fill in loops below
    dt = []  # date and time strings
    dbz95_h = []  # 95th percentile reflectivity in H
    dbz95_v = []  # 95th percentile reflectivity in V
    sh = []  # dictionary of statistics in H
    sv = []  # dictionary of statistics in V

    if inst == "csapr2":
        range_limit = c_range
        # Import clutter map information
        dataset = Dataset(
            cluttermapdir + "cluttermap_hsrhi_" + site + inst + "_composite.nc"
        )
        clutter_map_mask_h = dataset.variables["clutter_map_mask_zh"][:, :, :]
        clutter_map_mask_v = dataset.variables["clutter_map_mask_zv"][:, :, :]
        dataset.close()

        for f in glob.glob(os.path.join(datadir, "*csapr2*hsrhi*" + date + "*.??")):
            print(
                f
            )  # helpful for identifying which file causes a problem, may comment out if desired
            DateTime, DBZ95H, DBZ95V, SH, SV = calculate_dbz95_hsrhi(
                f,
                inst,
                range_limit,
                clutter_map_mask_h,
                clutter_mask_v=clutter_map_mask_v,
            )
            # Append output from each file to lists
            dt.append(DateTime)
            dbz95_h.append(DBZ95H)
            dbz95_v.append(DBZ95V)
            sh.append(SH)
            sv.append(SV)

        # Baseline 95th percentile reflectivity value calculated as mean value of 95th percentile reflectivity from all times in day
        dbz95_h_baseline = np.nanmedian(dbz95_h)
        dbz95_v_baseline = np.nanmedian(dbz95_v)
        print("DBZ95 H: ", dbz95_h_baseline, "DBZ95 V:", dbz95_v_baseline)

        # Calculate total number of radar gates used in calculation
        # H
        total_num_pts_h = []
        for i in range(0, len(sh)):
            total_num_pts_h.append(sh[i]["num_points"])
        total_num_pts_h = np.sum(total_num_pts_h)
        print("Total number of Zh gates flagged in clutter map = ", total_num_pts_h)
        # V
        total_num_pts_v = []
        for i in range(0, len(sv)):
            total_num_pts_v.append(sv[i]["num_points"])
        total_num_pts_v = np.sum(total_num_pts_v)
        print("Total number of Zv gates flagged in clutter map = ", total_num_pts_v)

        # Write baseline 95th reflectivity values to a netCDF file
        d = Dataset(
            baselinedir + "baseline_hsrhi_" + site + inst + "_" + date + ".nc",
            "w",
            format="NETCDF4_CLASSIC",
        )
        value = d.createDimension("value", 1)
        HDBZ95_BASE = d.createVariable("baseline_dbz95_zh", np.float64, ("value",))
        VDBZ95_BASE = d.createVariable("baseline_dbz95_zv", np.float64, ("value",))
        HDBZ95_BASE.long_name = "Baseline 95th percentile reflectivity (H)"
        VDBZ95_BASE.long_name = "Baseline 95th percentile reflectivity (V)"
        HDBZ95_BASE[:] = dbz95_h_baseline
        VDBZ95_BASE[:] = dbz95_v_baseline
        d.close()

    elif inst == "xsacr":
        range_limit = x_range
        # Import clutter map information
        dataset = Dataset(
            cluttermapdir + "cluttermap_hsrhi_" + site + inst + "_composite.nc"
        )
        clutter_map_mask_h = dataset.variables["clutter_map_mask_zh"][:, :, :]
        clutter_map_mask_v = dataset.variables["clutter_map_mask_zv"][:, :, :]
        dataset.close()

        for f in glob.glob(os.path.join(datadir, "*xsacr*hsrhi*" + date + "*.??")):
            print(
                f
            )  # helpful for identifying which file causes a problem, may comment out if desired
            try:
                DateTime, DBZ95H, DBZ95V, SH, SV = calculate_dbz95_hsrhi(
                    f,
                    inst,
                    range_limit,
                    clutter_map_mask_h,
                    clutter_mask_v=clutter_map_mask_v,
                )
            except IndexError:
                print("Bad file or problem")
            # Append output from each file to lists
            dt.append(DateTime)
            dbz95_h.append(DBZ95H)
            dbz95_v.append(DBZ95V)
            sh.append(SH)
            sv.append(SV)

        # Baseline 95th percentile reflectivity value calculated as mean value of 95th percentile reflectivity from all times in day
        dbz95_h_baseline = np.nanmedian(dbz95_h)
        dbz95_v_baseline = np.nanmedian(dbz95_v)
        print("DBZ95 H: ", dbz95_h_baseline, "DBZ95 V:", dbz95_v_baseline)

        # Calculate total number of radar gates used in calculation
        # H
        total_num_pts_h = []
        for i in range(0, len(sh)):
            total_num_pts_h.append(sh[i]["num_points"])
        total_num_pts_h = np.sum(total_num_pts_h)
        print("Total number of Zh gates flagged in clutter map = ", total_num_pts_h)
        # V
        total_num_pts_v = []
        for i in range(0, len(sv)):
            total_num_pts_v.append(sv[i]["num_points"])
        total_num_pts_v = np.sum(total_num_pts_v)
        print("Total number of Zv gates flagged in clutter map = ", total_num_pts_v)

        # Write baseline 95th reflectivity values to a netCDF file
        d = Dataset(
            baselinedir + "baseline_hsrhi_" + site + inst + "_" + date + ".nc",
            "w",
            format="NETCDF4_CLASSIC",
        )
        value = d.createDimension("value", 1)
        HDBZ95_BASE = d.createVariable("baseline_dbz95_zh", np.float64, ("value",))
        VDBZ95_BASE = d.createVariable("baseline_dbz95_zv", np.float64, ("value",))
        HDBZ95_BASE.long_name = "Baseline 95th percentile reflectivity (H)"
        VDBZ95_BASE.long_name = "Baseline 95th percentile reflectivity (V)"
        HDBZ95_BASE[:] = dbz95_h_baseline
        VDBZ95_BASE[:] = dbz95_v_baseline
        d.close()

    elif inst == "kasacr":
        range_limit = ka_range
        # Import clutter map information
        # dataset = Dataset(cluttermapdir+'cluttermap_hsrhi_'+site+inst+'_composite.nc')
        dataset = Dataset(
            cluttermapdir + "cluttermap_hsrhi_" + site + inst + "_" + date + ".nc"
        )
        clutter_map_mask_h = dataset.variables["clutter_map_mask_zh"][:, :, :]
        dataset.close()

        for f in glob.glob(os.path.join(datadir, "*kasacr*hsrhi*" + date + "*.??")):
            print(
                f
            )  # helpful for identifying which file causes a problem, may comment out if desired
            try:
                DateTime, DBZ95H, SH = calculate_dbz95_hsrhi(
                    f, inst, range_limit, clutter_map_mask_h, clutter_mask_v=None
                )
            except IndexError:
                print("Bad file or problem")
            # else:
            #    DateTime, DBZ95H, SH = calculate_dbz95_hsrhi(f,inst,range_limit,clutter_map_mask_h,clutter_mask_v=None)
            # Append output from each file to lists
            dt.append(DateTime)
            dbz95_h.append(DBZ95H)
            sh.append(SH)
        # Baseline 95th percentile reflectivity value calculated as mean value of 95th percentile reflectivity from all times in day
        dbz95_h_baseline = np.nanmedian(dbz95_h)
        print("DBZ95 H: ", dbz95_h_baseline)

        # Calculate total number of radar gates used in calculation
        # H
        total_num_pts_h = []
        for i in range(0, len(sh)):
            total_num_pts_h.append(sh[i]["num_points"])
        total_num_pts_h = np.sum(total_num_pts_h)
        print("Total number of Zh gates flagged in clutter map = ", total_num_pts_h)

        # Write baseline 95th reflectivity values to a netCDF file
        d = Dataset(
            baselinedir + "baseline_hsrhi_" + site + inst + "_" + date + ".nc",
            "w",
            format="NETCDF4_CLASSIC",
        )
        value = d.createDimension("value", 1)
        HDBZ95_BASE = d.createVariable("baseline_dbz95_zh", np.float64, ("value",))
        HDBZ95_BASE.long_name = "Baseline 95th percentile reflectivity (H)"
        HDBZ95_BASE[:] = dbz95_h_baseline
        d.close()
