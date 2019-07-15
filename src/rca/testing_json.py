#!/usr/bin/env python

# Testing a JSON file
import json

radar_config_file = './kaband_ppi.json'
defaults = json.load(open(radar_config_file))

z_thresh = defaults["z_threshold"]
print(z_thresh)