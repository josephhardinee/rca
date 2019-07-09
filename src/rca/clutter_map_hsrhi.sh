#!/bin/bash
#PBS -A arm
#PBS -N kasacrcor_0306
#PBS -q arm_high_mem
#PBS -l nodes=16:ppn=16
#PBS -l qos=std
#PBS -l walltime=00:30:00
#PBS -W group_list=cades-arm
#PBS -j oe
#PBS -m abe
#PBS -M alexis.hunzinger@pnnl.gov
#PBS -o o.log
#PBS -e e.log
#PBS -S /bin/bash

python /home/alexishunzinger/projects/taranis/taranis/calibration/clutter_map_hsrhi.py /home/alexishunzinger/data/proj-shared/data_transfer/cor/corkasacrcfrhsrhiM1.a1/ cor kasacr 20190306 /home/alexishunzinger/projects/taranis/taranis/calibration/figures/clutter_maps/
