#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
created on Tue June 03 08:41:00 2022

@author: pierrekawak
"""

import sys
import numpy as np
import matplotlib.pyplot as plt
import random
import sys
import pandas as pd

cryst_file_name      = "SandP_10.00_WLMC_results.out" 
nemat_file_name      = "SandP_10.50_WLMC_results.out" 

cryst_data = np.loadtxt(cryst_file_name, usecols=(0,2,3,5,6))
cryst_df   = pd.DataFrame({ 'T': cryst_data[:,0], 'Em': cryst_data[:,1], 'Cv': cryst_data[:,2], 'q6': cryst_data[:,3], 'P2': cryst_data[:,4] })
nemat_data = np.loadtxt(nemat_file_name, usecols=(0,2,3,5,6))
nemat_df   = pd.DataFrame({ 'T': nemat_data[:,0], 'Em': nemat_data[:,1], 'Cv': nemat_data[:,2], 'q6': nemat_data[:,3], 'P2': nemat_data[:,4] })

fig, ax = plt.subplots(2, 1, sharex=True, figsize=(4.00,2.00*2))
ax[0].plot(cryst_df["T"], cryst_df["Em"], color='blue', label='IC')
ax[0].plot(nemat_df["T"], nemat_df["Em"], color='red' , label='IN')
ax[0].set_ylabel(r"$U/\epsilon$", fontsize=12, labelpad=7.0)
ax[0].tick_params(axis='both', labelsize=10, pad=0)
ax[0].axvline(x=0.3715, color='b', alpha=0.7, ls=':', label=r'$T_{IC}$')
ax[0].axvline(x=0.248 , color='r', alpha=0.7, ls=':', label=r'$T_{IN}$')
ax[0].legend(loc='best', fontsize=12)#, prop={'size': 6})
ax[0].text(-0.23, 1.0, 'a)', fontsize=12, fontname='dejavusans', transform = ax[0].transAxes)
ax[0].set_xticks([])
ax[0].set_yticks([])

ax[1].plot(cryst_df["T"], cryst_df["Cv"]/90, color='blue', label='IC')
ax[1].plot(nemat_df["T"], nemat_df["Cv"]/90, color='red' , label='IN')
ax[1].set_yscale('log')
ax[1].set_ylabel(r"$C_{V}/k$", fontsize=12, labelpad=4.1)
ax[1].tick_params(axis='both', labelsize=10, pad=0)
ax[1].set_xticks([])
ax[1].set_yticks([])
ax[1].axvline(x=0.3715, color='b', alpha=0.7, ls=':', label=r'$T_{IC}$')
ax[1].axvline(x=0.248 , color='r', alpha=0.7, ls=':', label=r'$T_{IN}$')
ax[1].set_xlabel(r"$kT/\epsilon$", fontsize=12, labelpad=5)
ax[1].text(-0.23, 1.0, 'b)', fontsize=12, fontname='dejavusans', transform = ax[1].transAxes)

ax[1].set_xlim(0.2, 0.45)
ax[1].set_ylim(0.5, 20**3)
plt.subplots_adjust(left=0.08, top=0.998, bottom=0.062, right=0.998, hspace=0.01)
plt.savefig("fig-UandCv.pdf")
