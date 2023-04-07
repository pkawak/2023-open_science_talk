#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
created on Tue May 3 08:41:00 2022

@author: pierrekawak
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter, NullFormatter
import pandas as pd
from scipy import stats

def make_patch_spines_invisible(ax):
    ax.set_frame_on(True)
    ax.patch.set_visible(False)
    for sp in ax.spines.values():
        sp.set_visible(False)

Nc    = 125
Nb    = 10
sigma = 1
phi_prefix = r'$\phi=$'
kb_prefix = r'$k_{b}=$'
names_in_WL = ["T", "Em", "Cv", "q6", "P2", "n6", "r2e", "r2g", "sms"]

WL_result_files = np.array([
                     "../Lx11.000_kb0.10_WLMC_results.out", "../Lx11.000_kb1.00_WLMC_results.out", "../Lx11.000_kb10.0_WLMC_results.out",
                     "../Lx11.436_kb0.10_WLMC_results.out", "../Lx11.436_kb1.00_WLMC_results.out", "../Lx11.436_kb10.0_WLMC_results.out",
                     "../Lx13.000_kb0.10_WLMC_results.out", "../Lx13.000_kb1.00_WLMC_results.out", "../Lx13.000_kb10.0_WLMC_results.out",
                     "../Lx15.000_kb0.10_WLMC_results.out", "../Lx15.000_kb1.00_WLMC_results.out", "../Lx15.000_kb10.0_WLMC_results.out"
                 ,    "../Lx11.200_kb1.00_WLMC_results.out", "../Lx11.800_kb1.00_WLMC_results.out", "../Lx12.500_kb1.00_WLMC_results.out", "../Lx13.500_kb0.10_WLMC_results.out"
                 ,    "../Lx10.800_kb1.00_WLMC_results.out", "../Lx10.850_kb1.00_WLMC_results.out", "../Lx0.900_kb1.00_WLMC_results.out", "../Lx0.950_kb0.10_WLMC_results.out"
                    ])
WL_Ts_files = np.array([
                     "../Lx11.000_kb0.10_WLMC_Ts.out", "../Lx11.000_kb1.00_WLMC_Ts.out", "../Lx11.000_kb10.0_WLMC_Ts.out",
                     "../Lx11.436_kb0.10_WLMC_Ts.out", "../Lx11.436_kb1.00_WLMC_Ts.out", "../Lx11.436_kb10.0_WLMC_Ts.out",
                     "../Lx13.000_kb0.10_WLMC_Ts.out", "../Lx13.000_kb1.00_WLMC_Ts.out", "../Lx13.000_kb10.0_WLMC_Ts.out",
                     "../Lx15.000_kb0.10_WLMC_Ts.out", "../Lx15.000_kb1.00_WLMC_Ts.out", "../Lx15.000_kb10.0_WLMC_Ts.out"
                 ,    "../Lx11.200_kb1.00_WLMC_Ts.out", "../Lx11.800_kb1.00_WLMC_Ts.out", "../Lx12.500_kb1.00_WLMC_Ts.out", "../Lx13.500_kb1.00_WLMC_Ts.out"
                 ,    "../Lx10.800_kb1.00_WLMC_Ts.out", "../Lx10.850_kb1.00_WLMC_Ts.out", "../Lx10.900_kb1.00_WLMC_Ts.out", "../Lx10.950_kb1.00_WLMC_Ts.out"
                    ])
Lx_      = [11, 11.436, 13, 15]
Lx_      = np.repeat(Lx_, 3)
Lx_      = np.append(Lx_, [11.2, 11.8, 12.5, 13.5, 10.8, 10.85, 10.9, 10.95])
phi_     = Nc*Nb*sigma**3/Lx_**3*np.pi/6
kb_      = [0.1, 1, 10]
kb_      = np.tile(kb_, 4)
kb_      = np.append(kb_, [1,1,1,1, 1,1,1,1])

input_df = pd.DataFrame({'result_files': WL_result_files, 'Ts_files': WL_Ts_files, 'Lx': Lx_, 'phi': phi_, 'kb': kb_})

