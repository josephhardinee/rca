import glob
import numpy as np
import pandas as pd
import datetime
from aux.get_closest_time import get_closest_time

# Relative humidity filter function 
# See plot_hourly routine

# def function(one file)
# find the nearest RH time
# within a certain number of minutes
# determine if RH > 90%
# return 1 or 0, pass filter or not

def rh_filter(
    date,
    variable_dictionary,
    met_dataframe,
    rh_thresh
):
    """
    rh_filter uses a previously generated clutter map to 1) identify clutter gates;
    2) blank out identified clutter gates; 3) calculate integrated attentuation along each ray;
    4) threshold for integrated attentuation; 5) return a 1 or 0 for passing or not passing IAH filter
    
    Parameters
    ----------
    date: str
        YYYYMMDD
    variable_dictionary: dict
        dictionary with values, strings, and arrays of relevant radar data
        i.e. 'reflectivity_h', 'reflectivity_v', 'azimuth', 'range', 'date_time'
    met_path: str
        path to met station files
    rh_thresh: int
        threshold of relative humidity (%) for passing the RH filter
    
    Returns
    -------
    pass_filter: int
        0 or 1 (0=no, 1=yes)

    """

    date_time = variable_dictionary["date_time"]
    date_time = date_time[0:19] #change this to be yyyy-mm-dd hh-mm-ss
    #print(date_time)
    rca_time = datetime.datetime.strptime(date_time, '%Y-%m-%d %H:%M:%S') 
    #rca_time = date_time
    #print(rca_time)
    met_time = met_dataframe['time_offset']

    # Match RCA times to cormet times
    match = get_closest_time(met_time,rca_time)
    rh_match = met_dataframe['rh_mean'][match]

    if rh_match > rh_thresh:
        pass_filter = 0
    else:
        pass_filter = 1
    
    return date_time, rh_match, pass_filter 

    
