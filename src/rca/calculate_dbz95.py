import numpy as np
from .aux.create_masks import create_az_mask_ppi, create_az_mask_rhi


def calculate_dbz95_ppi(
<<<<<<< HEAD
    variable_dictionary, polarization, range_limit, radar_band, clutter_mask_h, clutter_mask_v=None
=======
    variable_dictionary,
    polarization,
    range_limit,
    radar_band,
    clutter_mask_h,
    clutter_mask_v=None,
>>>>>>> 4709ebfff9c7788e7ab7e4f2d1be45e84d18eb96
):
    """
    calculate_dbz95_ppi calculates the 95th percentile reflectivity for a given radar PPI file
    using the input PPI cluter map masks (H and/or V). Returns the date and time of the file,
    95th percentile reflectivity value for Zh and/or Zv, and dictionaries of statistics,
    including number of points, histogram/PDF, bins, CDF.
    
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
    dbz95_h: float (or array?)
        value of the 95th percentile clutter area reflectivity for H polarization
    stats_h: dict
        contains statistics from the PDF and CDF of the clutter area reflectivity in H polarization
        num_pts_h: number of points
        hn: number of histogram bins
        hbins: bin edges of histogram
        hp: CDF
        dbz95_h: 95th percentile reflectivity
    dbz95_v: float (or array?)
        value of the 95th percentile clutter area reflectivity for V polarization
    stats_v: dict
        contains statistics from the PDF and CDF of the clutter area reflectivity in V polarization
        num_pts_v: number of points
        vn: number of histogram bins
        vbins: bin edges of histogram
        vp: CDF
        dbz95_v: 95th percentile reflectivity

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
    #zh = zh + zh_offset
    ###########################

    range_shape = range_limit / 1000
    theta_list = np.arange(360)
    r_list = np.arange(range_shape)

    # H POLARIZATION
    zh_from_mask = []

    if radar_band == "ka":
        zh = zh + zh_offset
        for idx_az, az in enumerate(theta_list):
            az_mask = create_az_mask_ppi(az, theta, radar_band)
            zh_rays = zh[az_mask, :]
            zh_rays = np.ma.getdata(zh_rays)
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
                        zh_from_mask.append(zh_rays[:, rstart:rstop])

    else:
        for idx_az, az in enumerate(theta_list):
            az_mask = create_az_mask_ppi(az, theta, radar_band)
            zh_rays = zh[az_mask, :]
            zh_rays = np.ma.getdata(zh_rays)
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
                        zh_from_mask.append(zh_rays[:, rstart:rstop])

    all_zh = []
    for i in range(0, len(zh_from_mask)):
        if len(zh_from_mask[i]) != 0:
            for j in range(0, len(zh_from_mask[i])):
                for k in range(0, len(zh_from_mask[i][j])):
                    all_zh.append(zh_from_mask[i][j][k])

    num_pts_h = len(all_zh)
    hn, hbins = np.histogram(all_zh, bins=525, range=(-40.0, 65.0))

    # Calculate CDF of clutter area reflectivity
    hcdf = np.cumsum(hn)
    hp = hcdf / hcdf[-1] * 100
    x = np.arange(525) * (1 / 5) - 40

    # Find the value of reflectivity at the 95th percentile of CDF
    idx95 = (np.abs(hp - 95.0)).argmin()
    dbz95_h = x[idx95]


    stats_h = {
        "num_points": num_pts_h,
        "histo_n": hn,
        "histo_bins": hbins,
        "cdf": hp,
        "reflectivity_95": dbz95_h,
    }

    if polarization == "horizontal":
        return date_time, stats_h

    elif polarization == "dual":
        zv = variable_dictionary["reflectivity_v"]

        # V POLARIZATION
        zv_from_mask = []
        for idx_az, az in enumerate(theta_list):
            az_mask = create_az_mask_ppi(az, theta, radar_band)
            zv_rays = zv[az_mask, :]
            zv_rays = np.ma.getdata(zv_rays)
            for idx_ra, ra in enumerate(r_list):
                if clutter_mask_v[idx_az, idx_ra]:
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
                        zv_from_mask.append(zv_rays[:, rstart:rstop])

        all_zv = []
        for i in range(0, len(zv_from_mask)):
            if len(zv_from_mask[i]) != 0:
                for j in range(0, len(zv_from_mask[i])):
                    for k in range(0, len(zv_from_mask[i][j])):
                        all_zh.append(zv_from_mask[i][j][k])

        num_pts_v = len(all_zv)
        vn, vbins = np.histogram(all_zv, bins=525, range=(-40.0, 65.0))

        # Calculate CDF of clutter area reflectivity
        vcdf = np.cumsum(vn)
        vp = vcdf / vcdf[-1] * 100
        x = np.arange(525) * (1 / 5) - 40

        # Find the value of reflectivity at the 95th percentile of CDF
        idx95 = (np.abs(vp - 95.0)).argmin()
        dbz95_v = x[idx95]

        stats_v = {
            "num_points": num_pts_v,
            "histo_n": vn,
            "histo_bins": vbins,
            "cdf": vp,
            "reflectivity_95": dbz95_v,
        }

        return date_time, stats_h, stats_v

<<<<<<< HEAD
def calculate_dbz95_rhi(
    variable_dictionary, polarization, range_limit, radar_band, clutter_mask_h, clutter_mask_v=None
=======

def calculate_dbz95_rhi(
    variable_dictionary,
    polarization,
    range_limit,
    radar_band,
    clutter_mask_h,
    clutter_mask_v=None,
>>>>>>> 4709ebfff9c7788e7ab7e4f2d1be45e84d18eb96
):
    """
    calculate_dbz95_rhi calculates the 95th percentile reflectivity for a given radar HSRHI file
    using the input HSRHI cluter map masks (H and/or V). Returns the date and time of the file,
    95th percentile reflectivity value for Zh and/or Zv, and dictionaries of statistics,
    including number of points, histogram/PDF, bins, CDF.
    
    Parameters
    ----------
    variable_dictionary: dict
        dictionary with values, strings, and arrays of relevant radar data
        i.e. 'reflectivity_h', 'reflectivity_v', 'azimuth', 'range', 'date_time', 'elevation'
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
    dbz95_h: float (or array?)
        value of the 95th percentile clutter area reflectivity for H polarization
    stats_h: dict
        contains statistics from the PDF and CDF of the clutter area reflectivity in H polarization
        num_pts_h: number of points
        hn: number of histogram bins
        hbins: bin edges of histogram
        hp: CDF
        dbz95_h: 95th percentile reflectivity
    dbz95_v: float (or array?)
        value of the 95th percentile clutter area reflectivity for V polarization
    stats_v: dict
        contains statistics from the PDF and CDF of the clutter area reflectivity in V polarization
        num_pts_v: number of points
        vn: number of histogram bins
        vbins: bin edges of histogram
        vp: CDF
        dbz95_v: 95th percentile reflectivity

    """

    date_time = variable_dictionary["date_time"]
    r = variable_dictionary["range"]
    elev = variable_dictionary["elevation"]
    theta = variable_dictionary["azimuth"]
    zh = variable_dictionary["reflectivity_h"]

    date_int = int(date_time[0:4]+date_time[5:7]+date_time[8:10])

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
    if radar_band == 'ka' and date_int < 20190318:
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
    #a = 0.000631967738 
    #b = 0.971513669
    a = 0.00115481 #new from JCH Nov 14 2019
    b = 0.95361079
    gate_width = 0.025 #km
    iah_thresh = 0.1
    ########################################

    range_shape = range_limit / 1000
    elev_list = [1, 2, 3, 4, 5, 175, 176, 177, 178, 179]
    theta_list = [0, 30, 60, 90, 120, 150]
    r_list = np.arange(range_shape) + 1
    
    # H POLARIZATION
    zh_from_mask = []
<<<<<<< HEAD
    if radar_band == 'ka':
          iah = []
=======
    if radar_band == "ka":
>>>>>>> 4709ebfff9c7788e7ab7e4f2d1be45e84d18eb96
        for idx_az, az in enumerate(theta_list):
            if az == 0:
                continue
            else:
                pass
<<<<<<< HEAD
            az_mask = create_az_mask_hsrhi(az, theta)
            for idx_el, el in enumerate(elev_list):
                el_mask = np.abs(elev - el) < 0.5
                zh_rays = zh[np.logical_and(az_mask, el_mask), :]
                zh_rays_blank_clutter = zh_rays.copy()
                zh_rays_blank_clutter = np.ma.getdata(zh_rays_blank_clutter)
=======
            az_mask = create_az_mask_rhi(az, theta, radar_band)
            for idx_el, el in enumerate(elev_list):
                el_mask = np.abs(elev - el) < 0.5
                zh_rays = zh[np.logical_and(az_mask, el_mask), :]
>>>>>>> 4709ebfff9c7788e7ab7e4f2d1be45e84d18eb96
                for idx_ra, ra in enumerate(r_list):
                    if clutter_mask_h[idx_az, idx_el, idx_ra]:
                        if ra == range_shape:
                            continue
                        else:
                            rstart = np.where(r - (ra * 1000.0) >= 0.0)[0][0]
                            try:
<<<<<<< HEAD
                                rstop = np.where(r - (r_list[idx_ra + 1] * 1000.0) >= 0.0)[0][0]
                            except IndexError:
                                rstop = -1
                            zh_from_mask.append(zh_rays[:, rstart:rstop])
                            # Blank out clutter range gates 
                            zh_rays_blank_clutter[:, rstart:rstop] = -40.
                # Attenuation filtering
                ah_rays = a * (10**(zh_rays_blank_clutter/10))**b
                zh_rays = np.ma.getdata(zh_rays)
                iah_rays = np.empty(ah_rays.shape)
                for idx_ray, ray in enumerate(ah_rays[:,0]):
                    iah_rays[idx_ray,:] = np.cumsum(ah_rays[idx_ray,:])*gate_width*2
                iah_pass = np.ones(ah_rays.shape)
                iah_pass[iah_rays > iah_thresh] = 0
                iah.append(np.nanmean(iah_pass))
        if np.nanmean(iah) == 1:
            pass_filter = 1
        else:
            pass_filter = 0
    
    # Now for any band that is not Ka (C, X)
    else:
        for idx_az, az in enumerate(theta_list):
            az_mask = create_az_mask_hsrhi(az, theta)
=======
                                rstop = np.where(
                                    r - (r_list[idx_ra + 1] * 1000.0) >= 0.0
                                )[0][0]
                            except IndexError:
                                rstop = -1
                            zh_from_mask.append(zh_rays[:, rstart:rstop])

    # Now for any band that is not Ka (C, X)
    else:
        for idx_az, az in enumerate(theta_list):
            az_mask = create_az_mask_rhi(az, theta, radar_band)
>>>>>>> 4709ebfff9c7788e7ab7e4f2d1be45e84d18eb96
            for idx_el, el in enumerate(elev_list):
                el_mask = np.abs(elev - el) < 0.5
                zh_rays = zh[np.logical_and(az_mask, el_mask), :]
                zh_rays = np.ma.getdata(zh_rays)
                for idx_ra, ra in enumerate(r_list):
                    if clutter_mask_h[idx_az, idx_el, idx_ra]:
                        if ra == range_shape:
                            continue
                        else:
                            rstart = np.where(r - (ra * 1000.0) >= 0.0)[0][0]
                            try:
<<<<<<< HEAD
                                rstop = np.where(r - (r_list[idx_ra + 1] * 1000.0) >= 0.0)[
                                    0
                                ][0]
=======
                                rstop = np.where(
                                    r - (r_list[idx_ra + 1] * 1000.0) >= 0.0
                                )[0][0]
>>>>>>> 4709ebfff9c7788e7ab7e4f2d1be45e84d18eb96
                            except IndexError:
                                rstop = -1
                            zh_from_mask.append(zh_rays[:, rstart:rstop])

    all_zh = []
    for i in range(0, len(zh_from_mask)):
        if len(zh_from_mask[i]) != 0:
            for j in range(0, len(zh_from_mask[i])):
                for k in range(0, len(zh_from_mask[i][j])):
                    all_zh.append(zh_from_mask[i][j][k])

    num_pts_h = len(all_zh)
    hn, hbins = np.histogram(all_zh, bins=525, range=(-40.0, 65.0))
<<<<<<< HEAD
    
=======

>>>>>>> 4709ebfff9c7788e7ab7e4f2d1be45e84d18eb96
    # Calculate CDF of clutter area reflectivity
    hcdf = np.cumsum(hn)
    hp = hcdf / hcdf[-1] * 100
    x = np.arange(525) * (1 / 5) - 40
<<<<<<< HEAD
    
=======

>>>>>>> 4709ebfff9c7788e7ab7e4f2d1be45e84d18eb96
    # Find the value of reflectivity at the 95th percentile of CDF
    idx95 = (np.abs(hp - 95.0)).argmin()
    dbz95_h = x[idx95]

    if radar_band == 'ka':
        stats_h = {
            "num_points": num_pts_h,
            "histo_n": hn,
            "histo_bins": hbins,
            "cdf": hp,
            "reflectivity_95": dbz95_h,
            "pass_filter": pass_filter
    }
<<<<<<< HEAD
    else:
        stats_h = {
            "num_points": num_pts_h,
            "histo_n": hn,
            "histo_bins": hbins,
            "cdf": hp,
            "reflectivity_95": dbz95_h,
    }
=======
>>>>>>> 4709ebfff9c7788e7ab7e4f2d1be45e84d18eb96

    if polarization == "horizontal":
        return date_time, stats_h

    elif polarization == "dual":
        zv = variable_dictionary["reflectivity_v"]

        # V POLARIZATION
        zv_from_mask = []
        for idx_az, az in enumerate(theta_list):
            az_mask = create_az_mask_rhi(az, theta, radar_band)
            for idx_el, el in enumerate(elev_list):
                el_mask = np.abs(elev - el) < 0.5
                zv_rays = zv[np.logical_and(az_mask, el_mask), :]
                zv_rays = np.ma.getdata(zv_rays)
                for idx_ra, ra in enumerate(r_list):
                    if clutter_mask_v[idx_az, idx_el, idx_ra]:
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
                            zv_from_mask.append(zv_rays[:, rstart:rstop])

        all_zv = []
        for i in range(0, len(zv_from_mask)):
            if len(zv_from_mask[i]) != 0:
                for j in range(0, len(zv_from_mask[i])):
                    for k in range(0, len(zv_from_mask[i][j])):
                        all_zh.append(zv_from_mask[i][j][k])

        num_pts_v = len(all_zv)
        vn, vbins = np.histogram(all_zv, bins=525, range=(-40.0, 65.0))

        # Calculate CDF of clutter area reflectivity
        vcdf = np.cumsum(vn)
        vp = vcdf / vcdf[-1] * 100
        x = np.arange(525) * (1 / 5) - 40

        # Find the value of reflectivity at the 95th percentile of CDF
        idx95 = (np.abs(vp - 95.0)).argmin()
        dbz95_v = x[idx95]

        stats_v = {
            "num_points": num_pts_v,
            "histo_n": vn,
            "histo_bins": vbins,
            "cdf": vp,
            "reflectivity_95": dbz95_v,
        }

        return date_time, stats_h, stats_v
