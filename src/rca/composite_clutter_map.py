#!/usr/bin/env python
import sys
import os
import glob
import json
import numpy as np
from netCDF4 import Dataset
from rca.modules.get_pct_on_clutter_map import (
    get_pct_on_clutter_map_ppi,
    get_pct_on_clutter_map_hsrhi,
)


def composite_clutter_map(radar_config_file):
    """
        composite_clutter_map combines all daily clutter maps available or specified into a single composite clutter map
        for use in baseline and RCA calculation later. If more than 80% of the daily clutter points occur for all the daily
        clutter maps, that is considered a composite clutter point.
        The composite clutter map (array) is written to a netCDF.

        Parameters:
        --------------
        radar_config_file: str
                    path to JSON file containing specifications:
                        data directory
                        file extension
                        daily clutter map directory
                        scan type
                        polarization
                        site
                        instrument

        Returns:
        --------------
        (no specific return)
        however, a netCDF file is written out

        """

    config_vars = json.load(open(radar_config_file))
    datadir = config_vars["data_directory"]
    extension = config_vars["file_extension"]
    cluttermap_dir = config_vars["cluttermap_directory"]
    scantype = config_vars["scan_type"]
    polarization = config_vars["polarization"]
    site = config_vars["site_abbrev"]
    inst = config_vars["instrument_abbrev"]

    clutter_mask_h = []
    clutter_mask_v = []
    clutter_pct_h = []
    clutter_pct_v = []

    if polarization == "horizontal" and scantype == "ppi":
        for f in glob.glob(
            os.path.join(
                cluttermap_dir, "cluttermap_" + scantype + "_" + site + inst + "_*.nc"
            )
        ):
            print(f)
            ClutterMaskH, ClutterPCTH = get_pct_on_clutter_map_ppi(f, polarization)
            # Append output from each HSRHI file to lists
            clutter_mask_h.append(ClutterMaskH)
            clutter_pct_h.append(ClutterPCTH)

        array_h = np.zeros(
            (
                len(clutter_mask_h),
                len(clutter_mask_h[0][:, 0]),
                len(clutter_mask_h[0][0, :]),
            )
        )
        for i in range(0, len(clutter_mask_h)):
            array_h[i, :, :] = clutter_mask_h[i]
        pct_h = np.sum(array_h, axis=0) / len(array_h[:, 0, 0])
        clutter_map_h_mask = pct_h > 0.8
        dataset = Dataset(
            cluttermap_dir
            + "cluttermap_"
            + scantype
            + "_"
            + site
            + inst
            + "_composite.nc",
            "w",
            format="NETCDF4_CLASSIC",
        )
        azi = dataset.createDimension("azi", 360)
        rang = dataset.createDimension("rang", 10)
        HPCT_ON = dataset.createVariable(
            "clutter_gate_pcts_zh", np.float64, ("azi", "rang")
        )
        HMASK = dataset.createVariable("clutter_map_mask_zh", "i1", ("azi", "rang"))
        HPCT_ON.long_name = "Clutter grid gate percentages (Zh)"
        HMASK.long_name = "Clutter map mask (Zh)"
        HPCT_ON[:, :] = pct_h
        HMASK[:, :] = clutter_map_h_mask
        dataset.close()

    elif polarization == "horizontal" and scantype == "rhi":
        for f in glob.glob(
            os.path.join(
                cluttermap_dir, "cluttermap_" + scantype + "_" + site + inst + "_*.nc"
            )
        ):
            print(f)
            ClutterMaskH, ClutterPCTH = get_pct_on_clutter_map_hsrhi(f, polarization)
            # Append output from each HSRHI file to lists
            clutter_mask_h.append(ClutterMaskH)
            clutter_pct_h.append(ClutterPCTH)

        array_h = np.zeros(
            (
                len(clutter_mask_h),
                len(clutter_mask_h[0][:, :, 0]),
                len(clutter_mask_h[0][0, :, 0]),
                len(clutter_mask_h[0][0, 0, :]),
            )
        )
        for i in range(0, len(clutter_mask_h)):
            array_h[i, :, :, :] = clutter_mask_h[i]
        # Calculate percentage of "clutter ON" for each grid box in clutter map grid
        pct_h = np.sum(array_h, axis=0) / len(array_h[:, 0, 0, 0])
        clutter_map_h_mask = pct_h > 0.8
        dataset = Dataset(
            cluttermap_dir
            + "cluttermap_"
            + scantype
            + "_"
            + site
            + inst
            + "_composite.nc"
            "w",
            format="NETCDF4_CLASSIC",
        )
        azi = dataset.createDimension("azi", 6)
        rang = dataset.createDimension("rang", 20)
        el = dataset.createDimension("el", 10)
        HPCT_ON = dataset.createVariable(
            "clutter_gate_pcts_zh", np.float64, ("azi", "el", "rang")
        )
        HMASK = dataset.createVariable(
            "clutter_map_mask_zh", "i1", ("azi", "el", "rang")
        )
        HPCT_ON.long_name = "Clutter grid gate percentages (Zh)"
        HMASK.long_name = "Clutter map mask (Zh)"
        HPCT_ON[:, :, :] = pct_h
        HMASK[:, :, :] = clutter_map_h_mask
        dataset.close()

    elif polarization == "dual" and scantype == "ppi":
        for f in glob.glob(
            os.path.join(
                cluttermap_dir, "cluttermap_" + scantype + "_" + site + inst + "_*.nc"
            )
        ):
            print(f)
            ClutterMaskH, ClutterMaskV, ClutterPCTH, ClutterPCTV = get_pct_on_clutter_map_ppi(
                f, polarization
            )
            # Append output from each HSRHI file to lists
            clutter_mask_h.append(ClutterMaskH)
            clutter_mask_v.append(ClutterMaskV)
            clutter_pct_h.append(ClutterPCTH)
            clutter_pct_v.append(ClutterPCTV)

        array_h = np.zeros(
            (
                len(clutter_mask_h),
                len(clutter_mask_h[0][:, 0]),
                len(clutter_mask_h[0][0, :]),
            )
        )
        array_v = np.zeros(
            (
                len(clutter_mask_v),
                len(clutter_mask_v[0][:, 0]),
                len(clutter_mask_v[0][0, :]),
            )
        )
        for i in range(0, len(clutter_mask_h)):
            array_h[i, :, :] = clutter_mask_h[i]
            array_v[i, :, :] = clutter_mask_v[i]
        pct_h = np.sum(array_h, axis=0) / len(array_h[:, 0, 0])
        pct_v = np.sum(array_v, axis=0) / len(array_v[:, 0, 0])
        clutter_map_h_mask = pct_h > 0.8
        clutter_map_v_mask = pct_v > 0.8
        dataset = Dataset(
            cluttermap_dir
            + "cluttermap_"
            + scantype
            + "_"
            + site
            + inst
            + "_composite.nc",
            "w",
            format="NETCDF4_CLASSIC",
        )
        azi = dataset.createDimension("azi", 360)
        rang = dataset.createDimension("rang", 10)
        HPCT_ON = dataset.createVariable(
            "clutter_gate_pcts_zh", np.float64, ("azi", "rang")
        )
        VPCT_ON = dataset.createVariable(
            "clutter_gate_pcts_zv", np.float64, ("azi", "rang")
        )
        HMASK = dataset.createVariable("clutter_map_mask_zh", "i1", ("azi", "rang"))
        VMASK = dataset.createVariable("clutter_map_mask_zv", "i1", ("azi", "rang"))
        HPCT_ON.long_name = "Clutter grid gate percentages (Zh)"
        VPCT_ON.long_name = "Clutter grid gate percentages (Zv)"
        HMASK.long_name = "Clutter map mask (Zh)"
        VMASK.long_name = "Clutter map mask (Zv)"
        HPCT_ON[:, :] = pct_h
        VPCT_ON[:, :] = pct_v
        HMASK[:, :] = clutter_map_h_mask
        VMASK[:, :] = clutter_map_v_mask
        dataset.close()

    elif polarization == "dual" and scantype == "rhi":
        for f in glob.glob(
            os.path.join(
                cluttermap_dir, "cluttermap_" + scantype + "_" + site + inst + "_*.nc"
            )
        ):
            print(f)
            ClutterMaskH, ClutterMaskV, ClutterPCTH, ClutterPCTV = get_pct_on_clutter_map_hsrhi(
                f, polarization
            )
            # Append output from each HSRHI file to lists
            print(ClutterMaskH.shape)
            clutter_mask_h.append(ClutterMaskH)
            clutter_mask_v.append(ClutterMaskV)
            clutter_pct_h.append(ClutterPCTH)
            clutter_pct_v.append(ClutterPCTV)

        array_h = np.zeros(
            (
                len(clutter_mask_h),
                len(clutter_mask_h[0][:, :, 0]),
                len(clutter_mask_h[0][0, :, 0]),
                len(clutter_mask_h[0][0, 0, :]),
            )
        )
        array_v = np.zeros(
            (
                len(clutter_mask_v),
                len(clutter_mask_v[0][:, :, 0]),
                len(clutter_mask_v[0][0, :, 0]),
                len(clutter_mask_v[0][0, 0, :]),
            )
        )

        for i in range(0, len(clutter_mask_h)):
            array_h[i, :, :, :] = clutter_mask_h[i]
            array_v[i, :, :, :] = clutter_mask_v[i]

        pct_h = np.sum(array_h, axis=0) / len(array_h[:, 0, 0, 0])
        pct_v = np.sum(array_v, axis=0) / len(array_v[:, 0, 0, 0])
        clutter_map_h_mask = pct_h > 0.8
        clutter_map_v_mask = pct_v > 0.8

        dataset = Dataset(
            cluttermap_dir
            + "cluttermap_"
            + scantype
            + "_"
            + site
            + inst
            + "_composite.nc",
            "w",
            format="NETCDF4_CLASSIC",
        )
        azi = dataset.createDimension("azi", 6)
        rang = dataset.createDimension("rang", 40)
        el = dataset.createDimension("el", 10)
        HPCT_ON = dataset.createVariable(
            "clutter_gate_pcts_zh", np.float64, ("azi", "el", "rang")
        )
        VPCT_ON = dataset.createVariable(
            "clutter_gate_pcts_zv", np.float64, ("azi", "el", "rang")
        )
        HMASK = dataset.createVariable(
            "clutter_map_mask_zh", "i1", ("azi", "el", "rang")
        )
        VMASK = dataset.createVariable(
            "clutter_map_mask_zv", "i1", ("azi", "el", "rang")
        )
        HPCT_ON.long_name = "Clutter grid gate percentages (Zh)"
        VPCT_ON.long_name = "Clutter grid gate percentages (Zv)"
        HMASK.long_name = "Clutter map mask (Zh)"
        VMASK.long_name = "Clutter map mask (Zv)"
        HPCT_ON[:, :, :] = pct_h
        VPCT_ON[:, :, :] = pct_v
        HMASK[:, :, :] = clutter_map_h_mask
        VMASK[:, :, :] = clutter_map_v_mask
        dataset.close()
