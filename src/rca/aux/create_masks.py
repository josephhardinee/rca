import numpy as np

# create_masks contains functions to be used in RCA calculations
# 1) create_az_mask_ppi: creates a mask for a desired azimuth angle in a PPI file
# 2) create_az_mask_hsrhi: creates a mask for a desired azimuth angle in a RHI file


def create_az_mask_ppi(azimuth_value, azimuth_array):
    """
    create_az_mask_ppi creates a mask for a desired azimuth angle for an array of azimuth from a radar PPI file
    
    Parameters
    ----------
    azimuth_value: float
        value of the radar azimuth of interest
        i.e. 0., 27., 60., 120., etc.
    azimuth_array: array_like
        array of azimuth values to search through and find the appropriate azimuth
    
    Returns
    -------
    az_mask: MaskedArray
        array of same shape as azimuth_array, masked to highlight the desried azimuth value
    
    """
    
    if azimuth_value == 0.0:
        az_mask = np.logical_or(
            np.logical_and(
                azimuth_array > azimuth_value - 0.5, azimuth_array < azimuth_value + 0.5
            ),
            azimuth_array > 359.5,
        )
    else:
        az_mask = np.logical_and(
            azimuth_array > azimuth_value - 0.5, azimuth_array < azimuth_value + 0.5
        )
    return az_mask


def create_az_mask_hsrhi(azimuth_value, azimuth_array):
    """
    create_az_mask_hsrhi creates a mask for a desired azimuth angle for an array of azimuth from a radar HSRHI file
    
    Parameters
    ----------
    azimuth_value: float
        value of the radar azimuth of interest
        i.e. 30., 60., 120., etc.
    azimuth_array: array_like
        array of azimuth values to search through and find the appropriate azimuth
    
    Returns
    -------
    az_mask: MaskedArray
        array of same shape as azimuth_array, masked to highlight the desried azimuth value
    
    """
    
    if azimuth_value == 0.0:
        az_mask = np.logical_or(
            np.logical_and(
                azimuth_array > azimuth_value - 2.0, azimuth_array < azimuth_value + 2.0
            ),
            azimuth_array > 358.0,
        )
    else:
        az_mask = np.logical_and(
            azimuth_array > azimuth_value - 2.0, azimuth_array < azimuth_value + 2.0
        )
    return az_mask
