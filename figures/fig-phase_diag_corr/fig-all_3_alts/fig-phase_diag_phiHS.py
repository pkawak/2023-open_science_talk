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
from scipy.optimize import fsolve
from scipy.integrate import quad

Nc    = 125
Nb    = 10
sigma = 1
label_prefix = r'$\phi=$'

shade  = 0
fit    = 1
crit   = 1

do_kb0p10 = 1
do_kb1p00 = 1
do_kb10p0 = 1

shade_crystal = '#185ADB'
shade_nematic = '#FFC947'
shade_melt    = '#EFEFEF'

phi_min = 0.23
phi_max = 0.51
phi_max = 0.525
T_min   = 0.0
T_max   = 0.2
zeroT   = 0.0

# figure settings
test       = 1    # set equal to 1 for constrained_layout
fig_width  = 3/2*6.5 # inches
fig_height = 3.1  # inches

WL_Ts_files = np.array([
                     "../data_files/Lx11.000_kb0.10_WLMC_Ts.out", "../data_files/Lx11.000_kb1.00_WLMC_Ts.out", "../data_files/Lx11.000_kb10.0_WLMC_Ts.out",
                     "../data_files/Lx11.436_kb0.10_WLMC_Ts.out", "../data_files/Lx11.436_kb1.00_WLMC_Ts.out", "../data_files/Lx11.436_kb10.0_WLMC_Ts.out",
                     "../data_files/Lx13.000_kb0.10_WLMC_Ts.out", "../data_files/Lx13.000_kb1.00_WLMC_Ts.out", "../data_files/Lx13.000_kb10.0_WLMC_Ts.out",
                     "../data_files/Lx15.000_kb0.10_WLMC_Ts.out", "../data_files/Lx15.000_kb1.00_WLMC_Ts.out", "../data_files/Lx15.000_kb10.0_WLMC_Ts.out",
                     "../data_files/Lx11.200_kb1.00_WLMC_Ts.out", "../data_files/Lx11.800_kb1.00_WLMC_Ts.out", "../data_files/Lx12.500_kb1.00_WLMC_Ts.out", "../data_files/Lx13.500_kb1.00_WLMC_Ts.out",
                     "../data_files/Lx10.800_kb1.00_WLMC_Ts.out", "../data_files/Lx10.850_kb1.00_WLMC_Ts.out", "../data_files/Lx10.900_kb1.00_WLMC_Ts.out", "../data_files/Lx10.950_kb1.00_WLMC_Ts.out"
                    ])
Lx_      = [11, 11.436, 13, 15]
Lx_      = np.repeat(Lx_, 3)
Lx_      = np.append(Lx_, [11.2, 11.8, 12.5, 13.5, 10.8, 10.85, 10.9, 10.95])
phi_     = Nc*Nb*sigma**3/Lx_**3*np.pi/6
kb_      = [0.1, 1, 10]
kb_      = np.tile(kb_, 4)
kb_      = np.append(kb_, [1,1,1,1,1,1,1,1])

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

r_min = 0.0
r_max = 1.0
def return_dR_int(dist, T):
  return( 1 - np.exp(-WCA(dist)/T) )

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
reff2_kb0p10_scat = []
phi_mod2_kb0p10_scat = []
for phii, Ti in zip(phi_kb0p10_scat, T_kb0p10_scat):
  Ti *= 0.10
  reff = fsolve(return_reff_diff, 0.95, args=(Ti))[0]
  reff_kb0p10_scat.append(reff)
  phi_mod_kb0p10_scat.append(phii*reff**3)

  reff = quad(return_dR_int, r_min, r_max, args=(Ti))[0]
  reff2_kb0p10_scat.append(reff)
  phi_mod2_kb0p10_scat.append(phii*reff**3)

reff_kb0p10_NC_scat = []
phi_mod_kb0p10_NC_scat = []
reff2_kb0p10_NC_scat = []
phi_mod2_kb0p10_NC_scat = []
for phii, Ti in zip(phi_kb0p10_NC_scat, T_kb0p10_NC_scat):
  Ti *= 0.10
  reff = fsolve(return_reff_diff, 0.95, args=(Ti))[0]
  reff_kb0p10_NC_scat.append(reff)
  phi_mod_kb0p10_NC_scat.append(phii*reff**3)

  reff = quad(return_dR_int, r_min, r_max, args=(Ti))[0]
  reff2_kb0p10_NC_scat.append(reff)
  phi_mod2_kb0p10_NC_scat.append(phii*reff**3)

