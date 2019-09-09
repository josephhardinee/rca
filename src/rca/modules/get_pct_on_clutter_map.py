import numpy as np
from netCDF4 import Dataset

# get_pct_on_clutter_map.py contains 2 functions that extract variables from clutter map files for PPI and HSRHI
# 1) get_pct_on_clutter_map_ppi: extracts clutter flag/mask for a PPI clutter map
# 2) get_pct_on_clutter_map_hsrhi: extracts clutter flag/mask for an HSRHI clutter map


def get_pct_on_clutter_map_ppi(filename, polarization):
    "Grabbing clutter maps percentages and clutter map masks from files"
    """
    get_pct_on_clutter_map_ppi grabs and returns clutter map point percentage occurrences and clutter map
    masks from daily PPI clutter maps (in either H or H and V polarizations).
    Parameters:
    --------------
    filename: .nc file
            full path to daily clutter map file
    polarization: string
            specifies for which polarization user wants to create clutter flag array
            'dual': calculate for both H and V
            'horizontal': calculate only for H
    Returns:
    --------------
    clutter_map_mask_h: array
                    array of shape (azimuth, range) noting elements where clutter is flagged in the H polarization
                    #clutter present: 1
                    #no clutter present: 0
    clutter_map_mask_v: array
                    array of shape (azimuth, range) noting elements where clutter is flagged in the V polarization
                    #clutter present: 1
                    #no clutter present: 0
    clutter_map_pcts_h: array
                    array of shape (azimuth, range) percentage occurrence values of clutter map elements in the H polarization
    clutter_map_pcts_v: array
                    array of shape (azimuth, range) percentage occurrence values of clutter map elements in the V polarization
    """
    d = Dataset(filename)
    if polarization == "horizontal":
        clutter_map_mask_h = d.variables["clutter_map_mask_zh"][:, :]
        clutter_map_pcts_h = d.variables["clutter_gate_pcts_zh"][:, :]
        d.close()

        return clutter_map_mask_h, clutter_map_pcts_h

    elif polarization == "dual":
        clutter_map_mask_h = d.variables["clutter_map_mask_zh"][:, :]
        clutter_map_mask_v = d.variables["clutter_map_mask_zv"][:, :]
        clutter_map_pcts_h = d.variables["clutter_gate_pcts_zh"][:, :]
        clutter_map_pcts_v = d.variables["clutter_gate_pcts_zv"][:, :]
        d.close()

        return (
            clutter_map_mask_h,
            clutter_map_mask_v,
            clutter_map_pcts_h,
            clutter_map_pcts_v,
        )

def get_pct_on_clutter_map_hsrhi(filename, polarization):
    "Grabbing clutter maps percentages and clutter map masks from files"
    """
    get_pct_on_clutter_map_ppi grabs and returns clutter map point percentage occurrences and clutter map
    masks from daily HSRHI clutter maps (in either H or H and V polarizations).
    Parameters:
    --------------
    filename: .nc file
            full path to daily clutter map file
    polarization: string
            specifies for which polarization user wants to create clutter flag array
            'dual': calculate for both H and V
            'horizontal': calculate only for H
    Returns:
    --------------
    clutter_map_mask_h: array
                    array of shape (azimuth, elevation, range) noting elements where clutter is flagged in the H polarization
                    #clutter present: 1
                    #no clutter present: 0
    clutter_map_mask_v: array
                    array of shape (azimuth, elevation, range) noting elements where clutter is flagged in the V polarization
                    #clutter present: 1
                    #no clutter present: 0
    clutter_map_pcts_h: array
                    array of shape (azimuth, elevation, range) percentage occurrence values of clutter map elements in the H polarization
    clutter_map_pcts_v: array
                    array of shape (azimuth, elevation, range) percentage occurrence values of clutter map elements in the V polarization
    """
    d = Dataset(filename)
    if polarization == "horizontal":
        clutter_map_mask_h = d.variables["clutter_map_mask_zh"][:, :, :]
        clutter_map_pcts_h = d.variables["clutter_gate_pcts_zh"][:, :, :]
        d.close()

        return clutter_map_mask_h, clutter_map_pcts_h

    elif polarization == "dual":
        clutter_map_mask_h = d.variables["clutter_map_mask_zh"][:, :, :]
        clutter_map_mask_v = d.variables["clutter_map_mask_zv"][:, :, :]
        clutter_map_pcts_h = d.variables["clutter_gate_pcts_zh"][:, :, :]
        clutter_map_pcts_v = d.variables["clutter_gate_pcts_zv"][:, :, :]
        d.close()

        return (
            clutter_map_mask_h,
            clutter_map_mask_v,
            clutter_map_pcts_h,
            clutter_map_pcts_v,
        )
