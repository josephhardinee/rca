import numpy as np
from netCDF4 import Dataset

def pct_on_clutter_map_hsrhi(filename, clutter_v=None):
    "Grabbing clutter maps percentages and clutter map masks from files"
    d = Dataset(filename)
    if clutter_v == None:
        clutter_map_mask_h = d.variables['clutter_map_mask_zh'][:,:]
        clutter_map_pcts_h = d.variables['clutter_gate_pcts_zh'][:,:]
        d.close()
        
        return clutter_map_mask_h, clutter_map_pcts_h
    
    else:    
        clutter_map_mask_h = d.variables['clutter_map_mask_zh'][:,:]
        clutter_map_mask_v = d.variables['clutter_map_mask_zv'][:,:]
        clutter_map_pcts_h = d.variables['clutter_gate_pcts_zh'][:,:]
        clutter_map_pcts_v = d.variables['clutter_gate_pcts_zv'][:,:]
        d.close()

        return clutter_map_mask_h, clutter_map_mask_v, clutter_map_pcts_h, clutter_map_pcts_v
