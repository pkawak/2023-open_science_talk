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

Nc    = 125
Nb    = 10
sigma = 1.0

MC_file_name = "MCMC_results.out"
#WL_10p00_file_name = "like10.00_ext_canon_distro.out"
#WL_10p25_file_name = "like10.25_ext_canon_distro.out"
Lx_10p00           = 11.157216
Lx_10p25           = 11.436146
phi_10p00          = np.round(Nc*Nb*sigma**3/Lx_10p00**3*np.pi/6, 3)
phi_10p25          = np.round(Nc*Nb*sigma**3/Lx_10p25**3*np.pi/6, 3)

import pandas as pd
MC_df = pd.read_csv(MC_file_name, delimiter=' ', index_col=False)
MC_df = MC_df.rename(columns={"Temp": "T"})
MC_df = MC_df.rename(columns={"Emean": "Em"})
MC_df = MC_df.rename(columns={"clust": "n6"})
MC_df = MC_df.rename(columns={"Q6": "q6"})

# keep only the Harmonic component
MC_df = MC_df.loc[MC_df['angle'] == 1]

# group by angle, Lx, and Temp and average 'T' replicates
MC_df_avg = MC_df.groupby(['angle', 'Lx', 'T']).mean().reset_index()
MC_df_sem = MC_df.groupby(['angle', 'Lx', 'T']).sem().reset_index()

# filter by Lx
MC_10p00_df_avg = MC_df_avg.loc[MC_df_avg['Lx'] == Lx_10p00]
MC_10p00_df_sem = MC_df_sem.loc[MC_df_sem['Lx'] == Lx_10p00]
MC_10p25_df_avg = MC_df_avg.loc[MC_df_avg['Lx'] == Lx_10p25]
MC_10p25_df_sem = MC_df_sem.loc[MC_df_sem['Lx'] == Lx_10p25]

fig, ax = plt.subplots(4, 1, sharex=True, figsize=(3.25,2.0*4))#, constrained_layout=True)

ax[0].errorbar(MC_10p00_df_avg["T"], MC_10p00_df_avg["Em"], yerr=MC_10p00_df_sem["Em"], ls='none', color='red')
ax[0].scatter(MC_10p00_df_avg["T"], MC_10p00_df_avg["Em"], color='red', s=5, label=r'$\phi=$'+str(phi_10p00))
ax[0].errorbar(MC_10p25_df_avg["T"], MC_10p25_df_avg["Em"], yerr=MC_10p25_df_sem["Em"], ls='none', color='blue')
ax[0].scatter(MC_10p25_df_avg["T"], MC_10p25_df_avg["Em"], color='blue', s=5, label=r'$\phi=$'+str(phi_10p25))
#ax[0].plot(WL_10p00_df["T"], WL_10p00_df["Em"]/-Nc/(Nb-2), label=r'$\phi=$'+str(phi_10p00))
#ax[0].plot(WL_10p25_df["T"], WL_10p25_df["Em"]/-Nc/(Nb-2), label=r'$\phi=$'+str(phi_10p25))
##ax[0].plot(WL_10p30_df["T"], WL_10p30_df["Em"]/-Nc/(Nb-2), label=r'$\phi=$'+str(phi_10p30))
##ax[0].plot(WL_10p33_df["T"], WL_10p33_df["Em"]/-Nc/(Nb-2), label=r'$\phi=$'+str(phi_10p33))
##ax[0].plot(WL_10p50_df["T"], WL_10p50_df["Em"]/-Nc/(Nb-2), label=r'$\phi=$'+str(phi_10p50))
ax[0].set_ylabel(r"$\left<U\right>/k_{b}$", fontsize=10, labelpad=7)
ax[0].tick_params(axis='both', labelsize=8)
ax[0].legend(loc='best', fontsize=8)#, prop={'size': 6})

