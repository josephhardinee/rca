import numpy as np
from .aux.create_masks import create_az_mask_ppi, create_az_mask_rhi

# Attenutation filter function for Ka band
# Looks a lot like calculate dbz95 code

# def function(one file)
# iah filter like in calcdbz95
# return a 1 or 0 for passing or not passing

def iah_filter_ppi(
    variable_dictionary,
    polarization,
    range_limit,
    radar_band,
    clutter_mask_h,
    clutter_mask_v=None,
):
    """
    iah_filter_ppi uses a previously generated clutter map to 1) identify clutter gates;
    2) blank out identified clutter gates; 3) calculate integrated attentuation along each ray;
    4) threshold for integrated attentuation; 5) return a 1 or 0 for passing or not passing IAH filter
    
    Parameters
    ----------
    variable_dictionary: dict
        dictionary with values, strings, and arrays of relevant radar data
        i.e. 'reflectivity_h', 'reflectivity_v', 'azimuth', 'range', 'date_time'
    polarization: str
        specifies for which polarization user wants to create clutter flag array
        'dual': calculate for both H and V
        'horizontal': calculate only for H
    range_limit: int
        value of desired radar gate range limit
    radar_band: str
        one or two letter code for radar band
    clutter_mask_h: MaskedArray
        masked array denotes which elements are considered clutter
        used to extract reflectivity values from overlapping radar gates
        for H polarization
    clutter_mask_h: MaskedArray
        masked array denotes which elements are considered clutter
        used to extract reflectivity values from overlapping radar gates
        for V polarization
        default is None, array must be provided if calculating for V polarization
    
    Returns
    -------
    date_time: str
        date and time of the file
    pass_filter: int
        0 or 1 (0=no, 1=yes)

    """

    date_time = variable_dictionary["date_time"]
    r = variable_dictionary["range"]
    theta = variable_dictionary["azimuth"]
    zh = variable_dictionary["reflectivity_h"]

    ###########################
    # Special case
    #    KASACR calibration constant during CACTI
    #    zh(corrected) = zh(in_file) + zh_offset
    #    BEFORE 2019-03-18 16:42:33 UTC
    #        dirt on waveguide, reflectivity low
    #        zh_offset = 10.6 + difference of RCA going backward in time
    #    AFTER 2019-03-18 16:42:33 UTC
    #        waveguide cleaned
    #        zh_offset = 10.6
    zh_offset = 10.6
    zh = zh + zh_offset
    ###########################

    #######################################
    # Attenutation filtering
    # If a ray surpasses a certain threshold of integrated attenutation
    # (based on an Ah-Z relationship)
    # the whole file is ignored and move on to next file
    # i.e. dump out NaN for dbz95
    # FOR TESTING, OUTPUT TYPICAL DBZ95, JUST FLAG AS *WOULD BE TRASHED*
    # Ah = az^b, where z is in mm6m-3
    # Z = 10log10(z)  mm6m-3 => dBZ
    # z = 10^(Z/10)   dBZ => mm6m-3
    # ah = a * (10**(zh/10)) **b
    # a = 0.000631967738
    # b = 0.971513669
    a = 0.00115481  # new from JCH Nov 14 2019
    b = 0.95361079
    gate_width = 0.025  # km
    iah_thresh = 0.1
    ########################################

    range_shape = range_limit / 1000
    theta_list = np.arange(360)
    r_list = np.arange(range_shape)

    # H POLARIZATION
    zh_from_mask = []
    iah = []
    for idx_az, az in enumerate(theta_list):
        az_mask = create_az_mask_ppi(az, theta, radar_band)
        zh_rays_blank_clutter = zh[az_mask, :]
        zh_rays_blank_clutter = np.ma.getdata(zh_rays_blank_clutter)
        for idx_ra, ra in enumerate(r_list):
            if clutter_mask_h[idx_az, idx_ra]:
                if ra == range_shape:
                    continue
                else:
                    rstart = np.where(r - (ra * 1000.0) >= 0.0)[0][0]
                    try:
                        rstop = np.where(r - (r_list[idx_ra + 1] * 1000.0) >= 0.0)[
                            0
                        ][0]
                    except IndexError:
                        rstop = -1
                    # Blank out clutter range gates
                    zh_rays_blank_clutter[:, rstart:rstop] = -40.0
        # Attenuation filtering
        ah_rays = a * (10 ** (zh_rays_blank_clutter / 10)) ** b
        zh_rays = np.ma.getdata(zh_rays)
        iah_rays = np.empty(ah_rays.shape)
        for idx_ray, ray in enumerate(ah_rays[:, 0]):
            iah_rays[idx_ray, :] = np.cumsum(ah_rays[idx_ray, :]) * gate_width * 2
        iah_pass = np.ones(ah_rays.shape)
        iah_pass[iah_rays > iah_thresh] = 0
        iah.append(np.nanmean(iah_pass))

    if np.nanmean(iah) == 1:
        pass_filter = 1
    else:
        pass_filter = 0

    if polarization == "horizontal":
        return date_time, pass_filter

