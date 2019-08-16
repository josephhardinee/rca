#!/usr/bin/env python3
import sys
sys.path.append('/home/alexishunzinger/projects/github/rca/src/rca/modules/')
from composite_clutter_map import composite_clutter_map

file = '/home/alexishunzinger/projects/github/rca/src/rca/clutter_maps.json'
composite_clutter_map(file)