ax[1].errorbar(MC_10p00_df_avg["T"], MC_10p00_df_avg["P2"], yerr=MC_10p00_df_sem["P2"], ls='none', color='red')
ax[1].scatter(MC_10p00_df_avg["T"], MC_10p00_df_avg["P2"], color='red', s=5, label=r'$\phi=$'+str(phi_10p00))
ax[1].errorbar(MC_10p25_df_avg["T"], MC_10p25_df_avg["P2"], yerr=MC_10p25_df_sem["P2"], ls='none', color='blue')
ax[1].scatter(MC_10p25_df_avg["T"], MC_10p25_df_avg["P2"], color='blue', s=5, label=r'$\phi=$'+str(phi_10p25))
#ax[1].plot(WL_10p00_df["T"], WL_10p00_df["P2"], label=r'$\phi=$'+str(phi_10p00))
#ax[1].plot(WL_10p25_df["T"], WL_10p25_df["P2"], label=r'$\phi=$'+str(phi_10p25))
##ax[1].plot(WL_10p30_df["T"], WL_10p30_df["P2"], label=r'$\phi=$'+str(phi_10p30))
##ax[1].plot(WL_10p33_df["T"], WL_10p33_df["P2"], label=r'$\phi=$'+str(phi_10p33))
##ax[1].plot(WL_10p50_df["T"], WL_10p50_df["P2"], label=r'$\phi=$'+str(phi_10p50))
ax[1].set_ylabel(r"$P_{2}$", fontsize=10, labelpad=9)
ax[1].tick_params(axis='both', labelsize=8)

ax[2].errorbar(MC_10p00_df_avg["T"], MC_10p00_df_avg["n6"], yerr=MC_10p00_df_sem["n6"], ls='none', color='red')
ax[2].scatter(MC_10p00_df_avg["T"], MC_10p00_df_avg["n6"], color='red', s=5, label=r'$\phi=$'+str(phi_10p00))
ax[2].errorbar(MC_10p25_df_avg["T"], MC_10p25_df_avg["n6"], yerr=MC_10p25_df_sem["n6"], ls='none', color='blue')
ax[2].scatter(MC_10p25_df_avg["T"], MC_10p25_df_avg["n6"], color='blue', s=5, label=r'$\phi=$'+str(phi_10p25))
#ax[2].plot(WL_10p00_df["T"], WL_10p00_df["n6"], label=r'$\phi=$'+str(phi_10p00))
#ax[2].plot(WL_10p25_df["T"], WL_10p25_df["n6"], label=r'$\phi=$'+str(phi_10p25))
##ax[2].plot(WL_10p30_df["T"], WL_10p30_df["n6"], label=r'$\phi=$'+str(phi_10p30))
##ax[2].plot(WL_10p33_df["T"], WL_10p33_df["n6"], label=r'$\phi=$'+str(phi_10p33))
##ax[2].plot(WL_10p50_df["T"], WL_10p50_df["n6"], label=r'$\phi=$'+str(phi_10p50))
ax[2].set_ylabel(r"$n_{Q_{6}}$", fontsize=10, labelpad=9.5)
ax[2].tick_params(axis='both', labelsize=8)
#ax[2].set_yticks([0.35,0.40,0.45])
#ax[2].set_ylim(0,1)

multiplier = 1/Nc #/Nb
#ax[3].plot(WL_10p00_df["T"], WL_10p00_df["Cv"]*multiplier, label=r'$\phi=$'+str(phi_10p00))
#ax[3].plot(WL_10p25_df["T"], WL_10p25_df["Cv"]*multiplier, label=r'$\phi=$'+str(phi_10p25))
##ax[3].plot(WL_10p30_df["T"], WL_10p30_df["Cv"]*multiplier, label=r'$\phi=$'+str(phi_10p30))
##ax[3].plot(WL_10p33_df["T"], WL_10p33_df["Cv"]*multiplier, label=r'$\phi=$'+str(phi_10p33))
##ax[3].plot(WL_10p50_df["T"], WL_10p50_df["Cv"]*multiplier, label=r'$\phi=$'+str(phi_10p50))
ax[3].set_ylabel(r"$C_{V}/kN_{c}$", fontsize=10, labelpad=7)
ax[3].set_xlabel(r"$T_{r}$", fontsize=10, labelpad=5)
ax[3].tick_params(axis='both', labelsize=8)
ax[3].set_yscale('log')
#ax[3].set_ylim(1, 2*10**3) # 3*10**5*multiplier) #5*10**1*multiplier,4*10**5*multiplier)

