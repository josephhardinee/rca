#!/usr/bin/env python
import sys
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn import datasets, linear_model
from sklearn.metrics import mean_squared_error, r2_score
from scipy import stats

site = 'cor'

plt.style.use('publication')
params = {'mathtext.default': 'regular' }          
plt.rcParams.update(params)
plt.rcParams["axes.grid"] = False

csvpath = './cross_compare/'
csvpath2 = './datafiles/'
fig_outpath = './figures/'
csvfile1 = csvpath+'crosscal_cacti_xsacr_csapr2.csv'
csvfile2 = csvpath+'crosscal_cacti_xsacr_kasacr.csv'

csvfile_c = csvpath2+'daily_rcavalues_hsrhi_'+site+'csapr2.csv'
csvfile_x = csvpath2+'daily_rcavalues_hsrhi_'+site+'xsacr.csv'
csvfile_k = csvpath2+'daily_rcavalues_hsrhi_'+site+'kasacr.csv'

dc = pd.read_csv(csvfile_c)
dc = dc.sort_values(by='DATE')
dx = pd.read_csv(csvfile_x)
dx = dx.sort_values(by='DATE')
dk = pd.read_csv(csvfile_k)
dk = dk.sort_values(by='DATE')

# Change text box locations as needed
ylim = 0.0,20.0
lw = 0.3
lww = 0.3
#size = 11
#family = 'sans'

df = pd.read_csv(csvfile1)
df = df.sort_values(by='DATE')
df2 = pd.read_csv(csvfile2)
df2 = df2.sort_values(by='DATE')

fig, ax = plt.subplots()
ax.axhline(0.,linestyle='--',color='grey',zorder=-25)
ax.axhspan(-1.0, 1.0, facecolor='dimgrey', alpha=0.5,zorder=-100)
ax.axhspan(-2.0, 2.0, facecolor='gainsboro', alpha=0.5,zorder=-50)
# ax.scatter(dx['DATE'],dx['RCA_H'],
#            color='grey',
#            linewidth=lw,
#            label='XSACR RCA')
# ax.plot(dx['DATE'],dx['RCA_H'],
#            color='grey',
#            linewidth=lww,
#            label='')
# ax.scatter(dk['DATE'],dk['RCA_H'],
#            color='r',
#            linewidth=lw,
#            label='KaSACR RCA')
# ax.plot(dk['DATE'],dk['RCA_H'],
#            color='r',
#            linewidth=lww,
#            label='')
ax.scatter(df2['DATE'],df2['ZDIFF_MED'],
           color='k',
           linewidth=lw,
           label='Z(X - Ka)')
ax.plot(df2['DATE'],df2['ZDIFF_MED'],
           color='k',
           linewidth=lww,
           label='')
ax.scatter(dx['DATE'],dk['RCA_H']-dx['RCA_H'],
           color='r',
           linewidth=lw,
           label='RCA(Ka - X)')
ax.plot(dx['DATE'],dk['RCA_H']-dx['RCA_H'],
           color='r',
           linewidth=lww,
           label='')
ax.set_ylabel('dB')
ax.set_title('Daily median reflectivity (Z$_H$) difference and RCA difference at COR \n XSACR, KaSACR')
ax.set_ylim(ylim)
ax.set_xlim('2018-11-08','2019-03-18')
ax.legend()
#ax.scatter(baseline,0.0,marker='D',linewidth=lww,color='b')
#ax.text(xtext0,ytext,h_text,size=size,family=family)
locs, labs = plt.xticks()
plt.xticks(locs[::14])
plt.xticks
#plt.xticks(labs[::1])
#plt.xticks
plt.gcf().autofmt_xdate()
plt.savefig(fig_outpath+'timeseries_zdiff_rcadiff_cor_xka.png')


