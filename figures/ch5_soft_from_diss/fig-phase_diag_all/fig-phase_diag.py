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

fit    = 1
crit   = 1

phi_min = 0.29
phi_max = 0.50
T_min = 0.0
T_max = 0.34

label_prefix = r'$\phi=$'

# the hard stepflex system
Ts_files = "../figs-hard_step/fig-phase_diag/Ts.out"
Lx_crit  = (11.157216+11.436146)/2
phi_crit = Nc*Nb*sigma**3/Lx_crit**3*np.pi/6

# get data
df = pd.read_csv(Ts_files, index_col=False, delimiter=' ')
df['Tr']  = df['Tm']/df['kb']
df['phi'] = Nc*Nb*sigma**3/df['Lx']**3*np.pi/6
df_SandP  = df[df['dir'].str.contains("SandP_Nc125")]
phi_HTS_scat  = df_SandP['phi'].to_numpy()
T_HTS_scat    = df_SandP['Tr'].to_numpy()

phi_cryst = 0.47
T_HTS_IC_scat   = T_HTS_scat[phi_HTS_scat > phi_cryst]
phi_HTS_IC_scat = phi_HTS_scat[phi_HTS_scat > phi_cryst]
T_HTS_scat   = T_HTS_scat[phi_HTS_scat < phi_cryst]
phi_HTS_scat = phi_HTS_scat[phi_HTS_scat < phi_cryst]

# the hard harmflex system
Ts_files = "../figs-hard_harm/fig-phase_diag/Ts.out"

# get data
df = pd.read_csv(Ts_files, index_col=False, delimiter=' ')
df['Tr']  = df['Tm']/df['kb']
df['Tr2']  = df['Tm2']/df['kb']
df['phi'] = Nc*Nb*sigma**3/df['Lx']**3*np.pi/6
df_HTH  = df[df['dir'].str.contains("HTH_kb1.00")]
phi_HTH_scat  = df_HTH['phi'].to_numpy()
T_1_scat  = df_HTH['Tr'].to_numpy()
T_2_scat  = df_HTH['Tr2'].to_numpy()

phi_cryst = 0.3
T_HTH_scat      = T_1_scat
T_HTH_IC_scat   = T_2_scat[phi_HTH_scat > phi_cryst]
phi_HTH_IC_scat = phi_HTH_scat[phi_HTH_scat > phi_cryst]

# The soft harm harm system
WL_Ts_files = np.array([
                     "../figs-soft_harm_harm/Lx11.000_kb0.10_WLMC_Ts.out", "../figs-soft_harm_harm/Lx11.000_kb1.00_WLMC_Ts.out", "../figs-soft_harm_harm/Lx11.000_kb10.0_WLMC_Ts.out",
                     "../figs-soft_harm_harm/Lx11.436_kb0.10_WLMC_Ts.out", "../figs-soft_harm_harm/Lx11.436_kb1.00_WLMC_Ts.out", "../figs-soft_harm_harm/Lx11.436_kb10.0_WLMC_Ts.out",
                     "../figs-soft_harm_harm/Lx13.000_kb0.10_WLMC_Ts.out", "../figs-soft_harm_harm/Lx13.000_kb1.00_WLMC_Ts.out", "../figs-soft_harm_harm/Lx13.000_kb10.0_WLMC_Ts.out",
                     "../figs-soft_harm_harm/Lx15.000_kb0.10_WLMC_Ts.out", "../figs-soft_harm_harm/Lx15.000_kb1.00_WLMC_Ts.out", "../figs-soft_harm_harm/Lx15.000_kb10.0_WLMC_Ts.out"
                 ,    "../figs-soft_harm_harm/Lx11.200_kb1.00_WLMC_Ts.out", "../figs-soft_harm_harm/Lx11.800_kb1.00_WLMC_Ts.out", "../figs-soft_harm_harm/Lx12.500_kb1.00_WLMC_Ts.out", "../figs-soft_harm_harm/Lx13.500_kb1.00_WLMC_Ts.out"
                    ])
