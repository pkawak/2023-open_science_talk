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

labels  = 1
shade   = 1
fit     = 1
crit    = 1
scatter = 0

phi_min = 0.3
phi_max = 0.5
T_min = 0.0
T_max = 0.3

label_prefix = r'$\phi=$'

# get data
df = pd.read_csv(Ts_files, index_col=False, delimiter=' ')
df['Tr']  = df['Tm']/df['kb']
df['Tr2']  = df['Tm2']/df['kb']
df['phi'] = Nc*Nb*sigma**3/df['Lx']**3*np.pi/6
df_HTH  = df[df['dir'].str.contains("HTH_kb1.00")]
phi_scat  = df_HTH['phi'].to_numpy()
T_1_scat  = df_HTH['Tr'].to_numpy()
T_2_scat  = df_HTH['Tr2'].to_numpy()

phi_cryst = 0.31

T_IC_scat = T_2_scat
phi_IC_scat = phi_scat
T_IC_scat[T_IC_scat < 0.0001] = 0.0001
T_IC_scatt   = T_2_scat[phi_scat > phi_cryst]
phi_IC_scatt = phi_scat[phi_scat > phi_cryst]
T_scat      = T_1_scat

fig, ax = plt.subplots(1, figsize=(3.25,3.1))
# plot points
if scatter:
  ax.scatter(T_scat    , phi_scat    , color='g', marker="+", zorder=3, label="IN")
  ax.scatter(T_IC_scatt, phi_IC_scatt, color='r', marker="*", zorder=3, label="IC")

if fit:
  slope_IN, intercept_IN, r_value_IN, p_value_IN, std_err_IN = stats.linregress(phi_scat, T_scat)
  phi_IN_line = np.linspace(phi_min, phi_max, 1000)
  T_IN_line   = phi_IN_line*slope_IN + intercept_IN

  model_IN = np.poly1d(np.polyfit(phi_scat, T_scat, 3))
  phi_IN_quad = phi_IN_line
  T_IN_quad = model_IN(phi_IN_quad)
  
  slope_IC, intercept_IC, r_value_IC, p_value_IC, std_err_IC = stats.linregress(phi_IC_scat, np.log(T_IC_scat))
  phi_IC_line = np.linspace(phi_min, phi_max, 1000)
  T_IC_line   = np.exp(phi_IC_line*slope_IC + intercept_IC)
#  print("logT/a-b/a")
#  print("1/a" , 1/slope_IC)
#  print("-b/a", -intercept_IC/slope_IC)

  model_IC = np.poly1d(np.polyfit(phi_IC_scat, T_IC_scat, 3))
  phi_IC_quad = phi_IN_line
  T_IC_quad = model_IC(phi_IC_quad)

  phi_IN_model = phi_IN_line#phi_quad
  T_IN_model   = T_IN_line#T_quad
  phi_IC_model = phi_IC_line#phi_IC_quad
  T_IC_model   = T_IC_line#T_IC_quad

  T_IN_model[T_IC_model > T_IN_model] = T_IC_model[T_IC_model > T_IN_model]

  keep_idx = phi_IC_model > phi_cryst
  T_IC_model = T_IC_model[keep_idx]
  phi_IC_model = phi_IC_model[keep_idx]
  ax.plot(T_IN_model   , phi_IN_model   , color='g', zorder=2, label="IN")
  ax.plot(T_IC_model, phi_IC_model, color='r', zorder=2, label="IC")

if crit:
  ax.plot([T_min, model_IN(phi_cryst)], [phi_cryst, phi_cryst], ls='--', color='#00008b', zorder=1)


if labels:
  ax.text(0.63, 0.13, 'Isotropic (I)', weight='bold', color='k', fontsize=10, fontname='dejavusans', transform = ax.transAxes)
  ax.text(0.18, 0.90, 'Crystal (C)'  , weight='bold', color='k', fontsize=10, fontname='dejavusans', transform = ax.transAxes)
  ax.text(0.06, 0.45, 'Nematic'  , weight='bold', color='k', fontsize=10, fontname='dejavusans', transform = ax.transAxes)
  ax.text(0.12, 0.39, '(N)'  , weight='bold', color='k', fontsize=10, fontname='dejavusans', transform = ax.transAxes)

if shade:
  phi_below=[]
  i = 0
  region_1 = np.linspace(T_min, T_max, 100)
  for i in range(len(region_1)):
    idx = (np.abs(T_IC_model-region_1[i])).argmin()
    if idx == len(phi_IC_model)-1:
      idx = (np.abs(T_IN_model-region_1[i])).argmin()
      phi_below.append(phi_IN_model[idx])
      continue
    phi_below.append(phi_IC_model[idx])
  ax.fill_between(region_1[:len(phi_below)], phi_below, phi_max, color=['#185ADB'], alpha=0.5)
  
  phi_below_2=[]
  phi_above_2=[]
  i = 0
  region_2 = np.linspace(T_min, T_max, 100)
  for i in range(len(region_2)):
    idx1 = (np.abs(T_IN_model-region_2[i])).argmin()
    idx2 = (np.abs(T_IC_model-region_2[i])).argmin()
    if idx1 == len(phi_IN_model)-1:
      continue
    if idx2 == len(phi_IC_model)-1:
      continue
    phi_below_2.append(phi_IN_model[idx1])
    phi_above_2.append(phi_IC_model[idx2])
  ax.fill_between(region_2[:len(phi_below_2)], phi_below_2, phi_above_2, color=['#FFC947'], alpha=0.7)
  
  ax.fill_between(T_IN_model, phi_min, phi_IN_model, color=['#EFEFEF'], alpha=0.5)

ax.set_xlabel(r"$T_{r}$", fontsize=12, labelpad=6)#, labelpad=0.3)
ax.set_ylabel(r"$\phi$", fontsize=12, labelpad=5.5)
ax.tick_params(axis='both', labelsize=10, pad=0)
ax.set_xticks([0,0.1,0.2, 0.3, 0.4])
ax.set_yticks([0.30, 0.35, 0.40, 0.45, 0.50])
ax.set_xlim(T_min, T_max)
ax.set_ylim(0.30, 0.50)
ax.set_yticks([0.3, 0.4, 0.5])

plt.subplots_adjust(left=0.158, top=0.983, bottom=0.13, right=0.969)
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
