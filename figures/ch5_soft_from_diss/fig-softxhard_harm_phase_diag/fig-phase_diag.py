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

fit    = 1
crit   = 1

phi_min = 0.23
phi_max = 0.525
T_min = 0.0
T_max = 0.2

label_prefix = r'$\phi=$'

# the hard harmflex system
Ts_files = "hard_harm_Ts.out"

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

# The soft harm harm system
WL_Ts_files = np.array([
                     "soft_harm_harm_Lx11.000_kb0.10_Ts.out", "soft_harm_harm_Lx11.000_kb1.00_Ts.out", "soft_harm_harm_Lx11.000_kb10.0_Ts.out",
                     "soft_harm_harm_Lx11.436_kb0.10_Ts.out", "soft_harm_harm_Lx11.436_kb1.00_Ts.out", "soft_harm_harm_Lx11.436_kb10.0_Ts.out",
                     "soft_harm_harm_Lx13.000_kb0.10_Ts.out", "soft_harm_harm_Lx13.000_kb1.00_Ts.out", "soft_harm_harm_Lx13.000_kb10.0_Ts.out",
                     "soft_harm_harm_Lx15.000_kb0.10_Ts.out", "soft_harm_harm_Lx15.000_kb1.00_Ts.out", "soft_harm_harm_Lx15.000_kb10.0_Ts.out"
                 ,    "soft_harm_harm_Lx11.200_kb1.00_Ts.out", "soft_harm_harm_Lx11.800_kb1.00_Ts.out", "soft_harm_harm_Lx12.500_kb1.00_Ts.out", "soft_harm_harm_Lx13.500_kb1.00_Ts.out"
                 ,    "soft_harm_harm_Lx10.800_kb1.00_Ts.out", "soft_harm_harm_Lx10.850_kb1.00_Ts.out", "soft_harm_harm_Lx10.900_kb1.00_Ts.out", "soft_harm_harm_Lx10.950_kb1.00_Ts.out"
                    ])
Lx_      = [11, 11.436, 13, 15]
Lx_      = np.repeat(Lx_, 3)
Lx_      = np.append(Lx_, [11.2, 11.8, 12.5, 13.5, 10.8, 10.85, 10.9, 10.95])
phi_     = Nc*Nb*sigma**3/Lx_**3*np.pi/6
kb_      = [0.1, 1, 10]
kb_      = np.tile(kb_, 4)
kb_      = np.append(kb_, [1,1,1,1, 1,1,1,1])

input_df = pd.DataFrame({'Ts_files': WL_Ts_files, 'Lx': Lx_, 'phi': phi_, 'kb': kb_})
input_df = input_df.loc[input_df['kb'] == 1.0]

T_SHH_scat = []
T_SHH_NC_scat = []
phi_SHH_scat = []
phi_SHH_NC_scat = []
for i in range(len(input_df)):
  Ts_data_A = np.loadtxt(input_df['Ts_files'].iat[i], skiprows=1, ndmin=2)
  Ts_data_A[:,0] /= input_df['kb'].iat[i]
  print(input_df['Ts_files'].iat[i], Ts_data_A[:, 0], end=" ")
  if len(Ts_data_A) >= 2:
    T_SHH_scat.append(Ts_data_A[:,0][1])
    T_SHH_NC_scat.append(Ts_data_A[:,0][0])
    phi_SHH_scat.append(float(input_df['phi'].iat[i]))
    phi_SHH_NC_scat.append(float(input_df['phi'].iat[i]))
  elif len(Ts_data_A) == 1:
    T_SHH_scat.append(Ts_data_A[:,0][0])
    phi_SHH_scat.append(float(input_df['phi'].iat[i]))
    T_SHH_NC_scat.append(0)
    phi_SHH_NC_scat.append(float(input_df['phi'].iat[i]))
  print()
