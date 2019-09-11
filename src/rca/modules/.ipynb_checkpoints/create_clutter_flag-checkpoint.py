import numpy as np
from modules.create_masks import create_az_mask_ppi, create_az_mask_hsrhi

# create_clutter_flag contains 2 functions to create clutter flags (masks) for radar PPI and HSRHI files
# 1) create_clutter_flag_ppi: creates clutter flag/mask for a radar PPI file
# 2) create_clutter_flag_hsrhi: creates clutter flag/mask for a radar HSRHI file


def create_clutter_flag_ppi(variable_dictionary, polarization, range_limit, z_thresh):
    """
    create_clutter_flag_ppi creates a clutter flag array for a particular PPI radar file (using a precipitation-free day) that will be used for
    clutter map creation. It returns the datetime of the file and the clutter flag arrays for reflectivity in the chosen polarizations (H and V or just H)
    Parameters:
    --------------
    variable_dictionary: dict
                    dictionary with values, strings, and arrays of relevant radar data
                    i.e.
                    'reflectivity_h', 'reflectivity_v', 'azimuth', 'range', 'date_time'
    polarization: string
            specifies for which polarization user wants to create clutter flag array
            'dual': calculate for both H and V
            'horizontal': calculate only for H
    range_limit: integer
            value of desired radar gate range limit
    z_thresh: float
            reflectivity threshold for clutter cut off
            i.e. gate reflectivity must be greater than z_thresh to be considered clutter
    Returns:
    --------------
    date_time: string
                date and time of the file
    clutter_flag_h: array
                    array of shape (azimuth, elevation, range) noting elements where clutter is flagged in the H polarization
                    clutter present: 1
                    no clutter present: 0
    clutter_flag_v: array
                    array of shape (azimuth, elevation, range) noting elements where clutter is flagged in the V polarization
                    clutter present: 1
                    no clutter present: 0

    """
    ###############################
    # NEED TO CORRECT/ADD
    # 1) how to make variable names generic, or specify them elsewhere based on the file type (this should be able to happen in file_to_radar_object ?)
    # reflectivity_h = 'UZh' or 'reflectivity' or 'uncorrected_reflectivity_h'
    # reflectivity_v = 'UZv' or 'uncorrected_reflectivity_v'
    # diff_reflectivity = differential_reflectivity' <---- this only here or used if Zv variable is not readily available

    # 2) specify Z thresh at some point (in config file?)
    ###############################

    theta_list = np.arange(360)
    range_shape = range_limit / 1000
    r_list = np.arange(range_shape) + 1
    clutter_flag_h = np.zeros((len(theta_list), len(r_list)))
    clutter_flag_v = np.zeros((len(theta_list), len(r_list)))

    date_time = variable_dictionary['date_time']
    r = variable_dictionary['range']
    theta = variable_dictionary['azimuth']
    zh = variable_dictionary['reflectivity_h']

    # H POLARIZATION
    for idx_az, az in enumerate(theta_list):  # loop thru each azimuth in list
        az_mask = create_az_mask_ppi(az, theta)  # create mask for desired azimuths
        zh_rays = zh[
            az_mask, :
        ]  # get Zh values for only the desired elevation and azimuth
        for idx_ra, ra in enumerate(
            r_list
        ):  # loop thru each range gate in the range grid boxes (len = 80)
            if ra == range_shape:
                continue  # skip the last value in the range grid
            else:
                zh_ray_list = []
                rstart = np.where(r-(ra*1000.) >= 0.)[0][0]
                try:
                    rstop = np.where(r-(r_list[idx_ra+1]*1000.) >= 0.)[0][0]
                except IndexError:
                    rstop = -1
                for idx_z, z in enumerate(
                    zh_rays[:, rstart : rstop]
                ):  # loop thru each zh value in chunks of 10 100m range gates (1 km chunks)
                    if np.any(z >= z_thresh):
                        zh_ray_list.append(z)
                        clutter_flag_h[
                            idx_az, idx_ra
                        ] = (
                            1
                        )  # flag the grid box as clutter is any zh in the 1 km chunk is greater than the threshold value

    if polarization == "horizontal":
        return date_time, clutter_flag_h

    elif polarization == "dual":
        zv = variable_dictionary['reflectivity_v']

        # V POLARIZATION
        for idx_az, az in enumerate(theta_list):  # loop thru each azimuth in list
            az_mask = create_az_mask_ppi(az, theta)  # create mask for desired azimuths
            zv_rays = zv[
                az_mask, :
            ]  # get Zv values for only the desired elevation and azimuth
            for idx_ra, ra in enumerate(
                r_list
            ):  # loop thru each range gate in the range grid boxes (len = 80)
                if ra == range_shape:
                    continue  # skip the last value in the range grid
                else:
                    zv_ray_list = []
                    rstart = np.where(r-(ra*1000.) >= 0.)[0][0]
                    try:
                        rstop = np.where(r-(r_list[idx_ra+1]*1000.) >= 0.)[0][0]
                    except IndexError:
                        rstop = -1
                    for idx_z, z in enumerate(
                        zv_rays[:, rstart : rstop]
                    ):  # loop thru each zv value in chunks of 10 100m range gates (1 km chunks)
                        if np.any(z >= z_thresh):
                            zv_ray_list.append(z)
                            clutter_flag_v[
                                idx_az, idx_ra
                            ] = (
                                1
                            )  # flag the grid box as clutter is any zh in the 1 km chunk is greater than the threshold value

        return date_time, clutter_flag_h, clutter_flag_v


