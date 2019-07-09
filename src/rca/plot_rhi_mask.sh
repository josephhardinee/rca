#!/bin/bash
#PBS -A arm
#PBS -N mrhi
#PBS -q arm_high_mem
#PBS -l nodes=8:ppn=16
#PBS -l qos=std
#PBS -l walltime=01:00:00
#PBS -W group_list=cades-arm
#PBS -j oe
#PBS -m abe
#PBS -o o.log
#PBS -e e.log
#PBS -S /bin/bash

python /home/alexishunzinger/projects/taranis/taranis/calibration/plot_rhi_mask.py