plt.subplots_adjust(left=0.168, top=0.999, bottom=0.05, right=0.998, hspace=0.1)

import os
basename = os.path.splitext(__file__)[0]
plt.savefig(basename+".pdf")

#WL_10p30_file_name = "like10.30_ext_canon_distro.out"
#WL_10p33_file_name = "like10.33_ext_canon_distro.out"
#WL_10p50_file_name = "like10.50_ext_canon_distro.out"
#Lx_10p30           = 11.491932
#Lx_10p33           = 11.525404
#Lx_10p50           = 11.715077
#phi_10p30          = np.round(Nc*Nb*sigma**3/Lx_10p30**3*np.pi/6, 3)
#phi_10p33          = np.round(Nc*Nb*sigma**3/Lx_10p33**3*np.pi/6, 3)
#phi_10p50          = np.round(Nc*Nb*sigma**3/Lx_10p50**3*np.pi/6, 3)
#
#import pandas as pd
#
#WL_10p00_data    = np.loadtxt(WL_10p00_file_name, usecols=(0,1,2,3,4,5))
#WL_10p00_df      = pd.DataFrame({'T': WL_10p00_data[:,0],
#                         'Em': WL_10p00_data[:,1],
#                         'Cv': WL_10p00_data[:,2],
#                         'q6': WL_10p00_data[:,3],
#                         'P2': WL_10p00_data[:,4],
#                         'n6': WL_10p00_data[:,5]
#                        })
#
#WL_10p25_data = np.loadtxt(WL_10p25_file_name, usecols=(0,1,2,3,4,5))
#WL_10p25_df   = pd.DataFrame({'T': WL_10p25_data[:,0],
#                            'Em': WL_10p25_data[:,1],
#                            'Cv': WL_10p25_data[:,2],
#                            'q6': WL_10p25_data[:,3],
#                            'P2': WL_10p25_data[:,4],
#                            'n6': WL_10p25_data[:,5]
#                           })
#
#WL_10p30_data  = np.loadtxt(WL_10p30_file_name, usecols=(0,1,2,3,4,5))
#WL_10p30_df    = pd.DataFrame({'T': WL_10p30_data[:,0],
#                           'Em': WL_10p30_data[:,1],
#                           'Cv': WL_10p30_data[:,2],
#                           'q6': WL_10p30_data[:,3],
#                           'P2': WL_10p30_data[:,4],
#                           'n6': WL_10p30_data[:,5]
#                          })
#
#WL_10p33_data  = np.loadtxt(WL_10p33_file_name, usecols=(0,1,2,3,4,5))
#WL_10p33_df    = pd.DataFrame({'T': WL_10p33_data[:,0],
#                           'Em': WL_10p33_data[:,1],
#                           'Cv': WL_10p33_data[:,2],
#                           'q6': WL_10p33_data[:,3],
#                           'P2': WL_10p33_data[:,4],
#                           'n6': WL_10p33_data[:,5]
#                          })
#
#WL_10p50_data  = np.loadtxt(WL_10p50_file_name, usecols=(0,1,2,3,4,5))
#WL_10p50_df    = pd.DataFrame({'T': WL_10p50_data[:,0],
#                           'Em': WL_10p50_data[:,1],
#                           'Cv': WL_10p50_data[:,2],
#                           'q6': WL_10p50_data[:,3],
#                           'P2': WL_10p50_data[:,4],
#                           'n6': WL_10p50_data[:,5]
#                          })
#
##fig, ax = plt.subplots(1, figsize=(3.25,2.3))
#
##plt.close()
##phis = np.array([ phi_10p50, phi_10p33, phi_10p30, phi_10p25, phi_10p00 ])
##Lxs  = np.array([ Lx_10p50, Lx_10p33, Lx_10p30, Lx_10p25, Lx_10p00 ])
##plt.plot(np.arange(5),phis/np.amax(phis)) 
##plt.plot(np.arange(5),Lxs/np.amax(Lxs), c='r') 
##plt.show()
