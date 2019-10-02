# import pytest
# import rca
# import numpy as np

# from rca.modules import create_clutter_flag
# from rca.modules import create_masks

# testdata = np.load('/Users/hunz743/projects/github/rca/testdata/sample_var_arrays_ppi.npy').item()
# polarization = 'dual'
# range_limit = 5000
# z_thresh = 40.

# @pytest.mark.parametrize("testdict", testdata)
# def test_timedistance_v0(a, b, expected):
# def test_create_clutter_flag_ppi_returns_array():
#    ''' Tests whether create_clutter_flag_ppi returns a string and 2 np array objects
#    '''
#    testdata = np.load('/Users/hunz743/projects/github/rca/testdata/sample_var_arrays_ppi.npy').item()
#    polarization = 'dual'
#    range_limit = 5000
#    z_thresh = 40.
#    ret_value = create_clutter_flag.create_clutter_flag_ppi(testdata,polarization,range_limit,z_thresh)
#    #print(ret_value)
#    assert type(ret_value[0]) == str
#    assert type(ret_value[1]) == np.ndarray
#    assert type(ret_value[2]) == np.ndarray

# def test_create_clutter_flag_ppi_returns_binary():
#    ''' Tests whether create_clutter_flag_ppi returns only 0 or 1 in arrays
#    '''
#    testdata = np.load('/Users/hunz743/projects/github/rca/testdata/sample_var_arrays_ppi.npy').item()
#    polarization = 'dual'
#    range_limit = 5000
#    z_thresh = 40.
#    ret_value = create_clutter_flag.create_clutter_flag_ppi(testdata,polarization,range_limit,z_thresh)
#    #print(ret_value)
#    assert ret_value[1][0,0] == 0. or ret_value[1][0,0] == 1., 'Improper gate flagging'
#    assert ret_value[2][0,0] == 0. or ret_value[2][0,0] == 1., 'Improper gate flagging'


# def test_create_clutter_flag_rhi_returns_array():
#    ''' Tests whether create_clutter_flag_hsrhi returns a string and 2 np array objects
#    '''
#    testdata = np.load('/Users/hunz743/projects/github/rca/testdata/sample_var_arrays_rhi.npy').item()
#    polarization = 'horizontal'
#    range_limit = 5000
#    z_thresh = 40.
#    ret_value = create_clutter_flag.create_clutter_flag_hsrhi(testdata,polarization,range_limit,z_thresh)
#    #print(ret_value)
#    assert type(ret_value[0]) == str
#    assert type(ret_value[1]) == np.ndarray

# def test_create_clutter_flag_rhi_returns_binary():
#    ''' Tests whether create_clutter_flag_hsrhi returns only 0 or 1 in arrays
#    '''
#    testdata = np.load('/Users/hunz743/projects/github/rca/testdata/sample_var_arrays_rhi.npy').item()
#    polarization = 'horizontal'
#    range_limit = 5000
#    z_thresh = 40.
#    ret_value = create_clutter_flag.create_clutter_flag_hsrhi(testdata,polarization,range_limit,z_thresh)
#    print(ret_value[1].shape)
#    assert ret_value[1][0,0,0] == 0. or ret_value[1][0,0,0] == 1., 'Improper gate flagging'
