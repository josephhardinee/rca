import numpy as np

def create_az_mask_ppi(azimuth_value, azimuth_array):
    "Function that creates a mask for a desired azimuth angle in a PPI file"
    if azimuth_value == 0.:
        az_mask = np.logical_or(np.logical_and(azimuth_array > azimuth_value-0.5, azimuth_array < azimuth_value+0.5), azimuth_array > 359.5)
    else:
        az_mask = np.logical_and(azimuth_array > azimuth_value-0.5, azimuth_array < azimuth_value+0.5)
    return az_mask