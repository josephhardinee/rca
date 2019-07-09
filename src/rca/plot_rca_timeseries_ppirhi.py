#!/usr/bin/env python
import sys
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

if __name__ == "__main__":
    if len(sys.argv) < 7:
        print(
            "ERROR: Arguments are csv file path, output path for figures, site, instrument, location, baseline date"
        )
        sys.exit(0)

    csvpath = sys.argv[1]
    fig_outpath = sys.argv[2]
    site = sys.argv[3]
    inst = sys.argv[4]
    location = sys.argv[5]
    baseline = sys.argv[6]
    print(csvpath, fig_outpath, site, inst, baseline)

#plt.style.use('seaborn-paper')
plt.style.use('publication')
params = {'mathtext.default': 'regular' }          
plt.rcParams.update(params)

location = location[0:3]+' '+location[3:]

#location = 'COR CSAPR2'
csvfile_ppi = csvpath+'daily_rcavalues_ppi_'+site+inst+'.csv'
#csvfile_rhi = csvpath+'daily_rcavalues_hsrhi_'+site+inst+'_march.csv'
csvfile_rhi = csvpath+'daily_rcavalues_hsrhi_'+site+inst+'.csv'

dfp = pd.read_csv(csvfile_ppi)
dfp = dfp.sort_values(by='DATE')

dfr = pd.read_csv(csvfile_rhi)
dfr = dfr.sort_values(by='DATE')

# Change text box locations as needed
ylim = -1.0,2.0
lw = 0.1
lww = 0.5
ytext = 0.5 
xtext = 8.0
xtext0 = 0.2

size = 11
family = 'sans'

ppi_h = 'k'
ppi_v = 'dimgray'
rhi_h = 'firebrick'
rhi_v = 'darksalmon'

# Plot the H polarization RCA values only
fig, ax = plt.subplots()#figsize=[8,4])
ax.axhline(0.,linestyle='--',color='grey')
#PPI
ax.scatter(dfp['DATE'],dfp['RCA_H'],
               color=ppi_h,
               linewidth=lw,
               label='PPI')
ax.plot(dfp['DATE'],dfp['RCA_H'],
               color=ppi_h,
               linewidth=lww,
               label='')
#RHI
ax.scatter(dfr['DATE'],dfr['RCA_H'],
               color=rhi_h,
               linewidth=lw,
               label='RHI')
ax.plot(dfr['DATE'],dfr['RCA_H'],
               color=rhi_h,
               linewidth=lww,
               label='')
ax.legend()
ax.set_ylabel('RCA value')
ax.set_title('Daily RCA values ($Z_H$) at '+location)
ax.set_ylim(ylim)
#ax.set_xlim('2018-10-18','2018-11-13')
ax.scatter(baseline,0.0,marker='D',linewidth=1,color='b')
locs, labs = plt.xticks()
plt.xticks(locs[::5])
plt.xticks
plt.gcf().autofmt_xdate()
plt.savefig(fig_outpath+'rca_h_ppirhi_'+site+inst+'.png')

# fig, ax = plt.subplots()#figsize=[8,4])
# ax.axhline(0.,linestyle='--',color='grey')
# #PPI
# ax.scatter(dfp['DATE'],dfp['RCA_V'],
#                color=ppi_h,
#                linewidth=lw,
#                label='PPI')
# ax.plot(dfp['DATE'],dfp['RCA_V'],
#                color=ppi_h,
#                linewidth=lww,
#                label='')
# #RHI
# ax.scatter(dfr['DATE'],dfr['RCA_V'],
#                color=rhi_h,
#                linewidth=lw,
#                label='HSRHI')
# ax.plot(dfr['DATE'],dfr['RCA_V'],
#                color=rhi_h,
#                linewidth=lww,
#                label='')
# ax.legend()
# ax.set_ylabel('RCA value')
# ax.set_title('Daily RCA values (V) at '+location)
# ax.set_ylim(ylim)
# #ax.set_xlim('2018-10-18','2018-11-13')
# ax.scatter(baseline,0.0,marker='D',linewidth=1,color='b')
# locs, labs = plt.xticks()
# plt.xticks(locs[::7])
# plt.xticks
# plt.gcf().autofmt_xdate()
# plt.savefig(fig_outpath+'rca_v_ppirhi_'+site+inst+'.png')

# fig, ax = plt.subplots()#figsize=[8,4])
# ax.axhline(0.,linestyle='--',color='grey')
# #PPI
# ax.scatter(dfp['DATE'],dfp['RCA_H'],
#             color=ppi_h,
#             linewidth=lw,
#             label='PPI: H')
# ax.plot(dfp['DATE'],dfp['RCA_H'],
#             color=ppi_h,
#             linewidth=lww,
#             label='')
# ax.scatter(dfp['DATE'],dfp['RCA_V'],
#             color=ppi_v,
#             linewidth=lw,
#             label='PPI: V')
# ax.plot(dfp['DATE'],dfp['RCA_V'],
#             color=ppi_v,
#             linewidth=lww,
#             label='')
# #RHI
# ax.scatter(dfr['DATE'],dfr['RCA_H'],
#             color=rhi_h,
#             linewidth=lw,
#             label='HSRHI: H')
# ax.plot(dfr['DATE'],dfr['RCA_H'],
#             color=rhi_h,
#             linewidth=lww,
#             label='')
# ax.scatter(dfr['DATE'],dfr['RCA_V'],
#             color=rhi_v,
#             linewidth=lw,
#             label='HSRHI: V')
# ax.plot(dfr['DATE'],dfr['RCA_V'],
#             color=rhi_v,
#             linewidth=lww,
#             label='')
# ax.legend()
# ax.set_ylabel('RCA value')
# ax.set_title('Daily RCA values at '+location)
# ax.set_ylim(ylim)
# ax.scatter(baseline,0.0,marker='D',linewidth=0.8,color='b')
# locs, labs = plt.xticks()
# plt.xticks(locs[::7])
# plt.xticks
# plt.gcf().autofmt_xdate()
# plt.savefig(fig_outpath+'rca_hv_ppirhi_'+site+inst+'.png')
