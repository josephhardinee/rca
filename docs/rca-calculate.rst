Calculate RCA values
--------------------

.. code-block:: python

   # import commands
   from .daily_rca import daily_rca

   # select date, radar band and scan type and find corresponding configuration file
   # edit radar configuration file appropriately
   radar_config_file = '/__your_path_to__/rca/src/rca/config/__band_scan.json__'
   date = 'YYYYMMDD'
   daily_rca(radar_config_file,date)

   # to calculate daily RCA for multiple days (i.e. one week), loop the daily_rca function
   week = ['01','02','03','04','05','06','07']
   for day in week:
       date = '201910'+day
       daily_rca(radar_config_file,date)


