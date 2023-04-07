#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
created on Tue June 16 08:41:00 2020

@author: pierrekawak
"""

import sys
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d, Axes3D
import random
import sys

melting_file_name = "MCMC_results.out" 
WL_file_name      = "WLMC_results.out" 

comment_lines = 1
col1 = 1
data = np.loadtxt(melting_file_name, skiprows=comment_lines, usecols=(1,2,3,4,5,6,8))

import pandas as pd

#create DataFrame
df = pd.DataFrame({'T': data[:,0],
                   'time': data[:,1],
                   'Em': data[:,2],
                   'Es': data[:,3],
                   'conv': data[:,4],
                   'q6': data[:,5],
                   'P2': data[:,6]
                   })
res = df.groupby(['T']).mean().reset_index()
sem = df.groupby(['T']).sem().reset_index()

WL_data = np.loadtxt(WL_file_name, usecols=(0,2,3,5,6))

WL_df = pd.DataFrame({'T': WL_data[:,0],
                      'Em': WL_data[:,1],
                      'Cv': WL_data[:,2],
                      'q6': WL_data[:,3],
                      'P2': WL_data[:,4]
                      })

fig, ax = plt.subplots(3, 1, sharex=True, figsize=(3.25,2.0*3))

ax[0].errorbar(res["T"], res["Em"], yerr=sem["Em"], ls='none', color='red')
ax[0].scatter(res["T"], res["Em"], color='red', s=5, label='MCMC')
ax[0].plot(WL_df["T"], WL_df["Em"], color='blue', label='WLMC')
ax[0].set_ylabel(r"$U/\epsilon$", fontsize=10, labelpad=4.1)
ax[0].tick_params(axis='both', labelsize=8)
ax[0].axvline(x=0.2907, color='b', alpha=0.5, ls=':', label=r'$T_{r}=0.291$')
ax[0].legend(loc='best', fontsize=10)#, prop={'size': 6})
ax[0].text(-0.23, 1.0, '(a)', fontsize=12, fontname='dejavusans', transform = ax[0].transAxes)

ax[1].errorbar(res["T"], res["P2"], yerr=sem["q6"], ls='none', color='red')
ax[1].scatter(res["T"], res["P2"], color='red', s=5, label='MCMC')
ax[1].plot(WL_df["T"], WL_df["P2"], color='blue', label='WLMC')
ax[1].set_ylim(0,1)
ax[1].set_yticks([.2,.4,.6,.8])
ax[1].set_ylabel(r"$P_{2}$", fontsize=10, labelpad=11)
ax[1].tick_params(axis='both', labelsize=8)
ax[1].axvline(x=0.2907, color='b', alpha=0.5, ls=':')
ax[1].text(-0.23, 1.0, '(b)', fontsize=12, fontname='dejavusans', transform = ax[1].transAxes)

ax[2].errorbar(res["T"], res["q6"], yerr=sem["q6"], ls='none', color='red')
ax[2].scatter(res["T"], res["q6"], color='red', s=5, label='MCMC')
ax[2].plot(WL_df["T"], WL_df["q6"], color='blue', label='WLMC')
ax[2].set_ylabel(r"$Q_{6}$", fontsize=10, labelpad=6)
ax[2].tick_params(axis='both', labelsize=8)
ax[2].axvline(x=0.2907, color='b', alpha=0.5, ls=':')
ax[2].set_xlabel(r"$T_{r}$", fontsize=10, labelpad=5)
ax[2].text(-0.23, 1.0, '(c)', fontsize=12, fontname='dejavusans', transform = ax[2].transAxes)
plt.subplots_adjust(left=0.185, top=0.975, bottom=0.07, right=0.995, hspace=0.1)
plt.savefig("fig-WLMC_plus_MCMC_10.25.pdf")
