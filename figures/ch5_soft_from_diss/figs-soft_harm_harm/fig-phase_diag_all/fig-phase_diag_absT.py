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

Nc    = 125
Nb    = 10
sigma = 1
label_prefix = r'$\phi=$'

fit    = 1
crit   = 1

phi_min = 0.29
phi_max = 0.53
T_min = 0.0
T_max = 0.2

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

input_df = pd.DataFrame({'Ts_files': WL_Ts_files, 'Lx': Lx_, 'phi': phi_, 'kb': kb_})

# the kb = 0.1 data
input_kb0p10_df = input_df.loc[input_df['kb'] == 0.1]
T_kb0p10_scat = []
T_kb0p10_NC_scat = []
phi_kb0p10_scat = []
phi_kb0p10_NC_scat = []
for i in range(len(input_kb0p10_df)):
  Ts_data_A = np.loadtxt(input_kb0p10_df['Ts_files'].iat[i], skiprows=1, ndmin=2)
#  Ts_data_A[:,0] /= input_kb0p10_df['kb'].iat[i]
  if len(Ts_data_A) >= 2:
    T_kb0p10_scat.append(Ts_data_A[:,0][1])
    T_kb0p10_NC_scat.append(Ts_data_A[:,0][0])
    phi_kb0p10_scat.append(float(input_kb0p10_df['phi'].iat[i]))
    phi_kb0p10_NC_scat.append(float(input_kb0p10_df['phi'].iat[i]))
  elif len(Ts_data_A) == 1:
    T_kb0p10_scat.append(Ts_data_A[:,0][0])
    phi_kb0p10_scat.append(float(input_kb0p10_df['phi'].iat[i]))
    T_kb0p10_NC_scat.append(0)
    phi_kb0p10_NC_scat.append(float(input_kb0p10_df['phi'].iat[i]))
T_kb0p10_scat      = np.array(T_kb0p10_scat)
T_kb0p10_NC_scat   = np.array(T_kb0p10_NC_scat)
phi_kb0p10_scat    = np.array(phi_kb0p10_scat)
phi_kb0p10_NC_scat = np.array(phi_kb0p10_NC_scat)

# the kb = 1.0 data
input_kb1p00_df = input_df.loc[input_df['kb'] == 1.0]
T_kb1p00_scat = []
T_kb1p00_NC_scat = []
phi_kb1p00_scat = []
phi_kb1p00_NC_scat = []
for i in range(len(input_kb1p00_df)):
  Ts_data_A = np.loadtxt(input_kb1p00_df['Ts_files'].iat[i], skiprows=1, ndmin=2)
#  Ts_data_A[:,0] /= input_kb1p00_df['kb'].iat[i]
  if len(Ts_data_A) >= 2:
    T_kb1p00_scat.append(Ts_data_A[:,0][1])
    T_kb1p00_NC_scat.append(Ts_data_A[:,0][0])
    phi_kb1p00_scat.append(float(input_kb1p00_df['phi'].iat[i]))
    phi_kb1p00_NC_scat.append(float(input_kb1p00_df['phi'].iat[i]))
  elif len(Ts_data_A) == 1:
    T_kb1p00_scat.append(Ts_data_A[:,0][0])
    phi_kb1p00_scat.append(float(input_kb1p00_df['phi'].iat[i]))
    T_kb1p00_NC_scat.append(0)
    phi_kb1p00_NC_scat.append(float(input_kb1p00_df['phi'].iat[i]))
T_kb1p00_scat      = np.array(T_kb1p00_scat)
T_kb1p00_NC_scat   = np.array(T_kb1p00_NC_scat)
phi_kb1p00_scat    = np.array(phi_kb1p00_scat)
phi_kb1p00_NC_scat = np.array(phi_kb1p00_NC_scat)

# the kb = 10.0 data
input_kb10p0_df = input_df.loc[input_df['kb'] == 10.0]
T_kb10p0_scat = []
T_kb10p0_NC_scat = []
phi_kb10p0_scat = []
phi_kb10p0_NC_scat = []
for i in range(len(input_kb10p0_df)):
  Ts_data_A = np.loadtxt(input_kb10p0_df['Ts_files'].iat[i], skiprows=1, ndmin=2)
#  Ts_data_A[:,0] /= input_kb10p0_df['kb'].iat[i]
  if len(Ts_data_A) >= 2:
    T_kb10p0_scat.append(Ts_data_A[:,0][1])
    T_kb10p0_NC_scat.append(Ts_data_A[:,0][0])
    phi_kb10p0_scat.append(float(input_kb10p0_df['phi'].iat[i]))
    phi_kb10p0_NC_scat.append(float(input_kb10p0_df['phi'].iat[i]))
  elif len(Ts_data_A) == 1:
    T_kb10p0_scat.append(Ts_data_A[:,0][0])
    phi_kb10p0_scat.append(float(input_kb10p0_df['phi'].iat[i]))
    T_kb10p0_NC_scat.append(0)
    phi_kb10p0_NC_scat.append(float(input_kb10p0_df['phi'].iat[i]))
