#!/bin/bash
#PBS -A arm
#PBS -N compare_nov
#PBS -l nodes=16:ppn=16
#PBS -l walltime=00:20:00
#PBS -l qos=std
#PBS -W group_list=cades-arm
#PBS -q arm_high_mem
#PBS -j oe
#PBS -m abe
#PBS -M alexis.hunzinger@pnnl.gov
#PBS -o o.log
#PBS -e e.log
#PBS -S /bin/bash

python /Users/hunz743/projects/taranis/taranis/calibration/plot_zdiff.py  /Users/hunz743/projects/taranis/taranis/calibration/cross_compare/ /Users/hunz743/projects/taranis/taranis/calibration/figures/ xsacr kasacr 20181112
