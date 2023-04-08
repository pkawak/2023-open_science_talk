#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
created on Sat May 22 08:41:00 2021

@author: pierrekawak
"""

import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("tkagg")
from scipy import stats
import pandas as pd
from scipy.integrate import quad

Nc    = 125
Nb    = 10
sigma = 1

fit    = 1
crit   = 1

phi_min = 0.23
phi_max = 0.525
T_min = 0.0
T_max = 0.2
zeroT = 0.0

phi_HTH_cryst   = 0.31
WL_Ts_files = np.array([
                     "Lx11.000_kb0.10_WLMC_Ts.out", "Lx11.000_kb1.00_WLMC_Ts.out", "Lx11.000_kb10.0_WLMC_Ts.out",
                     "Lx11.436_kb0.10_WLMC_Ts.out", "Lx11.436_kb1.00_WLMC_Ts.out", "Lx11.436_kb10.0_WLMC_Ts.out",
                     "Lx13.000_kb0.10_WLMC_Ts.out", "Lx13.000_kb1.00_WLMC_Ts.out", "Lx13.000_kb10.0_WLMC_Ts.out",
                     "Lx15.000_kb0.10_WLMC_Ts.out", "Lx15.000_kb1.00_WLMC_Ts.out", "Lx15.000_kb10.0_WLMC_Ts.out",
                     "Lx11.200_kb1.00_WLMC_Ts.out", "Lx11.800_kb1.00_WLMC_Ts.out", "Lx12.500_kb1.00_WLMC_Ts.out", "Lx13.500_kb1.00_WLMC_Ts.out",
                     "Lx10.800_kb1.00_WLMC_Ts.out", "Lx10.850_kb1.00_WLMC_Ts.out", "Lx10.900_kb1.00_WLMC_Ts.out", "Lx10.950_kb1.00_WLMC_Ts.out"
                    ])
Lx_  = np.array([ float(name.split('x')[1].split('_')[0]) for name in WL_Ts_files ])
phi_     = Nc*Nb*sigma**3/Lx_**3*np.pi/6
kb_  = np.array([ float(name.split('b')[1].split('_')[0]) for name in WL_Ts_files ])

input_df = pd.DataFrame({"Ts_files": WL_Ts_files, "Lx": Lx_, "phi": phi_, "kb": kb_})

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

def return_reff_diff(reff, T, eps=1.0):
  target = 1.0*T
  return(WCA(reff) - target)

r_min = 0.0
r_max = 1.0
def return_dR_int(dist, T):
  return( 1 - np.exp(-WCA(dist)/T) )

reff_kb0p10_scat = []
phi_mod_kb0p10_scat = []
for phii, Ti in zip(phi_kb0p10_scat, T_kb0p10_scat):
  Ti *= 0.10
  reff = quad(return_dR_int, r_min, r_max, args=(Ti))[0]
  reff_kb0p10_scat.append(reff)
  phi_mod_kb0p10_scat.append(phii*reff**3)

reff_kb0p10_NC_scat = []
phi_mod_kb0p10_NC_scat = []
for phii, Ti in zip(phi_kb0p10_NC_scat, T_kb0p10_NC_scat):
  Ti *= 0.10
  reff = quad(return_dR_int, r_min, r_max, args=(Ti))[0]
  reff_kb0p10_NC_scat.append(reff)
  phi_mod_kb0p10_NC_scat.append(phii*reff**3)

reff_kb1p00_scat = []
phi_mod_kb1p00_scat = []
for phii, Ti in zip(phi_kb1p00_scat, T_kb1p00_scat):
  Ti *= 1.00
  reff = quad(return_dR_int, r_min, r_max, args=(Ti))[0]
  reff_kb1p00_scat.append(reff)
  phi_mod_kb1p00_scat.append(phii*reff**3)

reff_kb1p00_NC_scat = []
phi_mod_kb1p00_NC_scat = []
for phii, Ti in zip(phi_kb1p00_NC_scat, T_kb1p00_NC_scat):
  Ti *= 1.00
  reff = quad(return_dR_int, r_min, r_max, args=(Ti))[0]
  reff_kb1p00_NC_scat.append(reff)
  phi_mod_kb1p00_NC_scat.append(phii*reff**3)

reff_kb10p0_scat = []
phi_mod_kb10p0_scat = []
for phii, Ti in zip(phi_kb10p0_scat, T_kb10p0_scat):
  Ti *= 10.0
  reff = quad(return_dR_int, r_min, r_max, args=(Ti))[0]
  reff_kb10p0_scat.append(reff)
  phi_mod_kb10p0_scat.append(phii*reff**3)

reff_kb10p0_NC_scat = []
phi_mod_kb10p0_NC_scat = []
for phii, Ti in zip(phi_kb10p0_NC_scat, T_kb10p0_NC_scat):
  Ti *= 10.0
  reff = quad(return_dR_int, r_min, r_max, args=(Ti))[0]
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

T_HTH_NC_scat = T_2_scat
phi_HTH_NC_scat = phi_HTH_scat
T_HTH_NC_scat[T_HTH_NC_scat < 0.0001] = 0.0001
T_HTH_NC_scatt   = T_2_scat[phi_HTH_scat > phi_HTH_cryst]
phi_HTH_NC_scatt = phi_HTH_scat[phi_HTH_scat > phi_HTH_cryst]
T_HTH_scat      = T_1_scat

do_kb0p10 = 1
do_kb1p00 = 1
do_kb10p0 = 1

test = 0
# make figure and axis objects
fig0, ax0 = plt.subplots(1, 1, figsize=(2.75, 2.90), constrained_layout=test)
fig1, ax1 = plt.subplots(1, 1, figsize=(2.75, 2.90), constrained_layout=test)
fig2, ax2 = plt.subplots(1, 1, figsize=(2.70, 2.70), constrained_layout=test)
# plot points
#if do_HTH:
#  ax1.scatter(T_HTH_scat    , phi_HTH_scat    , color='b', marker='o', zorder=2, label=r"$IN$ hard")
#  ax1.scatter(T_HTH_NC_scatt, phi_HTH_NC_scatt, color='b', marker='*', s=50, zorder=2, label=r"$NC$ hard")
if do_kb0p10:
  ax1.scatter(T_kb0p10_scat   , phi_mod_kb0p10_scat   , marker='o', zorder=2, alpha=1.0, c='r', label=r"$IN$ $k_{b}^{*}=0.1$")
  ax1.scatter(T_kb0p10_NC_scat, phi_mod_kb0p10_NC_scat, marker='*', s=50, zorder=2, alpha=1.0, edgecolors='r', facecolors='r', label=r"$NC$ $k_{b}^{*}=0.1$")
  ax2.scatter(T_kb0p10_scat   , phi_mod_kb0p10_scat   , marker='o', zorder=2, alpha=1.0, c='r', label=r"$IN$ $k_{b}^{*}=0.1$")
  ax2.scatter(T_kb0p10_NC_scat, phi_mod_kb0p10_NC_scat, marker='*', s=50, zorder=2, alpha=1.0, edgecolors='r', facecolors='r', label=r"$NC$ $k_{b}^{*}=0.1$")
if do_kb1p00:
  ax1.scatter(T_kb1p00_scat   , phi_mod_kb1p00_scat   , marker='o', zorder=2, alpha=1.0, c='m', label=r"$IN$ $k_{b}^{*}=1$")
  ax1.scatter(T_kb1p00_NC_scat, phi_mod_kb1p00_NC_scat, marker='*', s=50, zorder=2, alpha=1.0, edgecolors='m', facecolors='m', label=r"$NC$ $k_{b}^{*}=1$")
  ax2.scatter(T_kb1p00_scat   , phi_mod_kb1p00_scat   , marker='o', zorder=2, alpha=1.0, c='m', label=r"$IN$ $k_{b}^{*}=1$")
  ax2.scatter(T_kb1p00_NC_scat, phi_mod_kb1p00_NC_scat, marker='*', s=50, zorder=2, alpha=1.0, edgecolors='m', facecolors='m', label=r"$NC$ $k_{b}^{*}=1$")
if do_kb10p0:
  ax1.scatter(T_kb10p0_scat   , phi_mod_kb10p0_scat   , marker='o', zorder=2, alpha=1.0, c='c', label=r"$IN$ $k_{b}^{*}=10$")
  ax1.scatter(T_kb10p0_NC_scat, phi_mod_kb10p0_NC_scat, marker='*', s=50, zorder=2, alpha=1.0, edgecolors='c', facecolors='none', label=r"$NC$ $k_{b}^{*}=10$")
  ax2.scatter(T_kb10p0_scat   , phi_mod_kb10p0_scat   , marker='o', zorder=2, alpha=1.0, c='c', label=r"$IN$ $k_{b}^{*}=10$")
  ax2.scatter(T_kb10p0_NC_scat, phi_mod_kb10p0_NC_scat, marker='*', s=50, zorder=2, alpha=1.0, edgecolors='c', facecolors='none', label=r"$NC$ $k_{b}^{*}=10$")

if do_kb0p10:
  ax0.scatter(T_kb0p10_scat   , phi_kb0p10_scat   , marker='o', zorder=2, alpha=1.0, c='r', label=r"$IN$ $k_{b}^{*}=0.1$")
  ax0.scatter(T_kb0p10_NC_scat, phi_kb0p10_NC_scat, marker='*', s=50, zorder=2, alpha=1.0, edgecolors='r', facecolors='r', label=r"$NC$ $k_{b}^{*}=0.1$")
if do_kb1p00:
  ax0.scatter(T_kb1p00_scat   , phi_kb1p00_scat   , marker='o', zorder=2, alpha=1.0, c='m', label=r"$IN$ $k_{b}^{*}=1$")
  ax0.scatter(T_kb1p00_NC_scat, phi_kb1p00_NC_scat, marker='*', s=50, zorder=2, alpha=1.0, edgecolors='m', facecolors='m', label=r"$NC$ $k_{b}^{*}=1$")
if do_kb10p0:
  ax0.scatter(T_kb10p0_scat   , phi_kb10p0_scat   , marker='o', zorder=2, alpha=1.0, c='c', label=r"$IN$ $k_{b}^{*}=10$")
  ax0.scatter(T_kb10p0_NC_scat, phi_kb10p0_NC_scat, marker='*', s=50, zorder=2, alpha=1.0, edgecolors='c', facecolors='none', label=r"$NC$ $k_{b}^{*}=10$")

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
#  ax1.scatter(T_kb0p10_NC_quad[idx_less_zero], phi_mod_kb0p10_NC_quad[idx_less_zero], c='k')

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

  # HTH IN linear fit
  slope_HTH, intercept_HTH, r_value_HTH, p_value_HTH, std_err_HTH = stats.linregress(phi_HTH_scat, T_HTH_scat)
  phi_HTH_line = np.linspace(phi_min, phi_max, 1000)
  T_HTH_line   = phi_HTH_line*slope_HTH + intercept_HTH

  # HTH IN quad fit
  model = np.poly1d(np.polyfit(phi_HTH_scat, T_HTH_scat, 2))
  phi_HTH_quad = np.linspace(phi_min, phi_max, 1000)
  T_HTH_quad = model(phi_HTH_quad)

  # HTH NC log(T) fit
  slope_HTH_NC, intercept_HTH_NC, r_value_HTH_NC, p_value_HTH_NC, std_err_HTH_NC = stats.linregress(phi_HTH_NC_scat, np.log(T_HTH_NC_scat))
  phi_HTH_NC_line = np.linspace(phi_min, phi_max, 1000)
  T_HTH_NC_line   = np.exp(phi_HTH_NC_line*slope_HTH_NC + intercept_HTH_NC)

  # HTH NC quad fit
  model_HTH_NC = np.poly1d(np.polyfit(phi_HTH_NC_scat, T_HTH_NC_scat, 5))
  phi_HTH_NC_quad = np.linspace(phi_min, phi_max, 1000)
  T_HTH_NC_quad = model_HTH_NC(phi_HTH_NC_quad)

  # choose fits for each
  phi_HTH_model    = phi_HTH_line
  T_HTH_model      = T_HTH_line
  phi_HTH_NC_model = phi_HTH_NC_quad
  T_HTH_NC_model   = T_HTH_NC_quad

#  # zero out everything after negative
#  last_neg_idx = np.amax(np.arange(len(T_HTH_NC_model))[T_HTH_NC_model < 0]+1)
#  T_HTH_NC_model[:last_neg_idx] = 0
#
  # remove points where T_HTH_model is larger than T_HTH_NC_model
  keep_idx = T_HTH_NC_model < T_HTH_model
  T_HTH_model = T_HTH_model[keep_idx]
  phi_HTH_model = phi_HTH_model[keep_idx]

  # separate points after intersection
  T_HTH_NC_assum   = T_HTH_NC_model  [np.invert(keep_idx)]
  phi_HTH_NC_assum = phi_HTH_NC_model[np.invert(keep_idx)]
  T_HTH_NC_model   = T_HTH_NC_model  [keep_idx]
  phi_HTH_NC_model = phi_HTH_NC_model[keep_idx]

  # remove all point less than or equal to 0
  keep_idx = T_HTH_NC_model > 0
  T_HTH_NC_model = T_HTH_NC_model[keep_idx]
  phi_HTH_NC_model = phi_HTH_NC_model[keep_idx]

  # no transitions below phi_HTH_cryst
  keep_idx = phi_HTH_NC_model > phi_HTH_cryst
  T_HTH_NC_model = T_HTH_NC_model[keep_idx]
  phi_HTH_NC_model = phi_HTH_NC_model[keep_idx]

  if do_HTH:
    ax1.plot(T_HTH_model   , phi_HTH_model   , color='b', ls='-', zorder=1)#, label="IN")
    ax1.plot(T_HTH_NC_model, phi_HTH_NC_model, color='b', ls='-', zorder=1)#, label="NC")
    ax1.plot(T_HTH_NC_assum, phi_HTH_NC_assum, color='b', ls='--', zorder=1)#, dashes=(5, 3))#, label="NC")
    ax2.plot(T_HTH_model   , phi_HTH_model   , color='b', ls='-', zorder=1)#, label="IN")
    ax2.plot(T_HTH_NC_model, phi_HTH_NC_model, color='b', ls='-', zorder=1)#, label="NC")
    ax2.plot(T_HTH_NC_assum, phi_HTH_NC_assum, color='b', ls='--', zorder=1)#, dashes=(5, 3))#, label="NC")
#  if do_kb0p10:
#    ax1.plot(T_kb0p10_model   , phi_mod_kb0p10_model   , color='r', zorder=1)#, label="IN")
#    ax1.plot(T_kb0p10_NC_model, phi_mod_kb0p10_NC_model, color='r', zorder=1)#, label="NC")
#  if do_kb1p00:
#    ax1.plot(T_kb1p00_model   , phi_mod_kb1p00_model   , color='m', zorder=1)#, label="IN")
#    ax1.plot(T_kb1p00_NC_model, phi_mod_kb1p00_NC_model, color='m', zorder=1)#, label="NC")
#  if do_kb10p0:
#    ax1.plot(T_kb10p0_model   , phi_mod_kb10p0_model   , color='c', zorder=1)#, label="IN")
#    ax1.plot(T_kb10p0_NC_model, phi_mod_kb10p0_NC_model, color='c', zorder=1)#, label="NC")

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
#  ax1.scatter(T_kb0p10_NC_quad[idx_less_zero], phi_kb0p10_NC_quad[idx_less_zero], c='k')

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
    ax0.plot(T_HTH_model   , phi_HTH_model   , color='b', ls='-', zorder=1)#, label="IN")
    ax0.plot(T_HTH_NC_model, phi_HTH_NC_model, color='b', ls='-', zorder=1)#, label="NC")
    ax0.plot(T_HTH_NC_assum, phi_HTH_NC_assum, color='b', ls='--', zorder=1)#, dashes=(5, 3))#, label="NC")
#  if do_kb0p10:
#    ax0.plot(T_kb0p10_model   , phi_kb0p10_model   , color='r', alpha=1, zorder=1)#, label="IN")
#    ax0.plot(T_kb0p10_NC_model, phi_kb0p10_NC_model, color='r', alpha=1, zorder=1)#, label="NC")
#  if do_kb1p00:
#    ax0.plot(T_kb1p00_model   , phi_kb1p00_model   , color='m', alpha=1, zorder=1)#, label="IN")
#    ax0.plot(T_kb1p00_NC_model, phi_kb1p00_NC_model, color='m', alpha=1, zorder=1)#, label="NC")
#  if do_kb10p0:
#    ax0.plot(T_kb10p0_model   , phi_kb10p0_model   , color='c', alpha=1, zorder=1)#, label="IN")
#    ax0.plot(T_kb10p0_NC_model, phi_kb10p0_NC_model, color='c', alpha=1, zorder=1)#, label="NC")

from matplotlib.lines import Line2D
legend_elements = [
                   Line2D([0], [0], marker='o', color='k', label='IN',
                          markerfacecolor='k', markersize=6),
                   Line2D([0], [0], marker='*', color='w', label='NC',
                          markerfacecolor='k', markersize=13),
               #    Line2D([0], [0], color='b', lw=2, label='hard rods'),
                   Line2D([0], [0], color='r', lw=2, label=r'$\epsilon_{\theta}^{*}=0.1$'),
                   Line2D([0], [0], color='m', lw=2, label=r'$\epsilon_{\theta}^{*}=1$'),
                   Line2D([0], [0], color='c', lw=2, label=r'$\epsilon_{\theta}^{*}=10$')
                  ]
ax0.legend(handles=legend_elements, loc='lower right', ncol=1, columnspacing=0.5, fontsize=10, handletextpad=1, handlelength=0.5, borderpad=0.5)#, bbox_to_anchor=(1.02,-0.02))
ax0.set_xlabel(r"$T_{r}$", fontsize=12, labelpad=4)
ax0.set_ylabel(r"$\phi$", fontsize=12, labelpad=1)
ax0.tick_params(axis='both', labelsize=9, pad=0)
ax0.set_xlim(T_min-0.004, T_max)
ax0.set_ylim(phi_min, phi_max)
ax0.set_xticks([0.0,0.05,0.1,0.15])
ax0.set_yticks([0.25, 0.3, 0.35, 0.4, 0.45, 0.5])
ax0.set_yticklabels(["", "0.3", "", "0.4", "", "0.5"])

ax1.set_xlabel(r"$T_{r}$", fontsize=12, labelpad=4)
ax1.set_ylabel(r"$\phi_{\mathrm{eff}}$", fontsize=12, labelpad=1)
ax1.tick_params(axis='both', labelsize=9, pad=0)
ax1.set_xlim(T_min-0.004, T_max)
ax1.set_ylim(phi_min, phi_max)
ax1.set_xticks([0.0,0.05,0.1,0.15])
ax1.set_yticks([0.25, 0.3, 0.35, 0.4, 0.45, 0.5])
ax1.set_yticklabels(["", "0.3", "", "0.4", "", "0.5"])

ax1.legend(handles=legend_elements, loc='lower right', ncol=1, columnspacing=0.5, fontsize=9, handletextpad=1, handlelength=0.5, borderpad=0.5)#, bbox_to_anchor=(1.02,-0.02))

ax2.set_xlabel(r"$T_{r}$", fontsize=10, labelpad=4)
ax2.set_ylabel(r"$\phi_{\mathrm{eff}}$", fontsize=10, labelpad=1)
ax2.tick_params(axis='both', labelsize=8, pad=0)
ax2.set_xlim(T_min-0.004, T_max)
ax2.set_ylim(phi_min, phi_max)
ax2.set_xticks([0.0,0.05,0.1,0.15])
ax2.set_yticks([0.25, 0.3, 0.35, 0.4, 0.45, 0.5])
ax2.set_yticklabels(["", "0.3", "", "0.4", "", "0.5"])

ax2.legend(handles=legend_elements, loc='lower right', ncol=1, columnspacing=0.5, fontsize=9, handletextpad=1, handlelength=0.5, borderpad=0.5)#, bbox_to_anchor=(1.02,-0.02))

if test == 0:
  fig0.subplots_adjust(left=0.162, top=0.996, bottom=0.132, right=0.996)
  fig1.subplots_adjust(left=0.162, top=0.996, bottom=0.132, right=0.996)
  fig2.subplots_adjust(left=0.146, top=0.996, bottom=0.125, right=0.996)

fig0.savefig("fig-phase_diag_phi_HS.pdf")
fig1.savefig("fig-phase_diag_phi_eff.pdf")
fig2.savefig("fig-phase_diag_phi_eff_small.pdf")

plt.close()
