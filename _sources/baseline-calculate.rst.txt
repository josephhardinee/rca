Calculate a baseline
---------------------

A baseline value represents the 95th percentile of clutter area reflectivity for a selected "baseline day". A wisely-chosen baseline day is a day with no precipitation or anomolous propagation. This day and calculated value will be used to compare with all other days' values to ultimately calculate the relative calibration adjustment (RCA) value.

To calculate a baseline value, a day's worth of radar files and a previously-generated clutter map are required. The baseline function returns the 95th percentile clutter area reflectivity and writes out a netCDF file containing the value. 

.. code-block:: python

   # import commands
   from .baseline import baseline
   
   # select baseline date and edit your desired radar_config_file
   radar_config_file = '/__your_path_to/rca/src/rca/config/__band_scan.json__'

   # baseline function will write a netCDF containing the 95th percentile reflectivity and will also return that value
   dbz95_h = baseline(radar_config_file)
   print('Baseline 95th percentile clutter area reflectivity = ',dbz95_h,' dBZ')

