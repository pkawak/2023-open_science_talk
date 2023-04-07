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

fit      = 1
crit     = 1

phi_min = 0.29
phi_max = 0.50
T_min = 0.0
T_max = 0.363

label_prefix = r'$\phi=$'

# the hard stepflex system
Ts_files = "hard_step_Ts.out"

# get data
df = pd.read_csv(Ts_files, index_col=False, delimiter=' ')
df['Tr']  = df['Tm']/df['kb']
df['phi'] = Nc*Nb*sigma**3/df['Lx']**3*np.pi/6
df_SandP  = df[df['dir'].str.contains("SandP_kb1.00")]
phi_HTS_scat  = df_SandP['phi'].to_numpy()
T_HTS_scat    = df_SandP['Tr'].to_numpy()
keep_idx = T_HTS_scat > 0.01
phi_HTS_scat = phi_HTS_scat[keep_idx]
T_HTS_scat = T_HTS_scat[keep_idx]

phi_HTS_cryst = 0.441
T_HTS_NC_scat   = T_HTS_scat[phi_HTS_scat > phi_HTS_cryst]
phi_HTS_NC_scat = phi_HTS_scat[phi_HTS_scat > phi_HTS_cryst]
T_HTS_scat   = T_HTS_scat[phi_HTS_scat < phi_HTS_cryst]
phi_HTS_scat = phi_HTS_scat[phi_HTS_scat < phi_HTS_cryst]

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

phi_HTH_cryst = 0.31
T_HTH_NC_scat = T_2_scat
phi_HTH_NC_scat = phi_HTH_scat
T_HTH_NC_scat[T_HTH_NC_scat < 0.0001] = 0.0001
T_HTH_NC_scatt   = T_2_scat[phi_HTH_scat > phi_HTH_cryst]
phi_HTH_NC_scatt = phi_HTH_scat[phi_HTH_scat > phi_HTH_cryst]
T_HTH_scat      = T_1_scat

print("HTS")
print(T_HTS_NC_scat, T_HTS_scat)
print(phi_HTS_NC_scat, phi_HTS_scat)
print((Nc*Nb*sigma**3/phi_HTS_NC_scat*np.pi/6)**(1/3), (Nc*Nb*sigma**3/phi_HTS_scat*np.pi/6)**(1/3))
idx_HTS_thr = np.round(((Nc*Nb*sigma**3/phi_HTS_NC_scat*np.pi/6)**(1/3)),3)==11.157
idx_HTS_one = np.round(((Nc*Nb*sigma**3/phi_HTS_scat*np.pi/6)**(1/3)),3)==11.436
idx_HTS_two = np.round(((Nc*Nb*sigma**3/phi_HTS_scat*np.pi/6)**(1/3)),3)==11.715
print("HTH")
print(T_HTH_scat)
print(phi_HTH_scat)
print((Nc*Nb*sigma**3/phi_HTH_scat*np.pi/6)**(1/3))

idx_HTH_thr = np.round(((Nc*Nb*sigma**3/phi_HTH_scat*np.pi/6)**(1/3)),3)==11.157
idx_HTH_one = np.round(((Nc*Nb*sigma**3/phi_HTH_scat*np.pi/6)**(1/3)),3)==11.436
idx_HTH_two = np.round(((Nc*Nb*sigma**3/phi_HTH_scat*np.pi/6)**(1/3)),3)==11.715
phi_one = phi_HTS_scat[idx_HTS_one][0]
phi_two = phi_HTS_scat[idx_HTS_two][0]
phi_thr = phi_HTS_NC_scat[idx_HTS_thr][0]
T_HTS_one = T_HTS_scat[idx_HTS_one][0]
T_HTS_two = T_HTS_scat[idx_HTS_two][0]
T_HTS_thr = T_HTS_NC_scat[idx_HTS_thr][0]
T_HTH_one = T_HTH_scat[idx_HTH_one][0]
T_HTH_two = T_HTH_scat[idx_HTH_two][0]
T_HTH_thr = T_HTH_scat[idx_HTH_thr][0]