T_SHH_scat      = np.array(T_SHH_scat)
T_SHH_NC_scat   = np.array(T_SHH_NC_scat)
phi_SHH_scat    = np.array(phi_SHH_scat)
phi_SHH_NC_scat = np.array(phi_SHH_NC_scat)
print("Lx phi T_IN")
[ print(round((125*10*np.pi/6/phiphi)**(1/3),3), phiphi, TT) for phiphi, TT in zip(phi_SHH_scat, T_SHH_scat) ]
print("phi T_NC")
[ print(round((125*10*np.pi/6/phiphi)**(1/3),3), phiphi, TT) for phiphi, TT in zip(phi_SHH_NC_scat, T_SHH_NC_scat) ]

def WCA(r, eps=1.0, sig=2**(-1/6), rc=1.0):
  if r > rc:
    return(0)
  sigbyr6 = sig/r
  sigbyr6 = sigbyr6**6
  return(4*eps*(sigbyr6**2 - sigbyr6) + eps)

def return_reff_diff(reff, T, eps=1.0):
  target = 1.0*T
  return(WCA(reff) - target)

from scipy.optimize import fsolve

reff_SHH_scat = []
phi_mod_SHH_scat = []
for phii, Ti in zip(phi_SHH_scat, T_SHH_scat):
  reff = fsolve(return_reff_diff, 0.95, args=(Ti))[0]
  reff_SHH_scat.append(reff)
  phi_mod_SHH_scat.append(phii*reff**3)

reff_SHH_NC_scat = []
phi_mod_SHH_NC_scat = []
for phii, Ti in zip(phi_SHH_NC_scat, T_SHH_NC_scat):
  reff = fsolve(return_reff_diff, 0.95, args=(Ti))[0]
  reff_SHH_NC_scat.append(reff)
  phi_mod_SHH_NC_scat.append(phii*reff**3)

reff_SHH_scat       = np.array(reff_SHH_scat)
phi_mod_SHH_scat    = np.array(phi_mod_SHH_scat)
reff_SHH_NC_scat    = np.array(reff_SHH_NC_scat)
phi_mod_SHH_NC_scat = np.array(phi_mod_SHH_NC_scat)

[ print(p, pm, r) for p, pm, r in zip(phi_SHH_scat, phi_mod_SHH_scat, reff_SHH_scat) ]
print("dsf")
[ print(p, pm, r) for p, pm, r in zip(phi_SHH_NC_scat, phi_mod_SHH_NC_scat, reff_SHH_NC_scat) ]

fig, ax = plt.subplots(1, 2, figsize=(6.5,3.1))
# plot points
ax[1].scatter(T_HTH_scat   , phi_HTH_scat       , color='b', marker='+', zorder=2, label=r"IN hard rods")
ax[1].scatter(T_HTH_NC_scatt, phi_HTH_NC_scatt    , color='b', marker='*', zorder=2, label=r"NC hard rods")
ax[1].scatter(T_SHH_scat   , phi_mod_SHH_scat   , color='m', marker='+', zorder=2, label=r"IN soft springs")
ax[1].scatter(T_SHH_NC_scat[T_SHH_NC_scat != 0], phi_mod_SHH_NC_scat[T_SHH_NC_scat != 0], color='m', marker='*', zorder=2, label=r"NC soft springs")
ax[0].scatter(T_HTH_scat   , phi_HTH_scat       , color='b', marker='+', zorder=2, label=r"IN hard rods")
ax[0].scatter(T_HTH_NC_scatt, phi_HTH_NC_scatt    , color='b', marker='*', zorder=2, label=r"NC hard rods")
ax[0].scatter(T_SHH_scat   , phi_SHH_scat       , color='m', marker='+', zorder=2, label=r"IN soft springs")
ax[0].scatter(T_SHH_NC_scat[T_SHH_NC_scat != 0], phi_SHH_NC_scat[T_SHH_NC_scat != 0]    , color='m', marker='*', zorder=2, label=r"NC soft springs")