def makeWLMCFigure(kb_A, Lx_A, figname, mod=0):
  fig, ax = plt.subplots(1, 1, figsize=(1.625,1.5))
  phi_A         = np.round(Nc*Nb*sigma**3/Lx_A**3*np.pi/6, 3)
  WL_A_file     = input_df.loc[(input_df['kb'] == kb_A) & (input_df['Lx'] == Lx_A)]['result_files'].iat[0]
  WL_A_df       = pd.read_csv(WL_A_file, index_col=False, delimiter=' ', names=names_in_WL)
  WL_A_df['Tr'] = WL_A_df['T']/kb_A
  WL_A_df       = WL_A_df.loc[WL_A_df['Tr'] > 0.02]
  WL_A_df       = WL_A_df.loc[WL_A_df['Tr'] < 0.2]
  multiplier = 1/Nc #/Nb
  #ax[0].plot(WL_A_df["Tr"], WL_A_df["Em"]/kb_A*multiplier, label=label_prefix+str(phi_A))
  #ax[0].set_ylabel(r"$\left<U\right>/Nk_{b}$", fontsize=10, labelpad=7)
  ax.plot(WL_A_df["Tr"], WL_A_df["P2"], color=plt.get_cmap('tab10')(0), label=phi_prefix+str(phi_A))
  ax.set_ylim(0,1)
#  ax.set_yticks([0, 0.45,0.85])
#  ax.plot(WL_A_df["Tr"], WL_A_df["Cv"]*multiplier, label=phi_prefix+str(phi_A))
#  ax.legend()
  #ax[3].set_xlabel(r"$T_{r}$", fontsize=10, labelpad=5)
  ax1 = ax.twinx()
  ax1.plot(WL_A_df["Tr"], WL_A_df["n6"], color=plt.get_cmap('tab10')(1), label=phi_prefix+str(phi_A))
  ax1.set_ylim(0,1)
  ax1.spines["left"].set_position(("axes", 0.0))
  make_patch_spines_invisible(ax1)
  ax1.spines["left"].set_visible(True)
  ax1.yaxis.set_label_position('left')
  ax1.yaxis.set_ticks_position('left')
  ax2 = ax.twinx()
  ax2.plot(WL_A_df["Tr"], WL_A_df["Cv"]*multiplier, color=plt.get_cmap('tab10')(2), label=phi_prefix+str(phi_A))
  ax2.set_yscale('log')
  ax2.set_ylim(10,70)
  ax2.yaxis.set_minor_formatter(NullFormatter())
  ax2.spines["left"].set_position(("axes", 0.0))
  make_patch_spines_invisible(ax2)
  ax2.spines["left"].set_visible(True)
  ax2.yaxis.set_label_position('left')
  ax2.yaxis.set_ticks_position('left')

  ax.tick_params(axis='both', labelsize=8)
  ax1.tick_params(axis='both', labelsize=8)
  ax2.tick_params(axis='both', labelsize=8)
  if mod == 0:
    ax.set_yticks([])
    ax1.set_yticks([])
    ax2.set_yticks([])
  elif mod == 1:
    ax.set_ylabel(r"$P_{2}$", fontsize=8, labelpad=1)
    ax.tick_params(axis='y', colors=plt.get_cmap('tab10')(0))
    ax.yaxis.label.set_color(plt.get_cmap('tab10')(0))
##    ax.set_yticks([0,1])
    ax1.set_yticks([])
    ax2.set_yticks([])
###    ax.tick_params(labelleft=False)    
###    ax1.tick_params(labelleft=False)    
###    ax2.tick_params(labelleft=False)    
  elif mod == 2:
    ax1.set_ylabel(r"$n_{Q_{6}}$", fontsize=8, labelpad=1)
    ax1.tick_params(axis='y', colors=plt.get_cmap('tab10')(1))
    ax1.yaxis.label.set_color(plt.get_cmap('tab10')(1))
    ax.set_yticks([])
    ax2.set_yticks([])
  elif mod == 3:
    ax2.set_ylabel(r"$C_{V}/kN_{c}$", fontsize=8, labelpad=-6)
    ax2.tick_params(axis='y', colors=plt.get_cmap('tab10')(2))
    ax2.yaxis.label.set_color(plt.get_cmap('tab10')(2))
    ax1.set_yticks([])
    ax.set_yticks([])
  ax.set_xticks([])
  ax1.set_xticks([])
  ax2.set_xticks([])
  plt.subplots_adjust(left=0.25, top=0.97, bottom=0.03, right=0.995)
  fig.savefig(figname)

