import numpy as np

def create_az_mask_hsrhi(azimuth_value, azimuth_array):
    "Function that creates a mask for a desired azimuth angle in an HSRHI file"
    if azimuth_value == 0.:
        az_mask = np.logical_or(np.logical_and(azimuth_array > azimuth_value-2., azimuth_array < azimuth_value+2.), azimuth_array > 358.)
    else:
        az_mask = np.logical_and(azimuth_array > azimuth_value-2., azimuth_array < azimuth_value+2.)
    return az_mask