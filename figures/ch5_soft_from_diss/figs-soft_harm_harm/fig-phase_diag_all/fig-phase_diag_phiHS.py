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

phi_min = 0.23
phi_max = 0.51
phi_max = 0.525
T_min = 0.0
T_max = 0.2
zeroT = 0.0

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
  Ts_data_A[:,0] /= input_kb0p10_df['kb'].iat[i]
  if len(Ts_data_A) >= 2:
    T_kb0p10_scat.append(Ts_data_A[:,0][1])
    T_kb0p10_NC_scat.append(Ts_data_A[:,0][0])
    phi_kb0p10_scat.append(float(input_kb0p10_df['phi'].iat[i]))
    phi_kb0p10_NC_scat.append(float(input_kb0p10_df['phi'].iat[i]))
  elif len(Ts_data_A) == 1:
    T_kb0p10_scat.append(Ts_data_A[:,0][0])
    phi_kb0p10_scat.append(float(input_kb0p10_df['phi'].iat[i]))
    T_kb0p10_NC_scat.append(zeroT)
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
  Ts_data_A[:,0] /= input_kb1p00_df['kb'].iat[i]
  if len(Ts_data_A) >= 2:
    T_kb1p00_scat.append(Ts_data_A[:,0][1])
    T_kb1p00_NC_scat.append(Ts_data_A[:,0][0])
    phi_kb1p00_scat.append(float(input_kb1p00_df['phi'].iat[i]))
    phi_kb1p00_NC_scat.append(float(input_kb1p00_df['phi'].iat[i]))
  elif len(Ts_data_A) == 1:
    T_kb1p00_scat.append(Ts_data_A[:,0][0])
    phi_kb1p00_scat.append(float(input_kb1p00_df['phi'].iat[i]))
    T_kb1p00_NC_scat.append(zeroT)
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
  Ts_data_A[:,0] /= input_kb10p0_df['kb'].iat[i]
  if len(Ts_data_A) >= 2:
    T_kb10p0_scat.append(Ts_data_A[:,0][1])
    T_kb10p0_NC_scat.append(Ts_data_A[:,0][0])
    phi_kb10p0_scat.append(float(input_kb10p0_df['phi'].iat[i]))
    phi_kb10p0_NC_scat.append(float(input_kb10p0_df['phi'].iat[i]))
  elif len(Ts_data_A) == 1:
    T_kb10p0_scat.append(Ts_data_A[:,0][0])
    phi_kb10p0_scat.append(float(input_kb10p0_df['phi'].iat[i]))
    T_kb10p0_NC_scat.append(zeroT)
    phi_kb10p0_NC_scat.append(float(input_kb10p0_df['phi'].iat[i]))
T_kb10p0_scat      = np.array(T_kb10p0_scat)
T_kb10p0_NC_scat   = np.array(T_kb10p0_NC_scat)
phi_kb10p0_scat    = np.array(phi_kb10p0_scat)
phi_kb10p0_NC_scat = np.array(phi_kb10p0_NC_scat)

def WCA(r, eps=1.0, sig=2**(-1/6), rc=1.0):
  if r > rc:
    return(0)
  sigbyr6 = sig/r
  sigbyr6 = sigbyr6**6
  return(4*eps*(sigbyr6**2 - sigbyr6) + eps)

#print(2**(-1/6), WCA(2**(-1/6)))
#print(0.99, WCA(0.99))
#print(1.0, WCA(1.0))
#print(1.2, WCA(1.2))
#rij   = np.linspace(0.75, 2.0, 1000)
#U_WCA = np.array([ WCA(R) for R in rij ])
#plt.plot(rij, U_WCA)
#plt.show()
#plt.close()

def return_reff_diff(reff, T, eps=1.0):
  target = 1.0*T
  return(WCA(reff) - target)

from scipy.optimize import fsolve
#T    = np.linspace(0.0001, 100.0, 1000)
#reff = [ fsolve(return_reff_diff, 0.8, args=(Ti))[0] for Ti in T ]
#plt.plot(T, reff)
#plt.hlines(2**(-1/6), np.amin(T), np.amax(T))
#plt.hlines(1.0, np.amin(T), np.amax(T))
#plt.show()
#plt.close()
#sys.exit()

reff_kb0p10_scat = []
phi_mod_kb0p10_scat = []
for phii, Ti in zip(phi_kb0p10_scat, T_kb0p10_scat):
  Ti *= 0.10
  reff = fsolve(return_reff_diff, 0.95, args=(Ti))[0]
  reff_kb0p10_scat.append(reff)
  phi_mod_kb0p10_scat.append(phii*reff**3)

reff_kb0p10_NC_scat = []
phi_mod_kb0p10_NC_scat = []
for phii, Ti in zip(phi_kb0p10_NC_scat, T_kb0p10_NC_scat):
  Ti *= 0.10
  reff = fsolve(return_reff_diff, 0.95, args=(Ti))[0]
  reff_kb0p10_NC_scat.append(reff)
  phi_mod_kb0p10_NC_scat.append(phii*reff**3)