reff_kb1p00_scat = []
phi_mod_kb1p00_scat = []
reff2_kb1p00_scat = []
phi_mod2_kb1p00_scat = []
for phii, Ti in zip(phi_kb1p00_scat, T_kb1p00_scat):
  Ti *= 1.00
  reff = fsolve(return_reff_diff, 0.95, args=(Ti))[0]
  reff_kb1p00_scat.append(reff)
  phi_mod_kb1p00_scat.append(phii*reff**3)

  reff = quad(return_dR_int, r_min, r_max, args=(Ti))[0]
  reff2_kb1p00_scat.append(reff)
  phi_mod2_kb1p00_scat.append(phii*reff**3)

reff_kb1p00_NC_scat = []
phi_mod_kb1p00_NC_scat = []
reff2_kb1p00_NC_scat = []
phi_mod2_kb1p00_NC_scat = []
for phii, Ti in zip(phi_kb1p00_NC_scat, T_kb1p00_NC_scat):
  Ti *= 1.00
  reff = fsolve(return_reff_diff, 0.95, args=(Ti))[0]
  reff_kb1p00_NC_scat.append(reff)
  phi_mod_kb1p00_NC_scat.append(phii*reff**3)

  reff = quad(return_dR_int, r_min, r_max, args=(Ti))[0]
  reff2_kb1p00_NC_scat.append(reff)
  phi_mod2_kb1p00_NC_scat.append(phii*reff**3)

reff_kb10p0_scat = []
phi_mod_kb10p0_scat = []
reff2_kb10p0_scat = []
phi_mod2_kb10p0_scat = []
for phii, Ti in zip(phi_kb10p0_scat, T_kb10p0_scat):
  Ti *= 10.0
  reff = fsolve(return_reff_diff, 0.95, args=(Ti))[0]
  reff_kb10p0_scat.append(reff)
  phi_mod_kb10p0_scat.append(phii*reff**3)

  reff = quad(return_dR_int, r_min, r_max, args=(Ti))[0]
  reff2_kb10p0_scat.append(reff)
  phi_mod2_kb10p0_scat.append(phii*reff**3)

reff_kb10p0_NC_scat = []
phi_mod_kb10p0_NC_scat = []
reff2_kb10p0_NC_scat = []
phi_mod2_kb10p0_NC_scat = []
for phii, Ti in zip(phi_kb10p0_NC_scat, T_kb10p0_NC_scat):
  Ti *= 10.0
  reff = fsolve(return_reff_diff, 0.95, args=(Ti))[0]
  reff_kb10p0_NC_scat.append(reff)
  phi_mod_kb10p0_NC_scat.append(phii*reff**3)

  reff = quad(return_dR_int, r_min, r_max, args=(Ti))[0]
  reff2_kb10p0_NC_scat.append(reff)
  phi_mod2_kb10p0_NC_scat.append(phii*reff**3)

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

reff2_kb0p10_scat       = np.array(reff2_kb0p10_scat)
phi_mod2_kb0p10_scat    = np.array(phi_mod2_kb0p10_scat)
reff2_kb0p10_NC_scat    = np.array(reff2_kb0p10_NC_scat)
phi_mod2_kb0p10_NC_scat = np.array(phi_mod2_kb0p10_NC_scat)
reff2_kb1p00_scat       = np.array(reff2_kb1p00_scat)
phi_mod2_kb1p00_scat    = np.array(phi_mod2_kb1p00_scat)
reff2_kb1p00_NC_scat    = np.array(reff2_kb1p00_NC_scat)
phi_mod2_kb1p00_NC_scat = np.array(phi_mod2_kb1p00_NC_scat)
reff2_kb10p0_scat       = np.array(reff2_kb10p0_scat)
phi_mod2_kb10p0_scat    = np.array(phi_mod2_kb10p0_scat)
reff2_kb10p0_NC_scat    = np.array(reff2_kb10p0_NC_scat)
phi_mod2_kb10p0_NC_scat = np.array(phi_mod2_kb10p0_NC_scat)

