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

WL_A_file_name   = "like10_ext_canon_distro.out"
WL_B_file_name   = "like10.25_ext_canon_distro.out"
WL_C_file_name   = "like10.5_ext_canon_distro.out"
WL_D_file_name   = "lx13.00_ext_canon_distro.out"

WL_A_file_params = "like10_params.json"
WL_B_file_params = "like10.25_params.json"
WL_C_file_params = "like10.5_params.json"
WL_D_file_params = "lx13.00_params.json"

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

Lx_A             = float(json.load(open(WL_A_file_params, "r+"))["Lx"])
Lx_B             = float(json.load(open(WL_B_file_params, "r+"))["Lx"])
Lx_C             = float(json.load(open(WL_C_file_params, "r+"))["Lx"])
Lx_D             = float(json.load(open(WL_D_file_params, "r+"))["Lx"])

phi_A            = np.round(Nc*Nb*sigma**3/Lx_A**3*np.pi/6, 3)
phi_B            = np.round(Nc*Nb*sigma**3/Lx_B**3*np.pi/6, 3)
phi_C            = np.round(Nc*Nb*sigma**3/Lx_C**3*np.pi/6, 3)
phi_D            = np.round(Nc*Nb*sigma**3/Lx_D**3*np.pi/6, 3)

test = 1
if test:
  fig, ax = plt.subplots(4, 1, sharex=True, figsize=(3.25,2.0*4), constrained_layout=True)
else:
  fig, ax = plt.subplots(4, 1, sharex=True, figsize=(3.25,2.0*4))#, constrained_layout=True)

multiplier = 1/Nc/(Nb-2)
ax[0].plot(WL_A_df["T"], WL_A_df["Em"]*multiplier, label=r'$\phi=$'+str(phi_A))
ax[0].plot(WL_B_df["T"], WL_B_df["Em"]*multiplier, label=r'$\phi=$'+str(phi_B))
ax[0].plot(WL_C_df["T"], WL_C_df["Em"]*multiplier, label=r'$\phi=$'+str(phi_C))
ax[0].plot(WL_D_df["T"], WL_D_df["Em"]*multiplier, label=r'$\phi=$'+str(phi_D))

ax[0].set_ylabel(r"$\left<U\right>/N_{c}(N_{b}-2)$", fontsize=10, labelpad=7)
#ax[0].set_ylabel(r"$-U_{\mathrm{angle}}/k_{b}\times10^{-2}$", fontsize=10, labelpad=11)
ax[0].tick_params(axis='both', labelsize=8)
ax[0].legend(loc='best', fontsize=8)#, prop={'size': 6})

ax[1].plot(WL_A_df["T"], WL_A_df["P2"], label=r'$\phi=$'+str(phi_A))
ax[1].plot(WL_B_df["T"], WL_B_df["P2"], label=r'$\phi=$'+str(phi_B))
ax[1].plot(WL_C_df["T"], WL_C_df["P2"], label=r'$\phi=$'+str(phi_C))
ax[1].plot(WL_D_df["T"], WL_D_df["P2"], label=r'$\phi=$'+str(phi_D))
ax[1].set_ylabel(r"$P_{2}$", fontsize=10, labelpad=9)
ax[1].tick_params(axis='both', labelsize=8)

ax[2].plot(WL_A_df["T"], WL_A_df["n6"], label=r'$\phi=$'+str(phi_A))
ax[2].plot(WL_B_df["T"], WL_B_df["n6"], label=r'$\phi=$'+str(phi_B))
ax[2].plot(WL_C_df["T"], WL_C_df["n6"], label=r'$\phi=$'+str(phi_C))
ax[2].plot(WL_D_df["T"], WL_D_df["n6"], label=r'$\phi=$'+str(phi_D))
ax[2].set_ylabel(r"$f_{\mathrm{cryst}}$", fontsize=10, labelpad=9.5)
ax[2].tick_params(axis='both', labelsize=8)

cutT = 0.005
multiplier = 1/Nc #/Nb
ax[3].plot(np.array(WL_A_df["T"])[WL_A_df["T"]>cutT], np.array(WL_A_df["Cv"])[WL_A_df["T"]>cutT]*multiplier, label=r'$\phi=$'+str(phi_A))
ax[3].plot(np.array(WL_B_df["T"])[WL_A_df["T"]>cutT], np.array(WL_B_df["Cv"])[WL_A_df["T"]>cutT]*multiplier, label=r'$\phi=$'+str(phi_B))
ax[3].plot(np.array(WL_C_df["T"])[WL_A_df["T"]>cutT], np.array(WL_C_df["Cv"])[WL_A_df["T"]>cutT]*multiplier, label=r'$\phi=$'+str(phi_C))
ax[3].plot(np.array(WL_D_df["T"])[WL_A_df["T"]>cutT], np.array(WL_D_df["Cv"])[WL_A_df["T"]>cutT]*multiplier, label=r'$\phi=$'+str(phi_D))
ax[3].set_ylabel(r"$C_{V}/kN_{c}$", fontsize=10, labelpad=7)
ax[3].set_xlabel(r"$T_{r}$", fontsize=10, labelpad=5)
ax[3].tick_params(axis='both', labelsize=8)
ax[3].set_yscale('log')

if test == 0:
  plt.subplots_adjust(left=0.18, top=0.997, bottom=0.05, right=0.995, hspace=0.1)

import os
basename = os.path.splitext(__file__)[0]
plt.savefig(basename+".pdf")
