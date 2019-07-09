import numpy as np

def get_nearest_idx(target, angle_array):
    """ Find index of nearest target in angle_array
    Parameters
    ----------
    target: float
        target value to match
    angle_array: np.ndarray
        array of values to search in
    """
    return np.argmin(np.abs(angle_array-target))