T_kb10p0_scat      = np.array(T_kb10p0_scat)
T_kb10p0_NC_scat   = np.array(T_kb10p0_NC_scat)
phi_kb10p0_scat    = np.array(phi_kb10p0_scat)
phi_kb10p0_NC_scat = np.array(phi_kb10p0_NC_scat)

do_kb0p10 = 1
do_kb1p00 = 1
do_kb10p0 = 1

fig, ax = plt.subplots(1, figsize=(3.25,3.1))
# plot points
if do_kb0p10:
  ax.scatter(T_kb0p10_scat   , phi_kb0p10_scat   , color='r', marker='+', zorder=2, label=r"$T_{\mathrm{IN}}(k_b=0.1)$")
  ax.scatter(T_kb0p10_NC_scat, phi_kb0p10_NC_scat, color='r', marker='*', zorder=2, label=r"$T_{\mathrm{NC}}(k_b=0.1)$")
if do_kb1p00:
  ax.scatter(T_kb1p00_scat   , phi_kb1p00_scat   , color='m', marker='+', zorder=2, label=r"$T_{\mathrm{IN}}(k_b=1)$")
  ax.scatter(T_kb1p00_NC_scat, phi_kb1p00_NC_scat, color='m', marker='*', zorder=2, label=r"$T_{\mathrm{NC}}(k_b=1)$")
if do_kb10p0:
  ax.scatter(T_kb10p0_scat   , phi_kb10p0_scat   , color='b', marker='+', zorder=2, label=r"$T_{\mathrm{IN}}(k_b=10)$")
  ax.scatter(T_kb10p0_NC_scat, phi_kb10p0_NC_scat, color='b', marker='*', zorder=2, label=r"$T_{\mathrm{NC}}(k_b=10)$")

if fit:
  # kb0.10
  slope, intercept, r_value, p_value, std_err = stats.linregress(phi_kb0p10_scat, T_kb0p10_scat)
  phi_kb0p10_line = np.linspace(phi_min, phi_max, 1000)
  T_kb0p10_line   = phi_kb0p10_line*slope + intercept

  one = max(len(phi_kb0p10_scat)-2, 1)
  model_kb0p10 = np.poly1d(np.polyfit(phi_kb0p10_scat, T_kb0p10_scat, one))
  phi_kb0p10_quad = np.linspace(phi_min, phi_max, 1000)
  T_kb0p10_quad = model_kb0p10(phi_kb0p10_quad)

  slope, intercept, r_value, p_value, std_err = stats.linregress(phi_kb0p10_NC_scat, T_kb0p10_NC_scat)
  phi_kb0p10_NC_line = np.linspace(phi_min, phi_max, 1000)
  T_kb0p10_NC_line   = phi_kb0p10_NC_line*slope + intercept
  
  one = max(len(phi_kb0p10_NC_scat)-3, 1)
  model_kb0p10_NC = np.poly1d(np.polyfit(phi_kb0p10_NC_scat, T_kb0p10_NC_scat, 10))#one))
  phi_kb0p10_NC_quad = np.linspace(phi_min, phi_max, 1000)
  T_kb0p10_NC_quad = model_kb0p10_NC(phi_kb0p10_NC_quad)
  idx_less_zero = (np.abs(T_kb0p10_NC_quad[50:]-0)).argmin()+50
#  print(idx_less_zero)
  T_kb0p10_NC_quad[:idx_less_zero] = 0