reff_kb1p00_scat = []
phi_mod_kb1p00_scat = []
for phii, Ti in zip(phi_kb1p00_scat, T_kb1p00_scat):
  Ti *= 1.00
  reff = fsolve(return_reff_diff, 0.95, args=(Ti))[0]
  reff_kb1p00_scat.append(reff)
  phi_mod_kb1p00_scat.append(phii*reff**3)

reff_kb1p00_NC_scat = []
phi_mod_kb1p00_NC_scat = []
for phii, Ti in zip(phi_kb1p00_NC_scat, T_kb1p00_NC_scat):
  Ti *= 1.00
  reff = fsolve(return_reff_diff, 0.95, args=(Ti))[0]
  reff_kb1p00_NC_scat.append(reff)
  phi_mod_kb1p00_NC_scat.append(phii*reff**3)

reff_kb10p0_scat = []
phi_mod_kb10p0_scat = []
for phii, Ti in zip(phi_kb10p0_scat, T_kb10p0_scat):
  Ti *= 10.0
  reff = fsolve(return_reff_diff, 0.95, args=(Ti))[0]
  reff_kb10p0_scat.append(reff)
  phi_mod_kb10p0_scat.append(phii*reff**3)

reff_kb10p0_NC_scat = []
phi_mod_kb10p0_NC_scat = []
for phii, Ti in zip(phi_kb10p0_NC_scat, T_kb10p0_NC_scat):
  Ti *= 10.0
  reff = fsolve(return_reff_diff, 0.95, args=(Ti))[0]
  reff_kb10p0_NC_scat.append(reff)
  phi_mod_kb10p0_NC_scat.append(phii*reff**3)

reff_kb0p10_scat       = np.array(reff_kb0p10_scat)
phi_mod_kb0p10_scat    = np.array(phi_mod_kb0p10_scat)
reff_kb0p10_NC_scat    = np.array(reff_kb0p10_NC_scat)
phi_mod_kb0p10_NC_scat = np.array(phi_mod_kb0p10_NC_scat)
reff_kb1p00_scat       = np.array(reff_kb1p00_scat)
phi_mod_kb1p00_scat    = np.array(phi_mod_kb1p00_scat)
reff_kb1p00_NC_scat    = np.array(reff_kb1p00_NC_scat)
phi_mod_kb1p00_NC_scat = np.array(phi_mod_kb1p00_NC_scat)
reff_kb10p0_scat       = np.array(reff_kb10p0_scat)
phi_mod_kb10p0_scat    = np.array(phi_mod_kb10p0_scat)
reff_kb10p0_NC_scat    = np.array(reff_kb10p0_NC_scat)
phi_mod_kb10p0_NC_scat = np.array(phi_mod_kb10p0_NC_scat)

# the hard harmflex system
Ts_files = "hard_harm_Ts.out"
do_HTH = 1

# get data
df = pd.read_csv(Ts_files, index_col=False, delimiter=' ')
df['Tr']  = df['Tm']/df['kb']
df['Tr2']  = df['Tm2']/df['kb']
df['phi'] = Nc*Nb*sigma**3/df['Lx']**3*np.pi/6
df_HTH  = df[df['dir'].str.contains("HTH_kb1.00")]
phi_HTH_scat  = df_HTH['phi'].to_numpy()
T_1_scat  = df_HTH['Tr'].to_numpy()
T_2_scat  = df_HTH['Tr2'].to_numpy()

phi_cryst = 0.31
T_HTH_NC_scat = T_2_scat
phi_HTH_NC_scat = phi_HTH_scat
T_HTH_NC_scat[T_HTH_NC_scat < 0.0001] = 0.0001
T_HTH_NC_scatt   = T_2_scat[phi_HTH_scat > phi_cryst]
phi_HTH_NC_scatt = phi_HTH_scat[phi_HTH_scat > phi_cryst]
T_HTH_scat      = T_1_scat

do_kb0p10 = 1
do_kb1p00 = 1
do_kb10p0 = 1

#print(T_kb0p10_NC_scat)
fig, ax = plt.subplots(1, 2, figsize=(6.5,3.1))
# plot points
#if do_HTH:
#  ax[1].scatter(T_HTH_scat    , phi_HTH_scat    , color='b', marker='+', zorder=2, label=r"$IN$ hard")
#  ax[1].scatter(T_HTH_NC_scatt, phi_HTH_NC_scatt, color='b', marker='*', zorder=2, label=r"$NC$ hard")
if do_kb0p10:
  ax[1].scatter(T_kb0p10_scat   , phi_mod_kb0p10_scat   , marker='+', zorder=2, alpha=1.0, c='r', label=r"$IN$ $k_{b}^{*}=0.1$")
  ax[1].scatter(T_kb0p10_NC_scat, phi_mod_kb0p10_NC_scat, marker='*', zorder=2, alpha=1.0, s=60, edgecolors='r', facecolors='r', label=r"$NC$ $k_{b}^{*}=0.1$")