idx_HTH_NC_one = np.round(((Nc*Nb*sigma**3/phi_HTH_NC_scat*np.pi/6)**(1/3)),3)==11.436
idx_HTH_NC_two = np.round(((Nc*Nb*sigma**3/phi_HTH_NC_scat*np.pi/6)**(1/3)),3)==11.715
idx_HTH_NC_thr = np.round(((Nc*Nb*sigma**3/phi_HTH_NC_scat*np.pi/6)**(1/3)),3)==11.157
T_HTH_NC_one = T_HTH_NC_scat[idx_HTH_NC_one][0]
T_HTH_NC_two = T_HTH_NC_scat[idx_HTH_NC_two][0]
T_HTH_NC_thr = T_HTH_NC_scat[idx_HTH_NC_thr][0]

print("phi", "T_m^HTS", "T_IN^HTH", "T_NC^HTH", "T_m/T_IN", "T_m/T_NC")
print(phi_thr, T_HTS_thr, T_HTH_thr, T_HTH_NC_thr, T_HTS_thr/T_HTH_thr, T_HTS_thr/T_HTH_NC_thr)
print(phi_one, T_HTS_one, T_HTH_one, T_HTH_NC_one, T_HTS_one/T_HTH_one, T_HTS_one/T_HTH_NC_one)
print(phi_two, T_HTS_two, T_HTH_two, T_HTH_NC_two, T_HTS_two/T_HTH_two, T_HTS_two/T_HTH_NC_two)

fig, ax = plt.subplots(1, figsize=(3.00,2.90))
# plot points
ax.scatter(T_HTS_scat    , phi_HTS_scat    , color='r', marker='o', zorder=2, label=r"IN Discrete")#$T^{\mathrm{HTS}}_{\mathrm{IN}}$")
ax.scatter(T_HTS_NC_scat , phi_HTS_NC_scat , color='r', marker='*', s=70, zorder=2, label=r"IC Discrete")#$T^{\mathrm{HTS}}_{\mathrm{IC}}$")
ax.scatter(T_HTH_scat    , phi_HTH_scat    , color='b', marker='o', zorder=2, label=r"IN Continuous")#$T^{\mathrm{HTH}}_{\mathrm{IN}}$")
ax.scatter(T_HTH_NC_scatt, phi_HTH_NC_scatt, color='b', marker='*', s=70, zorder=2, label=r"NC Continuous")#$T^{\mathrm{HTH}}_{\mathrm{IC}}$")

