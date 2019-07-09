#!/usr/bin/env python
import sys
import numpy as np
import matplotlib.pyplot as plt
from netCDF4 import Dataset 
from matplotlib.colors import BoundaryNorm
from matplotlib.colors import LinearSegmentedColormap
import copy

if __name__ == "__main__":
    if len(sys.argv) < 7:
        print(
            "ERROR: Arguments: Clutter map file directory, date, site, inst, location, output directory for plots"
        )
        sys.exit(0)

    cluttermapdir = sys.argv[1]
    date = sys.argv[2]
    site = sys.argv[3]
    inst = sys.argv[4]
    location = sys.argv[5]
    outputdir = sys.argv[6]

    plt.style.use('publication_radar')
    params = {'mathtext.default': 'regular' }          
    plt.rcParams.update(params)

    # KaSACR is only H polarization
    if inst == 'kasacr':
        # Import clutter map information
        d = Dataset(cluttermapdir+'cluttermap_hsrhi_'+site+inst+'_'+date+'.nc')
        clutter_map_mask_h = d.variables['clutter_map_mask_zh'][:,:,:]
        clutter_map_pcts_h = d.variables['clutter_gate_pcts_zh'][:,:,:]
        d.close()

        elev_e = np.arange(5)+1
        elev_w = np.arange(5)+1
        rang_e = np.arange(20)
        rang_w = np.arange(20)

        r_e, el_e = np.meshgrid(rang_e,elev_e)
        r_w, el_w = np.meshgrid(rang_w,elev_w)

        x_e = (r_e*np.sin(el_e*np.pi/180.))
        y_e = (r_e*np.cos(el_e*np.pi/180.))
        x_w = (r_w*np.sin(el_w*np.pi/180.))
        y_w = (r_w*np.cos(el_w*np.pi/180.))

        if date == 'composite':
            levels = [0,0.1,0.8,1]
            cmap_name = 'my_clutter'
            colors = ['w','lightgrey','k'] # Specify desired colors
            n_bins = 3                     # Discretizes the interpolation into bins
            cmap = LinearSegmentedColormap.from_list(cmap_name, colors, N=n_bins)
            norm = BoundaryNorm(levels, ncolors=cmap.N, clip=True) 
            cbar_label = 'Clutter point percentage occurrence'
            title = location[:3]+' '+location[3:]+' \n Composite'

        else:
            levels = [0,0.1,0.5,0.6,0.7,0.8,0.9,1]
            cmap_name = 'my_clutter'
            #colors = ['w','lightgrey','forestgreen','aquamarine','lightskyblue','mediumblue','indigo'] # Specify desired colors
            colors = ['w','lightgrey','#73D055FF','#20A387FF','#287D8EFF','#404788FF','#440154FF'] # Viridis color codes
            n_bins = 7 #[3, 6, 10, 100]  # Discretizes the interpolation into bins
            cmap = LinearSegmentedColormap.from_list(cmap_name, colors, N=n_bins)
            norm = BoundaryNorm(levels, ncolors=cmap.N, clip=True) 
            cbar_label = 'Clutter flag percentage occurrence (PCT_ON)'
            title = location[:3]+' '+location[3:]+' \n '+date[:4]+'-'+date[4:6]+'-'+date[6:]

        # H polarization
        # 1 column, 3 row plot
        fig, axes = plt.subplots(nrows=3,ncols=1,sharex=True,
                                 figsize=[12,8],constrained_layout=True)
        az_list = ['240','270','300']


        # Column 0
        for az_idx, az in enumerate(az_list):
            pts_h = clutter_map_pcts_h[az_idx+2,5:10,:]
            pts_h = pts_h[::-1,:]
            im = axes[az_idx].pcolormesh(y_w,x_w,pts_h,cmap=cmap,norm=norm)
            axes[az_idx].set_xlim([0,20])
            axes[az_idx].set_ylim([0,1])
            if az_idx == 0:
                axes[az_idx].set_title('Clutter map ($Z_H$) at '+title+' \n '+az+' deg.')
            elif az_idx == 2:
                axes[az_idx].set_xlabel('Dist. from radar (km)')
                axes[az_idx].set_title(az+' deg.')
            elif az_idx == 1:
                axes[az_idx].set_ylabel('Height (km)')
                axes[az_idx].set_title(az+' deg.')
            else:
                axes[az_idx].set_title(az+' deg.')
    
        fig.subplots_adjust(right=0.8)
        cbar_ax = fig.add_axes([0.85, 0.15, 0.02, 0.7])
        cbar = fig.colorbar(im, cax=cbar_ax)
        cbar.ax.set_ylabel(cbar_label)
        plt.savefig(outputdir+'cluttermap_hsrhi_h_'+site+inst+'_'+date+'.png')
        ######################################################################################### 

        # EAST and WEST 2 column, 6 row plot
        fig, axes = plt.subplots(nrows=6,ncols=2,sharex=True,
                                 figsize=[16,12],constrained_layout=True)
        az_list_w = ['180','210','240','270','300','330']
        az_list_e = ['0','30','60','90','120','150']

        # WEST column 0
        for az_idx, az in enumerate(az_list_w):
            west = clutter_map_pcts_h[az_idx,5:10,:]
            west = west[::-1,:]
            im = axes[az_idx,0].pcolormesh(y_w,x_w,west,cmap=cmap,norm=norm)
            axes[az_idx,0].set_xlim([0,20])
            axes[az_idx,0].set_ylim([0,2])
            if az_idx == 0:
                axes[az_idx,0].set_title('Clutter map ($Z_H$) at '+title+' \n '+az+' deg.')
            elif az_idx == 5:
                axes[az_idx,0].set_xlabel('Dist. from radar (km)')
                axes[az_idx,0].set_title(az+' deg.')
            elif az_idx == 3:
                axes[az_idx,0].set_ylabel('Height (km)')
                axes[az_idx,0].set_title(az+' deg.')
            else:
                axes[az_idx,0].set_title(az+' deg.')
   
        # EAST column 1
        for az_idx, az in enumerate(az_list_e):
            east = clutter_map_pcts_h[az_idx,0:5,:]
            im = axes[az_idx,1].pcolormesh(y_e,x_e,east,cmap=cmap,norm=norm)
            axes[az_idx,1].set_xlim([0,20])
            axes[az_idx,1].set_ylim([0,2])
            if az_idx == 0:
                axes[az_idx,1].set_title('Clutter map ($Z_H$) at '+title+' \n '+az+' deg.')
            elif az_idx == 5:
                axes[az_idx,1].set_xlabel('Dist. from radar (km)')
                axes[az_idx,1].set_title(az+' deg.')
            elif az_idx == 3:
                axes[az_idx,1].set_ylabel('Height (km)')
                axes[az_idx,1].set_title(az+' deg.')
            else:
                axes[az_idx,1].set_title(az+' deg.')
    
        fig.subplots_adjust(right=0.8)
        cbar_ax = fig.add_axes([0.85, 0.15, 0.02, 0.7])
        cbar = fig.colorbar(im, cax=cbar_ax)
        cbar.ax.set_ylabel(cbar_label)
        plt.savefig(outputdir+'cluttermap_hsrhi_h_'+site+inst+'_'+date+'_2col.png')

    elif inst == 'xsacr':
        d = Dataset(cluttermapdir+'cluttermap_hsrhi_'+site+inst+'_'+date+'.nc')
        clutter_map_mask_h = d.variables['clutter_map_mask_zh'][:,:,:]
        clutter_map_mask_v = d.variables['clutter_map_mask_zv'][:,:,:]
        clutter_map_pcts_h = d.variables['clutter_gate_pcts_zh'][:,:,:]
        clutter_map_pcts_v = d.variables['clutter_gate_pcts_zv'][:,:,:]
        d.close()

        elev_e = np.arange(5)+1
        elev_w = np.arange(5)+1
        rang_e = np.arange(20)
        rang_w = np.arange(20)

        r_e, el_e = np.meshgrid(rang_e,elev_e)
        r_w, el_w = np.meshgrid(rang_w,elev_w)

        x_e = (r_e*np.sin(el_e*np.pi/180.))
        y_e = (r_e*np.cos(el_e*np.pi/180.))
        x_w = (r_w*np.sin(el_w*np.pi/180.))
        y_w = (r_w*np.cos(el_w*np.pi/180.))

        if date == 'composite':
            levels = [0,0.1,0.8,1]
            cmap_name = 'my_clutter'
            colors = ['w','lightgrey','k'] # Specify desired colors
            n_bins = 3                     # Discretizes the interpolation into bins
            cmap = LinearSegmentedColormap.from_list(cmap_name, colors, N=n_bins)
            norm = BoundaryNorm(levels, ncolors=cmap.N, clip=True) 
            cbar_label = 'Clutter point percentage occurrence'
            title = location[:3]+' '+location[3:]+' \n Composite'

        else:
            levels = [0,0.1,0.5,0.6,0.7,0.8,0.9,1]
            cmap_name = 'my_clutter'
            #colors = ['w','lightgrey','forestgreen','aquamarine','lightskyblue','mediumblue','indigo'] # Specify desired colors
            colors = ['w','lightgrey','#73D055FF','#20A387FF','#287D8EFF','#404788FF','#440154FF'] # Viridis color codes
            n_bins = 7 #[3, 6, 10, 100]  # Discretizes the interpolation into bins
            cmap = LinearSegmentedColormap.from_list(cmap_name, colors, N=n_bins)
            norm = BoundaryNorm(levels, ncolors=cmap.N, clip=True)  
            cbar_label = 'Clutter flag percentage occurrence (PCT_ON)'
            title = location[:3]+' '+location[3:]+' \n '+date[:4]+'-'+date[4:6]+'-'+date[6:]

        # H polarization
        # 1 column, 6 row plot
        fig, axes = plt.subplots(nrows=6,ncols=1,sharex=True,
                                 figsize=[12,12],constrained_layout=True)
        az_list = ['0','180','210','240','270','300']

        # Column 0
        for az_idx, az in enumerate(az_list):
            if az_idx == 0:
                pts_h = clutter_map_pcts_h[az_idx,0:5,:]
            else:
                pts_h = clutter_map_pcts_h[az_idx-1,5:10,:]
                pts_h = pts_h[::-1,:]
            im = axes[az_idx].pcolormesh(y_w,x_w,pts_h,cmap=cmap,norm=norm)
            axes[az_idx].set_xlim([0,20])
            axes[az_idx].set_ylim([0,1])
            if az_idx == 0:
                axes[az_idx].set_title('Clutter map ($Z_H$) at '+title+' \n '+az+' deg.')
            elif az_idx == 5:
                axes[az_idx].set_xlabel('Dist. from radar (km)')
                axes[az_idx].set_title(az+' deg.')
            elif az_idx == 3:
                axes[az_idx].set_ylabel('Height (km)')
                axes[az_idx].set_title(az+' deg.')
            else:
                axes[az_idx].set_title(az+' deg.')
    
        fig.subplots_adjust(right=0.8)
        cbar_ax = fig.add_axes([0.85, 0.15, 0.02, 0.7])
        cbar = fig.colorbar(im, cax=cbar_ax)
        cbar.ax.set_ylabel(cbar_label)
        plt.savefig(outputdir+'cluttermap_hsrhi_h_'+site+inst+'_'+date+'.png')

        # V polarization
        # 1 column, 6 row plot
        fig, axes = plt.subplots(nrows=6,ncols=1,sharex=True,
                                 figsize=[12,12],constrained_layout=True)
        az_list = ['0','180','210','240','270','300']

        # Column 0
        for az_idx, az in enumerate(az_list):
            if az_idx == 0:
                pts_v = clutter_map_pcts_v[az_idx,0:5,:]
            else:
                pts_v = clutter_map_pcts_v[az_idx-1,5:10,:]
                pts_v = pts_v[::-1,:]
            im = axes[az_idx].pcolormesh(y_w,x_w,pts_v,cmap=cmap,norm=norm)
            axes[az_idx].set_xlim([0,20])
            axes[az_idx].set_ylim([0,1])
            if az_idx == 0:
                axes[az_idx].set_title('Clutter map ($Z_H$) at '+title+' \n '+az+' deg.')
            elif az_idx == 5:
                axes[az_idx].set_xlabel('Dist. from radar (km)')
                axes[az_idx].set_title(az+' deg.')
            elif az_idx == 3:
                axes[az_idx].set_ylabel('Height (km)')
                axes[az_idx].set_title(az+' deg.')
            else:
                axes[az_idx].set_title(az+' deg.')
    
        fig.subplots_adjust(right=0.8)
        cbar_ax = fig.add_axes([0.85, 0.15, 0.02, 0.7])
        cbar = fig.colorbar(im, cax=cbar_ax)
        cbar.ax.set_ylabel(cbar_label)
        plt.savefig(outputdir+'cluttermap_hsrhi_v_'+site+inst+'_'+date+'.png')
        ########################################################################################

        # EAST and WEST 2 column, 6 row plot
        fig, axes = plt.subplots(nrows=6,ncols=2,sharex=True,
                                 figsize=[16,12],constrained_layout=True)
        az_list_w = ['180','210','240','270','300','330']
        az_list_e = ['0','30','60','90','120','150']

        # WEST column 0
        for az_idx, az in enumerate(az_list_w):
            west = clutter_map_pcts_h[az_idx,5:10,:]
            west = west[::-1,:]
            im = axes[az_idx,0].pcolormesh(y_w,x_w,west,cmap=cmap,norm=norm)
            axes[az_idx,0].set_xlim([0,40])
            axes[az_idx,0].set_ylim([0,4])
            if az_idx == 0:
                axes[az_idx,0].set_title('Clutter map ($Z_H$) at '+title+' \n '+az+' deg.')
            elif az_idx == 5:
                axes[az_idx,0].set_xlabel('Dist. from radar (km)')
                axes[az_idx,0].set_title(az+' deg.')
            elif az_idx == 3:
                axes[az_idx,0].set_ylabel('Height (km)')
                axes[az_idx,0].set_title(az+' deg.')
            else:
                axes[az_idx,0].set_title(az+' deg.')
        # EAST column 1
        for az_idx, az in enumerate(az_list_e):
            east = clutter_map_pcts_h[az_idx,0:5,:]
            im = axes[az_idx,1].pcolormesh(y_e,x_e,east,cmap=cmap,norm=norm)
            axes[az_idx,1].set_xlim([0,40])
            axes[az_idx,1].set_ylim([0,4])
            if az_idx == 0:
                axes[az_idx,1].set_title('Clutter map ($Z_H$) at '+title+' \n '+az+' deg.')
            elif az_idx == 5:
                axes[az_idx,1].set_xlabel('Dist. from radar (km)')
                axes[az_idx,1].set_title(az+' deg.')
            elif az_idx == 3:
                axes[az_idx,1].set_ylabel('Height (km)')
                axes[az_idx,1].set_title(az+' deg.')
            else:
                axes[az_idx,1].set_title(az+' deg.')
    
        fig.subplots_adjust(right=0.8)
        cbar_ax = fig.add_axes([0.85, 0.15, 0.02, 0.7])
        cbar = fig.colorbar(im, cax=cbar_ax)
        cbar.ax.set_ylabel(cbar_label)
        plt.savefig(outputdir+'cluttermap_hsrhi_h_'+site+inst+'_'+date+'_2col.png')

        # V polarization
        # EAST and WEST 2 column, 6 row plot
        fig, axes = plt.subplots(nrows=6,ncols=2,sharex=True,
                                 figsize=[16,12],constrained_layout=True)
        az_list_w = ['180','210','240','270','300','330']
        az_list_e = ['0','30','60','90','120','150']

        # WEST column 0
        for az_idx, az in enumerate(az_list_w):
            west = clutter_map_pcts_v[az_idx,5:10,:]
            west = west[::-1,:]
            im = axes[az_idx,0].pcolormesh(y_w,x_w,west,cmap=cmap,norm=norm)
            axes[az_idx,0].set_xlim([0,40])
            axes[az_idx,0].set_ylim([0,4])
            if az_idx == 0:
                axes[az_idx,0].set_title('Clutter map ($Z_V$) at '+title+' \n '+az+' deg.')
            elif az_idx == 5:
                axes[az_idx,0].set_xlabel('Dist. from radar (km)')
                axes[az_idx,0].set_title(az+' deg.')
            elif az_idx == 3:
                axes[az_idx,0].set_ylabel('Height (km)')
                axes[az_idx,0].set_title(az+' deg.')
            else:
                axes[az_idx,0].set_title(az+' deg.')
        # EAST column 1
        for az_idx, az in enumerate(az_list_e):
            east = clutter_map_pcts_v[az_idx,0:5,:]
            im = axes[az_idx,1].pcolormesh(y_e,x_e,east,cmap=cmap,norm=norm)
            axes[az_idx,1].set_xlim([0,40])
            axes[az_idx,1].set_ylim([0,4])
            if az_idx == 0:
                axes[az_idx,1].set_title('Clutter map ($Z_V$) at '+title+' \n '+az+' deg.')
            elif az_idx == 5:
                axes[az_idx,1].set_xlabel('Dist. from radar (km)')
                axes[az_idx,1].set_title(az+' deg.')
            elif az_idx == 3:
                axes[az_idx,1].set_ylabel('Height (km)')
                axes[az_idx,1].set_title(az+' deg.')
            else:
                axes[az_idx,1].set_title(az+' deg.')
    
        fig.subplots_adjust(right=0.8)
        cbar_ax = fig.add_axes([0.85, 0.15, 0.02, 0.7])
        cbar = fig.colorbar(im, cax=cbar_ax)
        cbar.ax.set_ylabel(cbar_label)
        plt.savefig(outputdir+'cluttermap_hsrhi_v_'+site+inst+'_'+date+'_2col.png')

    else:
        d = Dataset(cluttermapdir+'cluttermap_hsrhi_'+site+inst+'_'+date+'.nc')
        #d = Dataset(cluttermapdir+'cluttermap_hsrhi_'+site+inst+'_'+date+'.nc')
        clutter_map_mask_h = d.variables['clutter_map_mask_zh'][:,:,:]
        clutter_map_mask_v = d.variables['clutter_map_mask_zv'][:,:,:]
        clutter_map_pcts_h = d.variables['clutter_gate_pcts_zh'][:,:,:]
        clutter_map_pcts_v = d.variables['clutter_gate_pcts_zv'][:,:,:]
        d.close()

        elev_e = np.arange(5)+1
        elev_w = np.arange(5)+1
        rang_e = np.arange(40)
        rang_w = np.arange(40)

        r_e, el_e = np.meshgrid(rang_e,elev_e)
        r_w, el_w = np.meshgrid(rang_w,elev_w)

        x_e = (r_e*np.sin(el_e*np.pi/180.))
        y_e = (r_e*np.cos(el_e*np.pi/180.))
        x_w = (r_w*np.sin(el_w*np.pi/180.))
        y_w = (r_w*np.cos(el_w*np.pi/180.))

        if date == 'composite':
            levels = [0,0.1,0.8,1]
            cmap_name = 'my_clutter'
            colors = ['w','lightgrey','k'] # Specify desired colors
            n_bins = 3                     # Discretizes the interpolation into bins
            cmap = LinearSegmentedColormap.from_list(cmap_name, colors, N=n_bins)
            norm = BoundaryNorm(levels, ncolors=cmap.N, clip=True) 
            cbar_label = 'Clutter point percentage occurrence'
            title = location[:3]+' '+location[3:]+' \n Composite'

        else:
            levels = [0,0.1,0.5,0.6,0.7,0.8,0.9,1]
            cmap_name = 'my_clutter'
            #colors = ['w','lightgrey','forestgreen','aquamarine','lightskyblue','mediumblue','indigo'] # Specify desired colors
            colors = ['w','lightgrey','#73D055FF','#20A387FF','#287D8EFF','#404788FF','#440154FF'] # Viridis color codes
            n_bins = 7 #[3, 6, 10, 100]  # Discretizes the interpolation into bins
            cmap = LinearSegmentedColormap.from_list(cmap_name, colors, N=n_bins)
            norm = BoundaryNorm(levels, ncolors=cmap.N, clip=True)  
            cbar_label = 'CLutter flag percentage occurrence (PCT_ON)'
            title = location[:3]+' '+location[3:]+' \n '+date[:4]+'-'+date[4:6]+'-'+date[6:]

        # H polarization
        # 1 column, 6 row plot
        fig, axes = plt.subplots(nrows=6,ncols=1,sharex=True,
                                 figsize=[12,12],constrained_layout=True)
        az_list = ['0','210','240','270','300','330']

        # Column 0
        for az_idx, az in enumerate(az_list):
            if az_idx == 0:
                pts_h = clutter_map_pcts_h[az_idx,0:5,:]
            else:
                pts_h = clutter_map_pcts_h[az_idx,5:10,:]
                pts_h = pts_h[::-1,:]
            im = axes[az_idx].pcolormesh(y_w,x_w,pts_h,cmap=cmap,norm=norm)
            axes[az_idx].set_xlim([0,40])
            axes[az_idx].set_ylim([0,4])
            if az_idx == 0:
                axes[az_idx].set_title('Clutter map ($Z_H$) at '+title+' \n '+az+' deg.')
            elif az_idx == 5:
                axes[az_idx].set_xlabel('Dist. from radar (km)')
                axes[az_idx].set_title(az+' deg.')
            elif az_idx == 3:
                axes[az_idx].set_ylabel('Height (km)')
                axes[az_idx].set_title(az+' deg.')
            else:
                axes[az_idx].set_title(az+' deg.')
    
        fig.subplots_adjust(right=0.8)
        cbar_ax = fig.add_axes([0.85, 0.15, 0.02, 0.7])
        cbar = fig.colorbar(im, cax=cbar_ax)
        cbar.ax.set_ylabel(cbar_label)
        plt.savefig(outputdir+'cluttermap_hsrhi_h_'+site+inst+'_'+date+'.png')

        # V polarization
        # 1 column, 6 row plot
        fig, axes = plt.subplots(nrows=6,ncols=1,sharex=True,
                                 figsize=[12,12],constrained_layout=True)
        az_list = ['0','210','240','270','300','330']

        # Column 0
        for az_idx, az in enumerate(az_list):
            if az_idx == 0:
                pts_v = clutter_map_pcts_v[az_idx,0:5,:]
            else:
                pts_v = clutter_map_pcts_v[az_idx,5:10,:]
                pts_v = pts_v[::-1,:]
            im = axes[az_idx].pcolormesh(y_w,x_w,pts_v,cmap=cmap,norm=norm)
            axes[az_idx].set_xlim([0,40])
            axes[az_idx].set_ylim([0,4])
            if az_idx == 0:
                axes[az_idx].set_title('Clutter map ($Z_V$) at '+title+' \n '+az+' deg.')
            elif az_idx == 5:
                axes[az_idx].set_xlabel('Dist. from radar (km)')
                axes[az_idx].set_title(az+' deg.')
            elif az_idx == 3:
                axes[az_idx].set_ylabel('Height (km)')
                axes[az_idx].set_title(az+' deg.')
            else:
                axes[az_idx].set_title(az+' deg.')
    
        fig.subplots_adjust(right=0.8)
        cbar_ax = fig.add_axes([0.85, 0.15, 0.02, 0.7])
        cbar = fig.colorbar(im, cax=cbar_ax)
        cbar.ax.set_ylabel(cbar_label)
        plt.savefig(outputdir+'cluttermap_hsrhi_v_'+site+inst+'_'+date+'.png')
        ########################################################################################

        # EAST and WEST 2 column, 6 row plot
        fig, axes = plt.subplots(nrows=6,ncols=2,sharex=True,
                                 figsize=[16,12],constrained_layout=True)
        az_list_w = ['180','210','240','270','300','330']
        az_list_e = ['0','30','60','90','120','150']

        # WEST column 0
        for az_idx, az in enumerate(az_list_w):
            west = clutter_map_pcts_h[az_idx,5:10,:]
            west = west[::-1,:]
            im = axes[az_idx,0].pcolormesh(y_w,x_w,west,cmap=cmap,norm=norm)
            axes[az_idx,0].set_xlim([0,40])
            axes[az_idx,0].set_ylim([0,4])
            if az_idx == 0:
                axes[az_idx,0].set_title('Clutter map ($Z_H$) at '+title+' \n '+az+' deg.')
            elif az_idx == 5:
                axes[az_idx,0].set_xlabel('Dist. from radar (km)')
                axes[az_idx,0].set_title(az+' deg.')
            elif az_idx == 3:
                axes[az_idx,0].set_ylabel('Height (km)')
                axes[az_idx,0].set_title(az+' deg.')
            else:
                axes[az_idx,0].set_title(az+' deg.')
        # EAST column 1
        for az_idx, az in enumerate(az_list_e):
            east = clutter_map_pcts_h[az_idx,0:5,:]
            im = axes[az_idx,1].pcolormesh(y_e,x_e,east,cmap=cmap,norm=norm)
            axes[az_idx,1].set_xlim([0,40])
            axes[az_idx,1].set_ylim([0,4])
            if az_idx == 0:
                axes[az_idx,1].set_title('Clutter map ($Z_H$) at '+title+' \n '+az+' deg.')
            elif az_idx == 5:
                axes[az_idx,1].set_xlabel('Dist. from radar (km)')
                axes[az_idx,1].set_title(az+' deg.')
            elif az_idx == 3:
                axes[az_idx,1].set_ylabel('Height (km)')
                axes[az_idx,1].set_title(az+' deg.')
            else:
                axes[az_idx,1].set_title(az+' deg.')
    
        fig.subplots_adjust(right=0.8)
        cbar_ax = fig.add_axes([0.85, 0.15, 0.02, 0.7])
        cbar = fig.colorbar(im, cax=cbar_ax)
        cbar.ax.set_ylabel(cbar_label)
        plt.savefig(outputdir+'cluttermap_hsrhi_h_'+site+inst+'_'+date+'_2col.png')

        # V polarization
        # EAST and WEST 2 column, 6 row plot
        fig, axes = plt.subplots(nrows=6,ncols=2,sharex=True,
                                 figsize=[16,12],constrained_layout=True)
        az_list_w = ['180','210','240','270','300','330']
        az_list_e = ['0','30','60','90','120','150']

        # WEST column 0
        for az_idx, az in enumerate(az_list_w):
            west = clutter_map_pcts_v[az_idx,5:10,:]
            west = west[::-1,:]
            im = axes[az_idx,0].pcolormesh(y_w,x_w,west,cmap=cmap,norm=norm)
            axes[az_idx,0].set_xlim([0,40])
            axes[az_idx,0].set_ylim([0,4])
            if az_idx == 0:
                axes[az_idx,0].set_title('Clutter map ($Z_V$) at '+title+' \n '+az+' deg.')
            elif az_idx == 5:
                axes[az_idx,0].set_xlabel('Dist. from radar (km)')
                axes[az_idx,0].set_title(az+' deg.')
            elif az_idx == 3:
                axes[az_idx,0].set_ylabel('Height (km)')
                axes[az_idx,0].set_title(az+' deg.')
            else:
                axes[az_idx,0].set_title(az+' deg.')
        # EAST column 1
        for az_idx, az in enumerate(az_list_e):
            east = clutter_map_pcts_v[az_idx,0:5,:]
            im = axes[az_idx,1].pcolormesh(y_e,x_e,east,cmap=cmap,norm=norm)
            axes[az_idx,1].set_xlim([0,40])
            axes[az_idx,1].set_ylim([0,4])
            if az_idx == 0:
                axes[az_idx,1].set_title('Clutter map ($Z_V$) at '+title+' \n '+az+' deg.')
            elif az_idx == 5:
                axes[az_idx,1].set_xlabel('Dist. from radar (km)')
                axes[az_idx,1].set_title(az+' deg.')
            elif az_idx == 3:
                axes[az_idx,1].set_ylabel('Height (km)')
                axes[az_idx,1].set_title(az+' deg.')
            else:
                axes[az_idx,1].set_title(az+' deg.')
    
        fig.subplots_adjust(right=0.8)
        cbar_ax = fig.add_axes([0.85, 0.15, 0.02, 0.7])
        cbar = fig.colorbar(im, cax=cbar_ax)
        cbar.ax.set_ylabel(cbar_label)
        plt.savefig(outputdir+'cluttermap_hsrhi_v_'+site+inst+'_'+date+'_2col.png')

    
