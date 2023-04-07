#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
created on Fri Apr 24 08:41:00 2022

@author: pierrekawak
"""

mc_file_name          = "mcmc_results.out"
wl_file_name          = "wlmc_results.out"
fytas_trans_file_name = "Fytas_Theo_trans.out"
fytas_r2g_file_name   = "Fytas_Theo_r2g.out"
# do you want to divide by N?
divisor = 156

# get MCMC data
import pandas as pd
df_mc  = pd.read_csv(mc_file_name, delimiter=" ", header=0)
res_mc = df_mc.groupby(['Temp']).mean().reset_index()
sem_mc = df_mc.groupby(['Temp']).sem().reset_index()
#unique_Temp = pd.unique(res['Temp'])
#print(r"$R^2_g$:", res[["Temp", "gyrDist", "gyrDist_s"]])
#print(r"$R^2_g$ simulation standard error:", res["gyrDist_s"])
#print(r"$R^2_g$ averaging standard error:", sem["gyrDist"])

# get WLMC data
df_wl  = pd.read_csv(wl_file_name, delimiter=" ", names=['Temp', 'energy', 'Cv', 'r2g'])
df_wl['Cv'] /= divisor

# get Fytas, Theo data
df_fytas_trans = pd.read_csv(fytas_trans_file_name, delimiter=" ", header=0)
fytas_seg = df_fytas_trans.loc[df_fytas_trans['lambda'] == 1.12]
fytas_Tc = fytas_seg.loc[fytas_seg['transition'] == 'T_collapse']
fytas_Tm = fytas_seg.loc[fytas_seg['transition'] == 'T_freezing']
Tc = fytas_Tc['Temp'].to_numpy()[0]
Tm = fytas_Tm['Temp'].to_numpy()[0]
df_fytas_r2g = pd.read_csv(fytas_r2g_file_name, delimiter=" ", header=0)
df_fytas_r2g = df_fytas_r2g.sort_values(by = ['lambda', 'Temp'])
df_fytas_r2g_1p12 = df_fytas_r2g.loc[df_fytas_r2g['lambda'] == 1.12]
import numpy as np
#from scipy import interpolate
#X_Y_Spline = interpolate.make_interp_spline(df_fytas_r2g_1p12['Temp'], df_fytas_r2g_1p12['r2g'], k=3)
##X_Y_Spline = interpolate.interp1d(df_fytas_r2g_1p12['Temp'], df_fytas_r2g_1p12['r2g'], kind="cubic")
#Temp_ = np.linspace(df_fytas_r2g_1p12['Temp'].min(), df_fytas_r2g_1p12['Temp'].max(), 500)
#r2g_  = X_Y_Spline(Temp_)
from scipy.ndimage.filters import gaussian_filter1d
Temp_ = df_fytas_r2g_1p12['Temp']
r2g_ = df_fytas_r2g_1p12['r2g']
#r2g_  = gaussian_filter1d(df_fytas_r2g_1p12['r2g'], sigma=10)

import matplotlib.pyplot as plt

# Energy plot
fig, ax = plt.subplots(figsize=(5,2.75), constrained_layout=True)
xx = 'Temp'
yy = 'energy'
ax.errorbar(res_mc[xx], res_mc[yy], yerr=sem_mc[yy], ls='', c='k', zorder = 3)
ax.scatter(res_mc[xx], res_mc[yy], c='r', label='MCMC', zorder = 2)
ax.plot(df_wl[xx], df_wl[yy], c='b', label='WLMC', zorder = 1)
ax.scatter(fytas_Tc[xx], fytas_Tc['Elow'] , c='g', marker='*', s=100, label=r"$T_{\mathrm{collapse}}^{\mathrm{Fytas, 2013}}$", zorder = 2)
ax.scatter(fytas_Tm[xx], fytas_Tm['Elow'] , c='m', marker='*', s=100, label=r"$T_{\mathrm{freeze}}^{\mathrm{Fytas, 2013}}$", zorder = 2)
ax.scatter(fytas_Tm[xx], fytas_Tm['Ehigh'], c='m', marker='*', s=100, label=r"$T_{\mathrm{freeze}}^{\mathrm{Fytas, 2013}}$", zorder = 2)
ax.set_xlim(0.1,1.2)
ax.set_xlabel(r"$kT/\epsilon$", fontsize=12, labelpad=5)
ax.set_ylabel(r"$\left<U\right>/\epsilon$", fontsize=12, labelpad=10)
ax.legend(loc='lower right', fontsize=12)
fig.savefig("subfig-U_vs_T.pdf")
plt.close()

# R2g plot
fig, ax = plt.subplots(figsize=(5,2.75), constrained_layout=True)
xx = 'Temp'
yy = 'r2g'
ax.errorbar(res_mc[xx], res_mc[yy], yerr=sem_mc[yy], ls='', c='k', zorder = 3)
ax.scatter(res_mc[xx], res_mc[yy], c='r', label='MCMC', zorder = 2)
ax.plot(df_wl[xx], df_wl[yy], c='b', label='WLMC', zorder = 1)
#ax.plot(df_fytas_r2g_1p12[xx], df_fytas_r2g_1p12[yy], c='g', label='Fytas, Theodorakis', zorder = 1)
ax.plot(Temp_, r2g_, c='g', label='Fytas, 2013', ls='-.', zorder = 1)
ax.set_yscale('log')
ax.set_xlim(0.1,1.2)
ax.set_xlabel(r"$kT/\epsilon$", fontsize=12, labelpad=5)
ax.set_ylabel(r"$\left<R^{2}_{g}\right>/\sigma^{2}$", fontsize=12, labelpad=10)
ax.legend(loc='lower right', fontsize=12)
fig.savefig("subfig-r2g_vs_T.pdf")
plt.close()

# get Cv peaks
import scipy.signal
Cv_ = df_wl['Cv'].to_numpy()
Temp2_ = df_wl['Temp'].to_numpy()
peaks = scipy.signal.find_peaks(Cv_)[0]
peak_strength = scipy.signal.peak_prominences(Cv_, peaks)[0]
peakTs = Temp2_[peaks]
peakUs = df_wl['energy'].to_numpy()[peaks].astype('float64')
sorted_idx = np.argsort(peak_strength)
sorted_peakTs = peakTs[sorted_idx]
sorted_peakUs = peakUs[sorted_idx]
sorted_peakCvs = Cv_[peaks][sorted_idx].astype('float64')
sorted_peak_strength = peak_strength[sorted_idx]

# Cv plot
howmany_peaks_label = 2
fig, ax = plt.subplots(figsize=(5,2.75), constrained_layout=True)
# WLMC Cv
ax.plot(Temp2_, Cv_, label="WLMC", zorder = 1)
# WLMC peaks
ax.scatter(sorted_peakTs[-1], sorted_peakCvs[-1], facecolors='none', edgecolors='r', marker='o', s=50, label=r"$T_{\mathrm{freeze}}^{\mathrm{WLMC}}$", zorder = 2)
ax.scatter(sorted_peakTs[-2], sorted_peakCvs[-2], facecolors='none', edgecolors='g', marker='o', s=50, label=r"$T_{\mathrm{collapse}}^{\mathrm{WLMC}}$", zorder = 2)
# Fytas transition Ts
Cv_at_Tc = Cv_[(np.abs(Temp2_ - Tc)).argmin()]
Cv_at_Tm = Cv_[(np.abs(Temp2_ - Tm)).argmin()]
ax.scatter(Tm, sorted_peakCvs[-1], facecolors='r', marker='x', s=50, label=r"$T_{\mathrm{freeze}}^{\mathrm{Fytas, 2013}}$", zorder = 2)
ax.scatter(Tc, Cv_at_Tc          , facecolors='g', marker='x', s=50, label=r"$T_{\mathrm{collapse}}^{\mathrm{Fytas, 2013}}$", zorder = 2)
ax.set_xlim(0.2,1.2)
ax.set_ylim(0.3,300)
ax.set_yscale("log")
ax.set_xlabel(r"$kT/\epsilon$", fontsize=12, labelpad=5)
ax.set_ylabel(r'$C_v/Nk$', fontsize=12, labelpad=15)
ax.legend(loc='best', fontsize=12)
fig.savefig("subfig-Cv_vs_T.pdf")
plt.close()

# all of them to share x
fig, ax = plt.subplots(3, 1, sharex=True, figsize=(5.5,2.5*3), constrained_layout=True)
# energy plot
xx = 'Temp'
yy = 'energy'
ax[0].errorbar(res_mc[xx], res_mc[yy], yerr=sem_mc[yy], ls='', c='k', zorder = 3)
ax[0].scatter(res_mc[xx], res_mc[yy], c='r', label='MCMC', zorder = 2)
ax[0].plot(df_wl[xx], df_wl[yy], c='b', label='WLMC', zorder = 1)
ax[0].scatter(fytas_Tc[xx], fytas_Tc['Elow'] , c='g', marker='*', s=100, label=r"$E_{\mathrm{collapse}}^{\mathrm{Fytas, 2013}}$", zorder = 2)
ax[0].scatter(fytas_Tm[xx], fytas_Tm['Elow'] , c='m', marker='*', s=100, label=r"$E_{\mathrm{freeze,crystal}}^{\mathrm{Fytas, 2013}}$", zorder = 2)
ax[0].scatter(fytas_Tm[xx], fytas_Tm['Ehigh'], c='m', marker='*', s=100, label=r"$E_{\mathrm{freeze,liquid}}^{\mathrm{Fytas, 2013}}$", zorder = 2)
ax[0].set_xlim(0.2,1.2)
ax[0].set_ylabel(r"$\left<U\right>/\epsilon$", fontsize=12, labelpad=10)
ax[0].legend(loc='lower right', fontsize=12)
# R2g plot
xx = 'Temp'
yy = 'r2g'
ax[1].plot(df_wl[xx], df_wl[yy], c='b', label='WLMC', zorder = 1)
ax[1].errorbar(res_mc[xx], res_mc[yy], yerr=sem_mc[yy], ls='', c='k', zorder = 3)
ax[1].scatter(res_mc[xx], res_mc[yy], c='r', label='MCMC', zorder = 2)
#a[1]x.plot(df_fytas_r2g_1p12[xx], df_fytas_r2g_1p12[yy], c='g', label='Fytas, Theodorakis', zorder = 1)
ax[1].plot(Temp_, r2g_, c='g', label='Fytas, 2013', ls='-.', zorder = 1)
ax[1].set_yscale('log')
ax[1].set_ylabel(r"$\left<R^{2}_{g}\right>/\sigma^{2}$", fontsize=12, labelpad=10)
ax[1].legend(loc='lower right', fontsize=12)
# Cv plot
howmany_peaks_label = 2
# WLMC Cv
ax[2].plot(Temp2_, Cv_, label="WLMC", zorder = 1)
# WLMC peaks
ax[2].scatter(sorted_peakTs[-1], sorted_peakCvs[-1], facecolors='none', edgecolors='r', marker='o', s=50, label=r"$T_{\mathrm{freeze}}^{\mathrm{WLMC}}$", zorder = 2)
ax[2].scatter(sorted_peakTs[-2], sorted_peakCvs[-2], facecolors='none', edgecolors='g', marker='o', s=50, label=r"$T_{\mathrm{collapse}}^{\mathrm{WLMC}}$", zorder = 2)
# Fytas transition Ts
ax[2].scatter(Tm, sorted_peakCvs[-1], facecolors='r', marker='x', s=50, label=r"$T_{\mathrm{freeze}}^{\mathrm{Fytas, 2013}}$", zorder = 2)
ax[2].scatter(Tc, Cv_at_Tc          , facecolors='g', marker='x', s=50, label=r"$T_{\mathrm{collapse}}^{\mathrm{Fytas, 2013}}$", zorder = 2)
ax[2].set_ylim(0.3,300)
ax[2].set_yscale("log")
ax[2].set_xlabel(r"$kT/\epsilon$", fontsize=12, labelpad=5)
ax[2].set_ylabel(r'$C_v/Nk$', fontsize=12, labelpad=15)
ax[2].legend(loc='best', fontsize=12)

plt.savefig("subfig-Fytas_MC_WL_replicate.pdf")
plt.close()
