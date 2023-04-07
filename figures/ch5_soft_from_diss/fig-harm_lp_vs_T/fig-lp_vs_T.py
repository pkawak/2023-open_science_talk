#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
created on Sat May 22 08:41:00 2021

@author: pierrekawak
"""

lp_file_name   = "avg-lpvsT.out"
cost_file_name = "avg-cos_theta_backbone.out"
filter_by = { "kb": 1.0 }

import pandas as pd

#get lp data
lp_df = pd.read_csv(lp_file_name, index_col=False, delimiter=" ", keep_default_na=False, na_values=['_'])
lp_df = lp_df.loc[(lp_df[list(filter_by)] == pd.Series(filter_by)).all(axis=1)]

#get cos_theta data
cost_df = pd.read_csv(cost_file_name, index_col=False, delimiter=" ", keep_default_na=False, na_values=['_'])
cost_df = cost_df.loc[(cost_df[list(filter_by)] == pd.Series(filter_by)).all(axis=1)]

import matplotlib.pyplot as plt
#figsize   = (4,6)
#fontsize  = 12
#labelsize = 10
figsize   = (2.5,3.6)
fontsize  = 10
labelsize = 8

fig, ax = plt.subplots(2, figsize=figsize, sharex=True, constrained_layout=True)

#ax[0].set_xlabel(r"$T_{r}$", fontsize=fontsize, labelpad=6)
ax[0].set_ylabel(r"$l_{p}/\sigma$", fontsize=fontsize, labelpad=-4)
ax[0].tick_params(axis='both', labelsize=labelsize)
ax[0].errorbar(lp_df["Tr"], lp_df["lp"], yerr=lp_df["lp_se"], fmt='.', color='m')
ax[0].set_yscale('log')
#ax[0].set_xscale('log')
ax[0].set_yticks([1,100])

ax[1].set_xlabel(r"$T_{r}$", fontsize=fontsize, labelpad=6)
ax[1].set_ylabel(r"$\cos(\theta)$", fontsize=fontsize, labelpad=0)
ax[1].errorbar(cost_df["Tr"], cost_df["costheta"], yerr=cost_df["costheta_se"], fmt='.', color='m')
#ax[1].set_yscale('log')
#ax[1].set_xscale('log')
ax[1].tick_params(axis='both', labelsize=labelsize)
ax[1].set_yticks([0.3,1.0])
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
