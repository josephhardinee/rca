import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import string

def plot_rca_timeseries_oneradar(rca_file,output_directory,baseline_date,polarization,scan_type,site,inst):
        """
        plot_rca_timeseries_oneradar

        Parameters:
        --------------
        rca_file: str
                path to RCA CSV file
        output_directory: str
                path to directory for output .png file(s)
        baseline_date: str
                YYYY-MM-DD format of baseline date in this dataset
        polarization: str
                specify the polarization(s) desired
                'horizontal'
                'dual'
        scan_type: str
                specify if the map is for PPI or RHI
                'ppi'
                'rhi'
        site: str
                site abbreviation
        inst: str
                instrument name
                        
        Returns:
        --------------
        (no specific return)
        however, plot is saved out

        """
        
        ylim = -3.0,3.0
        lw = 1.0
        base_lw = 1.5
        ytext = 2.0
        xtext = 8.0
        xtext0 = 2.0

        params = {'mathtext.default': 'regular',
                'family': 'sans',
                'size': 11}          
        plt.rcParams.update(params)
        
        df = pd.read_csv(rca_file)
        df = df.sort_values(by='DATE')
        
        h_mean = str(np.nanmean(df['RCA_H']))[0:4] # slice only first 3 digits
        h_std = str(np.nanstd(df['RCA_H'],ddof=1))[0:4]
        h_min = str(min(df['RCA_H']))[0:4]
        h_max = str(max(df['RCA_H']))[0:4]
        h_text = ' \n Mean:  '+h_mean+' \n St. Dev.: '+h_std+' \n Min.:    '+h_min+' \n Max.:    '+h_max+''
                
        fig, ax = plt.subplots(figsize=[8,4])
        ax.axhline(0.,linestyle='--',color='grey')
        ax.scatter(df['DATE'],df['RCA_H'],
                color='k',
                linewidth=lw)
        ax.plot(df['DATE'],df['RCA_H'],
                color='k',
                linewidth=lw)
        ax.scatter(baseline_date,0.0,marker='D',linewidth=base_lw,color='b')
        ax.set_ylabel('RCA value (dB)')
        ax.set_title('Daily RCA values ($Z_H$) at '+site.upper()+' '+inst.upper()+' \n '+scan_type.upper())
        ax.set_ylim(ylim)
        ax.text(xtext,ytext,h_text)
        locs, labs = plt.xticks()
        plt.xticks(locs[::1])
        plt.xticks
        plt.gcf().autofmt_xdate()
        plt.savefig(output_directory+'rca_h_'+scan_type+'_'+site+inst+'.png')
                
        if polarization == 'dual':
                v_mean = str(np.nanmean(df['RCA_V']))[0:4] # slice only first 3 digits
                v_std = str(np.nanstd(df['RCA_V'],ddof=1))[0:4]
                v_min = str(min(df['RCA_V']))[0:4]
                v_max = str(max(df['RCA_V']))[0:4]
                v_text = ' \n Mean:  '+v_mean+' \n St. Dev.:'+v_std+' \n Min.:   '+v_min+' \n Max.:   '+v_max+''
        
                fig, ax = plt.subplots(figsize=[8,4])
                ax.axhline(0.,linestyle='--',color='grey')
                ax.scatter(df['DATE'],df['RCA_V'],
                        color='k',
                        linewidth=lw)
                ax.plot(df['DATE'],df['RCA_V'],
                        color='k',
                        linewidth=lw)
                ax.scatter(baseline_date,0.0,marker='D',linewidth=base_lw,color='b')
                ax.set_ylabel('RCA value (dB)')
                ax.set_title('Daily RCA values ($Z_V$) at '+site.upper()+' '+inst.upper()+' \n '+scan_type.upper())
                ax.set_ylim(ylim)
                ax.text(xtext,ytext,v_text)
                locs, labs = plt.xticks()
                plt.xticks(locs[::1])
                plt.xticks
                plt.gcf().autofmt_xdate()
                plt.savefig(output_directory+'rca_v_'+scan_type+'_'+site+inst+'.png')
                
                # Plot H and V together (one plot or dual plot?)
                fig, axes = plt.subplots(nrows=2,ncols=1,sharex=True,
                                figsize=[8,5])
                axes[0].axhline(0.,linestyle='--',color='grey')
                axes[0].scatter(df['DATE'],df['RCA_H'],
                        color='k',
                        linewidth=lw)
                axes[0].plot(df['DATE'],df['RCA_H'],
                        color='k',
                        linewidth=lw)
                axes[0].set_ylabel('RCA value (dB)')
                axes[0].set_title('Daily RCA values ($Z_H$) at '+site.upper()+' '+inst.upper()+'\n '+scan_type.upper()+' \n Clutter map and Baseline: 2018-03-13')
                axes[0].set_ylim(ylim)
                axes[0].scatter(baseline_date,0.0,marker='D',linewidth=base_lw,color='b')
                axes[0].text(xtext,ytext,h_text)
                axes[0].text(0.03, 0.87, '('+string.ascii_lowercase[0]+')', transform=axes[0].transAxes, 
                        size=20, weight='regular')
                locs, labs = plt.xticks()
                plt.xticks(locs[::1])
                plt.xticks
                plt.gcf().autofmt_xdate()

                axes[1].axhline(0.,linestyle='--',color='grey')
                axes[1].scatter(df['DATE'],df['RCA_V'],
                        color='k',
                        linewidth=lw)
                axes[1].plot(df['DATE'],df['RCA_V'],
                        color='k',
                        linewidth=lw)
                axes[1].set_ylabel('RCA value (dB)')
                axes[1].set_title('Daily RCA values ($Z_V$) at '+site.upper()+' '+inst.upper()+'\n '+scan_type.upper()+'')
                axes[1].set_ylim(ylim)
                axes[1].scatter(baseline_date,0.0,marker='D',linewidth=base_lw,color='b')
                axes[1].text(xtext,ytext-1,v_text)
                axes[1].text(0.03, 0.87, '('+string.ascii_lowercase[1]+')', transform=axes[1].transAxes, 
                        size=20, weight='regular')
                locs, labs = plt.xticks()
                plt.xticks(locs[::1])
                plt.xticks
                plt.gcf().autofmt_xdate()
                plt.savefig(output_directory+'rca_hv_'+scan_type+'_'+site+inst+'.png')

    