def create_clutter_flag_hsrhi(variable_dictionary, polarization, range_limit, z_thresh):
    """
    create_clutter_flag_hsrhi creates a clutter flag array for a particular HSRHI radar file (using a precipitation-free day) that will be used for
    clutter map creation. It returns the datetime of the file and the clutter flag arrays for reflectivity in the chosen polarizations (H and V or just H)
    Parameters:
    --------------
    variable_dictionary: dict
                    dictionary with values, strings, and arrays of relevant radar data
                    i.e.
                    'reflectivity_h', 'reflectivity_v', 'azimuth', 'range', 'date_time'
    polarization: string
            specifies for which polarization user wants to create clutter flag array
            'dual': calculate for both H and V
            'horizontal': calculate only for H
    range_limit: integer
            value of desired radar gate range limit
    z_thresh: float
            reflectivity threshold for clutter cut off
            i.e. gate reflectivity must be greater than z_thresh to be considered clutter
    Returns:
    --------------
    date_time: string
                date and time of the file
    clutter_flag_h: array
                    array of shape (azimuth, elevation, range) noting elements where clutter is flagged in the H polarization
                    clutter present: 1
                    no clutter present: 0
    clutter_flag_v: array
                    array of shape (azimuth, elevation, range) noting elements where clutter is flagged in the V polarization
                    clutter present: 1
                    no clutter present: 0

    """
    ###############################
    # NEED TO CORRECT/ADD
    # 1) how to make variable names generic, or specify them elsewhere based on the file type (this should be able to happen in file_to_radar_object ?)
    # reflectivity_h = 'UZh' or 'reflectivity' or 'uncorrected_reflectivity_h'
    # reflectivity_v = 'UZv' or 'uncorrected_reflectivity_v'
    # diff_reflectivity = differential_reflectivity' <---- this only here or used if Zv variable is not readily available

    # 2) specify Z thresh at some point (in config file?)
    ###############################

    elev_list = [1, 2, 3, 4, 5, 175, 176, 177, 178, 179]
    theta_list = [0, 30, 60, 90, 120, 150]
    range_shape = range_limit / 1000
    r_list = np.arange(range_shape) + 1
    clutter_flag_h = np.zeros((len(theta_list), len(elev_list), len(r_list)))
    clutter_flag_v = np.zeros((len(theta_list), len(elev_list), len(r_list)))

    date_time = variable_dictionary['date_time']
    r = variable_dictionary['range']
    theta = variable_dictionary['azimuth']
    elev = variable_dictionary['elevation']
    zh = variable_dictionary['reflectivity_h']

    # H POLARIZATION
    for idx_az, az in enumerate(theta_list):  # loop thru each azimuth in list
        az_mask = create_az_mask_hsrhi(az, theta)  # create mask for desired azimuths
        for idx_el, el in enumerate(
            elev_list
        ):  # loop thru each element in desired elevation grid boxes
            el_mask = np.abs(elev - el) < 0.5  # create mask for desired elevations
            zh_rays = zh[
                np.logical_and(az_mask, el_mask), :
            ]  # get Zh values for only the desired elevation and azimuth
            for idx_ra, ra in enumerate(
                r_list
            ):  # loop thru each range gate in the range grid boxes (len = 80)
                if ra == range_shape:
                    continue  # skip the last value in the range grid
                else:
                    zh_ray_list = []
                    rstart = np.where(r-(ra*1000.) >= 0.)[0][0]
                    try:
                        rstop = np.where(r-(r_list[idx_ra+1]*1000.) >= 0.)[0][0]
                    except IndexError:
                        rstop = -1
                    for idx_z, z in enumerate(
                        zh_rays[:, rstart : rstop]
                    ):  # loop thru each zh value in chunks of 10 100m range gates (1 km chunks)
                        if np.any(z >= z_thresh):
                            zh_ray_list.append(z)
                            clutter_flag_h[
                                idx_az, idx_el, idx_ra
                            ] = (
                                1
                            )  # flag the grid box as clutter is any zh in the 1 km chunk is greater than the threshold value

    if polarization == "horizontal":
        return date_time, clutter_flag_h

    elif polarization == "dual":
        zv = variable_dictionary['reflectivity_v']

        # V POLARIZATION
        for idx_az, az in enumerate(theta_list):  # loop thru each azimuth in list
            az_mask = create_az_mask_hsrhi(
                az, theta
            )  # create mask for desired azimuths
            for idx_el, el in enumerate(
                elev_list
            ):  # loop thru each element in desired elevation grid boxes
                el_mask = np.abs(elev - el) < 0.5  # create mask for desired elevations
                # print(az,el)
                zv_rays = zv[
                    np.logical_and(az_mask, el_mask), :
                ]  # get Zv values for only the desired elevation and azimuth
                for idx_ra, ra in enumerate(
                    r_list
                ):  # loop thru each range gate in the range grid boxes (len = 80)
                    if ra == range_shape:
                        continue  # skip the last value in the range grid
                    else:
                        zv_ray_list = []
                        rstart = np.where(r-(ra*1000.) >= 0.)[0][0]
                        try:
                            rstop = np.where(r-(r_list[idx_ra+1]*1000.) >= 0.)[0][0]
                        except IndexError:
                            rstop = -1
                        for idx_z, z in enumerate(
                            zv_rays[:, rstart : rstop]
                        ):  # loop thru each zv value in chunks of 10 100m range gates (1 km chunks)
                            if np.any(z >= z_thresh):
                                zv_ray_list.append(z)
                                clutter_flag_v[
                                    idx_az, idx_el, idx_ra
                                ] = (
                                    1
                                )  # flag the grid box as clutter is any zh in the 1 km chunk is greater than the threshold value
                                
        return date_time, clutter_flag_h, clutter_flag_v
