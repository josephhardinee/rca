Create a clutter map
--------------------

.. jupyter-execute::

  import numpy as np
  import json
  import rca

  from rca.src.rca.clutter_map import clutter_map
  from rca.src.rca.aux.create_clutter_flag import create_clutter_flag_ppi, create_clutter_flag_rhi
  from rca.src.rca.aux.file_to_radar_object import file_to_radar_object

  print('this is a test')
