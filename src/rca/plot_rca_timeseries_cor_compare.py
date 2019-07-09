#!/usr/bin/env python
import sys
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

if __name__ == "__main__":
    if len(sys.argv) < 6:
        print(
            "ERROR: Arguments are csv file path, output path for figures, site, location, baseline date"
        )
        sys.exit(0)

    csvpath = sys.argv[1]
    fig_outpath = sys.argv[2]
    site = sys.argv[3]
    #inst = sys.argv[4]
    location = sys.argv[4]
    baseline = sys.argv[5]
    print(csvpath, fig_outpath, site, baseline)

#plt.style.use('publication')
params = {'mathtext.default': 'regular' }          
plt.rcParams.update(params)

csvfile_c = csvpath+'daily_rcavalues_hsrhi_'+site+'csapr2.csv'
csvfile_x = csvpath+'daily_rcavalues_hsrhi_'+site+'xsacr.csv'
csvfile_k = csvpath+'daily_rcavalues_hsrhi_'+site+'kasacr.csv'
#csvfile_c = csvpath+'daily_rcavalues_hsrhi_'+site+'csapr2_after1108.csv'
#csvfile_x = csvpath+'daily_rcavalues_hsrhi_'+site+'xsacr_after1108.csv'
#csvfile_k = csvpath+'daily_rcavalues_hsrhi_'+site+'kasacr_after1108.csv'
#csvfile_c = csvpath+'daily_rcavalues_hsrhi_'+site+'csapr2_full.csv'
#csvfile_x = csvpath+'daily_rcavalues_hsrhi_'+site+'xsacr.csv'
#csvfile_k = csvpath+'daily_rcavalues_hsrhi_'+site+'kasacr.csv'
#csvfile_z = csvpath+'cross_compare/crosscompare_xsacr_kasacr_COR_2.csv'

dc = pd.read_csv(csvfile_c)
dc = dc.sort_values(by='DATE')
dx = pd.read_csv(csvfile_x)
dx = dx.sort_values(by='DATE')
dk = pd.read_csv(csvfile_k)
dk = dk.sort_values(by='DATE')
#dz = pd.read_csv(csvfile_z)
#dz = dz.sort_values(by='DATE')

#print(dx.describe())
#print(dk.describe())
#print(dz.describe())

# Change text box locations as needed
ylim = -10.0,15.0
lw = 0.3
lww = 0.3
ytext = 0.5 
xtext = 8.0
xtext0 = 0.2
plt.rcParams["axes.grid"] = False

size = 11
family = 'sans'

c = 'k'
x = 'dimgray'
k = 'firebrick'

# Plot the H polarization RCA values only
fig, ax = plt.subplots()#figsize=[8,4])
ax.axhline(0.,linestyle='--',color='grey',zorder=-25)
ax.axhspan(-1.0, 1.0, facecolor='dimgrey', alpha=0.5,zorder=-100)
ax.axhspan(-2.0, 2.0, facecolor='gainsboro', alpha=0.5,zorder=-50)
# CSAPR2
ax.scatter(dc['DATE'],dc['RCA_H'],
               color=c,
               linewidth=lw,
               label='CSAPR2')
ax.plot(dc['DATE'],dc['RCA_H'],
               color=c,
               linewidth=lww,
               label='')
# XSACR
ax.scatter(dx['DATE'],dx['RCA_H'],
               color=x,
               linewidth=lw,
               label='XSACR')
ax.plot(dx['DATE'],dx['RCA_H'],
               color=x,
               linewidth=lww,
               label='')
# KASACR
ax.scatter(dk['DATE'],dk['RCA_H'],
               color=k,
               linewidth=lw,
               label='KASACR')
ax.plot(dk['DATE'],dk['RCA_H'],
               color=k,
               linewidth=lww,
               label='')
ax.legend()
ax.set_ylabel('RCA value')
ax.set_title('Daily RCA values ($Z_H$) at '+location+' \n CSAPR2, XSACR, KASACR')
ax.set_ylim(ylim)
ax.set_xlim('2018-11-08','2019-03-18')
ax.scatter(baseline,0.0,marker='D',linewidth=1,color='b')
#ax.axvline('2018-11-01')
locs, labs = plt.xticks()
plt.xticks(locs[::14])
plt.xticks
plt.gcf().autofmt_xdate()
plt.savefig(fig_outpath+'rca_h_hsrhi_'+site+'compare.png')

# Plot the V polarization RCA values only
fig, ax = plt.subplots()#figsize=[8,4])
ax.axhline(0.,linestyle='--',color='grey')
# CSAPR2
ax.scatter(dc['DATE'],dc['RCA_V'],
               color=c,
               linewidth=lw,
               label='CSAPR2')
ax.plot(dc['DATE'],dc['RCA_V'],
               color=c,
               linewidth=lww,
               label='')
# XSACR
ax.scatter(dx['DATE'],dx['RCA_V'],
               color=x,
               linewidth=lw,
               label='XSACR')
