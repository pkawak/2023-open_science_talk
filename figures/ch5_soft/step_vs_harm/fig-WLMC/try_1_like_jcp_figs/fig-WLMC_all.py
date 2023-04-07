#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
created on Tue June 21 08:41:00 2022

@author: pierrekawak
"""

import sys
import numpy as np
import matplotlib.cm as mcm
import matplotlib.pyplot as plt
import pandas as pd
import json

cm=1/2.54
fig_width = 13.998*cm/2
fig_height = 7.9*cm

Nc    = 125
Nb    = 10
sigma = 1

WL_step_file_name   = "hard-step-rods-lx11.224_ext_canon_distro.out"
WL_harm_file_name   = "hard-harm-rods-lx11.224_ext_canon_distro.out"

usecols          = (0,1,2,3,4,5)
names            = ['T', 'Em', 'Cv', 'q6', 'P2', 'n6']

WL_step_df          = pd.read_csv(WL_step_file_name, index_col=False, delimiter=' ', 
                                   usecols=usecols, names=names)
WL_harm_df          = pd.read_csv(WL_harm_file_name, index_col=False, delimiter=' ', 
                                   usecols=usecols, names=names)

Lx_step             = 11.224
Lx_harm             = 11.224

phi_step            = np.round(Nc*Nb*sigma**3/Lx_step**3*np.pi/6, 3)
phi_harm            = np.round(Nc*Nb*sigma**3/Lx_harm**3*np.pi/6, 3)
print(phi_step, phi_harm)

test = 0
if test:
  fig, ax = plt.subplots(2, 1, sharex=True, figsize=(3.13,2.0*2), constrained_layout=True)
else:
  fig, ax = plt.subplots(2, 1, sharex=True, figsize=(3.13,2.0*2))#, constrained_layout=True)
cutT = 0.005

cmap = mcm.get_cmap('pink')
cmaps = np.array([cmap((i+0.5)/9) for i in range(5)])

fig, ax = plt.subplots(1, 1, figsize=(fig_width,fig_height))
ax.plot(WL_step_df["T"], WL_step_df["P2"], c=cmaps[0], label='Stepwise')
ax.plot(WL_harm_df["T"], WL_harm_df["P2"], c=cmaps[4], label='Harmonic')
ax.set_ylabel(r"$P_{2}$", fontsize=10, labelpad=5)
ax.set_xlabel(r"$T_{r}$", fontsize=10, labelpad=4)
ax.tick_params(axis='both', labelsize=8)
ax.legend(loc='best', fontsize=10)
plt.subplots_adjust(left=0.18, top=0.997, bottom=0.125, right=0.995, hspace=0.1)
plt.savefig("fig-WLMC_all_P2.pdf")

fig, ax = plt.subplots(1, 1, figsize=(fig_width,fig_height))
ax.plot(WL_step_df["T"], WL_step_df["q6"], c=cmaps[0], label='Stepwise')
ax.plot(WL_harm_df["T"], WL_harm_df["q6"], c=cmaps[4], label='Harmonic')
ax.set_ylabel(r"$Q_{6}$", fontsize=10, labelpad=5)
ax.set_xlabel(r"$T_{r}$", fontsize=10, labelpad=4)
ax.tick_params(axis='both', labelsize=8)
ax.set_yticks([0.35, 0.40, 0.45, 0.50])
#ax.legend(loc='best', fontsize=10)
plt.subplots_adjust(left=0.205, top=0.997, bottom=0.125, right=0.995, hspace=0.1)
plt.savefig("fig-WLMC_all_Q6.pdf")

fig, ax = plt.subplots(1, 1, figsize=(fig_width,fig_height))
ax.plot(WL_step_df["T"], WL_step_df["n6"], c=cmaps[0], label='Stepwise')
ax.plot(WL_harm_df["T"], WL_harm_df["n6"], c=cmaps[4], label='Harmonic')
ax.set_ylabel(r"$f_{\mathrm{cryst}}$", fontsize=10, labelpad=5)
ax.set_xlabel(r"$T_{r}$", fontsize=10, labelpad=4)
ax.tick_params(axis='both', labelsize=8)
#ax.set_yticks([0.35, 0.40, 0.45, 0.50])
#ax.legend(loc='best', fontsize=10)
plt.subplots_adjust(left=0.205, top=0.997, bottom=0.125, right=0.995, hspace=0.1)
plt.savefig("fig-WLMC_all_n6.pdf")

fig_width = 13.998*cm
#fig, ax = plt.subplots(1, 1, figsize=(fig_width,fig_height))
fig, ax = plt.subplots(1, 1, figsize=(12*cm,9*cm))
ax.plot(WL_step_df["T"], WL_step_df["Cv"]*90/125, c=cmaps[0], label='Stepwise')
ax.plot(WL_harm_df["T"], WL_harm_df["Cv"]*90/125, c=cmaps[4], label='Harmonic')
ax.set_ylabel(r"$C_{V}$", fontsize=12, labelpad=9)
ax.set_xlabel(r"$T_{r}$", fontsize=12, labelpad=5)
ax.tick_params(axis='both', labelsize=10)
ax.legend()
ax.set_yscale('log')
ax.set_xlim([0.05, 0.5])
ax.set_ylim([0.5, 3e5])
#ax.legend(loc='best', fontsize=12)
#plt.annotate("Increasing $\phi$", xy=(0.15, 8e3), xytext=(0.22, 7e0),
#              arrowprops=dict(facecolor='black', arrowstyle='->'),
#              fontsize=13
#            )
plt.tight_layout()
#plt.subplots_adjust(left=0.115, top=0.997, bottom=0.146, right=0.995, hspace=0.1)
plt.savefig("fig-WLMC_all_Cv.pdf")