Lx_      = [11, 11.436, 13, 15]
Lx_      = np.repeat(Lx_, 3)
Lx_ = np.append(Lx_, [11.2, 11.8, 12.5, 13.5])
phi_     = Nc*Nb*sigma**3/Lx_**3*np.pi/6
kb_      = [0.1, 1, 10]
kb_      = np.tile(kb_, 4)
kb_ = np.append(kb_, [1,1,1,1])
input_df = pd.DataFrame({'Ts_files': WL_Ts_files, 'Lx': Lx_, 'phi': phi_, 'kb': kb_})
input_df = input_df.loc[input_df['kb'] == 1.0]

T_SHH_scat = []
T_SHH_IC_scat = []
phi_SHH_scat = []
phi_SHH_IC_scat = []
for i in range(len(input_df)):
  Ts_data_A = np.loadtxt(input_df['Ts_files'].iat[i], skiprows=1, ndmin=2)
  Ts_data_A[:,0] /= input_df['kb'].iat[i]
  if len(Ts_data_A) == 2:
    T_SHH_scat.append(Ts_data_A[:,0][1])
    T_SHH_IC_scat.append(Ts_data_A[:,0][0])
    phi_SHH_scat.append(float(input_df['phi'].iat[i]))
    phi_SHH_IC_scat.append(float(input_df['phi'].iat[i]))
  elif len(Ts_data_A) == 1:
    T_SHH_scat.append(Ts_data_A[:,0][0])
    phi_SHH_scat.append(float(input_df['phi'].iat[i]))
    T_SHH_IC_scat.append(0)
    phi_SHH_IC_scat.append(float(input_df['phi'].iat[i]))
T_SHH_scat      = np.array(T_SHH_scat)
T_SHH_IC_scat   = np.array(T_SHH_IC_scat)
phi_SHH_scat    = np.array(phi_SHH_scat)
phi_SHH_IC_scat = np.array(phi_SHH_IC_scat)

one = max(len(phi_SHH_scat)-2, 1)
model_SHH = np.poly1d(np.polyfit(phi_SHH_scat, T_SHH_scat, one))
phi_SHH_model = np.linspace(phi_min, phi_max, 1000)
T_SHH_model = model_SHH(phi_SHH_model)

one = max(len(phi_SHH_IC_scat)-3, 1)
model_SHH_IC = np.poly1d(np.polyfit(phi_SHH_IC_scat, T_SHH_IC_scat, one))
phi_SHH_IC_model = np.linspace(phi_min, phi_max, 1000)
T_SHH_IC_model = model_SHH_IC(phi_SHH_IC_model)

fig, ax = plt.subplots(1, figsize=(3.25,3.1))
# plot points
ax.scatter(T_HTS_scat   , phi_HTS_scat   , color='r', marker='_', zorder=2, label=r"$T^{\mathrm{HTS}}_{\mathrm{IN}}$")
ax.scatter(T_HTS_IC_scat, phi_HTS_IC_scat, color='r', marker='*', zorder=2, label=r"$T^{\mathrm{HTS}}_{\mathrm{IC}}$")
ax.scatter(T_HTH_scat   , phi_HTH_scat   , color='b', marker='_', zorder=2, label=r"$T^{\mathrm{HTH}}_{\mathrm{IN}}$")
ax.scatter(T_HTH_IC_scat, phi_HTH_IC_scat, color='b', marker='*', zorder=2, label=r"$T^{\mathrm{HTH}}_{\mathrm{IC}}$")
ax.scatter(T_SHH_scat   , phi_SHH_scat   , color='m', marker='_', zorder=2, label=r"$T^{\mathrm{SHH}}_{\mathrm{IN}}$")
ax.scatter(T_SHH_IC_scat, phi_SHH_IC_scat, color='m', marker='*', zorder=2, label=r"$T^{\mathrm{SHH}}_{\mathrm{IC}}$")