if do_kb1p00:
  ax[1].scatter(T_kb1p00_scat   , phi_mod_kb1p00_scat   , marker='+', zorder=2, alpha=1.0, c='m', label=r"$IN$ $k_{b}^{*}=1$")
  ax[1].scatter(T_kb1p00_NC_scat, phi_mod_kb1p00_NC_scat, marker='*', zorder=2, alpha=1.0, edgecolors='m', facecolors='m', label=r"$NC$ $k_{b}^{*}=1$")
if do_kb10p0:
  ax[1].scatter(T_kb10p0_scat   , phi_mod_kb10p0_scat   , marker='+', zorder=2, alpha=1.0, c='c', label=r"$IN$ $k_{b}^{*}=10$")
  ax[1].scatter(T_kb10p0_NC_scat, phi_mod_kb10p0_NC_scat, marker='*', zorder=2, alpha=1.0, s=35, edgecolors='c', facecolors='none', label=r"$NC$ $k_{b}^{*}=10$")

if do_kb0p10:
  ax[0].scatter(T_kb0p10_scat   , phi_kb0p10_scat   , marker='+', zorder=2, alpha=1.0, c='r', label=r"$IN$ $k_{b}^{*}=0.1$")
  ax[0].scatter(T_kb0p10_NC_scat, phi_kb0p10_NC_scat, marker='*', zorder=2, alpha=1.0, s=60, edgecolors='r', facecolors='r', label=r"$NC$ $k_{b}^{*}=0.1$")
if do_kb1p00:
  ax[0].scatter(T_kb1p00_scat   , phi_kb1p00_scat   , marker='+', zorder=2, alpha=1.0, c='m', label=r"$IN$ $k_{b}^{*}=1$")
  ax[0].scatter(T_kb1p00_NC_scat, phi_kb1p00_NC_scat, marker='*', zorder=2, alpha=1.0, edgecolors='m', facecolors='m', label=r"$NC$ $k_{b}^{*}=1$")
if do_kb10p0:
  ax[0].scatter(T_kb10p0_scat   , phi_kb10p0_scat   , marker='+', zorder=2, alpha=1.0, c='c', label=r"$IN$ $k_{b}^{*}=10$")
  ax[0].scatter(T_kb10p0_NC_scat, phi_kb10p0_NC_scat, marker='*', zorder=2, alpha=1.0, s=35, edgecolors='c', facecolors='none', label=r"$NC$ $k_{b}^{*}=10$")

#fit = 0
if fit:
  # kb0.10
  slope_kb0p10, intercept_kb0p10, r_value_kb0p10, p_value_kb0p10, std_err_kb0p10 = stats.linregress(phi_mod_kb0p10_scat, T_kb0p10_scat)
  phi_mod_kb0p10_line = np.linspace(phi_min, phi_max, 1000)
  T_kb0p10_line   = phi_mod_kb0p10_line*slope_kb0p10 + intercept_kb0p10

  one = max(len(phi_mod_kb0p10_scat)-2, 1)
  model_kb0p10 = np.poly1d(np.polyfit(phi_mod_kb0p10_scat, T_kb0p10_scat, 1))
  phi_mod_kb0p10_quad = np.linspace(phi_min, phi_max, 1000)
  T_kb0p10_quad = model_kb0p10(phi_mod_kb0p10_quad)

  slope_kb0p10_NC, intercept_kb0p10_NC, r_value_kb0p10_NC, p_value_kb0p10_NC, std_err_kb0p10_NC = stats.linregress(phi_mod_kb0p10_NC_scat, T_kb0p10_NC_scat)
  phi_mod_kb0p10_NC_line = np.linspace(phi_min, phi_max, 1000)
  T_kb0p10_NC_line   = phi_mod_kb0p10_NC_line*slope_kb0p10_NC + intercept_kb0p10_NC
  
  one = max(len(phi_mod_kb0p10_NC_scat)-3, 1)
  model_kb0p10_NC = np.poly1d(np.polyfit(phi_mod_kb0p10_NC_scat, T_kb0p10_NC_scat, 50))#one))
  phi_mod_kb0p10_NC_quad = np.linspace(phi_min, phi_max, 1000)
  T_kb0p10_NC_quad = model_kb0p10_NC(phi_mod_kb0p10_NC_quad)
  idx_less_zero = (np.abs(T_kb0p10_NC_quad[50:]-0)).argmin()+50
#  print(idx_less_zero)
  T_kb0p10_NC_quad[:idx_less_zero] = 0
