import matplotlib.pyplot as plt
import numpy as np
from netCDF4 import Dataset
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
from matplotlib.colors import BoundaryNorm
# plot_clutter_map.py

# Generic plotting function for clutter maps

def
plot_clutter_map(clutter_map_netcdf,output_directory,scan_type,map_type,polarization,max_range,site,inst,location):
    """
    plot_clutter_map

     Parameters:
     --------------
     clutter_map_netcdf: str
             path to clutter map netCDF
     output_directory: str
             path to directory for output .png file
     scan_type: str
             specify if the map is for PPI or RHI
             'ppi'
             'rhi'
     map_type: str
             specify if a daily or composite clutter map
             'daily'
             'composite'
     polarization: str
             specify the polarization(s) desired
             'horizontal'
             'dual'
     max_range: int
             maximum range to plot, in km
             i.e. 5, 10, 40
     site: str
             3-letter site abbreviation
             i.e. 'cor', 'ena'
     inst: str
             instrument name
             i.e. 'csapr2', 'kasacr'
     location: str
             site and instrument in all caps, no breaks for titling
             i.e. 'CORCSAPR2', 'ENAXSAPR2'
                       
     Returns:
     --------------
     (no specific return)
     however, plot is saved out

    """
    # Formatting specifications
    params = {'mathtext.default': 'regular' }          
    plt.rcParams.update(params)
    
    d = Dataset(clutter_map_netcdf)
    
    if scan_type == 'ppi':
        azimuth = np.arange(360)
        range_km = np.arange(max_range)+1
        range_m = range_km*1000
        range_min = max_range*1000*-1
        range_max = max_range*1000
        labs = np.linspace((max_range*-1),max_range,9)
        labs = labs.tolist()
            
        r, az = np.meshgrid(range_m,azimuth)
        x = (r*np.sin(az*np.pi/180.))
        y = (r*np.cos(az*np.pi/180.))
        
        if polarization == 'horizontal':
            clutter_map_mask_h_ppi = d.variables['clutter_map_mask_zh'][:,:]
            clutter_map_pcts_h_ppi = d.variables['clutter_gate_pcts_zh'][:,:]
            d.close()
          
            if map_type == 'daily':
                title_date = '' # THIS NEEDS TO BE SPECIFIED SOMEHOW
                levels = [0,0.1,0.5,0.6,0.7,0.8,0.9,1]
                cmap_name = 'daily_clutter'
                colors = ['w','lightgrey','#73D055FF','#20A387FF','#287D8EFF','#404788FF','#440154FF'] # Viridis color codes
                n_bins = 7  # Discretizes the interpolation into bins
                cbar_label = 'Clutter flag percentage occurrence (PCT_ON)'
                             
            elif map_type == 'composite':
                title_date = 'Composite'
                levels = [0,0.1,0.8,1]
                cmap_name = 'comp_clutter'
                colors = ['w','lightgrey','k'] # Specify desired colors
                n_bins = 3  # Discretizes the interpolation into bins
                cbar_label = 'Clutter point percentage occurrence (CMAP_ON)'              
            
            # Horizontal polarization
            cmap = LinearSegmentedColormap.from_list(cmap_name, colors, N=n_bins)
            norm = BoundaryNorm(levels, ncolors=cmap.N, clip=True) 
            fig, ax1 = plt.subplots(figsize=[7,6],constrained_layout=True)
            ax1.plot(x,y,(x**2+y**2)**(0.5),color='darkgrey')
            ax1.plot(x,y,(x**2+y**2)**(0.5),color='darkgrey')
            ax1.axvline(0,range_min,range_max,color='grey')
            ax1.axhline(0,range_min,range_max,color='grey')
            im = ax1.pcolormesh(x,y,clutter_map_pcts_h_ppi,
                                cmap=cmap,
                                norm=norm)
            ax1.set_xticklabels(labs)
            ax1.set_yticklabels(labs)
            cbar = fig.colorbar(im, ax=ax1)
            cbar.ax.set_ylabel(cbar_label)
            ax1.set_title('Clutter map ($Z_H$) at '+location[:3]+' '+location[3:]+' \n '+title_date)
            ax1.set_xlabel('W-E dist. from radar (km)')
            ax1.set_ylabel('N-S dist. from radar (km)')
            plt.savefig(output_directory+'cluttermap_ppi_h_'+site+inst+'_'+title_date+'.png')
            
            
        elif polarization == 'dual':
            clutter_map_mask_h_ppi = d.variables['clutter_map_mask_zh'][:,:]
            clutter_map_pcts_h_ppi = d.variables['clutter_gate_pcts_zh'][:,:]
            clutter_map_mask_v_ppi = d.variables['clutter_map_mask_zv'][:,:]
            clutter_map_pcts_v_ppi = d.variables['clutter_gate_pcts_zv'][:,:]
            d.close()
            
            if map_type == 'daily':
                title_date = '' # THIS NEEDS TO BE SPECIFIED SOMEHOW
                levels = [0,0.1,0.5,0.6,0.7,0.8,0.9,1]
                cmap_name = 'daily_clutter'
                colors = ['w','lightgrey','#73D055FF','#20A387FF','#287D8EFF','#404788FF','#440154FF'] # Viridis color codes
                n_bins = 7  # Discretizes the interpolation into bins
                cbar_label = 'Clutter flag percentage occurrence (PCT_ON)'
                             
            elif map_type == 'composite':
                title_date = 'Composite'
                levels = [0,0.1,0.8,1]
                cmap_name = 'comp_clutter'
                colors = ['w','lightgrey','k'] # Specify desired colors
                n_bins = 3  # Discretizes the interpolation into bins
                cbar_label = 'Clutter point percentage occurrence (CMAP_ON)'              
            
            # Horizontal polarization
            cmap = LinearSegmentedColormap.from_list(cmap_name, colors, N=n_bins)
            norm = BoundaryNorm(levels, ncolors=cmap.N, clip=True) 
            fig, ax1 = plt.subplots(figsize=[7,6],constrained_layout=True)
            ax1.plot(x,y,(x**2+y**2)**(0.5),color='darkgrey')
            ax1.plot(x,y,(x**2+y**2)**(0.5),color='darkgrey')
            ax1.axvline(0,range_min,range_max,color='grey')
            ax1.axhline(0,range_min,range_max,color='grey')
            im = ax1.pcolormesh(x,y,clutter_map_pcts_h_ppi,
                                cmap=cmap,
                                norm=norm)
            ax1.set_xticklabels(labs)
            ax1.set_yticklabels(labs)
            cbar = fig.colorbar(im, ax=ax1)
            cbar.ax.set_ylabel(cbar_label)
            ax1.set_title('Clutter map ($Z_H$) at '+location[:3]+' '+location[3:]+' \n '+title_date)
            ax1.set_xlabel('W-E dist. from radar (km)')
            ax1.set_ylabel('N-S dist. from radar (km)')
            plt.savefig(output_directory+'cluttermap_ppi_h_'+site+inst+'_'+title_date+'.png')
            
            # Vertical polarization
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
            ax1.set_title('Clutter map ($Z_V$) at '+location[:3]+' '+location[3:]+' \n '+title_date)
            ax1.set_xlabel('W-E dist. from radar (km)')
            ax1.set_ylabel('N-S dist. from radar (km)')
            plt.savefig(output_directory+'cluttermap_ppi_v_'+site+inst+'_'+title_date+'.png')
            
    # ---------------------------------------------------------------------------------------- 
    
    # FOR RHIS
    
    # Use caution here and adjust code for the different RHI azimuths you have
    
    # By default, this works with 12 different azimuths (every 30 degrees)
    
    # Need to adjust the following:
            # plt.subplots(nrows=6,ncols=2, ...)
            # az_list_w
            # az_list_e
            # west
            # numbering of az_idx
            
    # ----------------------------------------------------------------------------------------   
    elif scan_type == 'rhi':
        elev_e = np.arange(5)+1  # elevation is lowest 5 degrees
        elev_w = np.arange(5)+1
        range_e = np.arange(max_range)
        range_w = np.arange(max_range)

        r_e, el_e = np.meshgrid(range_e,elev_e)
        r_w, el_w = np.meshgrid(range_w,elev_w)

        x_e = (r_e*np.sin(el_e*np.pi/180.))
        y_e = (r_e*np.cos(el_e*np.pi/180.))
        x_w = (r_w*np.sin(el_w*np.pi/180.))
        y_w = (r_w*np.cos(el_w*np.pi/180.))
        
        if polarization == 'horizontal':
            clutter_map_mask_h = d.variables['clutter_map_mask_zh'][:,:,:]
            clutter_map_pcts_h = d.variables['clutter_gate_pcts_zh'][:,:,:]
            d.close()
            
            if map_type == 'daily':
                title_date = '' # THIS NEEDS TO BE SPECIFIED SOMEHOW
                levels = [0,0.1,0.5,0.6,0.7,0.8,0.9,1]
                cmap_name = 'daily_clutter'
                colors = ['w','lightgrey','#73D055FF','#20A387FF','#287D8EFF','#404788FF','#440154FF']
                n_bins = 7 
                cbar_label = 'Clutter flag percentage occurrence (PCT_ON)'
                
            elif map_type == 'composite':
                title_date = 'Composite'
                levels = [0,0.1,0.8,1]
                cmap_name = 'comp_clutter'
                colors = ['w','lightgrey','k']
                n_bins = 3
                cbar_label = 'Clutter point percentage occurrence (CMAP_ON)' 
            
            # Horizontal polarization
            cmap = LinearSegmentedColormap.from_list(cmap_name, colors, N=n_bins)
            norm = BoundaryNorm(levels, ncolors=cmap.N, clip=True)
            # EAST and WEST: 2 column, 6 row plot
            fig, axes = plt.subplots(nrows=6,ncols=2,sharex=True,
                                     figsize=[16,12],constrained_layout=True)
            az_list_w = ['180','210','240','270','300','330']
            az_list_e = ['0','30','60','90','120','150']
            # WEST column 0
            for az_idx, az in enumerate(az_list_w):
                west = clutter_map_pcts_h[az_idx,5:10,:]
                west = west[::-1,:]
                im = axes[az_idx,0].pcolormesh(y_w,x_w,west,cmap=cmap,norm=norm)
                axes[az_idx,0].set_xlim([0,max_range])
                axes[az_idx,0].set_ylim([0,2])
                if az_idx == 0:
                    axes[az_idx,0].set_title(title_date+' clutter map ($Z_H$) at '+location+' \n '+az+' deg.')
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
                    axes[az_idx,1].set_title(title_date+' clutter map ($Z_H$) at '+location+' \n '+az+' deg.')
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
            plt.savefig(output_directory+'cluttermap_hsrhi_h_'+site+inst+'_'+title_date+'.png')
                
        elif polarization == 'dual':
            clutter_map_mask_h = d.variables['clutter_map_mask_zh'][:,:,:]
            clutter_map_pcts_h = d.variables['clutter_gate_pcts_zh'][:,:,:]
            clutter_map_mask_v = d.variables['clutter_map_mask_zv'][:,:,:]
            clutter_map_pcts_v = d.variables['clutter_gate_pcts_zv'][:,:,:]
            d.close()
            
            if map_type == 'daily':
                title_date = '' # THIS NEEDS TO BE SPECIFIED SOMEHOW
                levels = [0,0.1,0.5,0.6,0.7,0.8,0.9,1]
                cmap_name = 'daily_clutter'
                colors = ['w','lightgrey','#73D055FF','#20A387FF','#287D8EFF','#404788FF','#440154FF']
                n_bins = 7 
                cbar_label = 'Clutter flag percentage occurrence (PCT_ON)'
                
            elif map_type == 'composite':
                title_date = 'Composite'
                levels = [0,0.1,0.8,1]
                cmap_name = 'comp_clutter'
                colors = ['w','lightgrey','k']
                n_bins = 3
                cbar_label = 'Clutter point percentage occurrence (CMAP_ON)'
            
            # Horizontal polarization
            cmap = LinearSegmentedColormap.from_list(cmap_name, colors, N=n_bins)
            norm = BoundaryNorm(levels, ncolors=cmap.N, clip=True)
            # EAST and WEST: 2 column, 6 row plot
            fig, axes = plt.subplots(nrows=6,ncols=2,sharex=True,
                                     figsize=[16,12],constrained_layout=True)
            az_list_w = ['180','210','240','270','300','330']
            az_list_e = ['0','30','60','90','120','150']
            # WEST column 0
            for az_idx, az in enumerate(az_list_w):
                west = clutter_map_pcts_h[az_idx,5:10,:]
                west = west[::-1,:]
                im = axes[az_idx,0].pcolormesh(y_w,x_w,west,cmap=cmap,norm=norm)
                axes[az_idx,0].set_xlim([0,max_range])
                axes[az_idx,0].set_ylim([0,2])
                if az_idx == 0:
                    axes[az_idx,0].set_title(title_date+' clutter map ($Z_H$) at '+location+' \n '+az+' deg.')
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
                    axes[az_idx,1].set_title(title_date+' clutter map ($Z_H$) at '+location+' \n '+az+' deg.')
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
            plt.savefig(output_directory+'cluttermap_hsrhi_h_'+site+inst+'_'+title_date+'.png')
            
            # Vertical polarization
            # EAST and WEST: 2 column, 6 row plot
            fig, axes = plt.subplots(nrows=6,ncols=2,sharex=True,
                                     figsize=[16,12],constrained_layout=True)
            az_list_w = ['180','210','240','270','300','330']
            az_list_e = ['0','30','60','90','120','150']
            # WEST column 0
            for az_idx, az in enumerate(az_list_w):
                west = clutter_map_pcts_v[az_idx,5:10,:]
                west = west[::-1,:]
                im = axes[az_idx,0].pcolormesh(y_w,x_w,west,cmap=cmap,norm=norm)
                axes[az_idx,0].set_xlim([0,max_range])
                axes[az_idx,0].set_ylim([0,2])
                if az_idx == 0:
                    axes[az_idx,0].set_title(title_date+' clutter map ($Z_V$) at '+location+' \n '+az+' deg.')
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
                axes[az_idx,1].set_xlim([0,20])
                axes[az_idx,1].set_ylim([0,2])
                if az_idx == 0:
                    axes[az_idx,1].set_title(title_date+' clutter map ($Z_V$) at '+location+' \n '+az+' deg.')
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
            plt.savefig(output_directory+'cluttermap_hsrhi_v_'+site+inst+'_'+title_date+'.png')
                   
    else:
        print("Must specify either 'ppi' or 'rhi' for scan_type")
    
