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
step_lp_file_name   = "step_avg-lpvsT.out"
step_cost_file_name = "step_avg-cos_theta_backbone.out"
harm_lp_file_name   = "harm_avg-lpvsT.out"
harm_cost_file_name = "harm_avg-cos_theta_backbone.out"
filter_by = { "kb": 1.0 } # , "costheta_s": 0.9 }

# get lp data
step_lp_df = pd.read_csv(step_lp_file_name, index_col=False, delimiter=" ", keep_default_na=False, na_values=['_'])
step_lp_df['costheta_s'] = np.round(np.cos(step_lp_df['theta_s']),3)
step_lp_df = step_lp_df.loc[(step_lp_df[list(filter_by)] == pd.Series(filter_by)).all(axis=1)]

harm_lp_df = pd.read_csv(harm_lp_file_name, index_col=False, delimiter=" ", keep_default_na=False, na_values=['_'])
harm_lp_df = harm_lp_df.loc[(harm_lp_df[list(filter_by)] == pd.Series(filter_by)).all(axis=1)]

# get cos_theta data
step_cost_df = pd.read_csv(step_cost_file_name, index_col=False, delimiter=" ", keep_default_na=False, na_values=['_'])
step_cost_df['costheta_s'] = np.round(np.cos(step_cost_df['theta_s']),3)
step_cost_df = step_cost_df.loc[(step_cost_df[list(filter_by)] == pd.Series(filter_by)).all(axis=1)]

harm_cost_df = pd.read_csv(harm_cost_file_name, index_col=False, delimiter=" ", keep_default_na=False, na_values=['_'])
harm_cost_df = harm_cost_df.loc[(harm_cost_df[list(filter_by)] == pd.Series(filter_by)).all(axis=1)]

# filter out stuff with T > 1
step_lp_df = step_lp_df.loc[step_lp_df['T'] < 1.01]
step_cost_df = step_cost_df.loc[step_cost_df['T'] < 1.01]
harm_lp_df = harm_lp_df.loc[harm_lp_df['T'] < 1.01]
harm_cost_df = harm_cost_df.loc[harm_cost_df['T'] < 1.01]

figsize   = (2.5,3.6)
fontsize  = 10
labelsize = 8
fig, ax = plt.subplots(2, figsize=figsize, sharex=True, constrained_layout=True)

#ax[0].set_xlabel(r"$T_{r}$", fontsize=fontsize, labelpad=6)
ax[0].set_ylabel(r"$l_{p}/\sigma$", fontsize=fontsize, labelpad=-4)
ax[0].tick_params(axis='both', labelsize=labelsize)
ax[0].errorbar(step_lp_df.loc[step_lp_df['costheta_s'] == 0.9]["Tr"], step_lp_df.loc[step_lp_df['costheta_s'] == 0.9]["lp"], yerr=step_lp_df.loc[step_lp_df['costheta_s'] == 0.9]["lp_se"], color='m')
ax[0].errorbar(step_lp_df.loc[step_lp_df['costheta_s'] == 0.8]["Tr"], step_lp_df.loc[step_lp_df['costheta_s'] == 0.8]["lp"], yerr=step_lp_df.loc[step_lp_df['costheta_s'] == 0.8]["lp_se"], color='r')
ax[0].errorbar(step_lp_df.loc[step_lp_df['costheta_s'] == 0.985]["Tr"], step_lp_df.loc[step_lp_df['costheta_s'] == 0.985]["lp"], yerr=step_lp_df.loc[step_lp_df['costheta_s'] == 0.985]["lp_se"], color='g')
ax[0].errorbar(harm_lp_df["Tr"], harm_lp_df["lp"], yerr=harm_lp_df["lp_se"], fmt='.', color='b')
ax[0].set_yscale('log')
#ax[0].set_xscale('log')
#ax[0].set_yticks([1,100])

ax[1].set_xlabel(r"$T_{r}$", fontsize=fontsize, labelpad=6)
ax[1].set_ylabel(r"$\cos(\theta)$", fontsize=fontsize, labelpad=0)
ax[1].errorbar(step_cost_df.loc[step_cost_df['costheta_s'] == 0.9]["Tr"], step_cost_df.loc[step_cost_df['costheta_s'] == 0.9]["costheta"], yerr=step_cost_df.loc[step_cost_df['costheta_s'] == 0.9]["costheta_se"], color='m', label=r'$\cos\theta_{s}=0.9$')
ax[1].errorbar(step_cost_df.loc[step_cost_df['costheta_s'] == 0.8]["Tr"], step_cost_df.loc[step_cost_df['costheta_s'] == 0.8]["costheta"], yerr=step_cost_df.loc[step_cost_df['costheta_s'] == 0.8]["costheta_se"], color='r', label=r'$\cos\theta_{s}=0.8$')
ax[1].errorbar(step_cost_df.loc[step_cost_df['costheta_s'] == 0.985]["Tr"], step_cost_df.loc[step_cost_df['costheta_s'] == 0.985]["costheta"], yerr=step_cost_df.loc[step_cost_df['costheta_s'] == 0.985]["costheta_se"], color='g', label=r'$\cos\theta_{s}=0.985$')
ax[1].errorbar(harm_cost_df["Tr"], harm_cost_df["costheta"], yerr=harm_cost_df["costheta_se"], fmt='.', color='b', label='harmonic')
ax[1].legend(loc='lower left', fontsize=labelsize, frameon=False, handlelength=1.8, handletextpad=0.3)
#ax[1].hlines(0.9, 0, 1, ls='--', color='k', label=r'$\cos\theta_{s}$')
ax[1].set_xscale('log')
#ax[1].set_xscale('log')
ax[1].tick_params(axis='both', labelsize=labelsize)
#ax[1].set_yticks([0.3,1.0])
from matplotlib.ticker import ScalarFormatter, NullFormatter
ax[1].yaxis.set_major_formatter(ScalarFormatter())
ax[1].yaxis.set_minor_formatter(NullFormatter())
#ax[1].xaxis.set_major_formatter(ScalarFormatter())