makeWLMCFigure(0.1, 11.000, "subfig-kb_0.1-Lx_11.000.pdf", 1)
makeWLMCFigure(1.0, 11.000, "subfig-kb_1.0-Lx_11.000.pdf", 2)
makeWLMCFigure(10., 11.000, "subfig-kb_10.-Lx_11.000.pdf", 3)
makeWLMCFigure(0.1, 11.436, "subfig-kb_0.1-Lx_11.436.pdf")
makeWLMCFigure(1.0, 11.436, "subfig-kb_1.0-Lx_11.436.pdf")
makeWLMCFigure(10., 11.436, "subfig-kb_10.-Lx_11.436.pdf")
makeWLMCFigure(0.1, 13.000, "subfig-kb_0.1-Lx_13.000.pdf")
makeWLMCFigure(1.0, 13.000, "subfig-kb_1.0-Lx_13.000.pdf")
makeWLMCFigure(10., 13.000, "subfig-kb_10.-Lx_13.000.pdf")
makeWLMCFigure(0.1, 15.000, "subfig-kb_0.1-Lx_15.000.pdf")
makeWLMCFigure(1.0, 15.000, "subfig-kb_1.0-Lx_15.000.pdf")
makeWLMCFigure(10., 15.000, "subfig-kb_10.-Lx_15.000.pdf")

