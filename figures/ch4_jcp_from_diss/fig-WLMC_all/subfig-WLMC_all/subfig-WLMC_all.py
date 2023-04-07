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

WL_10_file_name    = "Lx10_ext_canon_distro.out"
WL_10p25_file_name = "Lx10.25_ext_canon_distro.out"
WL_10p33_file_name = "Lx10.33_ext_canon_distro.out"
WL_10p5_file_name  = "Lx10.5_ext_canon_distro.out"
WL_10p75_file_name = "Lx10.75_ext_canon_distro.out"

import pandas as pd

WL_10_data    = np.loadtxt(WL_10_file_name, usecols=(0,2,3,5,6))
WL_10_df      = pd.DataFrame({'T': WL_10_data[:,0],
                         'Em': WL_10_data[:,1],
                         'Cv': WL_10_data[:,2],
                         'q6': WL_10_data[:,3],
                         'P2': WL_10_data[:,4]
                        })

WL_10p25_data = np.loadtxt(WL_10p25_file_name, usecols=(0,2,3,5,6))
WL_10p25_df   = pd.DataFrame({'T': WL_10p25_data[:,0],
                            'Em': WL_10p25_data[:,1],
                            'Cv': WL_10p25_data[:,2],
                            'q6': WL_10p25_data[:,3],
                            'P2': WL_10p25_data[:,4]
                           })

WL_10p33_data  = np.loadtxt(WL_10p33_file_name, usecols=(0,2,3,5,6))
WL_10p33_df    = pd.DataFrame({'T': WL_10p33_data[:,0],
                           'Em': WL_10p33_data[:,1],
                           'Cv': WL_10p33_data[:,2],
                           'q6': WL_10p33_data[:,3],
                           'P2': WL_10p33_data[:,4]
                          })

WL_10p5_data  = np.loadtxt(WL_10p5_file_name, usecols=(0,2,3,5,6))
WL_10p5_df    = pd.DataFrame({'T': WL_10p5_data[:,0],
                           'Em': WL_10p5_data[:,1],
                           'Cv': WL_10p5_data[:,2],
                           'q6': WL_10p5_data[:,3],
                           'P2': WL_10p5_data[:,4]
                          })

WL_10p75_data  = np.loadtxt(WL_10p75_file_name, usecols=(0,2,3,5,6))
WL_10p75_df    = pd.DataFrame({'T': WL_10p75_data[:,0],
                           'Em': WL_10p75_data[:,1],
                           'Cv': WL_10p75_data[:,2],
                           'q6': WL_10p75_data[:,3],
                           'P2': WL_10p75_data[:,4]
                          })

fig, ax = plt.subplots(3, 1, sharex=True, figsize=(3.25,2.0*3))
#fig, ax = plt.subplots(1, figsize=(3.25,2.3))

ax[0].plot(WL_10_df["T"], WL_10_df["P2"], label=r'$\phi=0.471$')
ax[0].plot(WL_10p25_df["T"], WL_10p25_df["P2"], label=r'$\phi=0.438$')
ax[0].plot(WL_10p33_df["T"], WL_10p33_df["P2"], label=r'$\phi_{c}=0.428$')
ax[0].plot(WL_10p5_df["T"], WL_10p5_df["P2"], label=r'$\phi=0.407$')
ax[0].plot(WL_10p75_df["T"], WL_10p75_df["P2"], label=r'$\phi=0.379$')
ax[0].set_ylabel(r"$P_{2}$", fontsize=10, labelpad=11)
ax[0].tick_params(axis='both', labelsize=8)
ax[0].legend(loc='best', fontsize=8)#, prop={'size': 6})
#ax[0].text(-0.23, 1.0, '(a)', fontsize=10, fontname='dejavusans', transform = ax[0].transAxes)


ax[1].plot(WL_10_df["T"], WL_10_df["q6"], label=r'$\phi=0.471$')
ax[1].plot(WL_10p25_df["T"], WL_10p25_df["q6"], label=r'$\phi=0.438$')
ax[1].plot(WL_10p33_df["T"], WL_10p33_df["q6"], label=r'$\phi_{c}=0.428$')
ax[1].plot(WL_10p5_df["T"], WL_10p5_df["q6"], label=r'$\phi=0.407$')
ax[1].plot(WL_10p75_df["T"], WL_10p75_df["q6"], label=r'$\phi=0.379$')
ax[1].set_ylabel(r"$Q_{6}$", fontsize=10, labelpad=7)
ax[1].tick_params(axis='both', labelsize=8)
#ax[1].text(-0.23, 1.0, '(b)', fontsize=10, fontname='dejavusans', transform = ax[1].transAxes)

ax[2].plot(WL_10_df["T"], WL_10_df["Cv"], label=r'$\phi=0.471$')
ax[2].plot(WL_10p25_df["T"], WL_10p25_df["Cv"], label=r'$\phi=0.438$')
ax[2].plot(WL_10p33_df["T"], WL_10p33_df["Cv"], label=r'$\phi_{c}=0.428$')
ax[2].plot(WL_10p5_df["T"], WL_10p5_df["Cv"], label=r'$\phi=0.407$')
ax[2].plot(WL_10p75_df["T"], WL_10p75_df["Cv"], label=r'$\phi=0.379$')
ax[2].set_ylabel(r"$C_{V}$", fontsize=10, labelpad=9)
ax[2].set_xlabel(r"$T_{r}$", fontsize=10, labelpad=5)
ax[2].tick_params(axis='both', labelsize=8)
ax[2].set_yscale('log')
#ax[2].text(-0.23, 1.0, '(c)', fontsize=10, fontname='dejavusans', transform = ax[2].transAxes)
#plt.subplots_adjust(left=0.18, top=0.99, bottom=0.18, right=0.99)
plt.subplots_adjust(left=0.18, top=0.997, bottom=0.07, right=0.995, hspace=0.1)
#plt.show()
#sys.exit()
plt.savefig("subfig-WLMC_all.pdf")
