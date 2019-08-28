import pyart
import numpy as np
import json


def get_var_arrays_from_radar_object(radar, radar_config_file):
    """ Input radar object and radar configuration (.json) file 
    to use PyART to extract variables to be used in calculations
    Returns variables in arrays or strings in a single dictionary
    """
    config_vars = json.load(open(radar_config_file))
    scantype = config_vars["scan_type"]
    polarization = config_vars["polarization"]
    range_limit = config_vars["range_limit"]

    if scantype == 'ppi':
        date_time = radar.time["units"].replace("seconds since ", "")
        r_start_idx = 0
        r_stop_idx = np.where(radar.range["data"] > range_limit)[0][0]
        # Using lowest elevation angle of PPI (0.5 deg)
        sweep_start_idx = radar.sweep_start_ray_index["data"][0]
        sweep_stop_idx = radar.sweep_end_ray_index["data"][0] + 1
        # Get variables (only the rays/gates needed)
        r = radar.range["data"][r_start_idx:r_stop_idx]
        theta = radar.azimuth["data"][sweep_start_idx:sweep_stop_idx]
        zh = radar.fields["reflectivity"]["data"][
            sweep_start_idx:sweep_stop_idx, r_start_idx:r_stop_idx
        ]

        if polarization == "horizontal":
            del radar
            var_dict = {
                    "date_time": date_time,
                    "range": r,
                    "azimuth": theta,
                    "reflectivity_h": zh
                    }
            return var_dict

        elif polarization == "dual":
            zv = radar.fields["reflectivity_v"]["data"][sweep_start_idx:sweep_stop_idx, r_start_idx:r_stop_idx]
            zdr = radar.fields["differential_reflectivity"]["data"][sweep_start_idx:sweep_stop_idx, r_start_idx:r_stop_idx]
            zv = 10 * np.log10((10 ** (zh / 10)) / (zdr))
            del radar
            var_dict = {
                    "date_time": date_time,
                    "range": r,
                    "azimuth": theta,
                    "reflectivity_h": zh,
                    "reflectivity_v": zv
                    }
            return var_dict

    if scantype == 'rhi':
        date_time = radar.time["units"].replace("seconds since ", "")
        r_start_idx = 0
        r_stop_idx = np.where(radar.range["data"] > range_limit)[0][0]
        r = radar.range["data"][r_start_idx:r_stop_idx]
        theta = radar.azimuth["data"]
        elev = radar.elevation["data"]
        zh = radar.fields["reflectivity"]["data"][:, r_start_idx:r_stop_idx]

        if polarization == "horizontal":
            del radar
            var_dict = {
                    "date_time": date_time,
                    "range": r,
                    "azimuth": theta,
                    "elevation": elev,
                    "reflectivity_h": zh
                    }
            return var_dict

        elif polarization == "dual":
            zv = radar.fields["reflectivity_v"]["data"][sweep_start_idx:sweep_stop_idx, r_start_idx:r_stop_idx]
            zdr = radar.fields["differential_reflectivity"]["data"][sweep_start_idx:sweep_stop_idx, r_start_idx:r_stop_idx]
            zv = 10 * np.log10((10 ** (zh / 10)) / (zdr))
            del radar
            var_dict = {
                    "date_time": date_time,
                    "range": r,
                    "azimuth": theta,
                    "elevation": elev,
                    "reflectivity_h": zh,
                    "reflectivity_v": zv
                    }
            return var_dict