#  ax[1].scatter(T_kb0p10_NC_quad[idx_less_zero], phi_mod_kb0p10_NC_quad[idx_less_zero], c='k')

  # kb1.00
  slope_kb1p00, intercept_kb1p00, r_value_kb1p00, p_value_kb1p00, std_err_kb1p00 = stats.linregress(phi_mod_kb1p00_scat, T_kb1p00_scat)
  phi_mod_kb1p00_line = np.linspace(phi_min, phi_max, 1000)
  T_kb1p00_line   = phi_mod_kb1p00_line*slope_kb1p00 + intercept_kb1p00

  one = max(len(phi_mod_kb1p00_scat)-2, 1)
  model_kb1p00 = np.poly1d(np.polyfit(phi_mod_kb1p00_scat, T_kb1p00_scat, 1))
  phi_mod_kb1p00_quad = np.linspace(phi_min, phi_max, 1000)
  T_kb1p00_quad = model_kb1p00(phi_mod_kb1p00_quad)

  slope_kb1p00_NC, intercept_kb1p00_NC, r_value_kb1p00_NC, p_value_kb1p00_NC, std_err_kb1p00_NC = stats.linregress(phi_mod_kb1p00_NC_scat, T_kb1p00_NC_scat)
  phi_mod_kb1p00_NC_line = np.linspace(phi_min, phi_max, 1000)
  T_kb1p00_NC_line   = phi_mod_kb1p00_NC_line*slope_kb1p00_NC + intercept_kb1p00_NC
  
  one = max(len(phi_mod_kb1p00_NC_scat)-3, 1)
  model_kb1p00_NC = np.poly1d(np.polyfit(phi_mod_kb1p00_NC_scat, T_kb1p00_NC_scat, 5))#one))
  phi_mod_kb1p00_NC_quad = np.linspace(phi_min, phi_max, 1000)
  T_kb1p00_NC_quad = model_kb1p00_NC(phi_mod_kb1p00_NC_quad)

  # kb10.0
  slope_kb10p0, intercept_kb10p0, r_value_kb10p0, p_value_kb10p0, std_err_kb10p0 = stats.linregress(phi_mod_kb10p0_scat, T_kb10p0_scat)
  phi_mod_kb10p0_line = np.linspace(phi_min, phi_max, 1000)
  T_kb10p0_line   = phi_mod_kb10p0_line*slope_kb10p0 + intercept_kb10p0

  one = max(len(phi_mod_kb10p0_scat)-2, 1)
  model_kb10p0 = np.poly1d(np.polyfit(phi_mod_kb10p0_scat, T_kb10p0_scat, 1))
  phi_mod_kb10p0_quad = np.linspace(phi_min, phi_max, 1000)
  T_kb10p0_quad = model_kb10p0(phi_mod_kb10p0_quad)

  slope_kb10p0_NC, intercept_kb10p0_NC, r_value_kb10p0_NC, p_value_kb10p0_NC, std_err_kb10p0_NC = stats.linregress(phi_mod_kb10p0_NC_scat, T_kb10p0_NC_scat)
  phi_mod_kb10p0_NC_line = np.linspace(phi_min, phi_max, 1000)
  T_kb10p0_NC_line   = phi_mod_kb10p0_NC_line*slope_kb10p0_NC + intercept_kb10p0_NC
  
  one = max(len(phi_mod_kb10p0_NC_scat)-3, 1)
  model_kb10p0_NC = np.poly1d(np.polyfit(phi_mod_kb10p0_NC_scat, T_kb10p0_NC_scat, 10))
  phi_mod_kb10p0_NC_quad = np.linspace(phi_min, phi_max, 1000)
  T_kb10p0_NC_quad = model_kb10p0_NC(phi_mod_kb10p0_NC_quad)

  T_kb0p10_model = T_kb0p10_line
  T_kb0p10_NC_model = T_kb0p10_NC_quad
  T_kb1p00_model = T_kb1p00_line
  T_kb1p00_NC_model = T_kb1p00_NC_quad
  T_kb10p0_model = T_kb10p0_line
  T_kb10p0_NC_model = T_kb10p0_NC_quad

  T_kb1p00_NC_model[:300] = 0
  #T_kb0p10_NC_model[T_kb0p10_NC_model > T_kb0p10_model] = T_kb0p10_model[T_kb0p10_NC_model > T_kb0p10_model]
  #T_kb1p00_NC_model[T_kb1p00_NC_model > T_kb1p00_model] = T_kb1p00_model[T_kb1p00_NC_model > T_kb1p00_model]
  #T_kb10p0_NC_model[T_kb10p0_NC_model > T_kb10p0_model] = T_kb10p0_model[T_kb10p0_NC_model > T_kb10p0_model]
  T_kb0p10_model[T_kb0p10_NC_model > T_kb0p10_model] = T_kb0p10_NC_model[T_kb0p10_NC_model > T_kb0p10_model]
  T_kb1p00_model[T_kb1p00_NC_model > T_kb1p00_model] = T_kb1p00_NC_model[T_kb1p00_NC_model > T_kb1p00_model]
  T_kb10p0_model[T_kb10p0_NC_model > T_kb10p0_model] = T_kb10p0_NC_model[T_kb10p0_NC_model > T_kb10p0_model]

  phi_mod_kb0p10_model = phi_mod_kb0p10_quad
  phi_mod_kb0p10_NC_model = phi_mod_kb0p10_NC_quad
  phi_mod_kb1p00_model = phi_mod_kb1p00_quad
  phi_mod_kb1p00_NC_model = phi_mod_kb1p00_NC_quad
  phi_mod_kb10p0_model = phi_mod_kb10p0_quad
  phi_mod_kb10p0_NC_model = phi_mod_kb10p0_NC_quad

  T_kb0p10_model[T_kb0p10_model<zeroT] = zeroT
  T_kb0p10_NC_model[T_kb0p10_NC_model<zeroT] = zeroT
  T_kb1p00_model[T_kb1p00_model<zeroT] = zeroT
  T_kb1p00_NC_model[T_kb1p00_NC_model<zeroT] = zeroT
  T_kb10p0_model[T_kb10p0_model<zeroT] = zeroT
  T_kb10p0_NC_model[T_kb10p0_NC_model<zeroT] = zeroT

  del_idx = T_kb0p10_model < T_max
  T_kb0p10_model = T_kb0p10_model[del_idx]
  phi_mod_kb0p10_model = phi_mod_kb0p10_model[del_idx]
  del_idx = T_kb0p10_NC_model < T_max
  T_kb0p10_NC_model = T_kb0p10_NC_model[del_idx]
  phi_mod_kb0p10_NC_model = phi_mod_kb0p10_NC_model[del_idx]
  del_idx = T_kb1p00_model < T_max
  T_kb1p00_model = T_kb1p00_model[del_idx]
  phi_mod_kb1p00_model = phi_mod_kb1p00_model[del_idx]
  del_idx = T_kb1p00_NC_model < T_max
  T_kb1p00_NC_model = T_kb1p00_NC_model[del_idx]
  phi_mod_kb1p00_NC_model = phi_mod_kb1p00_NC_model[del_idx]
  del_idx = T_kb10p0_model < T_max
  T_kb10p0_model = T_kb10p0_model[del_idx]
  phi_mod_kb10p0_model = phi_mod_kb10p0_model[del_idx]
  del_idx = T_kb10p0_NC_model < T_max
  T_kb10p0_NC_model = T_kb10p0_NC_model[del_idx]
  phi_mod_kb10p0_NC_model = phi_mod_kb10p0_NC_model[del_idx]

  # HTH
  slope_HTH, intercept_HTH, r_value_HTH, p_value_HTH, std_err_HTH = stats.linregress(phi_HTH_scat, T_HTH_scat)
  phi_HTH_line = np.linspace(phi_min, phi_max, 1000)
  T_HTH_line   = phi_HTH_line*slope_HTH + intercept_HTH

  model = np.poly1d(np.polyfit(phi_HTH_scat, T_HTH_scat, 2))
  phi_HTH_quad = np.linspace(phi_min, phi_max, 1000)
  T_HTH_quad = model(phi_HTH_quad)
  
  slope_HTH_NC, intercept_HTH_NC, r_value_HTH_NC, p_value_HTH_NC, std_err_HTH_NC = stats.linregress(phi_HTH_NC_scat, np.log(T_HTH_NC_scat))
  phi_HTH_NC_line = np.linspace(phi_min, phi_max, 1000)
  T_HTH_NC_line   = np.exp(phi_HTH_NC_line*slope_HTH_NC + intercept_HTH_NC)

  model_HTH_NC = np.poly1d(np.polyfit(phi_HTH_NC_scat, T_HTH_NC_scat, 3))
  phi_HTH_NC_quad = np.linspace(phi_min, phi_max, 1000)
  T_HTH_NC_quad = model_HTH_NC(phi_HTH_NC_quad)

  phi_HTH_model = phi_HTH_line
  T_HTH_model   = T_HTH_line
  phi_HTH_NC_model = phi_HTH_NC_line
  T_HTH_NC_model   = T_HTH_NC_line

  #del_idx = T_HTH_NC_model < T_HTH_model
  #phi_HTH_NC_model = phi_HTH_NC_model[del_idx]
  #T_HTH_NC_model = T_HTH_NC_model[del_idx]
  T_HTH_model[T_HTH_NC_model > T_HTH_model] = T_HTH_NC_model[T_HTH_NC_model > T_HTH_model]
  del_idx = T_HTH_NC_model > 0
  T_HTH_NC_model = T_HTH_NC_model[del_idx]
  phi_HTH_NC_model = phi_HTH_NC_model[del_idx]

  # no transitions below phi_cryst
  keep_idx = phi_HTH_NC_model > phi_cryst
  T_HTH_NC_model = T_HTH_NC_model[keep_idx]
  phi_HTH_NC_model = phi_HTH_NC_model[keep_idx]