def plot_rca_timeseries_tworadar(rca_file1,rca_file2,output_directory,baseline_date,polarization,scan_type,site,inst1,inst2,location):
        """
        plot_rca_timeseries_tworadar

        Parameters:
        --------------
        rca_file1: str
                path to RCA CSV file for radar 1
        rca_file2: str
                path to RCA CSV file for radar 2
        output_directory: str
                path to directory for output .png file(s)
        baseline_date: str
                YYYY-MM-DD format of baseline date in this dataset
        polarization: str
                specify the polarization(s) desired
                'horizontal'
                'dual'
        scan_type: str
                specify if the map is for PPI or RHI
                'ppi'
                'rhi'
        site: str
                site abbreviation
        inst1: str
                instrument name for radar 1
        inst2: str
                instrument name for radar 2
        location: str
                site and instrument (use for plot title)
                
                        
        Returns:
        --------------
        (no specific return)
        however, plot is saved out

        """
        
        ylim = -3.0,3.0
        lw = 1.0
        base_lw = 1.5
        ytext = 2.0
        xtext = 8.0
        xtext0 = 2.0

        params = {'mathtext.default': 'regular',
                'family': 'sans',
                'size': 11}          
        plt.rcParams.update(params)
        
        df1 = pd.read_csv(rca_file1)
        df2 = pd.read_csv(rca_file2)
        df1 = df1.sort_values(by='DATE')
        df2 = df2.sort_values(by='DATE')
        
        h_mean1 = str(np.nanmean(df1['RCA_H']))[0:4] # slice only first 3 digits
        h_std1 = str(np.nanstd(df1['RCA_H'],ddof=1))[0:4]
        h_min1 = str(min(df1['RCA_H']))[0:4]
        h_max1 = str(max(df1['RCA_H']))[0:4]
        h_text1 = ' \n Mean:  '+h_mean1+' \n St. Dev.: '+h_std1+' \n Min.:    '+h_min1+' \n Max.:    '+h_max1+''

        h_mean2 = str(np.nanmean(df2['RCA_H']))[0:4] # slice only first 3 digits
        h_std2 = str(np.nanstd(df2['RCA_H'],ddof=1))[0:4]
        h_min2 = str(min(df2['RCA_H']))[0:4]
        h_max2 = str(max(df2['RCA_H']))[0:4]
        h_text2 = ' \n Mean:  '+h_mean2+' \n St. Dev.: '+h_std2+' \n Min.:    '+h_min2+' \n Max.:    '+h_max2+''
                
        fig, ax = plt.subplots(figsize=[8,4])
        ax.axhline(0.,linestyle='--',color='grey')
        ax.scatter(df1['DATE'],df1['RCA_H'],
                color='k',
                linewidth=lw,
                label=inst1.upper())
        ax.plot(df1['DATE'],df1['RCA_H'],
                color='k',
                linewidth=lw,
                label='')
        ax.scatter(df2['DATE'],df2['RCA_H'],
                color='r',
                linewidth=lw,
                label=inst2.upper())
        ax.plot(df2['DATE'],df2['RCA_H'],
                color='r',
                linewidth=lw,
                label='')
        ax.scatter(baseline_date,0.0,marker='D',linewidth=base_lw,color='b')
        ax.set_ylabel('RCA value (dB)')
        ax.set_title('Daily RCA values ($Z_H$) at '+site.upper()+' '+inst1.upper()+' and '+inst2.upper()+' \n '+scan_type.upper())
        ax.set_ylim(ylim)
        #ax.text(xtext,ytext,h_text1)
        locs, labs = plt.xticks()
        plt.xticks(locs[::1])
        plt.xticks
        plt.gcf().autofmt_xdate()
        plt.savefig(output_directory+'rca_h_'+scan_type+'_'+site+inst1+'_'+site+inst2+'.png')
                
        if polarization == 'dual':
                v_mean1 = str(np.nanmean(df1['RCA_V']))[0:4] # slice only first 3 digits
                v_std1 = str(np.nanstd(df1['RCA_V'],ddof=1))[0:4]
                v_min1 = str(min(df1['RCA_V']))[0:4]
                v_max1 = str(max(df1['RCA_V']))[0:4]
                v_text1 = ' \n Mean:  '+v_mean1+' \n St. Dev.:'+v_std1+' \n Min.:   '+v_min1+' \n Max.:   '+v_max1+''

                v_mean2 = str(np.nanmean(df2['RCA_V']))[0:4] # slice only first 3 digits
                v_std2 = str(np.nanstd(df2['RCA_V'],ddof=1))[0:4]
                v_min2 = str(min(df2['RCA_V']))[0:4]
                v_max2 = str(max(df2['RCA_V']))[0:4]
                v_text2 = ' \n Mean:  '+v_mean2+' \n St. Dev.:'+v_std2+' \n Min.:   '+v_min2+' \n Max.:   '+v_max2+''
        
                fig, ax = plt.subplots(figsize=[8,4])
                ax.axhline(0.,linestyle='--',color='grey')
                ax.scatter(df1['DATE'],df1['RCA_V'],
                        color='k',
                        linewidth=lw,
                        label=inst1.upper())
                ax.plot(df1['DATE'],df1['RCA_V'],
                        color='k',
                        linewidth=lw,
                        label='')
                ax.scatter(df2['DATE'],df2['RCA_V'],
                        color='r',
                        linewidth=lw,
                        label=inst2.upper())
                ax.plot(df2['DATE'],df2['RCA_V'],
                        color='r',
                        linewidth=lw,
                        label='')
                ax.scatter(baseline_date,0.0,marker='D',linewidth=base_lw,color='b')
                ax.set_ylabel('RCA value (dB)')
                ax.set_title('Daily RCA values ($Z_V$) at '+site.upper()+' '+inst1.upper()+' and '+inst2.upper()+' \n '+scan_type.upper())
                ax.set_ylim(ylim)
                #ax.text(xtext,ytext,v_text1)
                locs, labs = plt.xticks()
                plt.xticks(locs[::1])
                plt.xticks
                plt.gcf().autofmt_xdate()
                plt.savefig(output_directory+'rca_v_'+scan_type+'_'+site+inst1+'_'+site+inst2+'.png')
                
                # Plot H and V together (one plot or dual plot?)
                fig, axes = plt.subplots(nrows=2,ncols=1,sharex=True,
                                figsize=[8,5])
                axes[0].axhline(0.,linestyle='--',color='grey')
                axes[0].scatter(df1['DATE'],df1['RCA_H'],
                        color='k',
                        linewidth=lw,
                        label=inst1.upper())
                axes[0].plot(df1['DATE'],df1['RCA_H'],
                        color='k',
                        linewidth=lw,
                        label='')
                axes[0].scatter(df2['DATE'],df2['RCA_H'],
                        color='r',
                        linewidth=lw,
                        label=inst2.upper())
                axes[0].plot(df2['DATE'],df2['RCA_H'],
                        color='r',
                        linewidth=lw,
                        label='')
                axes[0].set_ylabel('RCA value (dB)')
                axes[0].set_title('Daily RCA values ($Z_H$) at '+site.upper()+' '+inst1.upper()+' and '+inst2.upper()+'\n '+scan_type.upper())
                axes[0].set_ylim(ylim)
                axes[0].scatter(baseline_date,0.0,marker='D',linewidth=base_lw,color='b')
                #axes[0].text(xtext,ytext,h_text)
                axes[0].text(0.03, 0.87, '('+string.ascii_lowercase[0]+')', transform=axes[0].transAxes, 
                        size=20, weight='regular')
                locs, labs = plt.xticks()
                plt.xticks(locs[::1])
                plt.xticks
                plt.gcf().autofmt_xdate()

                axes[1].axhline(0.,linestyle='--',color='grey')
                axes[1].scatter(df1['DATE'],df1['RCA_V'],
                        color='k',
                        linewidth=lw,
                        label=inst1.upper())
                axes[1].plot(df1['DATE'],df1['RCA_V'],
                        color='k',
                        linewidth=lw,
                        label='')
                axes[1].scatter(df2['DATE'],df2['RCA_V'],
                        color='r',
                        linewidth=lw,
                        label=inst2.upper())
                axes[1].plot(df2['DATE'],df2['RCA_V'],
                        color='r',
                        linewidth=lw,
                        label='')
                axes[1].set_ylabel('RCA value (dB)')
                axes[1].set_title('Daily RCA values ($Z_V$) at '+site.upper()+' '+inst1.upper()+' and '+inst2.upper()+'\n '+scan_type.upper()+'')
                axes[1].set_ylim(ylim)
                axes[1].scatter(baseline_date,0.0,marker='D',linewidth=base_lw,color='b')
                #axes[1].text(xtext,ytext-1,v_text)
                axes[1].text(0.03, 0.87, '('+string.ascii_lowercase[1]+')', transform=axes[1].transAxes, 
                        size=20, weight='regular')
                locs, labs = plt.xticks()
                plt.xticks(locs[::1])
                plt.xticks
                plt.gcf().autofmt_xdate()
                plt.savefig(output_directory+'rca_hv_'+scan_type+'_'+site+inst1+'_'+site+inst2+'.png')