def iah_filter_rhi(
    variable_dictionary,
    polarization,
    range_limit,
    radar_band,
    clutter_mask_h,
    clutter_mask_v=None,
):
    """
    iah_filter_rhi uses a previously generated clutter map to 1) identify clutter gates;
    2) blank out identified clutter gates; 3) calculate integrated attentuation along each ray;
    4) threshold for integrated attentuation; 5) return a 1 or 0 for passing or not passing IAH filter
    
    Parameters
    ----------
    variable_dictionary: dict
        dictionary with values, strings, and arrays of relevant radar data
        i.e. 'reflectivity_h', 'reflectivity_v', 'azimuth', 'range', 'date_time'
    polarization: str
        specifies for which polarization user wants to create clutter flag array
        'dual': calculate for both H and V
        'horizontal': calculate only for H
    range_limit: int
        value of desired radar gate range limit
    radar_band: str
        one or two letter code for radar band
    clutter_mask_h: MaskedArray
        masked array denotes which elements are considered clutter
        used to extract reflectivity values from overlapping radar gates
        for H polarization
    clutter_mask_h: MaskedArray
        masked array denotes which elements are considered clutter
        used to extract reflectivity values from overlapping radar gates
        for V polarization
        default is None, array must be provided if calculating for V polarization
    
    Returns
    -------
    date_time: str
        date and time of the file
    pass_filter: int
        0 or 1 (0=no, 1=yes)

    """

    date_time = variable_dictionary["date_time"]
    r = variable_dictionary["range"]
    elev = variable_dictionary["elevation"]
    theta = variable_dictionary["azimuth"]
    zh = variable_dictionary["reflectivity_h"]

    ###########################
    # Special case
    #    KASACR calibration constant during CACTI
    #    zh(corrected) = zh(in_file) + zh_offset
    #    BEFORE 2019-03-18 16:42:33 UTC
    #        dirt on waveguide, reflectivity low
    #        zh_offset = 10.6 + difference of RCA going backward in time
    #    AFTER 2019-03-18 16:42:33 UTC
    #        waveguide cleaned
    #        zh_offset = 10.6
    zh_offset = 10.6
    zh = zh + zh_offset
    ###########################

    #######################################
    # Attenutation filtering
    # If a ray surpasses a certain threshold of integrated attenutation
    # (based on an Ah-Z relationship)
    # the whole file is ignored and move on to next file
    # i.e. dump out NaN for dbz95
    # FOR TESTING, OUTPUT TYPICAL DBZ95, JUST FLAG AS *WOULD BE TRASHED*
    # Ah = az^b, where z is in mm6m-3
    # Z = 10log10(z)  mm6m-3 => dBZ
    # z = 10^(Z/10)   dBZ => mm6m-3
    # ah = a * (10**(zh/10)) **b
    # a = 0.000631967738
    # b = 0.971513669
    a = 0.00115481  # new from JCH Nov 14 2019
    b = 0.95361079
    gate_width = 0.025  # km
    iah_thresh = 0.1
    ########################################

    range_shape = range_limit / 1000
    elev_list = [1, 2, 3, 4, 5, 175, 176, 177, 178, 179]
    theta_list = [0, 30, 60, 90, 120, 150]
    r_list = np.arange(range_shape) + 1

    # H POLARIZATION
    zh_from_mask = []
    iah = []

    for idx_az, az in enumerate(theta_list):
        if az == 0:
            continue
        else:
            pass
        az_mask = create_az_mask_rhi(az, theta, radar_band)
        for idx_el, el in enumerate(elev_list):
            el_mask = np.abs(elev - el) < 0.5
            zh_rays_blank_clutter = zh[np.logical_and(az_mask, el_mask), :]
            zh_rays_blank_clutter = np.ma.getdata(zh_rays_blank_clutter)
            for idx_ra, ra in enumerate(r_list):
                if clutter_mask_h[idx_az, idx_el, idx_ra]:
                    if ra == range_shape:
                        continue
                    else:
                        rstart = np.where(r - (ra * 1000.0) >= 0.0)[0][0]
                        try:
                            rstop = np.where(
                                r - (r_list[idx_ra + 1] * 1000.0) >= 0.0
                            )[0][0]
                        except IndexError:
                            rstop = -1
                        # Blank out clutter range gates
                        zh_rays_blank_clutter[:, rstart:rstop] = -40.0
            # Attenuation filtering
            ah_rays = a * (10 ** (zh_rays_blank_clutter / 10)) ** b
            iah_rays = np.empty(ah_rays.shape)
            for idx_ray, ray in enumerate(ah_rays[:, 0]):
                iah_rays[idx_ray, :] = (
                    np.cumsum(ah_rays[idx_ray, :]) * gate_width * 2
                )
            iah_pass = np.ones(ah_rays.shape)
            iah_pass[iah_rays > iah_thresh] = 0
            iah.append(np.nanmean(iah_pass))

    if np.nanmean(iah) == 1:
        pass_filter = 1
    else:
        pass_filter = 0

    if polarization == "horizontal":
        return date_time, pass_filter