#  print("HTH:T="   , str(round(slope_HTH, 3))   , "phi", str(round(intercept_HTH, 3))   , "R2", str(round(r_value_HTH, 5)), "p2", str(round(p_value_HTH, 5)))
#  print("kb0p10:T=", str(round(slope_kb0p10, 3)), "phi", str(round(intercept_kb0p10, 3)), "R2", str(round(r_value_kb0p10, 5)), "p2", str(round(p_value_kb0p10, 5)))
#  print("kb1p00:T=", str(round(slope_kb1p00, 3)), "phi", str(round(intercept_kb1p00, 3)), "R2", str(round(r_value_kb1p00, 5)), "p2", str(round(p_value_kb1p00, 5)))
#  print("kb10p0:T=", str(round(slope_kb10p0, 3)), "phi", str(round(intercept_kb10p0, 3)), "R2", str(round(r_value_kb10p0, 5)), "p2", str(round(p_value_kb10p0, 5)))

#  m1 = (slope_kb1p00-slope_kb0p10)/(1.0-0.1)
#  m2 = (slope_kb10p0-slope_kb0p10)/(10.0-0.1)
#  m3 = (slope_kb10p0-slope_kb1p00)/(10.0-1.0)
#  i1 = slope_kb0p10-m1*0.1
#  i2 = slope_kb0p10-m2*0.1
#  i3 = slope_kb1p00-m3*1.0
#  print(m1, i1)
#  print(m2, i2)
#  print(m3, i3)

  if do_HTH:
    ax[1].plot(T_HTH_model   , phi_HTH_model   , color='b', ls='--', dashes=(5, 3), zorder=1)#, label="IN")
    ax[1].plot(T_HTH_NC_model, phi_HTH_NC_model, color='b', ls='--', dashes=(5, 3), zorder=1)#, label="NC")
  if do_kb0p10:
    ax[1].plot(T_kb0p10_model   , phi_mod_kb0p10_model   , color='r', zorder=1)#, label="IN")
    ax[1].plot(T_kb0p10_NC_model, phi_mod_kb0p10_NC_model, color='r', zorder=1)#, label="NC")
  if do_kb1p00:
    ax[1].plot(T_kb1p00_model   , phi_mod_kb1p00_model   , color='m', zorder=1)#, label="IN")
    ax[1].plot(T_kb1p00_NC_model, phi_mod_kb1p00_NC_model, color='m', zorder=1)#, label="NC")
  if do_kb10p0:
    ax[1].plot(T_kb10p0_model   , phi_mod_kb10p0_model   , color='c', zorder=1)#, label="IN")
    ax[1].plot(T_kb10p0_NC_model, phi_mod_kb10p0_NC_model, color='c', zorder=1)#, label="NC")

  # kb0.10
  slope_kb0p10, intercept_kb0p10, r_value_kb0p10, p_value_kb0p10, std_err_kb0p10 = stats.linregress(phi_kb0p10_scat, T_kb0p10_scat)
  phi_kb0p10_line = np.linspace(phi_min, phi_max, 1000)
  T_kb0p10_line   = phi_kb0p10_line*slope_kb0p10 + intercept_kb0p10

  one = max(len(phi_kb0p10_scat)-2, 1)
  model_kb0p10 = np.poly1d(np.polyfit(phi_kb0p10_scat, T_kb0p10_scat, 1))
  phi_kb0p10_quad = np.linspace(phi_min, phi_max, 1000)
  T_kb0p10_quad = model_kb0p10(phi_kb0p10_quad)

  slope_kb0p10_NC, intercept_kb0p10_NC, r_value_kb0p10_NC, p_value_kb0p10_NC, std_err_kb0p10_NC = stats.linregress(phi_kb0p10_NC_scat, T_kb0p10_NC_scat)
  phi_kb0p10_NC_line = np.linspace(phi_min, phi_max, 1000)
  T_kb0p10_NC_line   = phi_kb0p10_NC_line*slope_kb0p10_NC + intercept_kb0p10_NC
  
  one = max(len(phi_kb0p10_NC_scat)-3, 1)
  model_kb0p10_NC = np.poly1d(np.polyfit(phi_kb0p10_NC_scat, T_kb0p10_NC_scat, 50))#one))
  phi_kb0p10_NC_quad = np.linspace(phi_min, phi_max, 1000)
  T_kb0p10_NC_quad = model_kb0p10_NC(phi_kb0p10_NC_quad)
  idx_less_zero = (np.abs(T_kb0p10_NC_quad[50:]-0)).argmin()+50
