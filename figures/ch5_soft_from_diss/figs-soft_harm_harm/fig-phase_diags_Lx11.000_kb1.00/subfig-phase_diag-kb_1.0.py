#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
created on Tue May 3 08:41:00 2022

@author: pierrekawak
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter, NullFormatter
from scipy import stats
import pandas as pd

def make_patch_spines_invisible(ax):
    ax.set_frame_on(True)
    ax.patch.set_visible(False)
    for sp in ax.spines.values():
        sp.set_visible(False)

Nc       = 125
Nb       = 10
sigma    = 1

labels = 1
shade  = 1
fit    = 1
crit   = 0

phi_min = 0.25#np.round(Nc*Nb*sigma**3/15**3*np.pi/6, 3)
phi_max = 0.55
T_min = 0.0
T_max = 0.21

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

#phase diagram time
def makePhaseDiag(kb_A, Lx_A, figname, mod=0):
  if mod == 0:
    T_min = 0.0
    T_max = 0.2
  else:
    T_min = 0.0
    T_max = 2.0
  
  T_IN_scat = []
  T_IC_scat = []
  kb_scat = []
  kb_IN_scat = []
  kb_IC_scat = []
  fig, ax = plt.subplots(1, figsize=(3.25,3.1))
  now_df = input_df
  if kb_A == 0:
    now_df = input_df.loc[input_df['Lx'] == Lx_A]
  else:
    now_df = input_df.loc[input_df['kb'] == kb_A]

  for i in range(len(now_df)):
   # print(now_df['Ts_files'].iat[i])
    Ts_data_A = np.loadtxt(now_df['Ts_files'].iat[i], skiprows=1, ndmin=2)
  #  print(Ts_data_A)
    if len(Ts_data_A) > 0:
#      Ts_data_A[:,0] /= now_df['kb'].iat[i]
      if len(Ts_data_A) == 2:
        T_IN_scat.append(Ts_data_A[:,0][1])
        T_IC_scat.append(Ts_data_A[:,0][0])
        if kb_A == 0:
          kb_IN_scat.append(now_df['kb'].iat[i])
          kb_IC_scat.append(now_df['kb'].iat[i])
        else:
          kb_IN_scat.append(now_df['phi'].iat[i])
          kb_IC_scat.append(now_df['phi'].iat[i])
      elif len(Ts_data_A) == 1:
        T_IN_scat.append(Ts_data_A[:,0][0])
        if kb_A == 0:
          kb_IN_scat.append(now_df['kb'].iat[i])
        else:
          kb_IN_scat.append(now_df['phi'].iat[i])
    if kb_A == 0:
      kb_scat.append(now_df['kb'].iat[i])
    else:
      kb_scat.append(now_df['phi'].iat[i])

  if kb_A == 0: 
    kb_min = 0.05
    kb_max = 15 #phi_A+0.2
    kb_lim_max = kb_max
  else:
    kb_min = 0.2
    kb_max = 0.8 #phi_A+0.2
    kb_lim_max = 0.55

  if len(kb_IN_scat) > 0:
    one = max(len(kb_IN_scat)-2, 1)
    model_IN = np.poly1d(np.polyfit(kb_IN_scat, T_IN_scat, one))#one))
    kb_IN_quad = np.linspace(kb_min, kb_max, 1000)
    T_IN_quad = model_IN(kb_IN_quad)

    slope_IN, intercept_IN, r_value_IN, p_value_IN, std_err_IN = stats.linregress(kb_IN_scat, T_IN_scat)
    kb_IN_line = np.linspace(kb_min, kb_max, 1000)
    T_IN_line   = kb_IN_line*slope_IN + intercept_IN

  else:
    kb_below_2=[]
    i = 0
    region_2 = np.linspace(T_min, T_max, 100)
    ax.fill_between(region_2, kb_min, kb_max, color=['#EFEFEF'], alpha=0.5)
    
    ax.tick_params(axis='both', labelsize=6)
    ax.set_xlim(T_min, T_max)
    ax.set_ylim(kb_min, kb_max)
    if kb_A == 0:
      ax.set_yscale('log')
    ax.yaxis.set_major_formatter(ScalarFormatter())
    plt.subplots_adjust(left=0.18, top=0.98, bottom=0.135, right=0.974)
    plt.savefig(figname)
    plt.close()
    return
  
  no_cryst = 0
  if len(kb_IC_scat) > 0:
    one = max(len(kb_IC_scat)-3, 1)
    model_IC = np.poly1d(np.polyfit(kb_IC_scat, T_IC_scat, one))
    kb_IC_quad = np.linspace(kb_min, kb_max, 1000)
    T_IC_quad = model_IC(kb_IC_quad)
    no_cryst = 1

    slope_IC, intercept_IC, r_value_IC, p_value_IC, std_err_IC = stats.linregress(kb_IC_scat, T_IC_scat)
    kb_IC_line = np.linspace(kb_min, kb_max, 1000)
    T_IC_line   = kb_IC_line*slope_IC + intercept_IC
  
  kb_IN_model = kb_IN_quad
  T_IN_model = T_IN_quad
  if len(kb_IC_scat) > 0:
    kb_IC_model = kb_IC_quad
    T_IC_model = T_IC_quad

  kb_IN_model = kb_IN_line
  T_IN_model = T_IN_line
  #if len(kb_IC_scat) > 0:
  #  kb_IC_model = kb_IC_line
  #  T_IC_model = T_IC_line
  
  if kb_A == 0:
    kb_below=[]
    kb_above=[]
    i = 0
    region_1 = np.linspace(T_min, T_max, 100)
    for i in range(len(region_1)):
      if no_cryst != 0:
        idx = (np.abs(T_IC_model-region_1[i])).argmin()
        kb_below.append(kb_IC_model[idx])
      idx = (np.abs(T_IN_model-region_1[i])).argmin()
      kb_above.append(kb_IN_model[idx])
    if no_cryst == 0:
      ax.fill_between(region_1, kb_min, kb_above, color=['#185ADB'], alpha=0.5)
    else:
      ax.fill_between(region_1, kb_below, kb_above, color=['#185ADB'], alpha=0.5)
    
    kb_below_2=[]
    i = 0
    region_2 = np.linspace(T_min, T_max, 100)
    for i in range(len(region_2)):
      idx = (np.abs(T_IN_model-region_2[i])).argmin()
      kb_below_2.append(kb_IN_model[idx])
    ax.fill_between(region_2, kb_below_2, kb_max, color=['#EFEFEF'], alpha=0.5)
    
    kb_above_3=[]
    i = 0
    region_3 = np.linspace(T_min, T_max, 100)
    for i in range(len(region_3)):
      if no_cryst != 0:
        idx = (np.abs(T_IC_model-region_3[i])).argmin()
        kb_above_3.append(kb_IC_model[idx])
    #ax.fill_between(region_2, kb_min, kb_max, color=['#185ADB'], alpha=0.5)
    if no_cryst != 0:
      ax.fill_between(region_3, kb_min, kb_above_3, color=['#FFC947'], alpha=0.7)
  else:
    kb_below=[]
    i = 0
    region_1 = np.linspace(T_min, T_max, 100)
    for i in range(len(region_1)):
      idx = (np.abs(T_IC_model-region_1[i])).argmin()
      kb_below.append(kb_IC_model[idx])
    ax.fill_between(region_1, kb_below, kb_max, color=['#FFC947'], alpha=0.7)

    kb_below_2=[]
    kb_above_2=[]
    i = 0
    region_2 = np.linspace(T_min, T_max, 100)
    for i in range(len(region_2)):
      idx = (np.abs(T_IN_model-region_2[i])).argmin()
      kb_below_2.append(kb_IN_model[idx])
      idx = (np.abs(T_IC_model-region_2[i])).argmin()
      kb_above_2.append(kb_IC_model[idx])
    ax.fill_between(region_2, kb_below_2, kb_above_2, color=['#185ADB'], alpha=0.5)

    ax.fill_between(T_IN_model, kb_min, kb_IN_model, color=['#EFEFEF'], alpha=0.5)

  ax.plot(T_IN_model, kb_IN_model, color='g', label="IN", zorder=1)
  if no_cryst != 0:
    ax.plot(T_IC_model, kb_IC_model, color='r', label="IC", zorder=1)
  ax.scatter(T_IN_scat, kb_IN_scat, color='g', label="IN", zorder=2)
  ax.scatter(T_IC_scat, kb_IC_scat, color='r', label="IC", zorder=2)
  ax.set_xlim(T_min, T_max)
  ax.set_ylim(kb_min, kb_lim_max)
  if kb_A == 0:
    ax.set_yscale('log')
  ax.yaxis.set_major_formatter(ScalarFormatter())
  if mod == 0:
#    ax.set_xlim(T_min, T_max)
#    ax.set_ylim(phi_min, phi_max)
  
    ax.set_xticks([0, 0.05, 0.1, 0.15])
    ax.set_ylabel(r"$\phi$", fontsize=10, labelpad=5.5)
  elif mod == 1:
#    ax.set_xlim(T_min, T_max)
#    ax.set_ylim(phi_min, phi_max)

    ax.set_xlabel(r"$T_{r}$", fontsize=10, labelpad=6)#, labelpad=0.3)
    ax.set_ylabel(r"$k_{b}$", fontsize=10, labelpad=5.5)

  ax.tick_params(axis='both', labelsize=8)
  plt.subplots_adjust(left=0.18, top=0.98, bottom=0.135, right=0.974)
  #plt.show()
  #sys.exit()
  plt.savefig(figname)
  plt.close()

makePhaseDiag(0, 11.000, "subfig-Lx_11.000.pdf", 1)
#makePhaseDiag(0, 11.436, "subfig-Lx_11.436.pdf", 0)
#makePhaseDiag(0, 13.000, "subfig-Lx_13.000.pdf", 0)
#makePhaseDiag(0, 15.000, "subfig-Lx_15.000.pdf", 0)
#makePhaseDiag(0.1, 0, "subfig-kb_0.1.pdf", 3)
makePhaseDiag(1.0, 0, "subfig-kb_1.0.pdf", 0)
#makePhaseDiag(10., 0, "subfig-kb_10..pdf", 2)