# the hard harmflex system
Ts_files = "hard_harm_Ts.out"
do_HTH = 1

# get data
df = pd.read_csv(Ts_files, index_col=False, delimiter=' ')
df['Tr']         = df['Tm']/df['kb']
df['Tr2']        = df['Tm2']/df['kb']
df['phi']        = Nc*Nb*sigma**3/df['Lx']**3*np.pi/6
df_HTH           = df[df['dir'].str.contains("HTH_kb1.00")]
phi_HTH_scat     = df_HTH['phi'].to_numpy()
T_HTH_1_scat     = df_HTH['Tr'].to_numpy()
T_HTH_2_scat     = df_HTH['Tr2'].to_numpy()

phi_HTH_cryst    = 0.31
T_HTH_NC_scat    = T_HTH_2_scat
phi_HTH_NC_scat  = phi_HTH_scat
T_HTH_NC_scat[T_HTH_NC_scat < 0.0001] = 0.0001
T_HTH_NC_scatt   = T_HTH_2_scat[phi_HTH_scat > phi_HTH_cryst]
phi_HTH_NC_scatt = phi_HTH_scat[phi_HTH_scat > phi_HTH_cryst]
T_HTH_scat       = T_HTH_1_scat

# make figure and axis objects
fig, axs = plt.subplots(1, 3, figsize=(fig_width, fig_height), constrained_layout=test)

# plot points
if do_HTH:
  axs[0].scatter(T_HTH_scat    , phi_HTH_scat    , color='b', marker='+', zorder=2, alpha=0.2, label=r"$IN$ hard")
  axs[0].scatter(T_HTH_NC_scatt, phi_HTH_NC_scatt, color='b', marker='*', zorder=2, alpha=0.2, label=r"$NC$ hard")
  axs[1].scatter(T_HTH_scat    , phi_HTH_scat    , color='b', marker='+', zorder=2, alpha=0.2, label=r"$IN$ hard")
  axs[1].scatter(T_HTH_NC_scatt, phi_HTH_NC_scatt, color='b', marker='*', zorder=2, alpha=0.2, label=r"$NC$ hard")
  axs[2].scatter(T_HTH_scat    , phi_HTH_scat    , color='b', marker='+', zorder=2, alpha=0.2, label=r"$IN$ hard")
  axs[2].scatter(T_HTH_NC_scatt, phi_HTH_NC_scatt, color='b', marker='*', zorder=2, alpha=0.2, label=r"$NC$ hard")
if do_kb0p10:
  axs[0].scatter(T_kb0p10_scat   , phi_kb0p10_scat   , marker='+', zorder=2, alpha=1.0, c='r', label=r"$IN$ $k_{b}^{*}=0.1$")
  axs[0].scatter(T_kb0p10_NC_scat, phi_kb0p10_NC_scat, marker='*', zorder=2, alpha=1.0, s=60, edgecolors='r', facecolors='r', label=r"$NC$ $k_{b}^{*}=0.1$")
  axs[1].scatter(T_kb0p10_scat   , phi_mod_kb0p10_scat   , marker='+', zorder=2, alpha=1.0, c='r', label=r"$IN$ $k_{b}^{*}=0.1$")
  axs[1].scatter(T_kb0p10_NC_scat, phi_mod_kb0p10_NC_scat, marker='*', zorder=2, alpha=1.0, s=60, edgecolors='r', facecolors='r', label=r"$NC$ $k_{b}^{*}=0.1$")
  axs[2].scatter(T_kb0p10_scat   , phi_mod2_kb0p10_scat   , marker='+', zorder=2, alpha=1.0, c='r', label=r"$IN$ $k_{b}^{*}=0.1$")
  axs[2].scatter(T_kb0p10_NC_scat, phi_mod2_kb0p10_NC_scat, marker='*', zorder=2, alpha=1.0, s=60, edgecolors='r', facecolors='r', label=r"$NC$ $k_{b}^{*}=0.1$")
