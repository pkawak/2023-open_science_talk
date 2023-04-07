#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
created on Tue June 14 08:41:00 2021

@author: pierrekawak
"""

import sys
import numpy as np
import matplotlib.pyplot as plt
import random

Nc    = 125
Nb    = 10
sigma = 1.0
label_prefix = r'$\phi=$'

names = ["T", "Em", "Cv", "q6", "P2", "n6", "r2e", "r2g", "sms"]

WL_A_file = "../Lx11.000_kb1.00_WLMC_results.out"
WL_B_file = "../Lx11.436_kb1.00_WLMC_results.out"
WL_C_file = "../Lx13.000_kb1.00_WLMC_results.out"
WL_D_file = "../Lx15.000_kb1.00_WLMC_results.out"
Lx_A      = 11.000
Lx_B      = 11.436
Lx_C      = 13.000
Lx_D      = 15.000
phi_A     = np.round(Nc*Nb*sigma**3/Lx_A**3*np.pi/6, 3)
phi_B     = np.round(Nc*Nb*sigma**3/Lx_B**3*np.pi/6, 3)
phi_C     = np.round(Nc*Nb*sigma**3/Lx_C**3*np.pi/6, 3)
phi_D     = np.round(Nc*Nb*sigma**3/Lx_D**3*np.pi/6, 3)
kb_A      = 1.00
kb_B      = 1.00
kb_C      = 1.00
kb_D      = 1.00

import pandas as pd
WL_A_df    = pd.read_csv(WL_A_file, index_col=False, delimiter=' ', names=names)
WL_B_df    = pd.read_csv(WL_B_file, index_col=False, delimiter=' ', names=names)
WL_C_df    = pd.read_csv(WL_C_file, index_col=False, delimiter=' ', names=names)
WL_D_df    = pd.read_csv(WL_D_file, index_col=False, delimiter=' ', names=names)

WL_A_df['Tr']    = WL_A_df['T']/kb_A
WL_B_df['Tr']    = WL_B_df['T']/kb_B
WL_C_df['Tr']    = WL_C_df['T']/kb_C
WL_D_df['Tr']    = WL_D_df['T']/kb_D

# filter all values under 0.01
WL_A_df = WL_A_df.loc[WL_A_df['Tr'] > 0.02]
WL_B_df = WL_B_df.loc[WL_B_df['Tr'] > 0.02]
WL_C_df = WL_C_df.loc[WL_C_df['Tr'] > 0.02]
WL_D_df = WL_D_df.loc[WL_D_df['Tr'] > 0.02]

WL_A_df = WL_A_df.loc[WL_A_df['Tr'] < 0.2]
WL_B_df = WL_B_df.loc[WL_B_df['Tr'] < 0.2]
WL_C_df = WL_C_df.loc[WL_C_df['Tr'] < 0.2]
WL_D_df = WL_D_df.loc[WL_D_df['Tr'] < 0.2]

fig, ax = plt.subplots(4, 1, sharex=True, figsize=(3.25,2.0*4), constrained_layout=True)

multiplier = 1/Nc/Nb
ax[0].plot(WL_A_df["Tr"], WL_A_df["Em"]/kb_A*multiplier, label=label_prefix+str(phi_A))
ax[0].plot(WL_B_df["Tr"], WL_B_df["Em"]/kb_B*multiplier, label=label_prefix+str(phi_B))
ax[0].plot(WL_C_df["Tr"], WL_C_df["Em"]/kb_C*multiplier, label=label_prefix+str(phi_C))
ax[0].plot(WL_D_df["Tr"], WL_D_df["Em"]/kb_D*multiplier, label=label_prefix+str(phi_D))
ax[0].set_ylabel(r"$\left<U\right>/Nk_{b}$", fontsize=10, labelpad=7)
ax[0].tick_params(axis='both', labelsize=8)
ax[0].legend(loc='best', fontsize=8)#, prop={'size': 6})

ax[1].plot(WL_A_df["Tr"], WL_A_df["P2"], label=label_prefix+str(phi_A))
ax[1].plot(WL_B_df["Tr"], WL_B_df["P2"], label=label_prefix+str(phi_B))
ax[1].plot(WL_C_df["Tr"], WL_C_df["P2"], label=label_prefix+str(phi_C))
ax[1].plot(WL_D_df["Tr"], WL_D_df["P2"], label=label_prefix+str(phi_D))
ax[1].set_ylabel(r"$P_{2}$", fontsize=10, labelpad=9)
ax[1].tick_params(axis='both', labelsize=8)
#ax[1].set_ylim(0.2,1)

ax[2].plot(WL_A_df["Tr"], WL_A_df["n6"], label=label_prefix+str(phi_A))
ax[2].plot(WL_B_df["Tr"], WL_B_df["n6"], label=label_prefix+str(phi_B))
ax[2].plot(WL_C_df["Tr"], WL_C_df["n6"], label=label_prefix+str(phi_C))
ax[2].plot(WL_D_df["Tr"], WL_D_df["n6"], label=label_prefix+str(phi_D))
ax[2].set_ylabel(r"$n_{Q_{6}}$", fontsize=10, labelpad=9.5)
ax[2].tick_params(axis='both', labelsize=8)
ax[2].set_ylim(0,1)

multiplier = 1/Nc #/Nb
ax[3].plot(WL_A_df["Tr"], WL_A_df["Cv"]*multiplier, label=label_prefix+str(phi_A))
ax[3].plot(WL_B_df["Tr"], WL_B_df["Cv"]*multiplier, label=label_prefix+str(phi_B))
ax[3].plot(WL_C_df["Tr"], WL_C_df["Cv"]*multiplier, label=label_prefix+str(phi_C))
ax[3].plot(WL_D_df["Tr"], WL_D_df["Cv"]*multiplier, label=label_prefix+str(phi_D))
ax[3].set_ylabel(r"$C_{V}/kN_{c}$", fontsize=10, labelpad=7)
ax[3].set_xlabel(r"$T_{r}$", fontsize=10, labelpad=5)
ax[3].tick_params(axis='both', labelsize=8)
ax[3].set_yscale('log')
from matplotlib.ticker import ScalarFormatter, NullFormatter
#ax[3].yaxis.set_major_formatter(ScalarFormatter())
ax[3].yaxis.set_minor_formatter(NullFormatter())
ax[3].set_ylim(10,100)

#plt.subplots_adjust(left=0.168, top=0.999, bottom=0.05, right=0.998, hspace=0.1)

import os
basename = os.path.splitext(__file__)[0]
plt.savefig(basename+".pdf")
