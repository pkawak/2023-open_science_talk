#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
created on Tue May 3 08:41:00 2022

@author: pierrekawak
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import pandas as pd

Nc    = 125
Nb    = 10
sigma = 1

labels = 0
shade  = 1
fit    = 1
crit   = 0

kb_min = 0.09
kb_max = 11 #phi_A+0.2
T_min = 0.01
T_max = 1.3

WL_Ts_files = np.array([
                     "../Lx11.000_kb0.10_WLMC_Ts.out", "../Lx11.000_kb1.00_WLMC_Ts.out", "../Lx11.000_kb10.0_WLMC_Ts.out",
                     "../Lx11.436_kb0.10_WLMC_Ts.out", "../Lx11.436_kb1.00_WLMC_Ts.out", "../Lx11.436_kb10.0_WLMC_Ts.out",
                     "../Lx13.000_kb0.10_WLMC_Ts.out", "../Lx13.000_kb1.00_WLMC_Ts.out", "../Lx13.000_kb10.0_WLMC_Ts.out",
                     "../Lx15.000_kb0.10_WLMC_Ts.out", "../Lx15.000_kb1.00_WLMC_Ts.out", "../Lx15.000_kb10.0_WLMC_Ts.out"
                 ,    "../Lx11.200_kb1.00_WLMC_Ts.out", "../Lx11.800_kb1.00_WLMC_Ts.out", "../Lx12.500_kb1.00_WLMC_Ts.out", "../Lx13.500_kb1.00_WLMC_Ts.out"
                    ])
Lx_      = [11, 11.436, 13, 15]
Lx_      = np.repeat(Lx_, 3)
Lx_      = np.append(Lx_, [11.2, 11.8, 12.5, 13.5])
phi_     = Nc*Nb*sigma**3/Lx_**3*np.pi/6
kb_      = [0.1, 1, 10]
kb_      = np.tile(kb_, 4)
kb_      = np.append(kb_, [1,1,1,1])

input_df = pd.DataFrame({'Ts_files': WL_Ts_files, 'Lx': Lx_, 'phi': phi_, 'kb': kb_})

T_scat = []
T_IC_scat = []
kb_scat = []
kb_scat = []
kb_IC_scat = []
now_df = input_df
now_df = input_df.loc[input_df['Lx'] == 11.000]

for i in range(len(now_df)):
 # print(now_df['Ts_files'].iat[i])
  Ts_data_A = np.loadtxt(now_df['Ts_files'].iat[i], skiprows=1, ndmin=2)
  if len(Ts_data_A) == 2:
    T_scat.append(Ts_data_A[:,0][1])
    T_IC_scat.append(Ts_data_A[:,0][0])
    kb_scat.append(now_df['kb'].iat[i])
    kb_IC_scat.append(now_df['kb'].iat[i])
  elif len(Ts_data_A) == 1:
    T_scat.append(Ts_data_A[:,0][0])
    kb_scat.append(now_df['kb'].iat[i])

fig, ax = plt.subplots(1, figsize=(3.25,3.1))
# plot points
ax.scatter(T_scat   , kb_scat   , color='g', marker="_", zorder=3, label="IN")
ax.scatter(T_IC_scat, kb_IC_scat, color='r', marker="*", zorder=3, label="IC")

if fit:
  slope, intercept, r_value, p_value, std_err = stats.linregress(kb_scat, np.log10(T_scat))
  kb_line = np.linspace(kb_min, kb_max, 1000)
  T_line   = 10**(kb_line*slope + intercept)

  one = max(len(kb_scat)-2, 1)
  print(one)
  model = np.poly1d(np.polyfit(kb_scat, T_scat, 2))#one))
  kb_quad = np.linspace(kb_min, kb_max, 1000)
  T_quad = model(kb_quad)

  slope_IC, intercept_IC, r_value_IC, p_value_IC, std_err_IC = stats.linregress(kb_IC_scat, T_IC_scat)
  kb_IC_line = np.linspace(kb_min, kb_max, 1000)
  T_IC_line   = kb_IC_line*slope_IC + intercept_IC

  one = max(len(kb_IC_scat)-3, 1)
  model_IC = np.poly1d(np.polyfit(kb_IC_scat, T_IC_scat, 2))
  kb_IC_quad = np.linspace(kb_min, kb_max, 1000)
  T_IC_quad = model_IC(kb_IC_quad)
  
  kb_model = kb_quad
  T_model = T_quad
  kb_IC_model = kb_IC_quad
  T_IC_model = T_IC_quad

  for i in range(len(T_IC_model)-1):
    if T_IC_model[i+1] < T_IC_model[i]:
      T_IC_model[i+1] = T_IC_model[i]
  ax.plot(T_model   , kb_model   , color='g', zorder=2, label="IN")
  ax.plot(T_IC_model, kb_IC_model, color='r', zorder=2, label="IC")

if labels:
  ax.text(0.68, 0.30 , 'Melt'   , weight='bold', color='k', fontsize=12, fontname='dejavusans', transform = ax.transAxes)
  ax.text(0.25, 0.81, 'Crystal', weight='bold', color='k', fontsize=12, fontname='dejavusans', transform = ax.transAxes)
  ax.text(0.15, 0.43, 'Nematic', weight='bold', color='k', fontsize=12, fontname='dejavusans', transform = ax.transAxes)

if shade:
  kb_below=[]
  i = 0
  region_1 = np.linspace(T_min, T_max, 1000)
  for i in range(len(region_1)):
    idx = (np.abs(T_IC_model-region_1[i])).argmin()
    if T_IC_model[idx] == np.amax(T_IC_model):
      continue
    kb_below.append(kb_IC_model[idx])
  region_1 = region_1[:len(kb_below)]
  ax.fill_between(region_1, kb_below, kb_max, color=['#FFC947'], alpha=0.5)

  kb_below_2=[]
  kb_above_2=[]
  i = 0
  region_2 = np.linspace(T_min, T_max, 1000)
  for i in range(len(region_2)):
    idx_ = (np.abs(T_model-region_2[i])).argmin()
    if T_model[idx] == np.amax(T_model):
      continue
    kb_below_2.append(kb_model[idx_])
    
    idx = (np.abs(T_IC_model-region_2[i])).argmin()
    if T_IC_model[idx] == np.amax(T_IC_model):
      kb_above_2.append(kb_max)
      continue
    kb_above_2.append(kb_IC_model[idx])

      
#    if i == len(region_2)-1:
#    print(region_2[i], T_model[idx], T_IC_model[idx])
#    print(region_2[i], "from:", kb_below_2[i], kb_above_2[i])
  region_2 = region_2[:len(kb_below_2)]
  ax.fill_between(region_2, kb_below_2, kb_above_2, color=['#185ADB'], alpha=0.5)
  
#  ax.fill_between(T_model, kb_min, kb_model, color=['#EFEFEF'], alpha=0.7)

ax.set_xlabel(r"$kT/\epsilon$", fontsize=10, labelpad=6)#, labelpad=0.3)
ax.set_ylabel(r"$k_{b}$", fontsize=10, labelpad=5.5)
ax.tick_params(axis='both', labelsize=8)
ax.set_xlim(T_min, T_max)
ax.set_ylim(kb_min, kb_max)
ax.set_yscale('log')
ax.set_xscale('log')

plt.subplots_adjust(left=0.18, top=0.98, bottom=0.135, right=0.974)
plt.savefig("subfig-phase_diag-Lx_11.000.pdf")
plt.close()
