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
nobond_lp_file_name   = "nobond_avg-lpvsT.out"
nobond_cost_file_name = "nobond_avg-cos_theta_backbone.out"
filter_by = { "kb": 1.0 }

# get lp data
lp_df = pd.read_csv(lp_file_name, index_col=False, delimiter=" ", keep_default_na=False, na_values=['_'])
lp_df = lp_df.loc[(lp_df[list(filter_by)] == pd.Series(filter_by)).all(axis=1)]
nobond_lp_df = pd.read_csv(nobond_lp_file_name, index_col=False, delimiter=" ", keep_default_na=False, na_values=['_'])
nobond_lp_df = nobond_lp_df.loc[(nobond_lp_df[list(filter_by)] == pd.Series(filter_by)).all(axis=1)]

# get cos_theta data
cost_df = pd.read_csv(cost_file_name, index_col=False, delimiter=" ", keep_default_na=False, na_values=['_'])
cost_df = cost_df.loc[(cost_df[list(filter_by)] == pd.Series(filter_by)).all(axis=1)]
nobond_cost_df = pd.read_csv(nobond_cost_file_name, index_col=False, delimiter=" ", keep_default_na=False, na_values=['_'])
nobond_cost_df = nobond_cost_df.loc[(nobond_cost_df[list(filter_by)] == pd.Series(filter_by)).all(axis=1)]

# filter out stuff with T > 1
lp_df = lp_df.loc[lp_df['T'] < 1.01]
cost_df = cost_df.loc[cost_df['T'] < 1.01]
nobond_lp_df = nobond_lp_df.loc[nobond_lp_df['T'] < 1.01]
nobond_cost_df = nobond_cost_df.loc[nobond_cost_df['T'] < 1.01]

figsize   = (2.5,3.6)
fontsize  = 10
labelsize = 8
fig, ax = plt.subplots(2, figsize=figsize, sharex=True, constrained_layout=True)

#ax[0].set_xlabel(r"$T_{r}$", fontsize=fontsize, labelpad=6)
ax[0].set_ylabel(r"$l_{p}/\sigma$", fontsize=fontsize, labelpad=-4)
ax[0].tick_params(axis='both', labelsize=labelsize)
ax[0].errorbar(lp_df["Tr"], lp_df["lp"], yerr=lp_df["lp_se"], fmt='.', color='m')
ax[0].errorbar(nobond_lp_df["Tr"], nobond_lp_df["lp"], yerr=nobond_lp_df["lp_se"], fmt='.', color='b')
ax[0].set_yscale('log')
#ax[0].set_xscale('log')
#ax[0].set_yticks([1,100])

ax[1].set_xlabel(r"$T_{r}$", fontsize=fontsize, labelpad=6)
ax[1].set_ylabel(r"$\cos(\theta)$", fontsize=fontsize, labelpad=0)
ax[1].errorbar(cost_df["Tr"], cost_df["costheta"], yerr=cost_df["costheta_se"], fmt='.', color='m', label='harmonic bond')
ax[1].errorbar(nobond_cost_df["Tr"], nobond_cost_df["costheta"], yerr=nobond_cost_df["costheta_se"], fmt='.', color='b', label='tangent bond')
ax[1].legend(loc='lower left', fontsize=labelsize, frameon=False, handlelength=1.8, handletextpad=0.3)
#ax[1].set_yscale('log')
#ax[1].set_xscale('log')
ax[1].tick_params(axis='both', labelsize=labelsize)
#ax[1].set_yticks([0.3,1.0])
from matplotlib.ticker import ScalarFormatter, NullFormatter
ax[1].yaxis.set_major_formatter(ScalarFormatter())
ax[1].yaxis.set_minor_formatter(NullFormatter())
#ax[1].xaxis.set_major_formatter(ScalarFormatter())

plt.savefig("fig-lp_vs_T_bond_comp.pdf")
plt.close()
#if big:
#  plt.subplots_adjust(left=0.147, top=0.995, bottom=0.156, right=0.998)
#else:
#  plt.subplots_adjust(left=0.21, top=0.99, bottom=0.23, right=0.985)

lp_df       = pd.read_csv(lp_file_name, index_col=False, delimiter=" ", keep_default_na=False, na_values=['_'])
cost_df     = pd.read_csv(cost_file_name, index_col=False, delimiter=" ", keep_default_na=False, na_values=['_'])
lp_df = lp_df.loc[lp_df['T'] < 1.01]
cost_df = cost_df.loc[cost_df['T'] < 1.01]

kb1_lp_df   = lp_df.loc[lp_df['kb'] == 1]
kb2_lp_df   = lp_df.loc[lp_df['kb'] == 2]
kb4_lp_df   = lp_df.loc[lp_df['kb'] == 4]
kb8_lp_df   = lp_df.loc[lp_df['kb'] == 8]

kb1_cost_df   = cost_df.loc[cost_df['kb'] == 1]
kb2_cost_df   = cost_df.loc[cost_df['kb'] == 2]
kb4_cost_df   = cost_df.loc[cost_df['kb'] == 4]
kb8_cost_df   = cost_df.loc[cost_df['kb'] == 8]

fig, ax = plt.subplots(2, figsize=figsize, sharex=True, constrained_layout=True)
cmap = plt.get_cmap('tab10')

#ax[0].set_xlabel(r"$T_{r}$", fontsize=fontsize, labelpad=6)
ax[0].set_ylabel(r"$l_{p}/\sigma$", fontsize=fontsize, labelpad=-4)
ax[0].tick_params(axis='both', labelsize=labelsize)
ax[0].errorbar(kb1_lp_df["Tr"], kb1_lp_df["lp"], yerr=kb1_lp_df["lp_se"], fmt='.', color=cmap(0))
ax[0].errorbar(kb2_lp_df["Tr"], kb2_lp_df["lp"], yerr=kb2_lp_df["lp_se"], fmt='.', color=cmap(1))
ax[0].errorbar(kb4_lp_df["Tr"], kb4_lp_df["lp"], yerr=kb4_lp_df["lp_se"], fmt='.', color=cmap(2))
ax[0].errorbar(kb8_lp_df["Tr"], kb8_lp_df["lp"], yerr=kb8_lp_df["lp_se"], fmt='.', color=cmap(3))
ax[0].set_yscale('log')
#ax[0].set_xscale('log')
#ax[0].set_yticks([1,100])

ax[1].set_xlabel(r"$T_{r}$", fontsize=fontsize, labelpad=6)
ax[1].set_ylabel(r"$\cos(\theta)$", fontsize=fontsize, labelpad=0)
ax[1].errorbar(kb1_cost_df["Tr"], kb1_cost_df["costheta"], yerr=kb1_cost_df["costheta_se"], fmt='.', color=cmap(0), label=r'$k_{b}=1$')
ax[1].errorbar(kb2_cost_df["Tr"], kb2_cost_df["costheta"], yerr=kb2_cost_df["costheta_se"], fmt='.', color=cmap(1), label=r'$k_{b}=2$')
ax[1].errorbar(kb4_cost_df["Tr"], kb4_cost_df["costheta"], yerr=kb4_cost_df["costheta_se"], fmt='.', color=cmap(2), label=r'$k_{b}=4$')
ax[1].errorbar(kb8_cost_df["Tr"], kb8_cost_df["costheta"], yerr=kb8_cost_df["costheta_se"], fmt='.', color=cmap(3), label=r'$k_{b}=8$')
ax[1].legend(loc='upper right', fontsize=labelsize, frameon=False, handlelength=1.8, handletextpad=0.3)
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