#  print(idx_less_zero)
  T_kb0p10_NC_quad[:idx_less_zero] = 0
#  ax[1].scatter(T_kb0p10_NC_quad[idx_less_zero], phi_kb0p10_NC_quad[idx_less_zero], c='k')

  # kb1.00
  slope_kb1p00, intercept_kb1p00, r_value_kb1p00, p_value_kb1p00, std_err_kb1p00 = stats.linregress(phi_kb1p00_scat, T_kb1p00_scat)
  phi_kb1p00_line = np.linspace(phi_min, phi_max, 1000)
  T_kb1p00_line   = phi_kb1p00_line*slope_kb1p00 + intercept_kb1p00

  one = max(len(phi_kb1p00_scat)-2, 1)
  model_kb1p00 = np.poly1d(np.polyfit(phi_kb1p00_scat, T_kb1p00_scat, 1))
  phi_kb1p00_quad = np.linspace(phi_min, phi_max, 1000)
  T_kb1p00_quad = model_kb1p00(phi_kb1p00_quad)

  slope_kb1p00_NC, intercept_kb1p00_NC, r_value_kb1p00_NC, p_value_kb1p00_NC, std_err_kb1p00_NC = stats.linregress(phi_kb1p00_NC_scat, T_kb1p00_NC_scat)
  phi_kb1p00_NC_line = np.linspace(phi_min, phi_max, 1000)
  T_kb1p00_NC_line   = phi_kb1p00_NC_line*slope_kb1p00_NC + intercept_kb1p00_NC
  
  one = max(len(phi_kb1p00_NC_scat)-3, 1)
  model_kb1p00_NC = np.poly1d(np.polyfit(phi_kb1p00_NC_scat, T_kb1p00_NC_scat, 5))#one))
  phi_kb1p00_NC_quad = np.linspace(phi_min, phi_max, 1000)
  T_kb1p00_NC_quad = model_kb1p00_NC(phi_kb1p00_NC_quad)

  # kb10.0
  slope_kb10p0, intercept_kb10p0, r_value_kb10p0, p_value_kb10p0, std_err_kb10p0 = stats.linregress(phi_kb10p0_scat, T_kb10p0_scat)
  phi_kb10p0_line = np.linspace(phi_min, phi_max, 1000)
  T_kb10p0_line   = phi_kb10p0_line*slope_kb10p0 + intercept_kb10p0

  one = max(len(phi_kb10p0_scat)-2, 1)
  model_kb10p0 = np.poly1d(np.polyfit(phi_kb10p0_scat, T_kb10p0_scat, 1))
  phi_kb10p0_quad = np.linspace(phi_min, phi_max, 1000)
  T_kb10p0_quad = model_kb10p0(phi_kb10p0_quad)

  slope_kb10p0_NC, intercept_kb10p0_NC, r_value_kb10p0_NC, p_value_kb10p0_NC, std_err_kb10p0_NC = stats.linregress(phi_kb10p0_NC_scat, T_kb10p0_NC_scat)
  phi_kb10p0_NC_line = np.linspace(phi_min, phi_max, 1000)
  T_kb10p0_NC_line   = phi_kb10p0_NC_line*slope_kb10p0_NC + intercept_kb10p0_NC
  
  one = max(len(phi_kb10p0_NC_scat)-3, 1)
  model_kb10p0_NC = np.poly1d(np.polyfit(phi_kb10p0_NC_scat, T_kb10p0_NC_scat, 10))
  phi_kb10p0_NC_quad = np.linspace(phi_min, phi_max, 1000)
  T_kb10p0_NC_quad = model_kb10p0_NC(phi_kb10p0_NC_quad)

  T_kb0p10_model = T_kb0p10_line
  T_kb0p10_NC_model = T_kb0p10_NC_quad
  T_kb1p00_model = T_kb1p00_line
  T_kb1p00_NC_model = T_kb1p00_NC_quad
  T_kb10p0_model = T_kb10p0_line
  T_kb10p0_NC_model = T_kb10p0_NC_quad

  T_kb1p00_NC_model[:300] = 0
  T_kb0p10_model[T_kb0p10_NC_model > T_kb0p10_model] = T_kb0p10_NC_model[T_kb0p10_NC_model > T_kb0p10_model]
  T_kb1p00_model[T_kb1p00_NC_model > T_kb1p00_model] = T_kb1p00_NC_model[T_kb1p00_NC_model > T_kb1p00_model]
  T_kb10p0_model[T_kb10p0_NC_model > T_kb10p0_model] = T_kb10p0_NC_model[T_kb10p0_NC_model > T_kb10p0_model]

  phi_kb0p10_model = phi_kb0p10_quad
  phi_kb0p10_NC_model = phi_kb0p10_NC_quad
  phi_kb1p00_model = phi_kb1p00_quad
  phi_kb1p00_NC_model = phi_kb1p00_NC_quad
  phi_kb10p0_model = phi_kb10p0_quad
  phi_kb10p0_NC_model = phi_kb10p0_NC_quad

  T_kb0p10_model[T_kb0p10_model<zeroT] = zeroT
  T_kb0p10_NC_model[T_kb0p10_NC_model<zeroT] = zeroT
  T_kb1p00_model[T_kb1p00_model<zeroT] = zeroT
  T_kb1p00_NC_model[T_kb1p00_NC_model<zeroT] = zeroT
  T_kb10p0_model[T_kb10p0_model<zeroT] = zeroT
  T_kb10p0_NC_model[T_kb10p0_NC_model<zeroT] = zeroT

  del_idx = T_kb0p10_model < T_max
  T_kb0p10_model = T_kb0p10_model[del_idx]
  phi_kb0p10_model = phi_kb0p10_model[del_idx]
  del_idx = T_kb0p10_NC_model < T_max
  T_kb0p10_NC_model = T_kb0p10_NC_model[del_idx]
  phi_kb0p10_NC_model = phi_kb0p10_NC_model[del_idx]
  del_idx = T_kb1p00_model < T_max
  T_kb1p00_model = T_kb1p00_model[del_idx]
  phi_kb1p00_model = phi_kb1p00_model[del_idx]
  del_idx = T_kb1p00_NC_model < T_max
  T_kb1p00_NC_model = T_kb1p00_NC_model[del_idx]
  phi_kb1p00_NC_model = phi_kb1p00_NC_model[del_idx]
  del_idx = T_kb10p0_model < T_max
  T_kb10p0_model = T_kb10p0_model[del_idx]
  phi_kb10p0_model = phi_kb10p0_model[del_idx]
  del_idx = T_kb10p0_NC_model < T_max
  T_kb10p0_NC_model = T_kb10p0_NC_model[del_idx]
  phi_kb10p0_NC_model = phi_kb10p0_NC_model[del_idx]

  if do_HTH:
    ax[0].plot(T_HTH_model   , phi_HTH_model   , color='b', ls='--', dashes=(5, 3), zorder=1)#, label="IN")
    ax[0].plot(T_HTH_NC_model, phi_HTH_NC_model, color='b', ls='--', dashes=(5, 3), zorder=1)#, label="NC")
  if do_kb0p10:
    ax[0].plot(T_kb0p10_model   , phi_kb0p10_model   , color='r', alpha=1, zorder=1)#, label="IN")
    ax[0].plot(T_kb0p10_NC_model, phi_kb0p10_NC_model, color='r', alpha=1, zorder=1)#, label="NC")
  if do_kb1p00:
    ax[0].plot(T_kb1p00_model   , phi_kb1p00_model   , color='m', alpha=1, zorder=1)#, label="IN")
    ax[0].plot(T_kb1p00_NC_model, phi_kb1p00_NC_model, color='m', alpha=1, zorder=1)#, label="NC")
  if do_kb10p0:
    ax[0].plot(T_kb10p0_model   , phi_kb10p0_model   , color='c', alpha=1, zorder=1)#, label="IN")
    ax[0].plot(T_kb10p0_NC_model, phi_kb10p0_NC_model, color='c', alpha=1, zorder=1)#, label="NC")

