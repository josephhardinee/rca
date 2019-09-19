import pytest
import rca
import numpy as np
from netCDF4 import Dataset

from rca.modules import calculate_dbz95
from rca.modules import create_masks

#@pytest.mark.parametrize("testdict", testdata)
#def test_timedistance_v0(a, b, expected):
#def test_create_clutter_flag_ppi_returns_array():
#    ''' Tests whether create_clutter_flag_ppi returns a string and 2 np array objects
#    '''
#    testdata = np.load('/Users/hunz743/projects/github/rca/testdata/sample_var_arrays_ppi.npy').item()
#    sample_clutter_map = '/Users/hunz743/projects/github/rca/testdata/sample_cluttermap_ppi.nc'
#    d = Dataset(sample_clutter_map)
#    sample_clutter_mask_h = d.variables['clutter_map_mask_zh'][:,:]
    #sample_clutter_mask_v = d.variables['clutter_map_mask_zv'][:,:]
#    polarization = 'horiztonal'
#    range_limit = 5000
#
#    print(sample_clutter_mask_h.shape)
#    print(testdata['reflectivity_h'].shape)

#    ret_value = calculate_dbz95.calculate_dbz95_ppi(testdata,polarization,range_limit,sample_clutter_mask_h,clutter_mask_v=None)
    #print(ret_value)
#    print(ret_value[1].shape)
#    print(type(ret_value[2]))

#    assert type(ret_value[0]) == str
#    assert type(ret_value[1]) == np.ndarray
#    assert type(ret_value[2]) == np.ndarray