fig, ax = plt.subplots()
ax.axhline(0.,linestyle='--',color='grey',zorder=-25)
ax.axhspan(-1.0, 1.0, facecolor='dimgrey', alpha=0.5,zorder=-100)
ax.axhspan(-2.0, 2.0, facecolor='gainsboro', alpha=0.5,zorder=-50)
ax.scatter(dx['DATE'],dx['RCA_H'],
           color='grey',
           linewidth=lw,
           label='XSACR RCA')
ax.plot(dx['DATE'],dx['RCA_H'],
           color='grey',
           linewidth=lww,
           label='')
ax.scatter(dk['DATE'],dk['RCA_H'],
           color='r',
           linewidth=lw,
           label='KaSACR RCA')
ax.plot(dk['DATE'],dk['RCA_H'],
           color='r',
           linewidth=lww,
           label='')
ax.scatter(df2['DATE'],df2['ZDIFF_MED'],
           color='k',
           linewidth=lw,
           label='Z(X - Ka)')
ax.plot(df2['DATE'],df2['ZDIFF_MED'],
           color='k',
           linewidth=lww,
           label='')
# ax.scatter(dx['DATE'],dk['RCA_H']-dx['RCA_H'],
#            color='blue',
#            linewidth=lw,
#            label='RCA(Ka - X)')
# ax.plot(dx['DATE'],dk['RCA_H']-dx['RCA_H'],
#            color='blue',
#            linewidth=lww,
#            label='')
ax.set_ylabel('dB')
ax.set_title('Daily median reflectivity (Z$_H$) difference and RCA at COR \n XSACR, KaSACR')
ax.set_ylim(ylim)
ax.set_xlim('2018-11-08','2019-03-18')
ax.legend()
#ax.scatter(baseline,0.0,marker='D',linewidth=lww,color='b')
#ax.text(xtext0,ytext,h_text,size=size,family=family)
locs, labs = plt.xticks()
plt.xticks(locs[::14])
plt.xticks
#plt.xticks(labs[::1])
#plt.xticks
plt.gcf().autofmt_xdate()
plt.savefig(fig_outpath+'timeseries_zdiff_rca_cor_xka.png')


dftest = pd.merge(df2['ZDIFF_MED'], dk['RCA_H']-dx['RCA_H'], left_index=True, right_index=True)
dftest2 = pd.merge(dftest, df2['NUMPS'], left_index=True, right_index=True)
print(dftest2)

num = dftest2['NUMPS']
#fltr = num<1000
zdiff = dftest['ZDIFF_MED']
rcadiff = dftest['RCA_H']
zdiff[num<1000] = np.nan
#rcadiff[num<1000] = np.nan
fltr2 = np.isnan(zdiff)
#rcadiff[fltr2] = np.nan

fig, ax = plt.subplots()
ax.axhline(0.,linestyle='--',color='grey',zorder=-25)
ax.axhspan(-1.0, 1.0, facecolor='dimgrey', alpha=0.5,zorder=-100)
ax.axhspan(-2.0, 2.0, facecolor='gainsboro', alpha=0.5,zorder=-50)
# ax.scatter(dx['DATE'],dx['RCA_H'],
#            color='grey',
#            linewidth=lw,
#            label='XSACR RCA')
# ax.plot(dx['DATE'],dx['RCA_H'],
#            color='grey',
#            linewidth=lww,
#            label='')
# ax.scatter(dk['DATE'],dk['RCA_H'],
#            color='r',
#            linewidth=lw,
#            label='KaSACR RCA')
# ax.plot(dk['DATE'],dk['RCA_H'],
#            color='r',
#            linewidth=lww,
#            label='')
ax.scatter(df2['DATE'],zdiff,
           color='k',
           linewidth=lw,
           label='Z(X - Ka)')
ax.plot(df2['DATE'],zdiff,
           color='k',
           linewidth=lww,
           label='')
<<<<<<< HEAD
ax.scatter(df2['DATE'],rcadiff,
           color='r',
           linewidth=lw,
           label='RCA(Ka - X)')