if fit:
  # HTH
  slope, intercept, r_value, p_value, std_err = stats.linregress(phi_HTH_scat, T_HTH_scat)
  phi_HTH_line = np.linspace(phi_min, phi_max, 1000)
  T_HTH_line   = phi_HTH_line*slope + intercept

  model = np.poly1d(np.polyfit(phi_HTH_scat, T_HTH_scat, 2))
  phi_HTH_quad = np.linspace(phi_min, phi_max, 1000)
  T_HTH_quad = model(phi_HTH_quad)
  
  #phi_HTH_NC_scat_stand = np.append(phi_HTH_NC_scat, [0.25, 0.297, 0.31] )
  #T_HTH_NC_scat_stand = np.append(T_HTH_NC_scat,     [0.,   0.,     0. ])
  slope, intercept, r_value, p_value, std_err = stats.linregress(phi_HTH_NC_scat, np.log(T_HTH_NC_scat))
  phi_HTH_NC_line = np.linspace(phi_min, phi_max, 1000)
  T_HTH_NC_line   = np.exp(phi_HTH_NC_line*slope + intercept)

  model_HTH_NC = np.poly1d(np.polyfit(phi_HTH_NC_scat, T_HTH_NC_scat, 3))
  phi_HTH_NC_quad = np.linspace(phi_min, phi_max, 1000)
  T_HTH_NC_quad = model_HTH_NC(phi_HTH_NC_quad)

  phi_HTH_model = phi_HTH_line
  T_HTH_model   = T_HTH_line
  phi_HTH_NC_model = phi_HTH_NC_line
  T_HTH_NC_model   = T_HTH_NC_line

#  del_idx = T_HTH_NC_model < T_HTH_model
#  phi_HTH_NC_model = phi_HTH_NC_model[del_idx]
#  T_HTH_NC_model = T_HTH_NC_model[del_idx]
  T_HTH_model[T_HTH_NC_model > T_HTH_model] = T_HTH_NC_model[T_HTH_NC_model > T_HTH_model]
  del_idx = T_HTH_NC_model > 0
  T_HTH_NC_model = T_HTH_NC_model[del_idx]
  phi_HTH_NC_model = phi_HTH_NC_model[del_idx]

  # no transitions below phi_cryst
  keep_idx = phi_HTH_NC_model > phi_cryst
  T_HTH_NC_model = T_HTH_NC_model[keep_idx]
  phi_HTH_NC_model = phi_HTH_NC_model[keep_idx]

  # SHH
  one = max(len(phi_mod_SHH_scat)-2, 1)
  model_SHH = np.poly1d(np.polyfit(phi_mod_SHH_scat, T_SHH_scat, 1))#one))
  phi_mod_SHH_model = np.linspace(phi_min, phi_max, 1000)
  T_SHH_model = model_SHH(phi_mod_SHH_model)
  del_idx = T_SHH_model>0
  T_SHH_model = T_SHH_model[del_idx]
  phi_mod_SHH_model = phi_mod_SHH_model[del_idx]
  
  one = max(len(phi_mod_SHH_NC_scat)-2, 1)
  model_SHH_NC = np.poly1d(np.polyfit(phi_mod_SHH_NC_scat, T_SHH_NC_scat, 5))#one))
  phi_mod_SHH_NC_model = np.linspace(phi_min, phi_max, 1000)
  T_SHH_NC_model = model_SHH_NC(phi_mod_SHH_NC_model)
  T_SHH_NC_model[T_SHH_NC_model < 0] = 0
  T_SHH_NC_model[:250] = 0
