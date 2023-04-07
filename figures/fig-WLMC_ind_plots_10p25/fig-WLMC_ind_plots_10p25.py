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

fig_width = 2.4
fig_height = 2.7

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

fig, ax = plt.subplots(1, 1, figsize=(fig_width,fig_height))
ax.plot(WL_df["T"], WL_df["Cv"], color='dimgray', label='WLMC')
ax.set_ylabel(r"$C_{V}$", fontsize=10, labelpad=3)
ax.set_xlabel(r"$T_{r}$", fontsize=10, labelpad=5)
ax.set_yscale('log')
ax.tick_params(axis='both', labelsize=8)
ax.axvline(x=0.2907, color='b', alpha=0.5, ls=':')
plt.subplots_adjust(left=0.15, top=0.99, bottom=0.13, right=0.995)
plt.savefig("fig-WLMC_Cv_10p25.pdf")

fig, ax = plt.subplots(1, 1, figsize=(fig_width,fig_height))
ax.plot(WL_df["T"], WL_df["Cv"], color='dimgray', label='WLMC')
ax.set_xlabel(r"$T_{r}$", fontsize=10, labelpad=4)
ax.set_ylabel(r"Heat Capacity$= C_{V}$", fontsize=10, labelpad=0.0)
ax.set_yscale('log')
ax.axvline(x=0.2907, color='b', alpha=0.5, ls=':')
ax.set_yticks([])
ax.set_xticks([])
plt.subplots_adjust(left=0.095, bottom=0.07, right=0.995, top=0.99)
#plt.subplots_adjust(left=0.12, top=0.99, bottom=0.09, right=0.995)
plt.savefig("fig-WLMC_Cv_plain_10p25.pdf")

fig, ax = plt.subplots(1, 1, figsize=(fig_width,fig_height))
ax.plot(WL_df["T"], WL_df["Em"], color='dimgray', label='WLMC')
ax.set_ylabel(r"Energy ($U_{tot}/\epsilon$)", fontsize=8, labelpad=4.1)
ax.set_xlabel(r"$T_{r}$", fontsize=8, labelpad=5)
ax.tick_params(axis='both', labelsize=8)
ax.axvline(x=0.2907, color='b', alpha=0.5, ls=':')
plt.subplots_adjust(left=0.15, top=0.99, bottom=0.13, right=0.995)
plt.savefig("fig-WLMC_U_10p25.pdf")

fig, ax = plt.subplots(1, 1, figsize=(fig_width,fig_height))
ax.plot(WL_df["T"], WL_df["P2"], color='dimgray', label='WLMC')
ax.set_ylim(0,1)
ax.set_yticks([.2,.4,.6,.8])
ax.set_ylabel("Nematic""\n"r"Order ($P_{2}$)", fontsize=8, labelpad=7)
ax.set_xlabel(r"$T_{r}$", fontsize=8, labelpad=5)
ax.tick_params(axis='both', labelsize=8)
ax.axvline(x=0.2907, color='b', alpha=0.5, ls=':')
plt.subplots_adjust(left=0.15, top=0.99, bottom=0.13, right=0.995)
plt.savefig("fig-WLMC_P2_10p25.pdf")

fig, ax = plt.subplots(1, 1, figsize=(fig_width,fig_height))
ax.plot(WL_df["T"], WL_df["q6"], color='dimgray', label='WLMC')
ax.set_ylabel(r"Crystallinity ($Q_{6}$)", fontsize=8, labelpad=6)
ax.set_xlabel(r"$T_{r}$", fontsize=8, labelpad=5)
ax.tick_params(axis='both', labelsize=8)
ax.axvline(x=0.2907, color='b', alpha=0.5, ls=':')
plt.subplots_adjust(left=0.15, top=0.99, bottom=0.13, right=0.995)
plt.savefig("fig-WLMC_Q6_10p25.pdf")
