#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
created on Sat May 22 08:41:00 2021

@author: pierrekawak
"""

import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import pandas as pd

Nc       = 125
Nb       = 10
sigma    = 1
Ts_files = "Ts.out"
Lx_crit  = (11.157216+11.436146)/2
phi_crit = Nc*Nb*sigma**3/Lx_crit**3*np.pi/6

labels = 1
shade  = 1
fit    = 1
crit   = 1

phi_min = 0.38
phi_max = 0.50
T_min = 0.0
T_max = 0.5

# get data
df = pd.read_csv(Ts_files, index_col=False, delimiter=' ')
df['Tr']  = df['Tm']/df['kb']
df['phi'] = Nc*Nb*sigma**3/df['Lx']**3*np.pi/6
df_SandP  = df[df['dir'].str.contains("SandP_")]
df_SandP  = df_SandP.loc[df['kb'] == 1]
phi_scat  = df_SandP['phi'].to_numpy()
T_scat    = df_SandP['Tr'].to_numpy()

fig, ax = plt.subplots(1, figsize=(3.25,3.1))
# plot points
ax.scatter(T_scat, phi_scat, color='r', zorder=2)

if fit:
  slope, intercept, r_value, p_value, std_err = stats.linregress(phi_scat, T_scat)
  phi_line = np.linspace(phi_min, phi_max, 1001)
  T_line   = phi_line*slope + intercept

  model = np.poly1d(np.polyfit(phi_scat, T_scat, 3))
  phi_quad = phi_line
  T_quad = model(phi_quad)
  
  #phi_model = phi_quad
  #T_model = T_quad
  phi_model = phi_line
  T_model = T_line

  ax.plot(T_model, phi_model, color='g', zorder=1)

if crit:
  ax.plot([T_min, model(phi_crit)], [phi_crit, phi_crit], ls='--', color='#00008b', zorder=1)

if labels:
  ax.text(0.72, 0.46 , 'Melt'   , weight='bold', color='k', fontsize=12, fontname='dejavusans', transform = ax.transAxes)
  ax.text(0.20, 0.80, 'Crystal', weight='bold', color='k', fontsize=12, fontname='dejavusans', transform = ax.transAxes)
  ax.text(0.10, 0.30, 'Nematic', weight='bold', color='k', fontsize=12, fontname='dejavusans', transform = ax.transAxes)

if shade:
  phi_below=[]
  i = 0
  region_1 = np.linspace(T_min, model(phi_crit), 1001)
  for i in range(len(region_1)):
    if region_1[i] < T_model[0]:
      phi_below.append(0.35)
    else:
      idx = (np.abs(T_model-region_1[i])).argmin()
     # print(region_1[i], idx, T_model[idx])
      phi_below.append(phi_model[idx])
  ax.fill_between(region_1, phi_below, phi_crit, color=['#FFC947'], alpha=0.7)
  
  phi_below_2=[]
  i = 0
  region_2 = np.linspace(T_min, T_max, 1001)
  for i in range(len(region_2)):
    if region_2[i] < T_model[0]:
      phi_below_2.append(phi_crit)
    else:
      idx = (np.abs(T_model-region_2[i])).argmin()
      phi_model_i = phi_model[idx]
      if phi_model_i < phi_crit:
        phi_below_2.append(phi_crit)
      else:
        phi_below_2.append(phi_model_i)
  ax.fill_between(region_2, phi_below_2, phi_max, color=['#185ADB'], alpha=0.5)
  
  if T_model[-1] < T_max:
#    ax.fill_between([T_model[-1]+0.004, T_max], phi_min, phi_max, color=['#EFEFEF'], alpha=0.5)
    ax.fill_between(np.append(T_model, [T_model[-1]+0.004, T_max]), phi_min, np.append(phi_model, [phi_max, phi_max]), color=['#EFEFEF'], alpha=0.5)
  else:
    ax.fill_between(T_model, phi_min, phi_model, color=['#EFEFEF'], alpha=0.5)

ax.set_xlabel(r"$T_{r}$", fontsize=10, labelpad=6)#, labelpad=0.3)
ax.set_ylabel(r"$\phi$", fontsize=10, labelpad=5.5)
ax.tick_params(axis='both', labelsize=8)
ax.set_xlim(T_min, T_max)
ax.set_ylim(phi_min, phi_max)
#ax.set_yticks([0.35, 0.4, 0.45, 0.5, 0.55])
ax.set_yticks([0.38, 0.42, 0.46, 0.5])

plt.subplots_adjust(left=0.18, top=0.98, bottom=0.135, right=0.974)
#plt.show()
#sys.exit()
plt.savefig("fig-phase_diag.pdf")
plt.close()
#left, width = .25, .5
#bottom, height = .25, .5
#right = left + width
#top = bottom + height
#ax.text(0.5 * (left + right), 0.5 * (bottom + top), 'middle',
#        horizontalalignment='center',
#        verticalalignment='center',
#        transform=ax.transAxes)
