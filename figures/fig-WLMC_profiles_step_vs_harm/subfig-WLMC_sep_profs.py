#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
created on Tue June 22 08:41:00 2022

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
what_is_x = "T"
cutT = 0.005
ax2ylim1 = 0.9
ax2ylim2 = 300
import os
basename = os.path.splitext(__file__)[0]

WL_step_file_name   = "hard-step-rods-lx11.224_ext_canon_distro.out"
WL_harm_file_name   = "hard-harm-rods-lx11.224_ext_canon_distro.out"

WL_step_file_params = "hard-step-rods-lx11.224_params.json"
WL_harm_file_params = "hard-harm-rods-lx11.224_params.json"

WL_step_file_Ts = "hard-step-rods-lx11.224_Ts.real.out"
WL_harm_file_Ts = "hard-harm-rods-lx11.224_Ts.real.out"

usecols          = (0,1,2,3,4,5)
names            = ['T', 'Em', 'Cv', 'q6', 'P2', 'n6']

WL_step_df          = pd.read_csv(WL_step_file_name, index_col=False, delimiter=' ', 
                                   usecols=usecols, names=names)
WL_harm_df          = pd.read_csv(WL_harm_file_name, index_col=False, delimiter=' ', 
                                   usecols=usecols, names=names)
WL_step_Ts_df       = pd.read_csv(WL_step_file_Ts, index_col=False, delimiter=' ')
WL_harm_Ts_df       = pd.read_csv(WL_harm_file_Ts, index_col=False, delimiter=' ')

Lx_step             = 11.224
Lx_harm             = 11.224

phi_step            = np.round(Nc*Nb*sigma**3/Lx_step**3*np.pi/6, 3)
phi_harm            = np.round(Nc*Nb*sigma**3/Lx_harm**3*np.pi/6, 3)

test=0
fig, axs = plt.subplots(1, 2, sharey=True, figsize=(5.5,2.92), constrained_layout=test)

# plot all the stepwise stuff
pp, = axs[0].plot(WL_step_df["P2"], WL_step_df[what_is_x]              , c=plt.get_cmap('tab10')(0), ls='-', label="Discrete")
pq, = axs[1].plot(WL_step_df["n6"], WL_step_df[what_is_x]              , c=plt.get_cmap('tab10')(0), ls='-', label="Discrete")
#pc, = axs[2].plot(np.array(WL_step_df["Cv"])[WL_step_df[what_is_x]>cutT]/Nc/(Nb-2)  , np.array(WL_step_df[what_is_x])[WL_step_df[what_is_x]>cutT]    , c=plt.get_cmap('tab10')(0), ls='-')#, label="Discrete")

# all the labels
axs[0].set_xlabel(r"Nematic order, $P_{2}$"                    , fontsize=10, labelpad=4.5)
axs[1].set_xlabel(r"Largest crystal fraction, $f_{\mathrm{cryst}}$"       , fontsize=10, labelpad=3.3)
#axs[2].set_xlabel(r"$C_{V}/kN_{\mathrm{bonds}}$", fontsize=10, labelpad=2.5)
axs[0].set_ylabel(r"Reduced Temperature $T_{r}$", fontsize=10, labelpad=1)
axs[0].tick_params(axis='both', labelsize=8, pad=0)
axs[1].tick_params(axis='both', labelsize=8, pad=0)
#axs[2].tick_params(axis='both', labelsize=8, pad=0)

ylim1 = -.01
ylim2 = 1
axs[0].set_xlim(ylim1, ylim2)
axs[1].set_xlim(ylim1, ylim2)
ax2yticks = [1,10,100]
#axs[2].set_xlim(ax2ylim1, ax2ylim2)
#axs[2].set_xscale('log')
#axs[2].set_xticks(ax2yticks)
axs[0].set_yticks([0, 0.1, 0.2, 0.3, 0.4, 0.5])
xlim1 = 0
xlim2 = 0.35
axs[0].set_ylim(xlim1, xlim2)

