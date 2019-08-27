import pytest
import rca
import numpy as np

from rca.modules import plot_rca_timeseries

def test_plot_rca_timeseries_oneradar_read_csv():
    ''' Tests whether plot_rca_timeseries_oneradar correctly reads in provided CSV file
    '''

    csv_file = '/path_to_csv/mock_daily_rca.csv'
    output_dir = ''
    baseline_date = ''
    pol = ''
    scan_type = ''

    plot_rca_timeseries.plot_rca_timeseries_oneradar(csv_file,)
    #ret_value = create_masks.create_az_mask_ppi(input_azi, input_array)
    #assert  type(ret_value) == np.ndarray