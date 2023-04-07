#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
created on Tue June 14 08:41:00 2021

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
WL_file_name_10p25 = "WLMC_data/Lx10.25_ext_canon_distro.out"
WL_file_name_10p75 = "WLMC_data/Lx10.75_ext_canon_distro.out"

WL_data_10p25 = np.loadtxt(WL_file_name_10p25, usecols=(0,2,3,5,6))
WL_df_10p25   = pd.DataFrame({'T': WL_data_10p25[:,0],
                             'Em': WL_data_10p25[:,1],
                             'Cv': WL_data_10p25[:,2],
                             'q6': WL_data_10p25[:,3],
                             'P2': WL_data_10p25[:,4]
                             })
WL_df_10p25    = WL_df_10p25[WL_df_10p25['T'] > minT]
WL_df_10p25    = WL_df_10p25[WL_df_10p25['T'] < maxT]

WL_data_10p75  = np.loadtxt(WL_file_name_10p75, usecols=(0,2,3,5,6))
WL_df_10p75    = pd.DataFrame({'T': WL_data_10p75[:,0],
                              'Em': WL_data_10p75[:,1],
                              'Cv': WL_data_10p75[:,2],
                              'q6': WL_data_10p75[:,3],
                              'P2': WL_data_10p75[:,4]
                              })
WL_df_10p75    = WL_df_10p75[WL_df_10p75['T'] > minT]
WL_df_10p75    = WL_df_10p75[WL_df_10p75['T'] < maxT]

melt_loc   = WL_df_10p25.loc[(WL_df_10p25['T']-0.45).abs().argsort()[0]]
melt_color = 'r'
nema_loc   = WL_df_10p75.loc[(WL_df_10p75['T']-0.001).abs().argsort()[0]]
nema_color = 'g'
crys_loc   = WL_df_10p25.loc[(WL_df_10p25['T']-0.001).abs().argsort()[0]]
crys_color = 'b'

fig, ax = plt.subplots(2, 2, sharex=True, figsize=(3.6,2.75))

ax[0,0].plot(WL_df_10p25["T"], WL_df_10p25["Em"], c = 'dimgray', label=r'$\phi=0.438$')
ax[0,0].plot(WL_df_10p75["T"], WL_df_10p75["Em"], c = 'dimgray', ls = '--', label=r'$\phi=0.379$')
ax[0,0].set_ylabel(r"Energy ($U_{tot}/\epsilon$)", fontsize=7.5, labelpad=4.0)
ax[0,0].tick_params(axis='both', labelsize=6)
ax[0,0].scatter(melt_loc['T'], melt_loc['Em'], s=16, c = melt_color)
ax[0,0].scatter(nema_loc['T'], nema_loc['Em'], s=16, c = nema_color)
ax[0,0].scatter(crys_loc['T'], crys_loc['Em'], s=16, c = crys_color)

ax[0,1].plot(WL_df_10p25["T"], WL_df_10p25["P2"], c = 'dimgray', label=r'$\phi=0.438$')
ax[0,1].plot(WL_df_10p75["T"], WL_df_10p75["P2"], c = 'dimgray', ls = '--', label=r'$\phi=0.379$')
ax[0,1].set_ylabel("Nematic""\n"r"Order ($P_{2}$)", fontsize=7.5, labelpad=3)
ax[0,1].tick_params(axis='both', labelsize=6)
ax[0,1].set_yticks([.2, .4, .6, .8])
ax[0,1].scatter(melt_loc['T'], melt_loc['P2'], s=16, c = melt_color)
ax[0,1].scatter(nema_loc['T'], nema_loc['P2'], s=16, c = nema_color)
ax[0,1].scatter(crys_loc['T'], crys_loc['P2'], s=16, c = crys_color)

ax[1,0].plot(WL_df_10p25["T"], WL_df_10p25["q6"], c = 'dimgray', label=r'$\phi=0.438$')
ax[1,0].plot(WL_df_10p75["T"], WL_df_10p75["q6"], c = 'dimgray', ls = '--', label=r'$\phi=0.379$')
ax[1,0].set_ylabel(r"Crystallinity ($Q_{6}$)", fontsize=7.5, labelpad=5)
ax[1,0].set_xlabel(r"$T_{r}$", fontsize=7.5, labelpad=4)
ax[1,0].tick_params(axis='both', labelsize=6)
ax[1,0].legend(loc='best', fontsize=7)
ax[1,0].scatter(melt_loc['T'], melt_loc['q6'], s=16, c = melt_color)
ax[1,0].scatter(nema_loc['T'], nema_loc['q6'], s=16, c = nema_color)
ax[1,0].scatter(crys_loc['T'], crys_loc['q6'], s=16, c = crys_color)

ax[1,1].plot(WL_df_10p25["T"], WL_df_10p25["Cv"], c = 'dimgray', label=r'$\phi=0.438$')
ax[1,1].plot(WL_df_10p75["T"], WL_df_10p75["Cv"], c = 'dimgray', ls = '--', label=r'$\phi=0.379$')
ax[1,1].set_ylabel(r"$C_{V}$", fontsize=7.5, labelpad=5)
ax[1,1].set_xlabel(r"$T_{r}$", fontsize=7.5, labelpad=4)
ax[1,1].tick_params(axis='both', labelsize=6)
ax[1,1].set_yscale('log')
ax[1,1].scatter(melt_loc['T'], melt_loc['Cv'], s=16, c = melt_color)
ax[1,1].scatter(nema_loc['T'], nema_loc['Cv'], s=16, c = nema_color)
ax[1,1].scatter(crys_loc['T'], crys_loc['Cv'], s=16, c = crys_color)
plt.subplots_adjust(left=0.14, top=0.997, bottom=0.12, right=0.995, hspace=0.1, wspace=0.41)
plt.savefig("subfig-WLMC_10.25_10.75.pdf")