if do_kb1p00:
  axs[0].scatter(T_kb1p00_scat   , phi_kb1p00_scat   , marker='+', zorder=2, alpha=1.0, c='m', label=r"$IN$ $k_{b}^{*}=1$")
  axs[0].scatter(T_kb1p00_NC_scat, phi_kb1p00_NC_scat, marker='*', zorder=2, alpha=1.0, edgecolors='m', facecolors='m', label=r"$NC$ $k_{b}^{*}=1$")
  axs[1].scatter(T_kb1p00_scat   , phi_mod_kb1p00_scat   , marker='+', zorder=2, alpha=1.0, c='m', label=r"$IN$ $k_{b}^{*}=1$")
  axs[1].scatter(T_kb1p00_NC_scat, phi_mod_kb1p00_NC_scat, marker='*', zorder=2, alpha=1.0, edgecolors='m', facecolors='m', label=r"$NC$ $k_{b}^{*}=1$")
  axs[2].scatter(T_kb1p00_scat   , phi_mod2_kb1p00_scat   , marker='+', zorder=2, alpha=1.0, c='m', label=r"$IN$ $k_{b}^{*}=1$")
  axs[2].scatter(T_kb1p00_NC_scat, phi_mod2_kb1p00_NC_scat, marker='*', zorder=2, alpha=1.0, edgecolors='m', facecolors='m', label=r"$NC$ $k_{b}^{*}=1$")
if do_kb10p0:
  axs[0].scatter(T_kb10p0_scat   , phi_kb10p0_scat   , marker='+', zorder=2, alpha=1.0, c='c', label=r"$IN$ $k_{b}^{*}=10$")
  axs[0].scatter(T_kb10p0_NC_scat, phi_kb10p0_NC_scat, marker='*', zorder=2, alpha=1.0, s=35, edgecolors='c', facecolors='none', label=r"$NC$ $k_{b}^{*}=10$")
  axs[1].scatter(T_kb10p0_scat   , phi_mod_kb10p0_scat   , marker='+', zorder=2, alpha=1.0, c='c', label=r"$IN$ $k_{b}^{*}=10$")
  axs[1].scatter(T_kb10p0_NC_scat, phi_mod_kb10p0_NC_scat, marker='*', zorder=2, alpha=1.0, s=35, edgecolors='c', facecolors='none', label=r"$NC$ $k_{b}^{*}=10$")
  axs[2].scatter(T_kb10p0_scat   , phi_mod2_kb10p0_scat   , marker='+', zorder=2, alpha=1.0, c='c', label=r"$IN$ $k_{b}^{*}=10$")
  axs[2].scatter(T_kb10p0_NC_scat, phi_mod2_kb10p0_NC_scat, marker='*', zorder=2, alpha=1.0, s=35, edgecolors='c', facecolors='none', label=r"$NC$ $k_{b}^{*}=10$")

