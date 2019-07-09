#!/bin/bash
#PBS -A arm
#PBS -N cmap_xsacr
#PBS -q arm_high_mem
#PBS -l nodes=16:ppn=16
#PBS -l qos=std
#PBS -l walltime=00:05:00
#PBS -W group_list=cades-arm
#PBS -j oe
#PBS -m abe
#PBS -M alexis.hunzinger@pnnl.gov
#PBS -o o.log
#PBS -e e.log
#PBS -S /bin/bash

python /home/alexishunzinger/projects/taranis/taranis/calibration/create_composite_clutter_map_hsrhi.py /home/alexishunzinger/projects/taranis/taranis/calibration/figures/clutter_maps/ /home/alexishunzinger/projects/taranis/taranis/calibration/ cor xsacr