plt.savefig("fig-lp_vs_T_cosT.pdf")
plt.close()
#if big:
#  plt.subplots_adjust(left=0.147, top=0.995, bottom=0.156, right=0.998)
#else:
#  plt.subplots_adjust(left=0.21, top=0.99, bottom=0.23, right=0.985)
figsize   = (2.5,5.4)
fig, ax = plt.subplots(3, figsize=figsize, sharex=True, constrained_layout=True)

Nc = 125
Nb = 10
step_lp_df['Em_step'] = [ -Nc*(Nb-2)*kbi if costi > costsi else 0 for kbi, costi, costsi in zip(step_lp_df['kb'], step_cost_df['costheta'], step_lp_df['costheta_s']) ]
step_lp_df['Em_harm'] = [ Nc*(Nb-2)*kbi*(1-costi) for kbi, costi in zip(step_lp_df['kb'], step_cost_df['costheta']) ]
harm_lp_df['Em_step'] = [ -Nc*(Nb-2)*kbi if costi > 0.9 else 0 for kbi, costi in zip(harm_lp_df['kb'], harm_cost_df['costheta']) ]
harm_lp_df['Em_harm'] = [ Nc*(Nb-2)*kbi*(1-costi) for kbi, costi in zip(harm_lp_df['kb'], harm_cost_df['costheta']) ]

ax[0].set_ylabel(r"$l_{p}/\sigma$", fontsize=fontsize, labelpad=-4)
ax[0].tick_params(axis='both', labelsize=labelsize)
ax[0].errorbar(step_lp_df.loc[step_lp_df['costheta_s'] == 0.9]["Tr"], step_lp_df.loc[step_lp_df['costheta_s'] == 0.9]["lp"], yerr=step_lp_df.loc[step_lp_df['costheta_s'] == 0.9]["lp_se"], color='m')
ax[0].errorbar(harm_lp_df["Tr"], harm_lp_df["lp"], yerr=harm_lp_df["lp_se"], fmt='.', color='b')
ax[0].set_yscale('log')

ax[1].set_xlabel(r"$T_{r}$", fontsize=fontsize, labelpad=6)
ax[1].set_ylabel(r"$\cos(\theta)$", fontsize=fontsize, labelpad=0)
ax[1].errorbar(step_cost_df.loc[step_cost_df['costheta_s'] == 0.9]["Tr"], step_cost_df.loc[step_cost_df['costheta_s'] == 0.9]["costheta"], yerr=step_cost_df.loc[step_cost_df['costheta_s'] == 0.9]["costheta_se"], color='m', label=r'$\cos\theta_{s}=0.9$')
ax[1].errorbar(harm_cost_df["Tr"], harm_cost_df["costheta"], yerr=harm_cost_df["costheta_se"], fmt='.', color='b', label='harmonic')
ax[1].legend(loc='lower left', fontsize=labelsize, frameon=False, handlelength=1.8, handletextpad=0.3)
ax[1].set_xscale('log')
ax[1].tick_params(axis='both', labelsize=labelsize)
from matplotlib.ticker import ScalarFormatter, NullFormatter
ax[1].yaxis.set_major_formatter(ScalarFormatter())
ax[1].yaxis.set_minor_formatter(NullFormatter())

ax[2].set_ylabel(r"$U/\epsilon$", fontsize=fontsize, labelpad=-4)
ax[2].tick_params(axis='both', labelsize=labelsize)
ax[2].scatter(step_lp_df.loc[step_lp_df['costheta_s'] == 0.9]["Tr"], 1000+step_lp_df.loc[step_lp_df['costheta_s'] == 0.9]["Em_step"], color='m', marker='+', label=r'$U_{\mathrm{step}}(\theta_{\mathrm{step}})+1000$')
ax[2].scatter(step_lp_df.loc[step_lp_df['costheta_s'] == 0.9]["Tr"], step_lp_df.loc[step_lp_df['costheta_s'] == 0.9]["Em_harm"], color='r', marker='+', label=r'$U_{\mathrm{harm}}(\theta_{\mathrm{step}})$')
ax[2].scatter(harm_lp_df["Tr"], 1000+harm_lp_df["Em_step"], color='g', s=5, label=r'$U_{\mathrm{step}}(\theta_{\mathrm{harm}})+1000$')
ax[2].scatter(harm_lp_df["Tr"], harm_lp_df["Em_harm"], color='b', s=5, label=r'$U_{\mathrm{harm}}(\theta_{\mathrm{harm}})$')
ax[2].legend(loc='best', fontsize=labelsize, frameon=False, handlelength=1.8,handletextpad=0.3)
#ax[2].set_yscale('log')

plt.savefig("fig-lp_vs_T.pdf")
plt.close()