def plot_rca_timeseries_threeradar(rca_file1,rca_file2,rca_file3,output_directory,baseline_date,polarization,scan_type,site,inst1,inst2,inst3,location):
        """
        plot_rca_timeseries_threeradar

        Parameters:
        --------------
        rca_file1: str
                path to RCA CSV file for radar 1
        rca_file2: str
                path to RCA CSV file for radar 2
        rca_file3: str
                path to RCA CSV file for radar 3
        output_directory: str
                path to directory for output .png file(s)
        baseline_date: str
                YYYY-MM-DD format of baseline date in this dataset
        polarization: str
                specify the polarization(s) desired
                'horizontal'
                'dual'
        scan_type: str
                specify if the map is for PPI or RHI
                'ppi'
                'rhi'
        site: str
                site abbreviation
        inst1: str
                instrument name for radar 1
        inst2: str
                instrument name for radar 2
        inst3: str
                instrument name for radar 3
        location: str
                site and instrument (use for plot title)
                
                        
        Returns:
        --------------
        (no specific return)
        however, plot is saved out

        """
        
        ylim = -3.0,3.0
        lw = 1.0
        base_lw = 1.5
        ytext = 2.0
        xtext = 8.0
        xtext0 = 2.0

        params = {'mathtext.default': 'regular',
                'family': 'sans',
                'size': 11}          
        plt.rcParams.update(params)
        
        df1 = pd.read_csv(rca_file1)
        df2 = pd.read_csv(rca_file2)
        df3 = pd.read_csv(rca_file3)
        df1 = df1.sort_values(by='DATE')
        df2 = df2.sort_values(by='DATE')
        df3 = df3.sort_values(by='DATE')
        
        h_mean1 = str(np.nanmean(df1['RCA_H']))[0:4] # slice only first 3 digits
        h_std1 = str(np.nanstd(df1['RCA_H'],ddof=1))[0:4]
        h_min1 = str(min(df1['RCA_H']))[0:4]
        h_max1 = str(max(df1['RCA_H']))[0:4]
        h_text1 = ' \n Mean:  '+h_mean1+' \n St. Dev.: '+h_std1+' \n Min.:    '+h_min1+' \n Max.:    '+h_max1+''

        h_mean2 = str(np.nanmean(df2['RCA_H']))[0:4] # slice only first 3 digits
        h_std2 = str(np.nanstd(df2['RCA_H'],ddof=1))[0:4]
        h_min2 = str(min(df2['RCA_H']))[0:4]
        h_max2 = str(max(df2['RCA_H']))[0:4]
        h_text2 = ' \n Mean:  '+h_mean2+' \n St. Dev.: '+h_std2+' \n Min.:    '+h_min2+' \n Max.:    '+h_max2+''

        h_mean3 = str(np.nanmean(df3['RCA_H']))[0:4] # slice only first 3 digits
        h_std3 = str(np.nanstd(df3['RCA_H'],ddof=1))[0:4]
        h_min3 = str(min(df3['RCA_H']))[0:4]
        h_max3 = str(max(df3['RCA_H']))[0:4]
        h_text3 = ' \n Mean:  '+h_mean3+' \n St. Dev.: '+h_std3+' \n Min.:    '+h_min3+' \n Max.:    '+h_max3+''
                
        fig, ax = plt.subplots(figsize=[8,4])
        ax.axhline(0.,linestyle='--',color='grey')
        ax.scatter(df1['DATE'],df1['RCA_H'],
                color='k',
                linewidth=lw,
                label=inst1.upper())
        ax.plot(df1['DATE'],df1['RCA_H'],
                color='k',
                linewidth=lw,
                label='')
        ax.scatter(df2['DATE'],df2['RCA_H'],
                color='r',
                linewidth=lw,
                label=inst2.upper())
        ax.plot(df2['DATE'],df2['RCA_H'],
                color='r',
                linewidth=lw,
                label='')
        ax.scatter(df3['DATE'],df3['RCA_H'],
                color='grey',
                linewidth=lw,
                label=inst3.upper())
        ax.plot(df3['DATE'],df3['RCA_H'],
                color='grey',
                linewidth=lw,
                label='')
        ax.scatter(baseline_date,0.0,marker='D',linewidth=base_lw,color='b')
        ax.set_ylabel('RCA value (dB)')
        ax.set_title('Daily RCA values ($Z_H$) at '+site.upper()+' '+inst1.upper()+', '+inst2.upper()+', '+inst3.upper()+' \n '+scan_type.upper())
        ax.set_ylim(ylim)
        #ax.text(xtext,ytext,h_text1)
        locs, labs = plt.xticks()
        plt.xticks(locs[::1])
        plt.xticks
        plt.gcf().autofmt_xdate()
        plt.savefig(output_directory+'rca_h_'+scan_type+'_'+site+inst1+'_'+site+inst2+'_'+site+inst3+'.png')
                
        if polarization == 'dual':
                v_mean1 = str(np.nanmean(df1['RCA_V']))[0:4] # slice only first 3 digits
                v_std1 = str(np.nanstd(df1['RCA_V'],ddof=1))[0:4]
                v_min1 = str(min(df1['RCA_V']))[0:4]
                v_max1 = str(max(df1['RCA_V']))[0:4]
                v_text1 = ' \n Mean:  '+v_mean1+' \n St. Dev.:'+v_std1+' \n Min.:   '+v_min1+' \n Max.:   '+v_max1+''

                v_mean2 = str(np.nanmean(df2['RCA_V']))[0:4] # slice only first 3 digits
                v_std2 = str(np.nanstd(df2['RCA_V'],ddof=1))[0:4]
                v_min2 = str(min(df2['RCA_V']))[0:4]
                v_max2 = str(max(df2['RCA_V']))[0:4]
                v_text2 = ' \n Mean:  '+v_mean2+' \n St. Dev.:'+v_std2+' \n Min.:   '+v_min2+' \n Max.:   '+v_max2+''

                v_mean3 = str(np.nanmean(df3['RCA_V']))[0:4] # slice only first 3 digits
                v_std3 = str(np.nanstd(df3['RCA_V'],ddof=1))[0:4]
                v_min3 = str(min(df3['RCA_V']))[0:4]
                v_max3 = str(max(df3['RCA_V']))[0:4]
                v_text3 = ' \n Mean:  '+v_mean3+' \n St. Dev.:'+v_std3+' \n Min.:   '+v_min3+' \n Max.:   '+v_max3+''
        
                fig, ax = plt.subplots(figsize=[8,4])
                ax.axhline(0.,linestyle='--',color='grey')
                ax.scatter(df1['DATE'],df1['RCA_V'],
                        color='k',
                        linewidth=lw,
                        label=inst1.upper())
                ax.plot(df1['DATE'],df1['RCA_V'],
                        color='k',
                        linewidth=lw,
                        label='')
                ax.scatter(df2['DATE'],df2['RCA_V'],
                        color='r',
                        linewidth=lw,
                        label=inst2.upper())
                ax.plot(df2['DATE'],df2['RCA_V'],
                        color='r',
                        linewidth=lw,
                        label='')
                ax.scatter(df3['DATE'],df3['RCA_V'],
                        color='grey',
                        linewidth=lw,
                        label=inst3.upper())
                ax.plot(df3['DATE'],df3['RCA_V'],
                        color='grey',
                        linewidth=lw,
                        label='')
                ax.scatter(baseline_date,0.0,marker='D',linewidth=base_lw,color='b')
                ax.set_ylabel('RCA value (dB)')
                ax.set_title('Daily RCA values ($Z_V$) at '+site.upper()+' '+inst1.upper()+', '+inst2.upper()+', '+inst3.upper()+' \n '+scan_type.upper())
                ax.set_ylim(ylim)
                #ax.text(xtext,ytext,v_text1)
                locs, labs = plt.xticks()
                plt.xticks(locs[::1])
                plt.xticks
                plt.gcf().autofmt_xdate()
                plt.savefig(output_directory+'rca_v_'+scan_type+'_'+site+inst1+'_'+site+inst2+'_'+site+inst3+'.png')
                
                # Plot H and V together (one plot or dual plot?)
                fig, axes = plt.subplots(nrows=2,ncols=1,sharex=True,
                                figsize=[8,5])
                axes[0].axhline(0.,linestyle='--',color='grey')
                axes[0].scatter(df1['DATE'],df1['RCA_H'],
                        color='k',
                        linewidth=lw,
                        label=inst1.upper())
                axes[0].plot(df1['DATE'],df1['RCA_H'],
                        color='k',
                        linewidth=lw,
                        label='')
                axes[0].scatter(df2['DATE'],df2['RCA_H'],
                        color='r',
                        linewidth=lw,
                        label=inst2.upper())
                axes[0].plot(df2['DATE'],df2['RCA_H'],
                        color='r',
                        linewidth=lw,
                        label='')
                axes[0].scatter(df3['DATE'],df3['RCA_H'],
                        color='grey',
                        linewidth=lw,
                        label=inst3.upper())
                axes[0].plot(df3['DATE'],df3['RCA_H'],
                        color='grey',
                        linewidth=lw,
                        label='')
                axes[0].set_ylabel('RCA value (dB)')
                axes[0].set_title('Daily RCA values ($Z_H$) at '+site.upper()+' '+inst1.upper()+', '+inst2.upper()+', '+inst3.upper()+'\n '+scan_type.upper())
                axes[0].set_ylim(ylim)
                axes[0].scatter(baseline_date,0.0,marker='D',linewidth=base_lw,color='b')
                #axes[0].text(xtext,ytext,h_text)
                axes[0].text(0.03, 0.87, '('+string.ascii_lowercase[0]+')', transform=axes[0].transAxes, 
                        size=20, weight='regular')
                locs, labs = plt.xticks()
                plt.xticks(locs[::1])
                plt.xticks
                plt.gcf().autofmt_xdate()

                axes[1].axhline(0.,linestyle='--',color='grey')
                axes[1].scatter(df1['DATE'],df1['RCA_V'],
                        color='k',
                        linewidth=lw,
                        label=inst1.upper())
                axes[1].plot(df1['DATE'],df1['RCA_V'],
                        color='k',
                        linewidth=lw,
                        label='')
                axes[1].scatter(df2['DATE'],df2['RCA_V'],
                        color='r',
                        linewidth=lw,
                        label=inst2.upper())
                axes[1].plot(df2['DATE'],df2['RCA_V'],
                        color='r',
                        linewidth=lw,
                        label='')
                axes[1].scatter(df3['DATE'],df3['RCA_V'],
                        color='grey',
                        linewidth=lw,
                        label=inst3.upper())
                axes[1].plot(df3['DATE'],df3['RCA_V'],
                        color='grey',
                        linewidth=lw,
                        label='')
                axes[1].set_ylabel('RCA value (dB)')
                axes[1].set_title('Daily RCA values ($Z_V$) at '+site.upper()+' '+inst1.upper()+', '+inst2.upper()+', '+inst3.upper()+'\n '+scan_type.upper())
                axes[1].set_ylim(ylim)
                axes[1].scatter(baseline_date,0.0,marker='D',linewidth=base_lw,color='b')
                #axes[1].text(xtext,ytext-1,v_text)
                axes[1].text(0.03, 0.87, '('+string.ascii_lowercase[1]+')', transform=axes[1].transAxes, 
                        size=20, weight='regular')
                locs, labs = plt.xticks()
                plt.xticks(locs[::1])
                plt.xticks
                plt.gcf().autofmt_xdate()
                plt.savefig(output_directory+'rca_hv_'+scan_type+'_'+site+inst1+'_'+site+inst2+'_'+site+inst3+'.png')

    
    
