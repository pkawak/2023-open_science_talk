#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
created on Sat May 22 08:41:00 2021

@author: pierrekawak
"""

import sys
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import math
from scipy.interpolate import make_interp_spline

l = 1.0 #bond length
N = 10 #chain length
lp_file_name   = "avg-lpvsT.out"
cost_file_name = "avg-cos_theta_backbone.out"
filter_by = { "kb": 1.0 , "costheta_s": 0.9 }

def get_cosT(Ti):
  return (0.5*(np.exp(1./Ti)*np.sin(th_s)**2 + np.cos(th_s)**2 - np.cos(th_m)**2) / (np.exp(1./Ti)*(1-np.cos(th_s)) + np.cos(th_s) - np.cos(th_m)))

# theoretical lp
T = np.linspace(0.01,1.0,10000)
th_s = np.arccos(0.9) #stepwise stiffness cutoff
th_m = math.pi#2.*np.pi/3. #max theta due to hard core restrictions
cosT = 0.5*(np.exp(1./T)*np.sin(th_s)**2 + np.cos(th_s)**2 - np.cos(th_m)**2) / (np.exp(1./T)*(1-np.cos(th_s)) + np.cos(th_s) - np.cos(th_m)) #formula for thermal average for an isolated bond angle doi:10.1103/PhysRevE.97.042501
#print(cosT[-1])
#print("T, cosT(T)")
#print(1/500, get_cosT(1/500))
#print(10000000, get_cosT(10000000))
#print((np.cos(th_s)+np.cos(th_m))/2)
#print((th_s+th_m)/2)
#print(np.cos((th_s+th_m)/2))
lp = 0.5 * l * ( (1+cosT)/(1-cosT) )

#get lp data
lp_df = pd.read_csv(lp_file_name, index_col=False, delimiter=" ", keep_default_na=False, na_values=['_'])
lp_df['costheta_s'] = np.round(np.cos(lp_df['theta_s']),3)
lp_df = lp_df.loc[(lp_df[list(filter_by)] == pd.Series(filter_by)).all(axis=1)]

#get cos_theta data
cost_df = pd.read_csv(cost_file_name, index_col=False, delimiter=" ", keep_default_na=False, na_values=['_'])
cost_df['costheta_s'] = np.round(np.cos(cost_df['theta_s']),3)
cost_df = cost_df.loc[(cost_df[list(filter_by)] == pd.Series(filter_by)).all(axis=1)]

#figsize   = (4,6)
#fontsize  = 12
#labelsize = 10
figsize   = (2.5,3.6)
fontsize  = 10
labelsize = 8

fig, ax = plt.subplots(2, figsize=figsize, sharex=True, constrained_layout=True)

#ax[0].set_xlabel(r"$T_{r}$", fontsize=fontsize, labelpad=6)
ax[0].set_ylabel(r"$l_{p}/\sigma$", fontsize=fontsize, labelpad=1)
ax[0].tick_params(axis='both', labelsize=labelsize)
ax[0].plot(T, lp, label=r"$\frac{1}{2}\frac{1+\cos\theta}{1-\cos\theta}$")
ax[0].errorbar(lp_df["Tr"], lp_df["lp"], yerr=lp_df["lp_se"], fmt='.', color='m')
ax[0].set_yscale('log')
#ax[0].set_xscale('log')
#ax[0].set_yticks([1,100])

ax[1].set_xlabel(r"$T_{r}$", fontsize=fontsize, labelpad=6)
ax[1].set_ylabel(r"$\cos(\theta)$", fontsize=fontsize, labelpad=5)
ax[1].errorbar(cost_df["Tr"], cost_df["costheta"], yerr=cost_df["costheta_se"], fmt='.', color='m', label='Ideal MCMC')
ax[1].plot(T, cosT, label="Theory")
ax[1].hlines(0.9, 0, 1, ls='--', color='k', label=r'$\cos\theta_{s}$')
ax[1].legend(loc='lower left', fontsize=labelsize, frameon=False, handlelength=1.8)
#ax[1].set_yscale('log')
#ax[1].set_xscale('log')
ax[1].tick_params(axis='both', labelsize=labelsize)
#ax[1].set_yticks([0.3,1.0])
from matplotlib.ticker import ScalarFormatter, NullFormatter
ax[1].yaxis.set_major_formatter(ScalarFormatter())
ax[1].yaxis.set_minor_formatter(NullFormatter())
#ax[1].xaxis.set_major_formatter(ScalarFormatter())

plt.savefig("fig-lp_vs_T.pdf")
plt.close()
#if big:
#  plt.subplots_adjust(left=0.147, top=0.995, bottom=0.156, right=0.998)
#else:
#  plt.subplots_adjust(left=0.21, top=0.99, bottom=0.23, right=0.985)