if fit:
  # HTS
  slope, intercept, r_value, p_value, std_err = stats.linregress(phi_HTS_scat, T_HTS_scat)
  phi_HTS_line = np.linspace(phi_min, phi_max, 1000)
  T_HTS_line   = phi_HTS_line*slope + intercept

  phi_HTS_model = phi_HTS_line
  T_HTS_model = T_HTS_line

  # HTH
  slope, intercept, r_value, p_value, std_err = stats.linregress(phi_HTH_scat, T_HTH_scat)
  phi_HTH_line = np.linspace(phi_min, phi_max, 1000)
  T_HTH_line   = phi_HTH_line*slope + intercept

  model = np.poly1d(np.polyfit(phi_HTH_scat, T_HTH_scat, 3))
  phi_HTH_quad = phi_HTS_line
  T_HTH_quad = model(phi_HTH_quad)
  
  slope, intercept, r_value, p_value, std_err = stats.linregress(phi_HTH_IC_scat, T_HTH_IC_scat)
  phi_HTH_IC_line = np.linspace(phi_min, phi_max, 1000)
  T_HTH_IC_line   = phi_HTH_IC_line*slope + intercept

  model_HTH_IC = np.poly1d(np.polyfit(phi_HTH_IC_scat, T_HTH_IC_scat, 3))
  phi_HTH_IC_quad = phi_HTS_line
  T_HTH_IC_quad = model_HTH_IC(phi_HTH_IC_quad)

  phi_HTH_model = phi_HTH_line
  T_HTH_model   = T_HTH_line
  phi_HTH_IC_model = phi_HTH_IC_line
  T_HTH_IC_model   = T_HTH_IC_line

#  del_idx = T_HTH_IC_model < T_HTH_model
#  phi_HTH_IC_model = phi_HTH_IC_model[del_idx]
#  T_HTH_IC_model = T_HTH_IC_model[del_idx]
  T_HTH_model[T_HTH_IC_model > T_HTH_model] = T_HTH_IC_model[T_HTH_IC_model > T_HTH_model]

  # SHH
  model = np.poly1d(np.polyfit(phi_SHH_scat, T_SHH_scat, 3))
  phi_SHH_model = phi_HTS_line
  T_SHH_model = model(phi_SHH_model)
  
  model_SHH_IC = np.poly1d(np.polyfit(phi_SHH_IC_scat, T_SHH_IC_scat, 3))
  phi_SHH_IC_model = phi_HTS_line
  T_SHH_IC_model = model_SHH_IC(phi_SHH_IC_model)

  ax.plot(T_HTS_model   , phi_HTS_model   , color='r', zorder=1)#)
  ax.plot(T_HTH_IC_model, phi_HTH_IC_model, color='b', zorder=1)#, label="IC")
  ax.plot(T_HTH_model   , phi_HTH_model   , color='b', zorder=1)#, label="IN")
  ax.plot(T_SHH_model   , phi_SHH_model   , color='m', zorder=1)#, label="IN")
  ax.plot(T_SHH_IC_model, phi_SHH_IC_model, color='m', zorder=1)#, label="IC")


ax.set_xlabel(r"$T_{r}$", fontsize=10, labelpad=6)#, labelpad=0.3)
ax.set_ylabel(r"$\phi$", fontsize=10, labelpad=5.5)
ax.tick_params(axis='both', labelsize=8)
ax.set_xlim(T_min, T_max)
ax.set_ylim(phi_min, phi_max)
ax.legend(loc='lower right', fontsize=8, handletextpad=0.01)
ax.set_yticks([0.3,0.4,0.5])
ax.set_xticks([0.0,0.1,0.2,0.3])

plt.subplots_adjust(left=0.156, top=0.98, bottom=0.135, right=0.974)
#plt.show()
#sys.exit()
plt.savefig("fig-phase_diag.pdf")
plt.close()