if fit:
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
  model_HTH_NC = np.poly1d(np.polyfit(phi_HTH_NC_scat, T_HTH_NC_scat, 4))
  phi_HTH_NC_quad = np.linspace(phi_min, phi_max, 1000)
  T_HTH_NC_quad = model_HTH_NC(phi_HTH_NC_quad)

  # choose fits for each
  phi_HTH_model    = phi_HTH_line
  T_HTH_model      = T_HTH_line
  phi_HTH_NC_model = phi_HTH_NC_quad
  T_HTH_NC_model   = T_HTH_NC_quad

  # zero out everything after negative
  last_neg_idx = np.amax(np.arange(len(T_HTH_NC_model))[T_HTH_NC_model < 0]+1)
  T_HTH_NC_model[:last_neg_idx] = 0

  # remove points where T_HTH_model is larger than T_HTH_NC_model
  keep_idx = T_HTH_NC_model < T_HTH_model
  T_HTH_model = T_HTH_model[keep_idx]
  phi_HTH_model = phi_HTH_model[keep_idx]

  # separate points after intersection
  T_HTH_NC_assum   = T_HTH_NC_model  [np.invert(keep_idx)]
  phi_HTH_NC_assum = phi_HTH_NC_model[np.invert(keep_idx)]
  T_HTH_NC_model   = T_HTH_NC_model  [keep_idx]
  phi_HTH_NC_model = phi_HTH_NC_model[keep_idx]

  # not sure what this does
  T_HTH_model[T_HTH_NC_model > T_HTH_model] = T_HTH_NC_model[T_HTH_NC_model > T_HTH_model]

  # remove all point less than or equal to 0
  keep_idx = T_HTH_NC_model > 0
  T_HTH_NC_model = T_HTH_NC_model[keep_idx]
  phi_HTH_NC_model = phi_HTH_NC_model[keep_idx]

  # no transitions below phi_HTH_cryst
  keep_idx = phi_HTH_NC_model > phi_HTH_cryst
  T_HTH_NC_model = T_HTH_NC_model[keep_idx]
  phi_HTH_NC_model = phi_HTH_NC_model[keep_idx]

  if do_HTH:
    axs[0].plot(T_HTH_model   , phi_HTH_model   , color='b', ls='--', dashes=(5, 3), zorder=1)#, label="IN")
    axs[0].plot(T_HTH_NC_model, phi_HTH_NC_model, color='b', ls='--', dashes=(5, 3), zorder=1)#, label="NC")
    axs[0].plot(T_HTH_NC_assum, phi_HTH_NC_assum, color='b', ls='--', dashes=(5, 3), zorder=1)#, label="NC")
    axs[1].plot(T_HTH_model   , phi_HTH_model   , color='b', ls='--', dashes=(5, 3), zorder=1)#, label="IN")
    axs[1].plot(T_HTH_NC_model, phi_HTH_NC_model, color='b', ls='--', dashes=(5, 3), zorder=1)#, label="NC")
    axs[1].plot(T_HTH_NC_assum, phi_HTH_NC_assum, color='b', ls='--', dashes=(5, 3), zorder=1)#, label="NC")
    axs[2].plot(T_HTH_model   , phi_HTH_model   , color='b', ls='--', dashes=(5, 3), zorder=1)#, label="IN")
    axs[2].plot(T_HTH_NC_model, phi_HTH_NC_model, color='b', ls='--', dashes=(5, 3), zorder=1)#, label="NC")
    axs[2].plot(T_HTH_NC_assum, phi_HTH_NC_assum, color='b', ls='--', dashes=(5, 3), zorder=1)#, label="NC")

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
  T_kb0p10_NC_quad[:idx_less_zero] = 0

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

  #T_kb0p10_NC_model[T_kb0p10_NC_model > T_kb0p10_model] = T_kb0p10_model[T_kb0p10_NC_model > T_kb0p10_model]
  #T_kb1p00_NC_model[T_kb1p00_NC_model > T_kb1p00_model] = T_kb1p00_model[T_kb1p00_NC_model > T_kb1p00_model]
  #T_kb10p0_NC_model[T_kb10p0_NC_model > T_kb10p0_model] = T_kb10p0_model[T_kb10p0_NC_model > T_kb10p0_model]
  T_kb0p10_model[T_kb0p10_NC_model > T_kb0p10_model] = T_kb0p10_NC_model[T_kb0p10_NC_model > T_kb0p10_model]
  T_kb1p00_model[T_kb1p00_NC_model > T_kb1p00_model] = T_kb1p00_NC_model[T_kb1p00_NC_model > T_kb1p00_model]
  T_kb10p0_model[T_kb10p0_NC_model > T_kb10p0_model] = T_kb10p0_NC_model[T_kb10p0_NC_model > T_kb10p0_model]

  phi_mod_kb0p10_model    = phi_mod_kb0p10_quad
  phi_mod_kb0p10_NC_model = phi_mod_kb0p10_NC_quad
  phi_mod_kb1p00_model    = phi_mod_kb1p00_quad
  phi_mod_kb1p00_NC_model = phi_mod_kb1p00_NC_quad
  phi_mod_kb10p0_model    = phi_mod_kb10p0_quad
  phi_mod_kb10p0_NC_model = phi_mod_kb10p0_NC_quad

  T_kb0p10_model[T_kb0p10_model<zeroT]       = zeroT
  T_kb0p10_NC_model[T_kb0p10_NC_model<zeroT] = zeroT
  T_kb1p00_model[T_kb1p00_model<zeroT]       = zeroT
  T_kb1p00_NC_model[T_kb1p00_NC_model<zeroT] = zeroT
  T_kb10p0_model[T_kb10p0_model<zeroT]       = zeroT
  T_kb10p0_NC_model[T_kb10p0_NC_model<zeroT] = zeroT

  keep_idx                = T_kb0p10_model < T_max
  T_kb0p10_model          = T_kb0p10_model[keep_idx]
  phi_mod_kb0p10_model    = phi_mod_kb0p10_model[keep_idx]
  keep_idx                = T_kb0p10_NC_model < T_max
  T_kb0p10_NC_model       = T_kb0p10_NC_model[keep_idx]
  phi_mod_kb0p10_NC_model = phi_mod_kb0p10_NC_model[keep_idx]
  keep_idx                = T_kb1p00_model < T_max
  T_kb1p00_model          = T_kb1p00_model[keep_idx]
  phi_mod_kb1p00_model    = phi_mod_kb1p00_model[keep_idx]
  keep_idx                = T_kb1p00_NC_model < T_max
  T_kb1p00_NC_model       = T_kb1p00_NC_model[keep_idx]
  phi_mod_kb1p00_NC_model = phi_mod_kb1p00_NC_model[keep_idx]
  keep_idx                = T_kb10p0_model < T_max
  T_kb10p0_model          = T_kb10p0_model[keep_idx]
  phi_mod_kb10p0_model    = phi_mod_kb10p0_model[keep_idx]
  keep_idx                = T_kb10p0_NC_model < T_max
  T_kb10p0_NC_model       = T_kb10p0_NC_model[keep_idx]
  phi_mod_kb10p0_NC_model = phi_mod_kb10p0_NC_model[keep_idx]

  do_kb0p10=False
  do_kb1p00=False
  do_kb10p0=False
  ax = axs[1]
  if do_kb0p10:
    ax.plot(T_kb0p10_model   , phi_mod_kb0p10_model   , color='r', zorder=1)#, label="IN")
    ax.plot(T_kb0p10_NC_model, phi_mod_kb0p10_NC_model, color='r', zorder=1)#, label="NC")
  if do_kb1p00:
    ax.plot(T_kb1p00_model   , phi_mod_kb1p00_model   , color='m', zorder=1)#, label="IN")
    ax.plot(T_kb1p00_NC_model, phi_mod_kb1p00_NC_model, color='m', zorder=1)#, label="NC")
  if do_kb10p0:
    ax.plot(T_kb10p0_model   , phi_mod_kb10p0_model   , color='c', zorder=1)#, label="IN")
    ax.plot(T_kb10p0_NC_model, phi_mod_kb10p0_NC_model, color='c', zorder=1)#, label="NC")

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
#  ax.scatter(T_kb0p10_NC_quad[idx_less_zero], phi_kb0p10_NC_quad[idx_less_zero], c='k')

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

  ax = axs[0]
  if do_kb0p10:
    ax.plot(T_kb0p10_model   , phi_kb0p10_model   , color='r', alpha=1, zorder=1)#, label="IN")
    ax.plot(T_kb0p10_NC_model, phi_kb0p10_NC_model, color='r', alpha=1, zorder=1)#, label="NC")
  if do_kb1p00:
    ax.plot(T_kb1p00_model   , phi_kb1p00_model   , color='m', alpha=1, zorder=1)#, label="IN")
    ax.plot(T_kb1p00_NC_model, phi_kb1p00_NC_model, color='m', alpha=1, zorder=1)#, label="NC")
  if do_kb10p0:
    ax.plot(T_kb10p0_model   , phi_kb10p0_model   , color='c', alpha=1, zorder=1)#, label="IN")
    ax.plot(T_kb10p0_NC_model, phi_kb10p0_NC_model, color='c', alpha=1, zorder=1)#, label="NC")

