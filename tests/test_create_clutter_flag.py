import pytest
import rca
import numpy as np

from rca.modules import create_clutter_flag

def test_create_clutter_flag_ppi_returns_array():
    ''' Tests whether create_clutter_flag_ppi returns an np array object
    '''

    #input_array = np.arange(118,122)
    #input_azi = 120

    #ret_value = create_masks.create_az_mask_ppi(input_azi, input_array)
    #assert  type(ret_value) == np.ndarray