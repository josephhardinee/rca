import numpy as np

# get_closest_time function

def get_closest_time(time_array, target_time):
    closest_time = np.argmin((abs(time_array - target_time)))
    return closest_time