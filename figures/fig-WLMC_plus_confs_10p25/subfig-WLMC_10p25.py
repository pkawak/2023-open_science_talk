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
import pandas as pd

maxT = 0.5
minT = 0.0
WL_file_name      = "WLMC_results.out" 
WL_data = np.loadtxt(WL_file_name, usecols=(0,2,3,5,6))
WL_df = pd.DataFrame({'T': WL_data[:,0],
                      'Em': WL_data[:,1],
                      'Cv': WL_data[:,2],
                      'q6': WL_data[:,3],
                      'P2': WL_data[:,4]
                      })
WL_df = WL_df[WL_df['T'] < maxT]
WL_df = WL_df[WL_df['T'] > minT]

fig, ax = plt.subplots(3, 1, sharex=True, figsize=(3.0,0.95*3))

ax[0].plot(WL_df["T"], WL_df["Em"], color='blue', label='WLMC')
ax[0].set_ylabel(r"Energy ($U_{tot}/\epsilon$)", fontsize=8, labelpad=4.1)
ax[0].tick_params(axis='both', labelsize=8)
ax[0].axvline(x=0.2907, color='b', alpha=0.5, ls=':')

ax[1].plot(WL_df["T"], WL_df["P2"], color='blue', label='WLMC')
ax[1].set_ylim(0,1)
ax[1].set_yticks([.2,.4,.6,.8])
ax[1].set_ylabel("Nematic""\n"r"Order ($P_{2}$)", fontsize=8, labelpad=7)
ax[1].tick_params(axis='both', labelsize=8)
ax[1].axvline(x=0.2907, color='b', alpha=0.5, ls=':')

ax[2].plot(WL_df["T"], WL_df["q6"], color='blue', label='WLMC')
ax[2].set_ylabel(r"Crystallinity ($Q_{6}$)", fontsize=8, labelpad=6)
ax[2].tick_params(axis='both', labelsize=8)
ax[2].axvline(x=0.2907, color='b', alpha=0.5, ls=':')
ax[2].set_xlabel(r"$T_{r}$", fontsize=8, labelpad=5)
plt.subplots_adjust(left=0.21, top=0.99, bottom=0.13, right=0.995, hspace=0.1)
plt.savefig("subfig-WLMC_10.25.pdf")
