#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
created on Fri Apr 25 08:41:00 2022

@author: pierrekawak
"""

import pandas as pd
import matplotlib.pyplot as plt

wl_file_name          = "wlmc_results.out"
# do you want to divide by N?
divisor = 200000

# get WLMC data
df_wl  = pd.read_csv(wl_file_name, delimiter=" ", names=['Temp', 'energy', 'Cv'])
Cv_ = df_wl['Cv'].to_numpy() / divisor
Temp_ = df_wl['Temp'].to_numpy()
energy_ = df_wl['energy'].to_numpy() / divisor

# Energy plot
fig, ax = plt.subplots(figsize=(5,2.75), constrained_layout=True)
ax.plot(Temp_, energy_, label='WLMC', zorder = 1)
ax.set_xlabel(r"$kT/\epsilon$", fontsize=12, labelpad=6)
ax.set_ylabel(r"$\left<U\right>/N\epsilon$", fontsize=12, labelpad=10)
ax.set_xlim(0.6,7.9)
fig.savefig("subfig-U_vs_T.pdf")
plt.close()

# Cv plot
fig, ax = plt.subplots(figsize=(5,2.75), constrained_layout=True)
# WLMC Cv
ax.plot(Temp_, Cv_, label="WLMC", zorder = 1)
ax.set_xlim(0.6,7.9)
ax.set_ylim(1e-3, 4e2)
ax.set_yscale("log")
ax.set_xlabel(r"$kT/\epsilon$", fontsize=12, labelpad=6)
ax.set_ylabel(r'$C_{V}/Nk$', fontsize=12, labelpad=10)
fig.savefig("subfig-Cv_vs_T.pdf")
plt.close()

# all of them to share x
fig, ax = plt.subplots(2, 1, sharex=True, figsize=(5.0,2.75*2), constrained_layout=True)
ax[0].plot(Temp_, energy_, label='WLMC', zorder = 1)
ax[0].set_ylabel(r"$\left<U\right>/N\epsilon$", fontsize=12, labelpad=10)
ax[0].set_xlim(0.6,7.9)
ax[1].plot(Temp_, Cv_, label="WLMC", zorder = 1)
ax[1].set_ylim(1e-3, 4e2)
ax[1].set_yscale("log")
ax[1].set_xlabel(r"$kT/\epsilon$", fontsize=12, labelpad=6)
ax[1].set_ylabel(r'$C_{V}/Nk$', fontsize=12, labelpad=10)

plt.savefig("subfig-2000x100x0.85_WL.pdf")
plt.close()