ax.plot(dx['DATE'],dx['RCA_V'],
               color=x,
               linewidth=lww,
               label='')
ax.legend()
ax.set_ylabel('RCA value')
ax.set_title('Daily RCA values (V) at '+location+' \n CSAPR2, XSACR, KASACR')
ax.set_ylim(ylim)
ax.scatter(baseline,0.0,marker='D',linewidth=1,color='b')
locs, labs = plt.xticks()
plt.xticks(locs[::7])
plt.xticks
plt.gcf().autofmt_xdate()
plt.savefig(fig_outpath+'rca_v_ppirhi_'+site+'compare.png')

# Plot the H polarization RCA values and Z difference between X and Ka
fig, ax = plt.subplots()#figsize=[8,4])
ax.axhline(0.,linestyle='--',color='grey')
# CSAPR2
ax.scatter(dc['DATE'],dc['RCA_H'],
               color=c,
               linewidth=lw,
               label='CSAPR2')
ax.plot(dc['DATE'],dc['RCA_H'],
               color=c,
               linewidth=lww,
               label='')
# XSACR
ax.scatter(dx['DATE'],dx['RCA_H'],
               color=x,
               linewidth=lw,
               label='XSACR')
ax.plot(dx['DATE'],dx['RCA_H'],
               color=x,
               linewidth=lww,
               label='')
# KASACR
ax.scatter(dk['DATE'],dk['RCA_H'],
               color=k,
               linewidth=lw,
               label='KASACR')
ax.plot(dk['DATE'],dk['RCA_H'],
               color=k,
               linewidth=lww,
               label='')
# ZDIFF X-Ka
ax.scatter(dz['DATE'],dz['ZDIFF_MEDIAN'],
               color='blue',
               linewidth=lw,
               label='Z(X) - Z(Ka)')
ax.plot(dz['DATE'],dz['ZDIFF_MEDIAN'],
               color='blue',
               linewidth=lww,
               label='')
ax.legend()
ax.set_ylabel('RCA value')
ax.set_title('Daily RCA values (H) at '+location+' \n with comparison of  Z(X) - Z(Ka)')
ax.set_ylim(-6,12)
ax.scatter(baseline,0.0,marker='D',linewidth=1,color='b')
locs, labs = plt.xticks()
plt.xticks(locs[::7])
plt.xticks
plt.gcf().autofmt_xdate()
plt.savefig(fig_outpath+'rca_h_hsrhi_'+site+'compare_with_zdiff.png')

# Plot the H polarization RCA values and Z difference between X and Ka
fig, ax = plt.subplots()#figsize=[8,4])
ax.axhline(0.,linestyle='--',color='grey')
# CSAPR2
#ax.scatter(dc['DATE'],dc['RCA_H'],
##               color=c,
#               linewidth=lw,
#               label='CSAPR2')
# ax.plot(dc['DATE'],dc['RCA_H'],
#                color=c,
#                linewidth=lww,
#                label='')
# # XSACR
# ax.scatter(dx['DATE'],dx['RCA_H'],
#                color=x,
#                linewidth=lw,
#                label='XSACR')
# ax.plot(dx['DATE'],dx['RCA_H'],
#                color=x,
#                linewidth=lww,
#                label='')
# # KASACR
# ax.scatter(dk['DATE'],dk['RCA_H'],
#                color=k,
#                linewidth=lw,
#                label='KASACR')
# ax.plot(dk['DATE'],dk['RCA_H'],
#                color=k,
#                linewidth=lww,
#                label='')
# ZDIFF X-Ka
ax.scatter(dz['DATE'],dz['ZDIFF_MEDIAN'],
               color='blue',
               linewidth=lw,
               label='Z(X) - Z(Ka)')
ax.plot(dz['DATE'],dz['ZDIFF_MEDIAN'],
               color='blue',
               linewidth=lww,
               label='')
# KASACR
ax.scatter(dk['DATE'],dk['RCA_H']-dx['RCA_H'],
               color=k,
               linewidth=lw,
               label='RCA(Ka) - RCA(X)')
ax.plot(dk['DATE'],dk['RCA_H']-dx['RCA_H'],
               color=k,
               linewidth=lww,
               label='')
# # diff - RCA
# ax.scatter(dz['DATE'],(dz['ZDIFF_MEDIAN']-(dk['RCA_H']-dx['RCA_H'])),
#                color='k',
#                linewidth=lw,
#                label='Z(X) - Z(Ka) - RCA(Ka) - RCA(X)')
# ax.plot(dz['DATE'],(dz['ZDIFF_MEDIAN']-(dk['RCA_H']-dx['RCA_H'])),
#                color='k',
#                linewidth=lww,
#                label='')
ax.legend()
ax.set_ylabel('RCA value')
ax.set_title('Daily RCA values (H) at '+location+' \n with comparison of  Z(X) - Z(Ka)')
ax.set_ylim(-6,12)
ax.scatter(baseline,0.0,marker='D',linewidth=1,color='b')
ax.axvline('2018-11-01')
locs, labs = plt.xticks()
plt.xticks(locs[::7])
plt.xticks
plt.gcf().autofmt_xdate()
plt.savefig(fig_outpath+'rca_h_hsrhi_'+site+'compare_with_zdiff_test.png')