ax.plot(df2['DATE'],rcadiff,
=======
ax.scatter(df2['DATE'],dftest['RCA_H'],
           color='r',
           linewidth=lw,
           label='RCA(Ka - X)')
ax.plot(df2['DATE'],dftest['RCA_H'],
>>>>>>> fca160f0e307ee2968215e0882c276048c9804e2
           color='r',
           linewidth=lww,
           label='')
ax.set_ylabel('dB')
ax.set_title('Daily median reflectivity (Z$_H$) difference and RCA difference at COR \n XSACR, KaSACR')
ax.set_ylim(ylim)
ax.set_xlim('2018-11-08','2019-03-18')
ax.legend()
#ax.scatter(baseline,0.0,marker='D',linewidth=lww,color='b')
#ax.text(xtext0,ytext,h_text,size=size,family=family)
locs, labs = plt.xticks()
plt.xticks(locs[::14])
plt.xticks
#plt.xticks(labs[::1])
#plt.xticks
plt.gcf().autofmt_xdate()
plt.savefig(fig_outpath+'timeseries_zdiff_rcadiff_cor_xka.png')

offset = np.nanmean(zdiff - rcadiff)
print(offset)
dftest['RCA_H'] = dftest['RCA_H']+offset
rcadiff = rcadiff+offset
#print(dftest['RCA_H'])

fig, ax = plt.subplots()
ax.axhline(0.,linestyle='--',color='grey',zorder=-25)
#ax.axhspan(-1.0, 1.0, facecolor='dimgrey', alpha=0.5,zorder=-100)
#ax.axhspan(-2.0, 2.0, facecolor='gainsboro', alpha=0.5,zorder=-50)
# ax.scatter(dx['DATE'],dx['RCA_H'],
#            color='grey',
#            linewidth=lw,
#            label='XSACR RCA')
# ax.plot(dx['DATE'],dx['RCA_H'],
#            color='grey',
#            linewidth=lww,
#            label='')
# ax.scatter(dk['DATE'],dk['RCA_H'],
#            color='r',
#            linewidth=lw,
#            label='KaSACR RCA')
# ax.plot(dk['DATE'],dk['RCA_H'],
#            color='r',
#            linewidth=lww,
#            label='')
ax.scatter(df2['DATE'],zdiff,
           color='k',
           linewidth=lw,
           label='Z(X - Ka)')
ax.plot(df2['DATE'],zdiff,
           color='k',
           linewidth=lww,
           label='')
<<<<<<< HEAD
ax.scatter(df2['DATE'],rcadiff,
           color='r',
           linewidth=lw,
           label='RCA(Ka - X)')
ax.plot(df2['DATE'],rcadiff,
=======
ax.scatter(df2['DATE'],dftest['RCA_H'],
           color='r',
           linewidth=lw,
           label='RCA(Ka - X)')
ax.plot(df2['DATE'],dftest['RCA_H'],
>>>>>>> fca160f0e307ee2968215e0882c276048c9804e2
           color='r',
           linewidth=lww,
           label='')
ax.set_ylabel('dB')
ax.set_title('Daily median reflectivity (Z$_H$) difference and RCA difference at COR \n XSACR, KaSACR (RCA difference offset +3.28)')
ax.set_ylim(ylim)
ax.set_xlim('2018-11-08','2019-03-18')
ax.legend()
#ax.scatter(baseline,0.0,marker='D',linewidth=lww,color='b')
#ax.text(xtext0,ytext,h_text,size=size,family=family)
locs, labs = plt.xticks()
plt.xticks(locs[::14])
plt.xticks
#plt.xticks(labs[::1])
#plt.xticks
plt.gcf().autofmt_xdate()
plt.savefig(fig_outpath+'timeseries_zdiff_rcadiffNormed_cor_xka.png')

fig, ax = plt.subplots()
ax.hist((zdiff-rcadiff)-3.28, bins=30)
ax.set_xlabel('Z(X-Ka) - RCA(Ka-X)')
ax.set_title('Distribution of differences between daily mean Z(X-Ka) and RCA(Ka-X)')
plt.gcf().autofmt_xdate()
plt.savefig(fig_outpath+'hist_zdiff_rcadiff.png')

dftest = dftest.dropna()
#print(dftest1)
x = dftest['ZDIFF_MED']
y = dftest['RCA_H']
num = dftest2['NUMPS']
fltr = num>1000
x = x[fltr]
y = y[fltr]
num = num[fltr]
#[numps>10000]

slope, intercept, r_value, p_value, std_err = stats.linregress(x,y)
xx = np.linspace(0,20,100)
yy = slope*xx + intercept

print('Slope:', slope, 'Intercept:', intercept, p_value, std_err)
print('r-squared:', r_value**2)
text = 'Slope: '+str(slope)[0:5]+'\nIntercept: '+str(intercept)[0:5]+'\nR$^2$: '+str(r_value**2)[0:5]

# Plot outputs
fig, ax = plt.subplots(figsize=(8,8))
plt.scatter(x,y,  color='black')#c=num, cmap='viridis')#color='black', 
plt.plot(xx,yy, color='orange')

ax.set_aspect('equal', 'datalim')
ax.set_ylabel('RCA(Ka - X)')
ax.set_xlabel('Z(X - Ka)')
ax.set_xlim(-5,20)
ax.set_ylim(-5,20)
ax.text(-3,15,text)
ax.set_title('Daily median reflectivity (Z$_H$) difference vs. RCA difference  \n at COR X/KaSACR')
plt.savefig(fig_outpath+'scatter_zdiff_xka_cor.png')

<<<<<<< HEAD
=======
fig, ax = plt.subplots()
ax.axhline(0.,linestyle='--',color='grey',zorder=-25)
ax.axhspan(-1.0, 1.0, facecolor='dimgrey', alpha=0.5,zorder=-100)
ax.axhspan(-2.0, 2.0, facecolor='gainsboro', alpha=0.5,zorder=-50)
# ax.scatter(dx['DATE'],dx['RCA_H'],
#            color='grey',
#            linewidth=lw,
#            label='XSACR RCA')
# ax.plot(dx['DATE'],dx['RCA_H'],
#            color='grey',
#            linewidth=lww,
#            label='')
# ax.scatter(dk['DATE'],dk['RCA_H'],
#            color='r',
#            linewidth=lw,
#            label='KaSACR RCA')
# ax.plot(dk['DATE'],dk['RCA_H'],
#            color='r',
#            linewidth=lww,
#            label='')
ax.scatter(df2['DATE'],df2['ZDIFF_MED'],
           color='k',
           linewidth=lw,
           label='Z(X - Ka)')
ax.plot(df2['DATE'],df2['ZDIFF_MED'],
           color='k',
           linewidth=lww,
           label='')
ax.scatter(dx['DATE'],dk['RCA_H']-dx['RCA_H'],
           color='r',
           linewidth=lw,
           label='RCA(Ka - X)')
ax.plot(dx['DATE'],dk['RCA_H']-dx['RCA_H'],
           color='r',
           linewidth=lww,
           label='')
ax.set_ylabel('dB')
ax.set_title('Daily median reflectivity (Z$_H$) difference and RCA difference at COR \n XSACR, KaSACR')
ax.set_ylim(ylim)
ax.set_xlim('2018-11-08','2019-03-18')
ax.legend()
#ax.scatter(baseline,0.0,marker='D',linewidth=lww,color='b')
#ax.text(xtext0,ytext,h_text,size=size,family=family)
locs, labs = plt.xticks()
plt.xticks(locs[::14])
plt.xticks
#plt.xticks(labs[::1])
#plt.xticks
plt.gcf().autofmt_xdate()
plt.savefig(fig_outpath+'timeseries_zdiff_rcadiff_cor_xka.png')
>>>>>>> fca160f0e307ee2968215e0882c276048c9804e2
