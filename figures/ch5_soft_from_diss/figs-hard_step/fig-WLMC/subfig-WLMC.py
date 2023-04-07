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
import pandas as pd
import json

Nc    = 125
Nb    = 10
sigma = 1

WL_A_file_name   = "like10.00_ext_canon_distro.out"
WL_B_file_name   = "like10.25_ext_canon_distro.out"
WL_C_file_name   = "like10.30_ext_canon_distro.out"
WL_D_file_name   = "like10.33_ext_canon_distro.out"
WL_E_file_name   = "like10.50_ext_canon_distro.out"

#WL_A_file_params = "like10.00_params.json"
#WL_B_file_params = "like10.25_params.json"
#WL_C_file_params = "like10.30_params.json"
#WL_D_file_params = "like10.33_params.json"
#WL_E_file_params = "like10.50_params.json"
#
usecols          = (0,1,2,3,4,5)
names            = ['T', 'Em', 'Cv', 'q6', 'P2', 'n6']

WL_A_df          = pd.read_csv(WL_A_file_name, index_col=False, delimiter=' ', 
                                   usecols=usecols, names=names)
WL_B_df          = pd.read_csv(WL_B_file_name, index_col=False, delimiter=' ', 
                                   usecols=usecols, names=names)
WL_C_df          = pd.read_csv(WL_C_file_name, index_col=False, delimiter=' ', 
                                   usecols=usecols, names=names)
WL_D_df          = pd.read_csv(WL_D_file_name, index_col=False, delimiter=' ', 
                                   usecols=usecols, names=names)
WL_E_df          = pd.read_csv(WL_E_file_name, index_col=False, delimiter=' ', 
                                   usecols=usecols, names=names)

Lx_A             = 11.157216
Lx_B             = 11.436146
Lx_C             = 11.491932
Lx_D             = 11.525404
Lx_E             = 11.715077

phi_A            = np.round(Nc*Nb*sigma**3/Lx_A**3*np.pi/6, 3)
phi_B            = np.round(Nc*Nb*sigma**3/Lx_B**3*np.pi/6, 3)
phi_C            = np.round(Nc*Nb*sigma**3/Lx_C**3*np.pi/6, 3)
phi_D            = np.round(Nc*Nb*sigma**3/Lx_D**3*np.pi/6, 3)
phi_E            = np.round(Nc*Nb*sigma**3/Lx_E**3*np.pi/6, 3)

fig, ax = plt.subplots(4, 1, sharex=True, figsize=(3.25,2.0*4))#, constrained_layout=True)

multiplier = 1/Nc/(Nb-2)
ax[0].plot(WL_A_df["T"], WL_A_df["Em"]*multiplier, label=r'$\phi=$'+str(phi_A))
ax[0].plot(WL_B_df["T"], WL_B_df["Em"]*multiplier, label=r'$\phi=$'+str(phi_B))
ax[0].plot(WL_C_df["T"], WL_C_df["Em"]*multiplier, label=r'$\phi=$'+str(phi_C))
ax[0].plot(WL_D_df["T"], WL_D_df["Em"]*multiplier, label=r'$\phi=$'+str(phi_D))
ax[0].plot(WL_E_df["T"], WL_E_df["Em"]*multiplier, label=r'$\phi=$'+str(phi_E))
ax[0].set_ylabel(r"$\left<U\right>/N_{c}(N_{b}-2)$", fontsize=10, labelpad=7)
ax[0].tick_params(axis='both', labelsize=8)
ax[0].legend(loc='best', fontsize=8)#, prop={'size': 6})

ax[1].plot(WL_A_df["T"], WL_A_df["P2"], label=r'$\phi=$'+str(phi_A))
ax[1].plot(WL_B_df["T"], WL_B_df["P2"], label=r'$\phi=$'+str(phi_B))
ax[1].plot(WL_C_df["T"], WL_C_df["P2"], label=r'$\phi=$'+str(phi_C))
ax[1].plot(WL_D_df["T"], WL_D_df["P2"], label=r'$\phi=$'+str(phi_D))
ax[1].plot(WL_E_df["T"], WL_E_df["P2"], label=r'$\phi=$'+str(phi_E))
ax[1].set_ylabel(r"$P_{2}$", fontsize=10, labelpad=9)
ax[1].tick_params(axis='both', labelsize=8)

ax[2].plot(WL_A_df["T"], WL_A_df["n6"], label=r'$\phi=$'+str(phi_A))
ax[2].plot(WL_B_df["T"], WL_B_df["n6"], label=r'$\phi=$'+str(phi_B))
ax[2].plot(WL_C_df["T"], WL_C_df["n6"], label=r'$\phi=$'+str(phi_C))
ax[2].plot(WL_D_df["T"], WL_D_df["n6"], label=r'$\phi=$'+str(phi_D))
ax[2].plot(WL_E_df["T"], WL_E_df["n6"], label=r'$\phi=$'+str(phi_E))
ax[2].set_ylabel(r"$f_{\mathrm{cryst}}$", fontsize=10, labelpad=9.5)
ax[2].tick_params(axis='both', labelsize=8)

multiplier = 1/Nc #/Nb
ax[3].plot(WL_A_df["T"], WL_A_df["Cv"]*multiplier, label=r'$\phi=$'+str(phi_A))
ax[3].plot(WL_B_df["T"], WL_B_df["Cv"]*multiplier, label=r'$\phi=$'+str(phi_B))
ax[3].plot(WL_C_df["T"], WL_C_df["Cv"]*multiplier, label=r'$\phi=$'+str(phi_C))
ax[3].plot(WL_D_df["T"], WL_D_df["Cv"]*multiplier, label=r'$\phi=$'+str(phi_D))
ax[3].plot(WL_E_df["T"], WL_E_df["Cv"]*multiplier, label=r'$\phi=$'+str(phi_E))
ax[3].set_ylabel(r"$C_{V}/kN_{c}$", fontsize=10, labelpad=7)
ax[3].set_xlabel(r"$T_{r}$", fontsize=10, labelpad=5)
ax[3].tick_params(axis='both', labelsize=8)
ax[3].set_yscale('log')
ax[3].set_ylim(1, 2*10**3) # 3*10**5*multiplier) #5*10**1*multiplier,4*10**5*multiplier)

plt.subplots_adjust(left=0.168, top=0.999, bottom=0.05, right=0.998, hspace=0.1)

import os
basename = os.path.splitext(__file__)[0]
plt.savefig(basename+".pdf")
#plt.close()
#phis = np.array([ phi_E, phi_D, phi_C, phi_B, phi_A ])
#Lxs  = np.array([ Lx_E, Lx_D, Lx_C, Lx_B, Lx_A ])
#plt.plot(np.arange(5),phis/np.amax(phis)) 
#plt.plot(np.arange(5),Lxs/np.amax(Lxs), c='r') 
#plt.show()
