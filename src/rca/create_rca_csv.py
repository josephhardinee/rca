#!/usr/bin/env python
import numpy as np
import os
import glob
import json
import csv


def create_rca_csv(radar_config_file):
    """
    create_rca_csv creates a CSV file specifically for keeping track of daily
RCA values generated by daily_rca.py 
    Parameters:
    --------------
    radar_config_file: str
                path to JSON file containing specifications:
                    data directory
                    file extension
                    clutter map directory
                    output directory for baseline netCDF
                    baseline date
                    scan type
                    polarization
                    site
                    instrument
                    range limit
                    
    Returns:
    --------------
    (no specific return)
    however, a CSV file is written out
    """

    config_vars = json.load(open(radar_config_file))
    daily_csv_dir = config_vars["daily_csv_dir"]
    scantype = config_vars["scan_type"]
    polarization = config_vars["polarization"]
    site = config_vars["site_abbrev"]
    inst = config_vars["instrument_abbrev"]

    header = ["DATE", "RCA_H", "RCA_V", "BASELINE"]
    daily_csv = daily_csv_dir + "daily_rca_" + scantype + "_" + site + inst + ".csv"
    with open(daily_csv, "w", newline="") as f:
        writer = csv.writer(f, delimiter=",")
        writer.writerow(header)  # write the header
