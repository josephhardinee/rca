#!/bin/bash
#PBS -A arm
#PBS -N cmap_xsaprI5
#PBS -q arm_high_mem
#PBS -l nodes=8:ppn=16
#PBS -l qos=std
#PBS -l walltime=00:05:00
#PBS -W group_list=cades-arm
#PBS -j oe
#PBS -m abe
#PBS -o o.log
#PBS -e e.log
#PBS -S /bin/bash

python /home/alexishunzinger/projects/taranis/taranis/calibration/create_composite_clutter_map_ppi.py /home/alexishunzinger/projects/taranis/taranis/calibration/ /home/alexishunzinger/projects/taranis/taranis/calibration/ sgp xsaprI5
