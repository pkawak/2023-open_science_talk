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

labels = 1
shade  = 1
fit    = 1
crit   = 1

phi_min = 0.375
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

phi_cryst = 0.440
T_IC_scat   = T_scat[phi_scat > phi_cryst]
phi_IC_scat = phi_scat[phi_scat > phi_cryst]
T_IN_scat   = T_scat[phi_scat < phi_cryst]
phi_IN_scat = phi_scat[phi_scat < phi_cryst]

ax.scatter(T_IN_scat, phi_IN_scat, color='r', marker='+', zorder=2, label=r"$T_{\mathrm{IN}}(N_{c}=125)$")
ax.scatter(T_IC_scat, phi_IC_scat, color='r', marker='*', zorder=2, label=r"$T_{\mathrm{IC}}(N_{c}=125)$")

# old stuff:
Ts_90_files = "90x10_Ts.mod.out"
df_90 = pd.read_csv(Ts_90_files, index_col=False, delimiter=' ')
df_90['Tr']  = df_90['Tm']/df_90['kb']
df_90['phi'] = 90*Nb*sigma**3/df_90['Lx']**3*np.pi/6
phi_90_scat  = df_90['phi'].to_numpy()
T_90_scat    = df_90['Tr'].to_numpy()
#ax.scatter(T_90_scat, phi_90_scat, color='m', zorder=2)

phi_90_cryst = 0.42
T_IC_90_scat   = T_90_scat[phi_90_scat > phi_90_cryst]
phi_IC_90_scat = phi_90_scat[phi_90_scat > phi_90_cryst]
T_90_scat   = T_90_scat[phi_90_scat < phi_90_cryst]
phi_90_scat = phi_90_scat[phi_90_scat < phi_90_cryst]
print(phi_90_scat)

ax.scatter(T_90_scat   , phi_90_scat   , color='b', marker='+', zorder=2, alpha=0.4, label=r"$T_{\mathrm{IN}}(N_{c}=90)$")
ax.scatter(T_IC_90_scat, phi_IC_90_scat, color='b', marker='*', zorder=2, alpha=0.4, label=r"$T_{\mathrm{IC}}(N_{c}=90)$")

if fit:
  slope_IC, intercept_IC, r_value_IC, p_value_IC, std_err_IC = stats.linregress(phi_IC_scat, T_IC_scat)
  phi_IC_line = np.linspace(phi_cryst, phi_max, 1001)
  T_IC_line   = phi_IC_line*slope_IC + intercept_IC

  model_IC = np.poly1d(np.polyfit(phi_IC_scat, T_IC_scat, 3))
  phi_IC_quad = phi_IC_line
  T_IC_quad = model_IC(phi_IC_quad)
  
  #phi_IC_model = phi_IC_quad
  #T_IC_model = T_IC_quad
  phi_IC_model = phi_IC_line
  T_IC_model = T_IC_line

  ax.plot(T_IC_model, phi_IC_model, color='g', zorder=1)

  slope_IN, intercept_IN, r_value_IN, p_value_IN, std_err_IN = stats.linregress(phi_IN_scat[0:-1], T_IN_scat[0:-1])
  phi_IN_line = np.linspace(phi_min, phi_cryst, 1001)
  T_IN_line   = phi_IN_line*slope_IN + intercept_IN

  model_IN = np.poly1d(np.polyfit(phi_IN_scat, T_IN_scat, 3))
  phi_IN_quad = phi_IN_line
  T_IN_quad = model_IN(phi_IN_quad)
  
  #phi_IN_model = phi_IN_quad
  #T_IN_model = T_IN_quad
  phi_IN_model = phi_IN_line
  T_IN_model = T_IN_line

  ax.plot(T_IN_model, phi_IN_model, color='g', zorder=1)

if crit:
  ax.plot([T_min, model_IN(phi_cryst)], [phi_cryst, phi_cryst], ls='--', color='#00008b', zorder=1)

# print Tcryst
T_cryst_IN = model_IN(phi_cryst)
T_cryst_IC = model_IC(phi_cryst)
print(T_cryst_IN,T_cryst_IC,(T_cryst_IN+T_cryst_IC)/2)

if labels:
  ax.text(0.72, 0.46 , 'Melt'   , weight='bold', color='k', fontsize=12, fontname='dejavusans', transform = ax.transAxes)
  ax.text(0.20, 0.75, 'Crystal', weight='bold', color='k', fontsize=12, fontname='dejavusans', transform = ax.transAxes)
  ax.text(0.10, 0.24, 'Nematic', weight='bold', color='k', fontsize=12, fontname='dejavusans', transform = ax.transAxes)

if shade:
  phi_below=[]
  i = 0
  region_1 = np.linspace(T_min, model_IN(phi_cryst), 1001)
  for i in range(len(region_1)):
    if region_1[i] < T_IN_model[0]:
      phi_below.append(0.35)
    else:
      idx = (np.abs(T_IN_model-region_1[i])).argmin()
     # print(region_1[i], idx, T_IN_model[idx])
      phi_below.append(phi_IN_model[idx])
  ax.fill_between(region_1, phi_below, phi_cryst, color=['#FFC947'], alpha=0.7)
  
  phi_below_2=[]
  i = 0
  region_2 = np.linspace(T_min, T_max, 1001)
  for i in range(len(region_2)):
    if region_2[i] < T_IC_model[0]:
      phi_below_2.append(phi_cryst)
    else:
      idx = (np.abs(T_IC_model-region_2[i])).argmin()
      phi_IC_model_i = phi_IC_model[idx]
      if phi_IC_model_i < phi_cryst:
        phi_below_2.append(phi_cryst)
      else:
        phi_below_2.append(phi_IC_model_i)
  ax.fill_between(region_2, phi_below_2, phi_max, color=['#185ADB'], alpha=0.5)
  
  phi_above_3=[]
  i = 0
  region_3 = np.linspace(T_min, T_max, 1001)
  for i in range(len(region_2)):
    if region_3[i] > T_IN_model[-1]:
      idx = (np.abs(T_IC_model-region_3[i])).argmin()
      phi_above_3.append(phi_IC_model[idx])
    else:
      idx = (np.abs(T_IN_model-region_3[i])).argmin()
      phi_above_3.append(phi_IN_model[idx])
  ax.fill_between(region_3, phi_min, phi_above_3, color=['#EFEFEF'], alpha=0.5)

ax.set_xlabel(r"$T_{r}$", fontsize=10, labelpad=6)#, labelpad=0.3)
ax.set_ylabel(r"$\phi$", fontsize=10, labelpad=5.5)
ax.tick_params(axis='both', labelsize=8)
ax.set_xlim(T_min, T_max)
ax.set_ylim(phi_min, phi_max)
ax.legend(loc='lower right', fontsize=8, handletextpad=0.01)
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
