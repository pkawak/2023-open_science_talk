#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
created on Tue June 14 08:41:00 2021

@author: pierrekawak
"""

import sys
import numpy as np
import matplotlib.cm as mcm
import matplotlib.pyplot as plt
import pandas as pd

cm=1/2.54
fig_width = 2.55
fig_height = 2.85

WL_10p00_file_name = "Lx10.00_ext_canon_distro.out"
WL_10p25_file_name = "Lx10.25_ext_canon_distro.out"
WL_10p33_file_name = "Lx10.33_ext_canon_distro.out"
WL_10p50_file_name = "Lx10.50_ext_canon_distro.out"
WL_10p75_file_name = "Lx10.75_ext_canon_distro.out"

WL_10p00_data    = np.loadtxt(WL_10p00_file_name, usecols=(0,1,2,3,4,5), skiprows=1)
WL_10p00_df      = pd.DataFrame({'T': WL_10p00_data[:,0],
                         'Em': WL_10p00_data[:,1],
                         'Cv': WL_10p00_data[:,2],
                         'q6': WL_10p00_data[:,3],
                         'P2': WL_10p00_data[:,4],
                         'n6': WL_10p00_data[:,5]
                        })

WL_10p25_data = np.loadtxt(WL_10p25_file_name, usecols=(0,1,2,3,4,5), skiprows=1)
WL_10p25_df   = pd.DataFrame({'T': WL_10p25_data[:,0],
                         'Em': WL_10p25_data[:,1],
                         'Cv': WL_10p25_data[:,2],
                         'q6': WL_10p25_data[:,3],
                         'P2': WL_10p25_data[:,4],
                         'n6': WL_10p25_data[:,5]
                         })

WL_10p33_data  = np.loadtxt(WL_10p33_file_name, usecols=(0,1,2,3,4,5), skiprows=1)
WL_10p33_df    = pd.DataFrame({'T': WL_10p33_data[:,0],
                           'Em': WL_10p33_data[:,1],
                           'Cv': WL_10p33_data[:,2],
                           'q6': WL_10p33_data[:,3],
                           'P2': WL_10p33_data[:,4],
                         'n6': WL_10p33_data[:,5]
                          })

WL_10p50_data  = np.loadtxt(WL_10p50_file_name, usecols=(0,1,2,3,4), skiprows=1)
WL_10p50_df    = pd.DataFrame({'T': WL_10p50_data[:,0],
                           'Em': WL_10p50_data[:,1],
                           'Cv': WL_10p50_data[:,2],
                           'q6': WL_10p50_data[:,3],
                           'P2': WL_10p50_data[:,4]#,
#                         'n6': WL_10p50_data[:,5]
                          })

WL_10p75_data  = np.loadtxt(WL_10p75_file_name, usecols=(0,1,2,3,4,5), skiprows=1)
WL_10p75_df    = pd.DataFrame({'T': WL_10p75_data[:,0],
                           'Em': WL_10p75_data[:,1],
                           'Cv': WL_10p75_data[:,2],
                           'q6': WL_10p75_data[:,3],
                           'P2': WL_10p75_data[:,4],
                         'n6': WL_10p75_data[:,5]
                          })

cmap = mcm.get_cmap('pink')
cmaps = np.array([cmap((i+0.5)/9) for i in range(5)])

fig, ax = plt.subplots(1, 1, figsize=(fig_width,fig_height))
ax.plot(WL_10p00_df["T"], WL_10p00_df["P2"], c=cmaps[0], label=r'$\phi=0.471$')
ax.plot(WL_10p25_df["T"], WL_10p25_df["P2"], c=cmaps[1], label=r'$\phi=0.438$')
ax.plot(WL_10p33_df["T"], WL_10p33_df["P2"], c=cmaps[2], label=r'$\phi_{c}=0.428$')
ax.plot(WL_10p50_df["T"], WL_10p50_df["P2"], c=cmaps[3], label=r'$\phi=0.407$')
ax.plot(WL_10p75_df["T"], WL_10p75_df["P2"], c=cmaps[4], label=r'$\phi=0.379$')
ax.set_ylabel(r"Nematic order, $P_{2}$", fontsize=12, labelpad=5)
ax.set_xlabel(r"$T_{r}$", fontsize=12, labelpad=4)
ax.set_xticks([0.2, 0.4, 0.6, 0.8, 1.0])
ax.tick_params(axis='both', labelsize=10, pad=0)
plt.subplots_adjust(left=0.202, top=0.997, bottom=0.14, right=0.996, hspace=0.1)
plt.annotate("Increasing $\phi$", xy=(0.07, 0.40), xytext=(0.50, 0.70),
              arrowprops=dict(facecolor='black', arrowstyle='<-'),
              fontsize=10
            )
plt.savefig("fig-WLMC_all_P2.pdf")

fig, ax = plt.subplots(1, 1, figsize=(fig_width,fig_height))
ax.plot(WL_10p00_df["T"], WL_10p00_df["q6"], c=cmaps[0], label=r'$\phi=0.471$')
ax.plot(WL_10p25_df["T"], WL_10p25_df["q6"], c=cmaps[1], label=r'$\phi=0.438$')
ax.plot(WL_10p33_df["T"], WL_10p33_df["q6"], c=cmaps[2], label=r'$\phi_{c}=0.428$')
ax.plot(WL_10p50_df["T"], WL_10p50_df["q6"], c=cmaps[3], label=r'$\phi=0.407$')
ax.plot(WL_10p75_df["T"], WL_10p75_df["q6"], c=cmaps[4], label=r'$\phi=0.379$')
ax.set_ylabel(r"Measure of crystallinity, $Q_{6}$", fontsize=12, labelpad=5)
ax.set_xlabel(r"$T_{r}$", fontsize=12, labelpad=4)
ax.tick_params(axis='both', labelsize=10, pad=0)
ax.set_xticks([0.2, 0.4, 0.6, 0.8, 1.0])
ax.set_yticks([0.35, 0.40, 0.45, 0.50])
ax.set_yticklabels(["", "0.4", "", "0.5"])
plt.annotate("Increasing $\phi$", xy=(0.90, 0.48), xytext=(0.07, 0.35),
              arrowprops=dict(facecolor='black', arrowstyle='->'),
              fontsize=10
            )
plt.subplots_adjust(left=0.205, top=0.997, bottom=0.14, right=0.996, hspace=0.1)
plt.savefig("fig-WLMC_all_Q6.pdf")

fig, ax = plt.subplots(1, 1, figsize=(fig_width,fig_height))
ax.plot(WL_10p00_df["T"], WL_10p00_df["n6"], c=cmaps[0], label=r'$\phi=0.471$')
ax.plot(WL_10p25_df["T"], WL_10p25_df["n6"], c=cmaps[1], label=r'$\phi=0.438$')
ax.plot(WL_10p33_df["T"], WL_10p33_df["n6"], c=cmaps[2], label=r'$\phi_{c}=0.428$')
#ax.plot(WL_10p50_df["T"], WL_10p50_df["n6"], c=cmaps[3], label=r'$\phi=0.407$')
ax.plot(WL_10p75_df["T"], WL_10p75_df["n6"], c=cmaps[4], label=r'$\phi=0.379$')
ax.set_ylabel(r"$f_{\mathrm{cryst}}$", fontsize=12, labelpad=5)
ax.set_xlabel(r"$T_{r}$", fontsize=12, labelpad=4)
ax.tick_params(axis='both', labelsize=10, pad=0)
#ax.set_yticks([0.35, 0.40, 0.45, 0.50])
#ax.legend(loc='best', fontsize=12)
plt.subplots_adjust(left=0.222, top=0.997, bottom=0.127, right=0.997, hspace=0.1)
plt.savefig("fig-WLMC_all_n6.pdf")

fig, ax = plt.subplots(1, 1, figsize=(5.0,2.85))
ax.plot(WL_10p00_df["T"], WL_10p00_df["Cv"], c=cmaps[0], label=r'$\phi=0.471$')
ax.plot(WL_10p25_df["T"], WL_10p25_df["Cv"], c=cmaps[1], label=r'$\phi=0.438$')
ax.plot(WL_10p33_df["T"], WL_10p33_df["Cv"], c=cmaps[2], label=r'$\phi_{c}=0.428$')
ax.plot(WL_10p50_df["T"], WL_10p50_df["Cv"], c=cmaps[3], label=r'$\phi=0.407$')
ax.plot(WL_10p75_df["T"], WL_10p75_df["Cv"], c=cmaps[4], label=r'$\phi=0.379$')
ax.set_ylabel(r"Heat Capacity, $C_{V}$", fontsize=12, labelpad=9)
ax.set_xlabel(r"Reduced Temperature, $T_{r}$", fontsize=12, labelpad=5)
ax.tick_params(axis='both', labelsize=10, pad=0)
ax.set_yscale('log')
ax.set_xlim([0.05, 0.6])
ax.set_xticks([0.1, 0.2, 0.3, 0.4, 0.5])
#ax.legend(loc='best', fontsize=12)
plt.annotate("Increasing $\phi$", xy=(0.15, 8e3), xytext=(0.25, 3e0),
              arrowprops=dict(facecolor='black', arrowstyle='<-'),
              fontsize=13
            )
plt.subplots_adjust(left=0.122, top=0.997, bottom=0.14, right=0.998, hspace=0.1)
plt.savefig("fig-WLMC_all_Cv.pdf")
