Create a clutter map
--------------------

Create a daily clutter map
~~~~~~~~~~~~~~~~~~~~~~~~~~
A clutter map is calculated following the steps outlined in the eRCA methodlogy (TODO: link or figure here). It requires a day's worth of radar files of PPI or RHI scan type. 

.. code-block:: python
   
   # import commands
   from .clutter_map import clutter_map

   # select a radar and scan type and corresponding radar_config_file
   radar_config_file = '/__your_path_to__/rca/src/rca/config/__band_scan.json__'
   date = 'YYYYMMDD'
   
   # adjust specifications in radar_config_file as needed
   # netCDF is written for the date and output in specified directory (see radar_config_file)
   clutter_map(radar_config_file,date)

   # repeat daily clutter map procedure for as many dates as desried
   date_list = [20191029, 20191030, 20191031]
   for date in date_list:
       clutter_map(radar_config_file,date)

Create a composite clutter map
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

It is recommended with the eRCA technique to generate a composite clutter map to calculate RCA values. A composite clutter map utilizes multiple single-day clutter maps to to select the *most* stable clutter points identified for a particular radar at a given location.

.. code-block:: python

   # import commands
   from .composite_clutter_map import composite_clutter_map
   
   # use all available daily clutter maps to generate a composite clutter map
   # edit the clutter_map.json config file to specify radar, scan type, and input
   # and output directory
   clutter_map_config_file = '__your_path_to__/rca/src/rca/config/clutter_maps.json'
   composite_clutter_map(clutter_map_config_file)
