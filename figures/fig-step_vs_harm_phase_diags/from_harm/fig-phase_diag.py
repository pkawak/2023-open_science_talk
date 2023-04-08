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

Nc    = 125
Nb    = 10
sigma = 1
Ts_files = "Ts.out"

labels = 1
shade  = 1
fit    = 1
crit   = 0
scatter= 0

shade_crystal  = "#185ADB"
shade_nematic  = "#FFC947"
shade_melt     = "#FFFFFF"

marker_IN       = "o"
marker_IN_size  = 5
marker_IN_size2 = 10
marker_NC       = "^"
marker_NC_size  = 5
marker_NC_size2 = 20
marker_IC       = "s"
marker_IC_size  = 5
marker_IC_size2 = 15

fontsize  = 10
labelsize = 8 # sets ticklabel sizes

phi_min = 0.3
phi_max = 0.5
T_min = 0.00
T_max = 0.30
phi_HTH_cryst = 0.31

# figure settings
test       = 0    # set equal to 1 for constrained_layout
fig_width  = 3.25 # inches
fig_height = 3.10 # inches

# get data
df_HTH         = pd.read_csv(Ts_files, index_col=False, delimiter=" ")
df_HTH         = df_HTH[df_HTH["dir"].str.contains("HTH_kb1.00")]
df_HTH["Tr"]   = df_HTH["Tm"]/df_HTH["kb"]
df_HTH["Tr2"]  = df_HTH["Tm2"]/df_HTH["kb"]
df_HTH["phi"]  = Nc*Nb*sigma**3/df_HTH["Lx"]**3*np.pi/6

phi_HTH_scat   = df_HTH["phi"].to_numpy()
T_HTH_1_scat   = df_HTH["Tr"].to_numpy()
T_HTH_2_scat   = df_HTH["Tr2"].to_numpy()

T_HTH_NC_scat    = T_HTH_2_scat
phi_HTH_NC_scat  = phi_HTH_scat
T_HTH_NC_scat[T_HTH_NC_scat < 0.0001] = 0.0001
T_HTH_NC_scatt   = T_HTH_2_scat[phi_HTH_scat > phi_HTH_cryst]
phi_HTH_NC_scatt = phi_HTH_scat[phi_HTH_scat > phi_HTH_cryst]
T_HTH_scat       = T_HTH_1_scat

#%%%%%
T_HTH_NC_scat = T_HTH_NC_scatt
phi_HTH_NC_scat = phi_HTH_NC_scatt
#%%%%%

# make figure and axis objects
fig, ax = plt.subplots(1, figsize=(fig_width, fig_height), constrained_layout=test)

# plot points
if scatter:
  ax.scatter(T_HTH_scat    , phi_HTH_scat    , color="g", marker="+", zorder=3, label="IN")
  ax.scatter(T_HTH_NC_scatt, phi_HTH_NC_scatt, color="r", marker="*", zorder=3, label="IC")

ax.set_xlim(T_min, T_max)
ax.set_xlabel(r"$T_{r}$", fontsize=12, labelpad=6)#, labelpad=0.3)
ax.set_ylabel(r"$\phi$" , fontsize=12, labelpad=5.5)
ax.tick_params(axis='both', labelsize=10, pad=0)
ax.set_xticks([0,0.1,0.2, 0.3])
ax.set_ylim(0.30, 0.50)
ax.set_yticks([0.3, 0.4, 0.5])

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
  model_HTH_NC = np.poly1d(np.polyfit(phi_HTH_NC_scat, T_HTH_NC_scat, 5))
  phi_HTH_NC_quad = np.linspace(phi_min, phi_max, 1000)
  T_HTH_NC_quad = model_HTH_NC(phi_HTH_NC_quad)

  # choose fits for each
  phi_HTH_model    = phi_HTH_line
  T_HTH_model      = T_HTH_line
  phi_HTH_NC_model = phi_HTH_NC_quad
  T_HTH_NC_model   = T_HTH_NC_quad

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

  ax.plot(T_HTH_model   , phi_HTH_model   , color="g", ls="-", zorder=2)
  ax.plot(T_HTH_NC_model, phi_HTH_NC_model, color="r", ls="-", zorder=2)
  ax.plot(T_HTH_NC_assum, phi_HTH_NC_assum, color="r", ls="-", zorder=2)
#  idx = (np.abs(phi_HTH_model-phi_HTH_cryst)).argmin()
#  T_max_ = T_HTH_model[idx]
#  ax.plot([T_min, max(T_HTH_NC_model)], [max(phi_HTH_NC_model), max(phi_HTH_NC_model)], ls="--", color="#00008b", zorder=2, label=r"$\phi_{\mathrm{IN}}^{*}$")

if crit:
  ax.plot([T_min, model(phi_HTH_cryst)], [phi_HTH_cryst, phi_HTH_cryst], ls='--', color='#00008b', zorder=1)

if labels:
  ax.text(0.63, 0.13, "Isotropic (I)", weight="bold", color="k", fontsize=10, fontname="dejavusans", transform = ax.transAxes)
  ax.text(0.18, 0.9, "Crystal (C)"  , weight="bold", color="k", fontsize=10, fontname="dejavusans", transform = ax.transAxes)
  ax.text(0.09, 0.45, "Nematic"      , weight="bold", color="k", fontsize=10, fontname="dejavusans", transform = ax.transAxes)
  ax.text(0.15, 0.39, "(N)"          , weight="bold", color="k", fontsize=10, fontname="dejavusans", transform = ax.transAxes)

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

if test == 0:
  plt.subplots_adjust(left=0.163, top=0.983, bottom=0.135, right=0.969)
plt.savefig("fig-phase_diag.pdf")
plt.close()