if fit:
  # HTS
  slope_HTS_IC, intercept_HTS_IC, r_value_HTS_IC, p_value_HTS_IC, std_err_HTS_IC = stats.linregress(phi_HTS_NC_scat, T_HTS_NC_scat)
  phi_HTS_NC_line = np.linspace(phi_HTS_cryst, phi_max, 1000)
  T_HTS_NC_line   = phi_HTS_NC_line*slope_HTS_IC + intercept_HTS_IC

  phi_HTS_NC_model = phi_HTS_NC_line
  T_HTS_NC_model = T_HTS_NC_line

  slope_HTS, intercept_HTS, r_value_HTS, p_value_HTS, std_err_HTS = stats.linregress(phi_HTS_scat, T_HTS_scat)
  phi_HTS_line = np.linspace(phi_min, phi_HTS_cryst, 1000)
  T_HTS_line   = phi_HTS_line*slope_HTS + intercept_HTS

  phi_HTS_model = phi_HTS_line
  T_HTS_model = T_HTS_line

  # HTH
  slope_HTH, intercept_HTH, r_value_HTH, p_value_HTH, std_err_HTH = stats.linregress(phi_HTH_scat, T_HTH_scat)
  phi_HTH_line = np.linspace(phi_min, phi_max, 1000)
  T_HTH_line   = phi_HTH_line*slope_HTH + intercept_HTH

  model = np.poly1d(np.polyfit(phi_HTH_scat, T_HTH_scat, 3))
  phi_HTH_quad = np.linspace(phi_min, phi_max, 1000)
  T_HTH_quad = model(phi_HTH_quad)
  
  slope, intercept, r_value, p_value, std_err = stats.linregress(phi_HTH_NC_scat, np.log(T_HTH_NC_scat))
  phi_HTH_NC_line = np.linspace(phi_min, phi_max, 1000)
  T_HTH_NC_line   = np.exp(phi_HTH_NC_line*slope + intercept)

  model_HTH_IC = np.poly1d(np.polyfit(phi_HTH_NC_scat, T_HTH_NC_scat, 3))
  phi_HTH_NC_quad = np.linspace(phi_min, phi_max, 1000)
  T_HTH_NC_quad = model_HTH_IC(phi_HTH_NC_quad)

  phi_HTH_model = phi_HTH_line
  T_HTH_model   = T_HTH_line
  phi_HTH_NC_model = phi_HTH_NC_line
  T_HTH_NC_model   = T_HTH_NC_line

  del_idx = T_HTH_NC_model < T_HTH_model
  phi_HTH_NC_model = phi_HTH_NC_model[del_idx]
  T_HTH_NC_model = T_HTH_NC_model[del_idx]

  keep_idx = phi_HTH_NC_model > phi_HTH_cryst
  T_HTH_NC_model = T_HTH_NC_model[keep_idx]
  phi_HTH_NC_model = phi_HTH_NC_model[keep_idx]

  print(r"HTS: Tr=", str(slope_HTS), r"phi", str(intercept_HTS))
  print(r"HTH: Tr=", str(slope_HTH), r"phi", str(intercept_HTH))
  print("slope_HTS/slope_HTH", slope_HTS/slope_HTH)
  print("intercept_HTS/intercept_HTH", intercept_HTS/intercept_HTH)
  print("slope_HTH/slope_HTS", slope_HTH/slope_HTS)
  print("intercept_HTH/intercept_HTS", intercept_HTH/intercept_HTS)
  print(r"HTS: Tr(0.35)=", str(slope_HTS*0.35+intercept_HTS))
  print(r"HTH: Tr(0.35)=", str(slope_HTH*0.35+intercept_HTH))
  print(r"HTSTr(0.35)/HTHTr(0.35)", str((slope_HTS*0.35+intercept_HTS)/(slope_HTH*0.35+intercept_HTH)))
  print(r"HTSTr(0.3)/HTHTr(0.3)", str((slope_HTS*0.3+intercept_HTS)/(slope_HTH*0.3+intercept_HTH)))
  print(r"HTSTr(0.4)/HTHTr(0.4)", str((slope_HTS*0.4+intercept_HTS)/(slope_HTH*0.4+intercept_HTH)))

  ax.plot(T_HTS_model   , phi_HTS_model   , color='r', zorder=1)#)
  ax.plot(T_HTS_NC_model   , phi_HTS_NC_model   , color='r', zorder=1)#)

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

  # no transitions below phi_HTH_cryst
  keep_idx = phi_HTH_NC_model > phi_HTH_cryst
  T_HTH_NC_model = T_HTH_NC_model[keep_idx]
  phi_HTH_NC_model = phi_HTH_NC_model[keep_idx]
  ax.plot(T_HTH_model   , phi_HTH_model   , color='b', zorder=1)#, label="IN")
  ax.plot(T_HTH_NC_model, phi_HTH_NC_model, color='b', zorder=1)#, label="IC")

ax.set_xlabel(r"$T_{r}$", fontsize=12, labelpad=5.0)
ax.set_ylabel(r"$\phi$", fontsize=12, labelpad=5.5)
ax.tick_params(axis='both', labelsize=10, pad=0)
ax.set_xlim(T_min, T_max)
ax.set_ylim(phi_min, phi_max)
ax.legend(loc='lower right', fontsize=10, handletextpad=0.01)
ax.set_yticks([0.3,0.4,0.5])
ax.set_xticks([0.0,0.1,0.2,0.3])

#plt.subplots_adjust(left=0.096, top=0.98, bottom=0.142, right=0.998)
plt.subplots_adjust(left=0.177, top=0.98, bottom=0.14, right=0.997)
#plt.show()
#sys.exit()
plt.savefig("fig-phase_diag.pdf")
plt.close()