ax.set_xlabel(r"$T_{r}$", fontsize=10, labelpad=6)#, labelpad=0.3)
ax.set_ylabel(r"$\phi$", fontsize=10, labelpad=5.5)
ax.tick_params(axis='both', labelsize=8, pad=0)
ax.set_xlim(T_min-0.004, T_max)
ax.set_ylim(phi_min, phi_max)
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
ax.legend(handles=legend_elements, loc='lower right', ncol=1, columnspacing=1.0, fontsize=7.5, handletextpad=1, handlelength=0.5, borderpad=0.5)#, bbox_to_anchor=(1.02,-0.02))
ax.set_yticks([0.25, 0.3, 0.35, 0.4, 0.45, 0.5])
ax.set_yticklabels(["", "0.3", "", "0.4", "", "0.5"])
ax.set_xticks([0.0,0.1,0.2])

if shade:
  phi_HTH_NC_model = np.append(phi_HTH_NC_model, phi_HTH_NC_assum)
  T_HTH_NC_model = np.append(T_HTH_NC_model, T_HTH_NC_assum)
  phi_below=[]
  i = 0
  region_1 = np.linspace(T_min, T_max, 100)
  for i in range(len(region_1)):
    idx = (np.abs(T_HTH_NC_model-region_1[i])).argmin()
    if idx == len(phi_HTH_NC_model)-1:
      idx = (np.abs(T_HTH_model-region_1[i])).argmin()
      phi_below.append(phi_HTH_model[idx])
      continue
    phi_below.append(phi_HTH_NC_model[idx])
  ax.fill_between(region_1[:len(phi_below)], phi_below, phi_max, color=[shade_crystal], alpha=0.5)

  phi_below_2=[]
  phi_above_2=[]
  i = 0
  region_2 = np.linspace(T_min, T_max, 100)
  for i in range(len(region_2)):
    idx1 = (np.abs(T_HTH_model-region_2[i])).argmin()
    idx2 = (np.abs(T_HTH_NC_model-region_2[i])).argmin()
    if idx1 == len(phi_HTH_model)-1:
      continue
    if idx2 == len(phi_HTH_NC_model)-1:
      continue
    phi_below_2.append(phi_HTH_model[idx1])
    phi_above_2.append(phi_HTH_NC_model[idx2])
  ax.fill_between(region_2[:len(phi_below_2)], phi_below_2, phi_above_2, color=[shade_nematic], alpha=0.7)

  ax.fill_between(T_HTH_model                               , phi_min, phi_HTH_model                                   , linewidth=0.0, color=[shade_melt], alpha=0.7)
  ax.fill_between(np.append(T_HTH_model[-1], T_HTH_NC_assum), phi_min, np.append(phi_HTH_NC_assum[0], phi_HTH_NC_assum), linewidth=0.0, color=[shade_melt], alpha=0.7)

