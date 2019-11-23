import numpy as np

# create_masks contains functions to be used in RCA calculations
# 1) create_az_mask_ppi: creates a mask for a desired azimuth angle in a PPI file
# 2) create_az_mask_rhi: creates a mask for a desired azimuth angle in a RHI file


def create_az_mask_ppi(azimuth_value, azimuth_array, radar_band):
    """
    create_az_mask_ppi creates a mask for a desired azimuth angle for an array of azimuth from a radar PPI file
    
    Parameters
    ----------
    azimuth_value: float
        value of the radar azimuth of interest
        i.e. 0., 27., 60., 120., etc.
    azimuth_array: array_like
        array of azimuth values to search through and find the appropriate azimuth
    radar_band: str
        one or two letter code noting radar band (used for thresholding depending on beam width)
    
    Returns
    -------
    az_mask: MaskedArray
        array of same shape as azimuth_array, masked to highlight the desried azimuth value
    
    """

    if radar_band == "c":
        threshold = 0.5
    elif radar_band == "x":
        threshold = 0.5
    elif radar_band == "ka":
        threshold = 0.1

    if azimuth_value == 0.0:
        az_mask = np.logical_or(
            np.logical_and(
                azimuth_array > azimuth_value - threshold,
                azimuth_array < azimuth_value + threshold,
            ),
            azimuth_array > 360 - threshold,
        )
    else:
        az_mask = np.logical_and(
            azimuth_array > azimuth_value - threshold,
            azimuth_array < azimuth_value + threshold,
        )
    return az_mask


def create_az_mask_rhi(azimuth_value, azimuth_array, radar_band):
    """
    create_az_mask_rhi creates a mask for a desired azimuth angle for an array of azimuth from a radar RHI file
    
    Parameters
    ----------
    azimuth_value: float
        value of the radar azimuth of interest
        i.e. 30., 60., 120., etc.
    azimuth_array: array_like
        array of azimuth values to search through and find the appropriate azimuth
    radar_band: str
        one or two letter code noting radar band (used for thresholding depending on beam width)
    
    Returns
    -------
    az_mask: MaskedArray
        array of same shape as azimuth_array, masked to highlight the desried azimuth value
    
    """

    if radar_band == "c":
        threshold = 0.4
    elif radar_band == "x":
        threshold = 0.4
    elif radar_band == "ka":
        threshold = 0.1

    if azimuth_value == 0.0:
        az_mask = np.logical_or(
            np.logical_and(
                azimuth_array > azimuth_value - threshold,
                azimuth_array < azimuth_value + threshold,
            ),
            azimuth_array > 360 - threshold,
        )
    else:
        az_mask = np.logical_and(
            azimuth_array > azimuth_value - threshold,
            azimuth_array < azimuth_value + threshold,
        )
    return az_mask
