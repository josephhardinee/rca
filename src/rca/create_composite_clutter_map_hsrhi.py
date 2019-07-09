#!/usr/bin/env python
import sys
import os
import glob
import numpy as np
from netCDF4 import Dataset
from pct_on_clutter_map_hsrhi import pct_on_clutter_map_hsrhi

if __name__ == "__main__":
    if len(sys.argv) < 5:
        print(
            "ERROR: Arguments: Clutter map file directory, output directory for composite file, site, instrument"
        )
        sys.exit(0)

    cluttermapdir = sys.argv[1]
    outputdir = sys.argv[2]
    site = sys.argv[3]
    inst = sys.argv[4]

    clutter_mask_h = []
    clutter_mask_v = []
    clutter_pct_h = []
    clutter_pct_v = []

    if inst == 'kasacr':      # KaSACR is H polarization only
        for f in glob.glob(os.path.join(cluttermapdir, 'cluttermap_hsrhi_'+site+inst+'_*.nc')):
            print(f)
            ClutterMaskH, ClutterPCTH  = pct_on_clutter_map_hsrhi(f, clutter_v=None)
            # Append output from each HSRHI file to lists
            clutter_mask_h.append(ClutterMaskH)
            clutter_pct_h.append(ClutterPCTH)

        array_h = np.zeros((len(clutter_mask_h),len(clutter_mask_h[0][:,:,0]),len(clutter_mask_h[0][0,:,0]),len(clutter_mask_h[0][0,0,:])))

        for i in range(0,len(clutter_mask_h)):
            array_h[i,:,:,:] = clutter_mask_h[i]
    
        # Calculate percentage of "clutter ON" for each grid box in clutter map grid
        pct_h = np.sum(array_h,axis=0)/len(array_h[:,0,0,0])
        clutter_map_h_mask = pct_h > 0.8
        print(pct_h.shape, clutter_map_h_mask.shape)
        dataset = Dataset(outputdir+'cluttermap_hsrhi_'+site+inst+'_composite.nc',
                            'w',format='NETCDF4_CLASSIC')
        azi = dataset.createDimension('azi', 6)
        rang = dataset.createDimension('rang', 20)
        el = dataset.createDimension('el', 10)
        HPCT_ON = dataset.createVariable('clutter_gate_pcts_zh', np.float64, ('azi','el','rang'))
        HMASK = dataset.createVariable('clutter_map_mask_zh', 'i1', ('azi','el','rang'))
        HPCT_ON.long_name = 'Clutter grid gate percentages (Zh)'
        HMASK.long_name = 'Clutter map mask (Zh)'
        HPCT_ON[:,:,:] = pct_h
        HMASK[:,:,:] = clutter_map_h_mask
        dataset.close()

    elif inst == 'xsacr':
        for f in glob.glob(os.path.join(cluttermapdir, 'cluttermap_hsrhi_'+site+inst+'_*.nc')):
            print(f)
            ClutterMaskH, ClutterMaskV, ClutterPCTH, ClutterPCTV = pct_on_clutter_map_hsrhi(f, clutter_v=True)
            # Append output from each HSRHI file to lists
            print(ClutterMaskH.shape)
            clutter_mask_h.append(ClutterMaskH)
            clutter_mask_v.append(ClutterMaskV)
            clutter_pct_h.append(ClutterPCTH)
            clutter_pct_v.append(ClutterPCTV)

        array_h = np.zeros((len(clutter_mask_h),len(clutter_mask_h[0][:,:,0]),len(clutter_mask_h[0][0,:,0]),len(clutter_mask_h[0][0,0,:])))
        array_v = np.zeros((len(clutter_mask_v),len(clutter_mask_v[0][:,:,0]),len(clutter_mask_v[0][0,:,0]),len(clutter_mask_v[0][0,0,:])))

        for i in range(0,len(clutter_mask_h)):
            array_h[i,:,:,:] = clutter_mask_h[i]
            array_v[i,:,:,:] = clutter_mask_v[i]
    
        pct_h = np.sum(array_h,axis=0)/len(array_h[:,0,0,0])
        pct_v = np.sum(array_v,axis=0)/len(array_v[:,0,0,0])
        clutter_map_h_mask = pct_h > 0.8
        clutter_map_v_mask = pct_v > 0.8

        dataset = Dataset(outputdir+'cluttermap_hsrhi_'+site+inst+'_composite.nc',
                            'w',format='NETCDF4_CLASSIC')
        azi = dataset.createDimension('azi', 6)
        rang = dataset.createDimension('rang', 20)
        el = dataset.createDimension('el', 10)
        HPCT_ON = dataset.createVariable('clutter_gate_pcts_zh', np.float64, ('azi','el','rang'))
        VPCT_ON = dataset.createVariable('clutter_gate_pcts_zv', np.float64, ('azi','el','rang'))
        HMASK = dataset.createVariable('clutter_map_mask_zh', 'i1', ('azi','el','rang'))
        VMASK = dataset.createVariable('clutter_map_mask_zv', 'i1', ('azi','el','rang'))
        HPCT_ON.long_name = 'Clutter grid gate percentages (Zh)'
        VPCT_ON.long_name = 'Clutter grid gate percentages (Zv)'
        HMASK.long_name = 'Clutter map mask (Zh)'
        VMASK.long_name = 'Clutter map mask (Zv)'
        HPCT_ON[:,:,:] = pct_h
        VPCT_ON[:,:,:] = pct_v
        HMASK[:,:,:] = clutter_map_h_mask
        VMASK[:,:,:] = clutter_map_v_mask
        dataset.close()

    else:
        for f in glob.glob(os.path.join(cluttermapdir, 'cluttermap_hsrhi_'+site+inst+'_*.nc')):
            print(f)
            ClutterMaskH, ClutterMaskV, ClutterPCTH, ClutterPCTV = pct_on_clutter_map_hsrhi(f, clutter_v=True)
            # Append output from each HSRHI file to lists
            print(ClutterMaskH.shape)
            clutter_mask_h.append(ClutterMaskH)
            clutter_mask_v.append(ClutterMaskV)
            clutter_pct_h.append(ClutterPCTH)
            clutter_pct_v.append(ClutterPCTV)

        array_h = np.zeros((len(clutter_mask_h),len(clutter_mask_h[0][:,:,0]),len(clutter_mask_h[0][0,:,0]),len(clutter_mask_h[0][0,0,:])))
        array_v = np.zeros((len(clutter_mask_v),len(clutter_mask_v[0][:,:,0]),len(clutter_mask_v[0][0,:,0]),len(clutter_mask_v[0][0,0,:])))

        for i in range(0,len(clutter_mask_h)):
            array_h[i,:,:,:] = clutter_mask_h[i]
            array_v[i,:,:,:] = clutter_mask_v[i]
    
        pct_h = np.sum(array_h,axis=0)/len(array_h[:,0,0,0])
        pct_v = np.sum(array_v,axis=0)/len(array_v[:,0,0,0])
        clutter_map_h_mask = pct_h > 0.8
        clutter_map_v_mask = pct_v > 0.8

        dataset = Dataset(outputdir+'cluttermap_hsrhi_'+site+inst+'_composite.nc',
                            'w',format='NETCDF4_CLASSIC')
        azi = dataset.createDimension('azi', 6)
        rang = dataset.createDimension('rang', 40)
        el = dataset.createDimension('el', 10)
        HPCT_ON = dataset.createVariable('clutter_gate_pcts_zh', np.float64, ('azi','el','rang'))
        VPCT_ON = dataset.createVariable('clutter_gate_pcts_zv', np.float64, ('azi','el','rang'))
        HMASK = dataset.createVariable('clutter_map_mask_zh', 'i1', ('azi','el','rang'))
        VMASK = dataset.createVariable('clutter_map_mask_zv', 'i1', ('azi','el','rang'))
        HPCT_ON.long_name = 'Clutter grid gate percentages (Zh)'
        VPCT_ON.long_name = 'Clutter grid gate percentages (Zv)'
        HMASK.long_name = 'Clutter map mask (Zh)'
        VMASK.long_name = 'Clutter map mask (Zv)'
        HPCT_ON[:,:,:] = pct_h
        VPCT_ON[:,:,:] = pct_v
        HMASK[:,:,:] = clutter_map_h_mask
        VMASK[:,:,:] = clutter_map_v_mask
        dataset.close()