ax = axs[1]
ax.set_xlabel(r"$T_{r}$", fontsize=10, labelpad=6)#, labelpad=0.3)
ax.set_ylabel(r"$\phi_{\mathrm{eff}}$", fontsize=10, labelpad=5.5)
ax.tick_params(axis='both', labelsize=8, pad=0)
ax.set_xlim(T_min-0.004, T_max)
ax.set_ylim(phi_min, phi_max)
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
ax.legend(handles=legend_elements, loc='lower right', ncol=1, columnspacing=1.0, fontsize=7.5, handletextpad=1, handlelength=0.5, borderpad=0.5)#, bbox_to_anchor=(1.02,-0.02))
ax.set_yticks([0.25, 0.3, 0.35, 0.4, 0.45, 0.5])
ax.set_yticklabels(["", "0.3", "", "0.4", "", "0.5"])
ax.set_xticks([0.0,0.1,0.2])

axs[2].set_xlabel(r"$T_{r}$", fontsize=10, labelpad=6)#, labelpad=0.3)
axs[2].set_ylabel(r"$\phi_{\mathrm{eff}}^{\mathrm{new}}$", fontsize=10, labelpad=5.5)
axs[2].tick_params(axis='both', labelsize=8, pad=0)
axs[2].set_xlim(T_min-0.004, T_max)
axs[2].set_ylim(phi_min, phi_max)
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
axs[2].legend(handles=legend_elements, loc='lower right', ncol=1, columnspacing=1.0, fontsize=7.5, handletextpad=1, handlelength=0.5, borderpad=0.5)#, bbox_to_anchor=(1.02,-0.02))
axs[2].set_yticks([0.25, 0.3, 0.35, 0.4, 0.45, 0.5])
axs[2].set_yticklabels(["", "0.3", "", "0.4", "", "0.5"])
axs[2].set_xticks([0.0,0.1,0.2])

axs[0].text(-0.16, 0.95, r"a)", fontsize=12, transform=axs[0].transAxes)
axs[1].text(-0.16, 0.95, r"b)", fontsize=12, transform=axs[1].transAxes)
axs[2].text(-0.16, 0.95, r"c)", fontsize=12, transform=axs[2].transAxes)

#plt.subplots_adjust(left=0.071, top=0.999, bottom=0.118, right=0.999)
#plt.show()
#sys.exit()
plt.savefig("fig-phase_diag_phiHS.pdf")
plt.close()