ax[0].set_xlabel(r"$T_{r}$", fontsize=10, labelpad=6)#, labelpad=0.3)
ax[0].set_ylabel(r"$\phi$", fontsize=10, labelpad=5.5)
ax[0].tick_params(axis='both', labelsize=8, pad=0)
ax[0].set_xlim(T_min-0.004, T_max)
ax[0].set_ylim(phi_min, phi_max)
from matplotlib.lines import Line2D
legend_elements = [
                   Line2D([0], [0], marker='+', color='k', label='IN',
                          markerfacecolor='k', markersize=6),
                   Line2D([0], [0], marker='*', color='w', label='NC',
                          markerfacecolor='k', markersize=10),
                   Line2D([0], [0], color='b', lw=2, label='hard rods'),
                   Line2D([0], [0], color='r', lw=2, label=r'$k_{b}^{*}=0.1$'),
                   Line2D([0], [0], color='m', lw=2, label=r'$k_{b}^{*}=1$'),
                   Line2D([0], [0], color='c', lw=2, label=r'$k_{b}^{*}=10$')
                  ]
ax[0].legend(handles=legend_elements, loc='lower right', ncol=1, columnspacing=1.0, fontsize=7.5, handletextpad=1, handlelength=0.5, borderpad=0.5)#, bbox_to_anchor=(1.02,-0.02))
ax[0].set_yticks([0.25, 0.3, 0.35, 0.4, 0.45, 0.5])
ax[0].set_yticklabels(["", "0.3", "", "0.4", "", "0.5"])
ax[0].set_xticks([0.0,0.1,0.2])