median_megadiff = np.nanmedian( dz['ZDIFF_MEDIAN']-(dk['RCA_H']-dx['RCA_H']) )
print(median_megadiff)
med_arr = np.zeros((len(dz['DATE'])))
med_arr[:] = median_megadiff
print(len(med_arr))
fig, ax = plt.subplots()#figsize=[8,4])
ax.axhline(0.,linestyle='--',color='grey')
ax.axhline(median_megadiff,color='b')
ax.fill_between(dz['DATE'],med_arr-1.,med_arr+1,facecolor='grey')
# diff - RCA
ax.scatter(dz['DATE'],(dz['ZDIFF_MEDIAN']-(dk['RCA_H']-dx['RCA_H'])),
               color='k',
               linewidth=lw,
               label='Z(X) - Z(Ka) - RCA(Ka) - RCA(X)')
ax.plot(dz['DATE'],(dz['ZDIFF_MEDIAN']-(dk['RCA_H']-dx['RCA_H'])),
               color='k',
               linewidth=lww,
               label='')
ax.legend()
ax.set_ylabel('RCA value')
ax.set_title('Daily RCA difference (H) of X and Ka  \n subtracted from Z(X) - Z(Ka) ')
ax.set_ylim(-6,12)
#ax.scatter(baseline,0.0,marker='D',linewidth=1,color='b')
ax.axvline('2018-11-01')
locs, labs = plt.xticks()
plt.xticks(locs[::7])
plt.xticks
plt.gcf().autofmt_xdate()
plt.savefig(fig_outpath+'rca_h_hsrhi_'+site+'compare_with_zdiff_diff.png')

####################################################
fig, ax = plt.subplots()#figsize=[8,4])
ax.axhline(0.,linestyle='--',color='grey')
#ax.axhline(median_megadiff,color='b')
#ax.fill_between(dz['DATE'],med_arr-1.,med_arr+1,facecolor='grey')
# diff - RCA
# ax.scatter(dz['DATE'],(dz['ZDIFF_MEDIAN']-(dk['RCA_H']-dx['RCA_H'])),
#                color='k',
#                linewidth=lw,
#                label='Z(X) - Z(Ka) - RCA(Ka) - RCA(X)')
# ax.plot(dz['DATE'],(dz['ZDIFF_MEDIAN']-(dk['RCA_H']-dx['RCA_H'])),
#                color='k',
#                linewidth=lww,
#                label='')
# ZDIFF MEDIAN 1ST HALF OF DAY
ax.scatter(dz['DATE'],dz['ZDIFF_MEDIAN_00-12'],
               color='k',
               linewidth=lw,
               label='Z(X) - Z(Ka) 00-12 Z')
ax.plot(dz['DATE'],dz['ZDIFF_MEDIAN_00-12'],
               color='k',
               linewidth=lww,
               label='')
# ZDIFF MEDIAN 1ST HALF OF DAY
ax.scatter(dz['DATE'],dz['ZDIFF_MEDIAN_12-24'],
               color='g',
               linewidth=lw,
               label='Z(X) - Z(Ka) 12-00 Z')
ax.plot(dz['DATE'],dz['ZDIFF_MEDIAN_12-24'],
               color='g',
               linewidth=lww,
               label='')
# DIFF OF ZDIFF MEDIAN 1ST HALF/2nd HALF
ax.scatter(dz['DATE'],(dz['ZDIFF_MEDIAN_00-12']-dz['ZDIFF_MEDIAN_12-24']),
               color='b',
               linewidth=lw,
               label='Difference between black and green')
ax.plot(dz['DATE'],(dz['ZDIFF_MEDIAN_00-12']-dz['ZDIFF_MEDIAN_12-24']),
               color='b',
               linewidth=lww,
               label='')
ax.legend()
ax.set_ylabel('RCA value')
ax.set_title('Daily median Z(X) - Z(Ka) separated by 1st/2nd half of day')
ax.set_ylim(-3,15)
#ax.scatter(baseline,0.0,marker='D',linewidth=1,color='b')
ax.axvline('2018-11-01')
ax.axhline(np.nanmedian(dz['ZDIFF_MEDIAN_00-12']-dz['ZDIFF_MEDIAN_12-24']),color='b',linestyle='--')
locs, labs = plt.xticks()
plt.xticks(locs[::7])
plt.xticks
plt.gcf().autofmt_xdate()
plt.savefig(fig_outpath+'rca_h_hsrhi_'+site+'compare_with_zdiff_diurnal.png')