#phase diagram time
def makePhaseDiag(kb_A, Lx_A, figname, mod=0):
  Tmin = 0.0
  Tmax = 0.2
  
  T_IN_scat = []
  T_IC_scat = []
  kb_scat = []
  kb_IN_scat = []
  kb_IC_scat = []
  fig, ax = plt.subplots(1, 1, figsize=(1.625,1.5))
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
      Ts_data_A[:,0] /= now_df['kb'].iat[i]
      if len(Ts_data_A) >= 2:
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
    region_2 = np.linspace(Tmin, Tmax, 100)
    ax.fill_between(region_2, kb_min, kb_max, color=['#EFEFEF'], alpha=0.5)
    
    ax.tick_params(axis='both', labelsize=6)
    ax.set_xlim(Tmin, Tmax)
    ax.set_ylim(kb_min, kb_max)
    if kb_A == 0:
      ax.set_yscale('log')
    ax.yaxis.set_major_formatter(ScalarFormatter())
    ax.set_xticks([])
    ax.set_yticks([])
    plt.subplots_adjust(left=0.25, top=0.97, bottom=0.03, right=0.995)
    plt.savefig(figname)
    plt.close()
    return
  
  no_cryst = 0
  if len(kb_IC_scat) > 0:
    one = max(len(kb_IC_scat)-3, 1)
    model_IC = np.poly1d(np.polyfit(kb_IC_scat, T_IC_scat, one))
    if kb_A == 1.0:
      model_IC = np.poly1d(np.polyfit(kb_IC_scat, T_IC_scat, 3))
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

  if len(kb_IC_scat) > 0:
    keep_idx = T_IC_model < T_IN_model
    T_IC_model = T_IC_model[keep_idx]
    kb_IC_model = kb_IC_model[keep_idx]
  #if len(kb_IC_scat) > 0:
  #  kb_IC_model = kb_IC_line
  #  T_IC_model = T_IC_line
  
  if kb_A == 0:
    kb_below=[]
    kb_above=[]
    i = 0
    region_1 = np.linspace(Tmin, Tmax, 100)
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
    region_2 = np.linspace(Tmin, Tmax, 100)
    for i in range(len(region_2)):
      idx = (np.abs(T_IN_model-region_2[i])).argmin()
      kb_below_2.append(kb_IN_model[idx])
    ax.fill_between(region_2, kb_below_2, kb_max, color=['#EFEFEF'], alpha=0.5)
    
    kb_above_3=[]
    i = 0
    region_3 = np.linspace(Tmin, Tmax, 100)
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
    region_1 = np.linspace(Tmin, Tmax, 100)
    for i in range(len(region_1)):
      idx = (np.abs(T_IC_model-region_1[i])).argmin()
      if T_IC_model[idx] == np.amax(T_IC_model):
        continue
      kb_below.append(kb_IC_model[idx])
    region_1 = region_1[:len(kb_below)]
    ax.fill_between(region_1, kb_below, kb_max, color=['#FFC947'], alpha=0.7)

    kb_below_2=[]
    kb_above_2=[]
    i = 0
    region_2 = np.linspace(Tmin, Tmax, 100)
    for i in range(len(region_2)):
      idx = (np.abs(T_IC_model-region_2[i])).argmin()
      idx2 = (np.abs(T_IN_model-region_2[i])).argmin()
      if kb_A == 1:
        if T_IC_model[idx] == np.amax(T_IC_model):
          continue
      kb_above_2.append(kb_IC_model[idx])
      kb_below_2.append(kb_IN_model[idx2])
    region_2 = region_2[:len(kb_below_2)]
    ax.fill_between(region_2, kb_below_2, kb_above_2, color=['#185ADB'], alpha=0.5)

    ax.fill_between(T_IN_model, kb_min, kb_IN_model, color=['#EFEFEF'], alpha=0.5)

  if no_cryst != 0:
    ax.plot(T_IC_model, kb_IC_model, color='r', label="IC", zorder=1)
  ax.plot(T_IN_model, kb_IN_model, color='g', label="IN", zorder=1)
  ax.scatter(T_IN_scat, kb_IN_scat, color='g', label="IN", zorder=2)
  ax.scatter(T_IC_scat, kb_IC_scat, color='r', label="IC", zorder=2)
  ax.tick_params(axis='both', labelsize=6)
  ax.set_xlim(Tmin, Tmax)
  ax.set_ylim(kb_min, kb_lim_max)
  if kb_A == 0:
    ax.set_yscale('log')
  ax.yaxis.set_major_formatter(ScalarFormatter())
  if mod == 0:
    ax.set_xticks([])
    ax.set_yticks([])
  elif mod == 1:
    ax.set_xticks([])
    ax.set_ylabel(r"$k_{b}$", fontsize=8, labelpad=0)
  elif mod == 2:
    ax.set_yticks([])
    ax.set_xlabel(r"$T_{r}$", fontsize=8, labelpad=6)#, labelpad=0.3)
    ax.set_xticks([0, 0.05, 0.1, 0.15])
  elif mod == 3:
    ax.set_xticks([0, 0.05, 0.1, 0.15])
    ax.set_xlabel(r"$T_{r}$", fontsize=8, labelpad=6)#, labelpad=0.3)
    ax.set_ylabel(r"$\phi$", fontsize=8, labelpad=2)
  if kb_A == 0:
    plt.subplots_adjust(left=0.25, top=0.97, bottom=0.03, right=0.995)
  else:
    plt.subplots_adjust(left=0.25, top=0.9999, bottom=0.25, right=0.995)
  #plt.show()
  #sys.exit()
  plt.savefig(figname)
  plt.close()

makePhaseDiag(0, 11.000, "subfig-Lx_11.000.pdf", 1)
makePhaseDiag(0, 11.436, "subfig-Lx_11.436.pdf", 0)
makePhaseDiag(0, 13.000, "subfig-Lx_13.000.pdf", 0)
makePhaseDiag(0, 15.000, "subfig-Lx_15.000.pdf", 0)
makePhaseDiag(0.1, 0, "subfig-kb_0.1.pdf", 3)
makePhaseDiag(1.0, 0, "subfig-kb_1.0.pdf", 2)
makePhaseDiag(10., 0, "subfig-kb_10..pdf", 2)
