import numpy as np
from .aux.create_masks import create_az_mask_ppi, create_az_mask_hsrhi

def calculate_dbz95_ppi(
    variable_dictionary, polarization, range_limit, clutter_mask_h, clutter_mask_v=None
):
    """
    calculate_dbz95_hsrhi calculates the 95th percentile reflectivity for a given radar HSRHI file
    using the input HSRHI cluter map masks (H and/or V). Returns the date and time of the file,
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

    range_shape = range_limit / 1000
    theta_list = np.arange(360)
    r_list = np.arange(range_shape)

    # H POLARIZATION
    zh_from_mask = []
    for idx_az, az in enumerate(theta_list):
        az_mask = create_az_mask_ppi(az, theta)
        zh_rays = zh[az_mask, :]
        zh_rays = np.ma.getdata(zh_rays)
        for idx_ra, ra in enumerate(r_list):
            if clutter_mask_h[idx_az, idx_ra]:
                if ra == range_shape:
                    continue
                else:
                    rstart = np.where(r - (ra * 1000.0) >= 0.0)[0][0]
                    try:
                        rstop = np.where(r - (r_list[idx_ra + 1] * 1000.0) >= 0.0)[0][0]
                    except IndexError:
                        rstop = -1
                    zh_from_mask.append(zh_rays[:, rstart:rstop])

    all_zh = []
    for i in range(0, len(zh_from_mask)):
        if len(zh_from_mask[i]) != 0:
            for j in range(0, len(zh_from_mask[i])):
                for k in range(0, len(zh_from_mask[i][j])):
                    all_zh.append(zh_from_mask[i][j][k])
    print("num pts = ", len(all_zh))

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
    print("dbz95H = ", dbz95_h)
    if polarization == "horizontal":
        return date_time, dbz95_h, stats_h

    elif polarization == "dual":
        zv = variable_dictionary["reflectivity_v"]

        # V POLARIZATION
        zv_from_mask = []
        for idx_az, az in enumerate(theta_list):
            az_mask = create_az_mask_ppi(az, theta)
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
        print("num pts = ", len(all_zv))

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
        print("dbz95V = ", dbz95_v)
        return date_time, dbz95_h, dbz95_v, stats_h, stats_v


def calculate_dbz95_hsrhi(
    variable_dictionary, polarization, range_limit, clutter_mask_h, clutter_mask_v=None
):
    """
    calculate_dbz95_hsrhi calculates the 95th percentile reflectivity for a given radar HSRHI file
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

    range_shape = range_limit / 1000
    elev_list = [1, 2, 3, 4, 5, 175, 176, 177, 178, 179]
    theta_list = [0, 30, 60, 90, 120, 150]
    r_list = np.arange(range_shape) + 1

    # H POLARIZATION
    zh_from_mask = []
    for idx_az, az in enumerate(theta_list):
        az_mask = create_az_mask_hsrhi(az, theta)
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
    print("num pts = ", len(all_zh))

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
    print("dbz95H = ", dbz95_h)
    if polarization == "horizontal":
        return date_time, dbz95_h, stats_h

    elif polarization == "dual":
        zv = variable_dictionary["reflectivity_v"]

        # V POLARIZATION
        zv_from_mask = []
        for idx_az, az in enumerate(theta_list):
            az_mask = create_az_mask_hsrhi(az, theta)
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
        print("num pts = ", len(all_zv))

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
        print("dbz95V = ", dbz95_v)
        return date_time, dbz95_h, dbz95_v, stats_h, stats_v