ax[1].set_xlabel(r"$T_{r}$", fontsize=10, labelpad=6)#, labelpad=0.3)
ax[1].set_ylabel(r"$\phi_{\mathrm{eff}}$", fontsize=10, labelpad=5.5)
ax[1].tick_params(axis='both', labelsize=8, pad=0)
ax[1].set_xlim(T_min-0.004, T_max)
ax[1].set_ylim(phi_min, phi_max)
from matplotlib.lines import Line2D
legend_elements = [
                   Line2D([0], [0], marker='+', color='k', label='IN',
                          markerfacecolor='k', markersize=6),
                   Line2D([0], [0], marker='*', color='w', label='NC',
                          markerfacecolor='k', markersize=10),
                   Line2D([0], [0], color='b', lw=2, label='hard rods'),
                   Line2D([0], [0], color='r', lw=2, label=r'$k_{b}^{*}=0.1$'),
                   Line2D([0], [0], color='m', lw=2, label=r'$k_{b}^{*}=1$'),
                   Line2D([0], [0], color='c', lw=2, label=r'$k_{b}^{*}=10$')
                  ]
ax[1].legend(handles=legend_elements, loc='lower right', ncol=1, columnspacing=1.0, fontsize=7.5, handletextpad=1, handlelength=0.5, borderpad=0.5)#, bbox_to_anchor=(1.02,-0.02))
ax[1].set_yticks([0.25, 0.3, 0.35, 0.4, 0.45, 0.5])
ax[1].set_yticklabels(["", "0.3", "", "0.4", "", "0.5"])
ax[1].set_xticks([0.0,0.1,0.2])

ax[0].text(-0.16, 0.95, r"a)", fontsize=12, transform=ax[0].transAxes)
ax[1].text(-0.16, 0.95, r"b)", fontsize=12, transform=ax[1].transAxes)

#plt.subplots_adjust(left=0.156, top=0.98, bottom=0.135, right=0.974)
plt.subplots_adjust(left=0.071, top=0.999, bottom=0.118, right=0.999)
#plt.show()
#sys.exit()
plt.savefig("fig-phase_diag_phiHS.pdf")
plt.close()