#  T_SHH_NC_model[T_SHH_NC_model > T_SHH_model] = T_SHH_model[T_SHH_NC_model > T_SHH_model]
  T_SHH_model[T_SHH_NC_model > T_SHH_model] = T_SHH_NC_model[T_SHH_NC_model > T_SHH_model]

  ax[1].plot(T_HTH_model   , phi_HTH_model   , color='b', zorder=1)#, label="IN")
  ax[1].plot(T_HTH_NC_model, phi_HTH_NC_model, color='b', zorder=1)#, label="IC")
  ax[1].plot(T_SHH_model   , phi_mod_SHH_model   , color='m', zorder=1)#, label="IN")
  ax[1].plot(T_SHH_NC_model, phi_mod_SHH_NC_model, color='m', zorder=1)#, label="IC")

  # SHH
  one = max(len(phi_SHH_scat)-2, 1)
  model_SHH = np.poly1d(np.polyfit(phi_SHH_scat, T_SHH_scat, 1))#one))
  phi_SHH_model = np.linspace(phi_min, phi_max, 1000)
  T_SHH_model = model_SHH(phi_SHH_model)
  del_idx = T_SHH_model>0
  T_SHH_model = T_SHH_model[del_idx]
  phi_SHH_model = phi_SHH_model[del_idx]
  
  one = max(len(phi_SHH_NC_scat)-2, 1)
  model_SHH_NC = np.poly1d(np.polyfit(phi_SHH_NC_scat, T_SHH_NC_scat, 5))#one))
  phi_SHH_NC_model = np.linspace(phi_min, phi_max, 1000)
  T_SHH_NC_model = model_SHH_NC(phi_SHH_NC_model)
  T_SHH_NC_model[T_SHH_NC_model < 0] = 0
  T_SHH_NC_model[:250] = 0
  T_SHH_NC_model[T_SHH_NC_model > T_SHH_model] = T_SHH_model[T_SHH_NC_model > T_SHH_model]
  T_SHH_model[T_SHH_NC_model > T_SHH_model] = T_SHH_NC_model[T_SHH_NC_model > T_SHH_model]

  T_SHH_NC_scat[T_SHH_NC_scat < 1e-4] = 0.0001
  slope, intercept, r_value, p_value, std_err = stats.linregress(phi_SHH_NC_scat, np.log(T_SHH_NC_scat))
  phi_SHH_NC_line = np.linspace(phi_min, phi_max, 1000)
  T_SHH_NC_line   = np.exp(phi_SHH_NC_line*slope + intercept)

  ax[0].plot(T_HTH_model   , phi_HTH_model       , color='b', zorder=1)#, label="IN")
  ax[0].plot(T_HTH_NC_model, phi_HTH_NC_model    , color='b', zorder=1)#, label="IC")
  ax[0].plot(T_SHH_model   , phi_SHH_model   , color='m', alpha=1, zorder=1)#, label="IN")
  ax[0].plot(T_SHH_NC_model, phi_SHH_NC_model, color='m', alpha=1, zorder=1)#, label="IC")
#  ax[0].plot(T_SHH_NC_line, phi_SHH_NC_line, color='m', alpha=1, zorder=1)#, label="IC")

ax[1].set_xlabel(r"$T_{r}$", fontsize=10, labelpad=6)#, labelpad=0.3)
ax[1].set_ylabel(r"$\phi_{\mathrm{eff}}$", fontsize=10, labelpad=5.5)
ax[1].tick_params(axis='both', labelsize=8, pad=0)
ax[1].set_xlim(T_min-0.004, T_max)
ax[1].set_ylim(phi_min, phi_max)
ax[1].legend(loc='lower right', fontsize=8, handletextpad=0.01)
ax[1].set_yticks([0.25, 0.3, 0.35, 0.4, 0.45, 0.5])
ax[1].set_yticklabels(["", "0.3", "", "0.4", "", 0.5])
ax[1].set_xticks([0.0,0.05, 0.1, 0.15])

ax[0].set_xlabel(r"$T_{r}$", fontsize=10, labelpad=6)#, labelpad=0.3)
ax[0].set_ylabel(r"$\phi$", fontsize=10, labelpad=5.5)
ax[0].tick_params(axis='both', labelsize=8, pad=0)
ax[0].set_xlim(T_min-0.004, T_max)
ax[0].set_ylim(phi_min, phi_max)
ax[0].legend(loc='lower right', fontsize=8, handletextpad=0.01)
ax[0].set_yticks([0.25, 0.3, 0.35, 0.4, 0.45, 0.5])
ax[0].set_yticklabels(["", "0.3", "", "0.4", "", 0.5])
ax[0].set_xticks([0.0,0.05, 0.1, 0.15])

ax[0].text(-0.16, 0.95, r"a)", fontsize=12, transform=ax[0].transAxes)
ax[1].text(-0.16, 0.95, r"b)", fontsize=12, transform=ax[1].transAxes)

#plt.subplots_adjust(left=0.156, top=0.98, bottom=0.135, right=0.974)
plt.subplots_adjust(left=0.071, top=0.999, bottom=0.118, right=0.999)

#plt.show()
#sys.exit()
plt.savefig("fig-phase_diag.pdf")
plt.close()