# save
axs[0].legend(loc='lower left' , handlelength=1.0, handletextpad=0.8)
if test == 0:
  fig.subplots_adjust(left=0.075, bottom=0.12, right=0.98, top=0.996, hspace=-0.1)
plt.savefig(basename+"_1.pdf")

axs[0].hlines(WL_step_Ts_df['peak_T'].iat[0], 0, 1, colors=plt.get_cmap('tab10')(0), ls='--')#, label=r"$I \rightarrow C$")
axs[1].hlines(WL_step_Ts_df['peak_T'].iat[0], 0, 1, colors=plt.get_cmap('tab10')(0), ls='--', label=r"$I \rightarrow C$")
#axs[2].hlines(WL_step_Ts_df['peak_T'].iat[0], ax2ylim1, ax2ylim2, colors=plt.get_cmap('tab10')(0), ls='--', label=r"$I \rightarrow C$")
# save
axs[0].legend(loc='lower left' , handlelength=1.0, handletextpad=0.8)
#axs[2].legend(loc='lower right', handlelength=3.0, handletextpad=0.8)
plt.savefig(basename+"_2.pdf")

# all the harmonic stuff
pp, = axs[0].plot(WL_harm_df["P2"], WL_harm_df[what_is_x]              , c=plt.get_cmap('tab10')(3), ls='-', label="Continuous")
pq, = axs[1].plot(WL_harm_df["n6"], WL_harm_df[what_is_x]              , c=plt.get_cmap('tab10')(3), ls='-', label="Continuous")
#pc, = axs[2].plot(np.array(WL_harm_df["Cv"])[WL_step_df[what_is_x]>cutT]/Nc/(Nb-2)  , np.array(WL_harm_df[what_is_x])[WL_step_df[what_is_x]>cutT]    , c=plt.get_cmap('tab10')(3), ls='-')#, label="Continuous")

# save
axs[0].legend(loc='lower left' , handlelength=1.0, handletextpad=0.8)
#axs[2].legend(loc='lower right', handlelength=3.0, handletextpad=0.8)
plt.savefig(basename+"_3.pdf")

axs[0].hlines(WL_harm_Ts_df['peak_T'].iat[1], 0, 1, colors=plt.get_cmap('tab10')(3), ls='--')#, label=r"$I \rightarrow N$")
axs[0].hlines(WL_harm_Ts_df['peak_T'].iat[0], 0, 1, colors=plt.get_cmap('tab10')(3), ls='-.')#, label=r"$N \rightarrow C$")
axs[1].hlines(WL_harm_Ts_df['peak_T'].iat[1], 0, 1, colors=plt.get_cmap('tab10')(3), ls='--', label=r"$I \rightarrow N$")
axs[1].hlines(WL_harm_Ts_df['peak_T'].iat[0], 0, 1, colors=plt.get_cmap('tab10')(3), ls='-.', label=r"$N \rightarrow C$")
#axs[2].hlines(WL_harm_Ts_df['peak_T'].iat[1], ax2ylim1, ax2ylim2, colors=plt.get_cmap('tab10')(3), ls='--', label=r"$I \rightarrow N$")
#axs[2].hlines(WL_harm_Ts_df['peak_T'].iat[0], ax2ylim1, ax2ylim2, colors=plt.get_cmap('tab10')(3), ls='-.', label=r"$N \rightarrow C$")
#axs[1].hlines(WL_harm_df["n6"], WL_harm_df[what_is_x]              , c=plt.get_cmap('tab10')(3), ls='-', label="Continuous")
#axs[2].hlines(np.array(WL_step_df["Cv"])[WL_step_df[what_is_x]>cutT]/Nc/(Nb-2)  , np.array(WL_step_df[what_is_x])[WL_step_df[what_is_x]>cutT]    , c=plt.get_cmap('tab10')(0), ls='-', label="Discrete")

# save
axs[0].legend(loc='lower left' , handlelength=1.0, handletextpad=0.8)
#axs[2].legend(loc='lower right', handlelength=3.0, handletextpad=0.8)
plt.savefig(basename+"_4.pdf")
