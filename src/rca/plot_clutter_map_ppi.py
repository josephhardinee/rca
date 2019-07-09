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
            "ERROR: Arguments: Clutter map file directory, clutter map date (YYYYMMDD or composite), site, instrument, location (for labeling plot, e.g. CORCSAPR2), output directory for plots"
        )
        sys.exit(0)

    cluttermapdir = sys.argv[1]
    date = sys.argv[2]
    site = sys.argv[3]
    inst = sys.argv[4]
    location = sys.argv[5]
    outputdir = sys.argv[6]
    
    #plt.style.use('publication_radar')
    params = {'mathtext.default': 'regular' }          
    plt.rcParams.update(params)

    azimuth = np.arange(360)
    if inst == 'kasacr':
        # Import clutter map information
        d = Dataset(cluttermapdir+'cluttermap_ppi_'+site+inst+'_'+date+'.nc')
        #d = Dataset(cluttermapdir+'taranis_calibration_cluttermap_ppi_'+site+inst+'_'+date+'.nc')
        clutter_map_mask_h_ppi = d.variables['clutter_map_mask_zh'][:,:]
        clutter_map_pcts_h_ppi = d.variables['clutter_gate_pcts_zh'][:,:]

        rang = np.arange(10)+1
        line_min = -10000
        line_max = 10000
        labs = [-10,-7.5,-5,-2.5,0,2.5,5,7.5,10]

        rang = rang*1000
        r, az = np.meshgrid(rang,azimuth)
        x = (r*np.sin(az*np.pi/180.))
        y = (r*np.cos(az*np.pi/180.))

        if date == 'composite':
            levels = [0,0.1,0.8,1]
            cmap_name = 'my_clutter'
            colors = ['w','lightgrey','k'] # Specify desired colors
            n_bins = 3 #[3, 6, 10, 100]  # Discretizes the interpolation into bins
            cmap = LinearSegmentedColormap.from_list(cmap_name, colors, N=n_bins)
            norm = BoundaryNorm(levels, ncolors=cmap.N, clip=True) 
            cbar_label = 'Clutter point percentage occurrence'
        
            # Plot PPI H
            fig, ax1 = plt.subplots(figsize=[7,6],constrained_layout=True)
            ax1.plot(x,y,(x**2+y**2)**(0.5),color='darkgrey')
            ax1.plot(x,y,(x**2+y**2)**(0.5),color='darkgrey')
            ax1.axvline(0,line_min,line_max,color='grey')
            ax1.axhline(0,line_min,line_max,color='grey')
            im = ax1.pcolormesh(x,y,clutter_map_pcts_h_ppi,
                                cmap=cmap,
                                norm=norm)
            ax1.set_xticklabels(labs)
            ax1.set_yticklabels(labs)
            cbar = fig.colorbar(im, ax=ax1)
            cbar.ax.set_ylabel(cbar_label)
            ax1.set_title('Clutter map ($Z_H$) at '+location[:3]+' '+location[3:]+' \n Composite')
            ax1.set_xlabel('W-E dist. from radar (km)')
            ax1.set_ylabel('N-S dist. from radar (km)')
            plt.savefig(outputdir+'cluttermap_ppi_h_on_'+site+inst+'_'+date+'.png')
        

        else:
            # Create a mask for gates that are NOT considered clutter (individual day)
            #not_gates_h = clutter_map_pcts_h_ppi < 0.5
            #clutter_map_h = np.copy(clutter_map_pcts_h_ppi)
            #clutter_map_h[not_gates_h] = np.nan
            #not_gates_v = clutter_map_pcts_v_ppi < 0.5
            #clutter_map_v = np.copy(clutter_map_pcts_v_ppi)
            #clutter_map_v[not_gates_v] = np.nan

            levels = [0,0.1,0.5,0.6,0.7,0.8,0.9,1]
            cmap_name = 'my_clutter'
            #colors = ['w','lightgrey','forestgreen','aquamarine','lightskyblue','mediumblue','indigo'] # Specify desired colors
            colors = ['w','lightgrey','#73D055FF','#20A387FF','#287D8EFF','#404788FF','#440154FF'] # Viridis color codes
            n_bins = 7 #[3, 6, 10, 100]  # Discretizes the interpolation into bins
            cmap = LinearSegmentedColormap.from_list(cmap_name, colors, N=n_bins)
            norm = BoundaryNorm(levels, ncolors=cmap.N, clip=True) 
            cbar_label = 'Clutter flag percentage occurrence (PCT_ON)'

            #levels = np.arange(11)/10
            #cmap = plt.get_cmap('nipy_spectral_r')
            #cmap_name = 'my_clutter'
            #colors = ['w','lightgrey','k'] # Specify desired colors
            #n_bins = 3 #[3, 6, 10, 100]  # Discretizes the interpolation into bins
            #cmap = LinearSegmentedColormap.from_list(cmap_name, colors, N=n_bins)
            #norm = BoundaryNorm(levels, ncolors=cmap.N, clip=True) 
            
            # Plot PPI H
            fig, ax1 = plt.subplots(figsize=[7,6],constrained_layout=True)
            ax1.plot(x,y,(x**2+y**2)**(0.5),color='darkgrey')
            ax1.plot(x,y,(x**2+y**2)**(0.5),color='darkgrey')
            ax1.axvline(0,line_min,line_max,color='grey')
            ax1.axhline(0,line_min,line_max,color='grey')
            im = ax1.pcolormesh(x,y,clutter_map_pcts_h_ppi,
                                cmap=cmap,
                                norm=norm)
            
            ax1.set_xticklabels(labs)
            ax1.set_yticklabels(labs)
            cbar = fig.colorbar(im, ax=ax1)
            cbar.ax.set_ylabel(cbar_label)
            ax1.set_title('Clutter map ($Z_H$) at '+location[:3]+' '+location[3:]+' \n '+date[:4]+'-'+date[4:6]+'-'+date[6:])
            ax1.set_xlabel('W-E dist. from radar (km)')
            ax1.set_ylabel('N-S dist. from radar (km)')
            plt.savefig(outputdir+'cluttermap_ppi_h_'+site+inst+'_'+date+'.png')

    else:
        # Import clutter map information
        d = Dataset(cluttermapdir+'cluttermap_ppi_'+site+inst+'_'+date+'.nc')
        #d = Dataset(cluttermapdir+'taranis_calibration_cluttermap_ppi_'+site+inst+'_'+date+'.nc')
        clutter_map_mask_h_ppi = d.variables['clutter_map_mask_zh'][:,:]
        clutter_map_mask_v_ppi = d.variables['clutter_map_mask_zv'][:,:]
        clutter_map_pcts_h_ppi = d.variables['clutter_gate_pcts_zh'][:,:]
        clutter_map_pcts_v_ppi = d.variables['clutter_gate_pcts_zv'][:,:]
        d.close()
        if inst == 'csapr2' or site == 'sgp':
            rang = np.arange(10)+1
            line_min = -10000
            line_max = 10000
            labs = [-10,-7.5,-5,-2.5,0,2.5,5,7.5,10]
        elif site == 'ena':
            rang = np.arange(5)+1
            line_min = -5000
            line_max = 5000
            labs = [-5,-4,-2,0,2,4,5]

        rang = rang*1000
        r, az = np.meshgrid(rang,azimuth)
        x = (r*np.sin(az*np.pi/180.))
        y = (r*np.cos(az*np.pi/180.))

        if date == 'composite':
            levels = [0,0.1,0.8,1]
            cmap_name = 'my_clutter'
            colors = ['w','lightgrey','k'] # Specify desired colors
            n_bins = 3 #[3, 6, 10, 100]  # Discretizes the interpolation into bins
            cmap = LinearSegmentedColormap.from_list(cmap_name, colors, N=n_bins)
            norm = BoundaryNorm(levels, ncolors=cmap.N, clip=True) 
            cbar_label = 'Clutter point percentage occurrence (CMAP_ON)'
            
            # Plot PPI H
            fig, ax1 = plt.subplots(figsize=[7,6],constrained_layout=True)
            ax1.plot(x,y,(x**2+y**2)**(0.5),color='darkgrey')
            ax1.plot(x,y,(x**2+y**2)**(0.5),color='darkgrey')
            ax1.axvline(0,line_min,line_max,color='grey')
            ax1.axhline(0,line_min,line_max,color='grey')
            im = ax1.pcolormesh(x,y,clutter_map_pcts_h_ppi,
                                cmap=cmap,
                                norm=norm)
            ax1.set_xticklabels(labs)
            ax1.set_yticklabels(labs)
            cbar = fig.colorbar(im, ax=ax1)
            cbar.ax.set_ylabel(cbar_label)
            ax1.set_title('Clutter map ($Z_H$) at '+location[:3]+' '+location[3:]+' \n Composite')
            ax1.set_xlabel('W-E dist. from radar (km)')
            ax1.set_ylabel('N-S dist. from radar (km)')
            plt.savefig(outputdir+'cluttermap_ppi_h_on_'+site+inst+'_'+date+'.png')
            
            # Plot PPI V
            fig, ax1 = plt.subplots(figsize=[7,6],constrained_layout=True)
            ax1.plot(x,y,(x**2+y**2)**(0.5),color='darkgrey')
            ax1.plot(x,y,(x**2+y**2)**(0.5),color='darkgrey')
            ax1.axvline(0,line_min,line_max,color='grey')
            ax1.axhline(0,line_min,line_max,color='grey')
            im = ax1.pcolormesh(x,y,clutter_map_pcts_v_ppi,
                                cmap=cmap,
                                norm=norm)
            ax1.set_xticklabels(labs)
            ax1.set_yticklabels(labs)
            cbar = fig.colorbar(im, ax=ax1)
            cbar.ax.set_ylabel(cbar_label)
            ax1.set_title('Clutter map ($Z_V$) at '+location[:3]+' '+location[3:]+' \n Composite')
            ax1.set_xlabel('W-E dist. from radar (km)')
            ax1.set_ylabel('N-S dist. from radar (km)')
            plt.savefig(outputdir+'cluttermap_ppi_v_on_'+site+inst+'_'+date+'.png')

        else:
            # Create a mask for gates that are NOT considered clutter (individual day)
            #not_gates_h = clutter_map_pcts_h_ppi < 0.5
            #clutter_map_h = np.copy(clutter_map_pcts_h_ppi)
            #clutter_map_h[not_gates_h] = np.nan
            #not_gates_v = clutter_map_pcts_v_ppi < 0.5
            #clutter_map_v = np.copy(clutter_map_pcts_v_ppi)
            #clutter_map_v[not_gates_v] = np.nan

            levels = [0,0.1,0.5,0.6,0.7,0.8,0.9,1]
            cmap_name = 'my_clutter'
            #colors = ['w','lightgrey','forestgreen','aquamarine','lightskyblue','mediumblue','indigo'] # Specify desired colors
            colors = ['w','lightgrey','#73D055FF','#20A387FF','#287D8EFF','#404788FF','#440154FF'] # Viridis color codes
            n_bins = 7 #[3, 6, 10, 100]  # Discretizes the interpolation into bins
            cmap = LinearSegmentedColormap.from_list(cmap_name, colors, N=n_bins)
            norm = BoundaryNorm(levels, ncolors=cmap.N, clip=True) 
            cbar_label = 'Clutter flag percentage occurrence (PCT_ON)'

            #levels = np.arange(11)/10
            #cmap = plt.get_cmap('nipy_spectral_r')
            #cmap_name = 'my_clutter'
            #colors = ['w','lightgrey','k'] # Specify desired colors
            #n_bins = 3 #[3, 6, 10, 100]  # Discretizes the interpolation into bins
            #cmap = LinearSegmentedColormap.from_list(cmap_name, colors, N=n_bins)
            #norm = BoundaryNorm(levels, ncolors=cmap.N, clip=True) 
            
            # Plot PPI H
            fig, ax1 = plt.subplots(figsize=[7,6],constrained_layout=True)
            ax1.plot(x,y,(x**2+y**2)**(0.5),color='darkgrey')
            ax1.plot(x,y,(x**2+y**2)**(0.5),color='darkgrey')
            ax1.axvline(0,line_min,line_max,color='grey')
            ax1.axhline(0,line_min,line_max,color='grey')
            im = ax1.pcolormesh(x,y,clutter_map_pcts_h_ppi,
                                cmap=cmap,
                                norm=norm)
            
            ax1.set_xticklabels(labs)
            ax1.set_yticklabels(labs)
            cbar = fig.colorbar(im, ax=ax1)
            cbar.ax.set_ylabel(cbar_label)
            ax1.set_title('Clutter map ($Z_H$) at '+location[:3]+' '+location[3:]+' \n '+date[:4]+'-'+date[4:6]+'-'+date[6:])
            ax1.set_xlabel('W-E dist. from radar (km)')
            ax1.set_ylabel('N-S dist. from radar (km)')
            plt.savefig(outputdir+'cluttermap_ppi_h_'+site+inst+'_'+date+'.png')

            # Plot PPI V
            fig, ax1 = plt.subplots(figsize=[7,6],constrained_layout=True)
            ax1.plot(x,y,(x**2+y**2)**(0.5),color='darkgrey')
            ax1.plot(x,y,(x**2+y**2)**(0.5),color='darkgrey')
            ax1.axvline(0,line_min,line_max,color='grey')
            ax1.axhline(0,line_min,line_max,color='grey')
            im = ax1.pcolormesh(x,y,clutter_map_pcts_v_ppi,
                                cmap=cmap,
                                norm=norm)
            
            ax1.set_xticklabels(labs)
            ax1.set_yticklabels(labs)
            cbar = fig.colorbar(im, ax=ax1)
            cbar.ax.set_ylabel(cbar_label)
            ax1.set_title('Clutter map ($Z_V$) at '+location[:3]+' '+location[3:]+' \n '+date[:4]+'-'+date[4:6]+'-'+date[6:])
            ax1.set_xlabel('W-E dist. from radar (km)')
            ax1.set_ylabel('N-S dist. from radar (km)')
            plt.savefig(outputdir+'cluttermap_ppi_v_'+site+inst+'_'+date+'.png')

    