#  ax.scatter(T_kb0p10_NC_model[idx_less_zero], phi_kb0p10_NC_model[idx_less_zero], c='k')

  # kb1.00
  slope, intercept, r_value, p_value, std_err = stats.linregress(phi_kb1p00_scat, T_kb1p00_scat)
  phi_kb1p00_line = np.linspace(phi_min, phi_max, 1000)
  T_kb1p00_line   = phi_kb1p00_line*slope + intercept

  one = max(len(phi_kb1p00_scat)-2, 1)
  model_kb1p00 = np.poly1d(np.polyfit(phi_kb1p00_scat, T_kb1p00_scat, one))
  phi_kb1p00_quad = np.linspace(phi_min, phi_max, 1000)
  T_kb1p00_quad = model_kb1p00(phi_kb1p00_quad)

  slope, intercept, r_value, p_value, std_err = stats.linregress(phi_kb1p00_NC_scat, T_kb1p00_NC_scat)
  phi_kb1p00_NC_line = np.linspace(phi_min, phi_max, 1000)
  T_kb1p00_NC_line   = phi_kb1p00_NC_line*slope + intercept
  
  one = max(len(phi_kb1p00_NC_scat)-3, 1)
  model_kb1p00_NC = np.poly1d(np.polyfit(phi_kb1p00_NC_scat, T_kb1p00_NC_scat, 2))#one))
  phi_kb1p00_NC_quad = np.linspace(phi_min, phi_max, 1000)
  T_kb1p00_NC_quad = model_kb1p00_NC(phi_kb1p00_NC_quad)

  # kb10.0
  slope, intercept, r_value, p_value, std_err = stats.linregress(phi_kb10p0_scat, T_kb10p0_scat)
  phi_kb10p0_line = np.linspace(phi_min, phi_max, 1000)
  T_kb10p0_line   = phi_kb10p0_line*slope + intercept

  one = max(len(phi_kb10p0_scat)-2, 1)
  model_kb10p0 = np.poly1d(np.polyfit(phi_kb10p0_scat, T_kb10p0_scat, one))
  phi_kb10p0_quad = np.linspace(phi_min, phi_max, 1000)
  T_kb10p0_quad = model_kb10p0(phi_kb10p0_quad)

  slope, intercept, r_value, p_value, std_err = stats.linregress(phi_kb10p0_NC_scat, T_kb10p0_NC_scat)
  phi_kb10p0_NC_line = np.linspace(phi_min, phi_max, 1000)
  T_kb10p0_NC_line   = phi_kb10p0_NC_line*slope + intercept
  
  one = max(len(phi_kb10p0_NC_scat)-3, 1)
  model_kb10p0_NC = np.poly1d(np.polyfit(phi_kb10p0_NC_scat, T_kb10p0_NC_scat, one))
  phi_kb10p0_NC_quad = np.linspace(phi_min, phi_max, 1000)
  T_kb10p0_NC_quad = model_kb10p0_NC(phi_kb10p0_NC_quad)

  phi_kb0p10_model    = phi_kb0p10_line
  phi_kb0p10_NC_model = phi_kb0p10_NC_quad
  phi_kb1p00_model    = phi_kb1p00_line
  phi_kb1p00_NC_model = phi_kb1p00_NC_quad
  phi_kb10p0_model    = phi_kb10p0_line
  phi_kb10p0_NC_model = phi_kb10p0_NC_quad

  T_kb0p10_model    = T_kb0p10_line
  T_kb0p10_NC_model = T_kb0p10_NC_quad
  T_kb1p00_model    = T_kb1p00_line
  T_kb1p00_NC_model = T_kb1p00_NC_quad
  T_kb10p0_model    = T_kb10p0_line
  T_kb10p0_NC_model = T_kb10p0_NC_quad

  T_kb0p10_model[T_kb0p10_model<0] = 0
  T_kb0p10_NC_model[T_kb0p10_NC_model<0] = 0
  T_kb1p00_model[T_kb1p00_model<0] = 0
  T_kb1p00_NC_model[T_kb1p00_NC_model<0] = 0
  T_kb10p0_model[T_kb10p0_model<0] = 0
  T_kb10p0_NC_model[T_kb10p0_NC_model<0] = 0

  keepidx_kb0p10 = T_kb0p10_NC_model > T_kb0p10_model
  keepidx_kb1p00 = T_kb1p00_NC_model > T_kb1p00_model
  keepidx_kb10p0 = T_kb10p0_NC_model > T_kb10p0_model
  T_kb0p10_NC_model[keepidx_kb0p10] = T_kb0p10_model[keepidx_kb0p10]
  T_kb1p00_NC_model[keepidx_kb1p00] = T_kb1p00_model[keepidx_kb1p00]
  T_kb10p0_NC_model[keepidx_kb10p0] = T_kb10p0_model[keepidx_kb10p0]

  if do_kb0p10:
    ax.plot(T_kb0p10_model   , phi_kb0p10_model   , color='r', zorder=1)#, label="IN")
    ax.plot(T_kb0p10_NC_model, phi_kb0p10_NC_model, color='r', zorder=1)#, label="NC")
  if do_kb1p00:
    ax.plot(T_kb1p00_model   , phi_kb1p00_model   , color='m', zorder=1)#, label="IN")
    ax.plot(T_kb1p00_NC_model, phi_kb1p00_NC_model, color='m', zorder=1)#, label="NC")
  if do_kb10p0:
    ax.plot(T_kb10p0_model   , phi_kb10p0_model   , color='b', zorder=1)#, label="IN")
    ax.plot(T_kb10p0_NC_model, phi_kb10p0_NC_model, color='b', zorder=1)#, label="NC")

ax.set_xlabel(r"$kT/\epsilon$", fontsize=10, labelpad=6)#, labelpad=0.3)
ax.set_xscale('log')
ax.set_xlim(0.003,1.5)
ax.set_ylabel(r"$\phi$", fontsize=10, labelpad=5.5)
ax.tick_params(axis='both', labelsize=8)
ax.set_ylim(phi_min, phi_max)
ax.legend(loc='lower right', fontsize=8, handletextpad=0.01)
ax.set_yticks([0.3,0.4,0.5])
#ax.set_xticks([0.0,0.1,0.2])

plt.subplots_adjust(left=0.156, top=0.98, bottom=0.135, right=0.974)
#plt.show()
#sys.exit()
plt.savefig("fig-phase_diag_absT.pdf")
plt.close()
