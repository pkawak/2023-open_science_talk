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

fit   = 1
crit  = 1

phi_min = 0.23
phi_max = 0.525
T_min = 0.0
T_max = 0.2

phi_HTH_cryst   = 0.31

# the hard harmflex system
Ts_files = "hard_harm_Ts.out"

# get data
df = pd.read_csv(Ts_files, index_col=False, delimiter=" ")
df["Tr"]  = df["Tm"]/df["kb"]
df["Tr2"]  = df["Tm2"]/df["kb"]
df["phi"] = Nc*Nb*sigma**3/df["Lx"]**3*np.pi/6
df_HTH  = df[df["dir"].str.contains("HTH_kb1.00")]
phi_HTH_scat  = df_HTH["phi"].to_numpy()
T_1_scat  = df_HTH["Tr"].to_numpy()
T_2_scat  = df_HTH["Tr2"].to_numpy()

T_HTH_NC_scat = T_2_scat
phi_HTH_NC_scat = phi_HTH_scat
T_HTH_NC_scat[T_HTH_NC_scat < 0.0001] = 0.0001
T_HTH_NC_scatt   = T_2_scat[phi_HTH_scat > phi_HTH_cryst]
phi_HTH_NC_scatt = phi_HTH_scat[phi_HTH_scat > phi_HTH_cryst]
T_HTH_scat      = T_1_scat

# The soft harm harm system
WL_Ts_files = np.array([
                     "soft_harm_harm_Lx11.000_kb0.10_Ts.out", "soft_harm_harm_Lx11.000_kb1.00_Ts.out", "soft_harm_harm_Lx11.000_kb10.0_Ts.out",
                     "soft_harm_harm_Lx11.436_kb0.10_Ts.out", "soft_harm_harm_Lx11.436_kb1.00_Ts.out", "soft_harm_harm_Lx11.436_kb10.0_Ts.out",
                     "soft_harm_harm_Lx13.000_kb0.10_Ts.out", "soft_harm_harm_Lx13.000_kb1.00_Ts.out", "soft_harm_harm_Lx13.000_kb10.0_Ts.out",
                     "soft_harm_harm_Lx15.000_kb0.10_Ts.out", "soft_harm_harm_Lx15.000_kb1.00_Ts.out", "soft_harm_harm_Lx15.000_kb10.0_Ts.out",
                     "soft_harm_harm_Lx11.200_kb1.00_Ts.out", "soft_harm_harm_Lx11.800_kb1.00_Ts.out", "soft_harm_harm_Lx12.500_kb1.00_Ts.out", "soft_harm_harm_Lx13.500_kb1.00_Ts.out",
                     "soft_harm_harm_Lx10.800_kb1.00_Ts.out", "soft_harm_harm_Lx10.850_kb1.00_Ts.out", "soft_harm_harm_Lx10.900_kb1.00_Ts.out", "soft_harm_harm_Lx10.950_kb1.00_Ts.out"
                    ])
Lx_  = np.array([ float(name.split('x')[1].split('_')[0]) for name in WL_Ts_files ])
phi_     = Nc*Nb*sigma**3/Lx_**3*np.pi/6
kb_  = np.array([ float(name.split('b')[1].split('_')[0]) for name in WL_Ts_files ])

input_df = pd.DataFrame({"Ts_files": WL_Ts_files, "Lx": Lx_, "phi": phi_, "kb": kb_})
input_df = input_df.loc[input_df["kb"] == 1.0]

T_SHH_scat = []
T_SHH_NC_scat = []
phi_SHH_scat = []
phi_SHH_NC_scat = []
for i in range(len(input_df)):
  Ts_data_A = np.loadtxt(input_df["Ts_files"].iat[i], skiprows=1, ndmin=2)
  Ts_data_A[:,0] /= input_df["kb"].iat[i]
#  print(input_df["Ts_files"].iat[i], Ts_data_A[:, 0], end=" ")
  if len(Ts_data_A) >= 2:
    T_SHH_scat.append(Ts_data_A[:,0][1])
    T_SHH_NC_scat.append(Ts_data_A[:,0][0])
    phi_SHH_scat.append(float(input_df["phi"].iat[i]))
    phi_SHH_NC_scat.append(float(input_df["phi"].iat[i]))
  elif len(Ts_data_A) == 1:
    T_SHH_scat.append(Ts_data_A[:,0][0])
    phi_SHH_scat.append(float(input_df["phi"].iat[i]))
    T_SHH_NC_scat.append(0)
    phi_SHH_NC_scat.append(float(input_df["phi"].iat[i]))
#  print()
T_SHH_scat      = np.array(T_SHH_scat)
T_SHH_NC_scat   = np.array(T_SHH_NC_scat)
phi_SHH_scat    = np.array(phi_SHH_scat)
phi_SHH_NC_scat = np.array(phi_SHH_NC_scat)
#print("Lx phi T_IN")
#[ print(round((125*10*np.pi/6/phiphi)**(1/3),3), phiphi, TT) for phiphi, TT in zip(phi_SHH_scat, T_SHH_scat) ]
#print("phi T_NC")
#[ print(round((125*10*np.pi/6/phiphi)**(1/3),3), phiphi, TT) for phiphi, TT in zip(phi_SHH_NC_scat, T_SHH_NC_scat) ]

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

reff_SHH_scat = []
phi_mod_SHH_scat = []
for phii, Ti in zip(phi_SHH_scat, T_SHH_scat):
  reff = quad(return_dR_int, r_min, r_max, args=(Ti))[0]
  reff_SHH_scat.append(reff)
  phi_mod_SHH_scat.append(phii*reff**3)

reff_SHH_NC_scat = []
phi_mod_SHH_NC_scat = []
for phii, Ti in zip(phi_SHH_NC_scat, T_SHH_NC_scat):
  reff = quad(return_dR_int, r_min, r_max, args=(Ti))[0]
  reff_SHH_NC_scat.append(reff)
  phi_mod_SHH_NC_scat.append(phii*reff**3)

reff_SHH_scat       = np.array(reff_SHH_scat)
phi_mod_SHH_scat    = np.array(phi_mod_SHH_scat)
reff_SHH_NC_scat    = np.array(reff_SHH_NC_scat)
phi_mod_SHH_NC_scat = np.array(phi_mod_SHH_NC_scat)

#[ print(p, pm, r) for p, pm, r in zip(phi_SHH_scat, phi_mod_SHH_scat, reff_SHH_scat) ]
#print("dsf")
#[ print(p, pm, r) for p, pm, r in zip(phi_SHH_NC_scat, phi_mod_SHH_NC_scat, reff_SHH_NC_scat) ]

test = 0
# make figure and axis objects
fig0, ax0 = plt.subplots(1, 1, figsize=(3.00, 2.90), constrained_layout=test)
fig1, ax1 = plt.subplots(1, 1, figsize=(3.00, 2.90), constrained_layout=test)
# plot points
ax1.scatter(T_HTH_scat                       , phi_HTH_scat                           , color="b", marker="o", zorder=2, label=r"IN hard rods")
ax1.scatter(T_HTH_NC_scatt                   , phi_HTH_NC_scatt                       , color="b", marker="*", s=70, zorder=2, label=r"NC hard rods")
ax1.scatter(T_SHH_scat                       , phi_mod_SHH_scat                       , color="m", marker="o", zorder=2, label=r"IN soft springs")
ax1.scatter(T_SHH_NC_scat[T_SHH_NC_scat != 0], phi_mod_SHH_NC_scat[T_SHH_NC_scat != 0], color="m", marker="*", s=70, zorder=2, label=r"NC soft springs")
ax0.scatter(T_HTH_scat                       , phi_HTH_scat                           , color="b", marker="o", zorder=2, label=r"IN hard rods")
ax0.scatter(T_HTH_NC_scatt                   , phi_HTH_NC_scatt                       , color="b", marker="*", s=70, zorder=2, label=r"NC hard rods")
ax0.scatter(T_SHH_scat                       , phi_SHH_scat                           , color="m", marker="o", zorder=2, label=r"IN soft springs")
ax0.scatter(T_SHH_NC_scat[T_SHH_NC_scat != 0], phi_SHH_NC_scat[T_SHH_NC_scat != 0]    , color="m", marker="*", s=70, zorder=2, label=r"NC soft springs")

if fit:
  # HTH IN linear fit
  slope, intercept, r_value, p_value, std_err = stats.linregress(phi_HTH_scat, T_HTH_scat)
  phi_HTH_line = np.linspace(phi_min, phi_max, 1000)
  T_HTH_line   = phi_HTH_line*slope + intercept

  # HTH IN quad fit
  model = np.poly1d(np.polyfit(phi_HTH_scat, T_HTH_scat, 2))
  phi_HTH_quad = np.linspace(phi_min, phi_max, 1000)
  T_HTH_quad = model(phi_HTH_quad)

  # HTH NC log(T) fit
  slope, intercept, r_value, p_value, std_err = stats.linregress(phi_HTH_NC_scat, np.log(T_HTH_NC_scat))
  phi_HTH_NC_line = np.linspace(phi_min, phi_max, 1000)
  T_HTH_NC_line   = np.exp(phi_HTH_NC_line*slope + intercept)

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

  ax1.plot(T_HTH_model   , phi_HTH_model   , color="b", zorder=1)#, label="IN")
  ax1.plot(T_HTH_NC_model, phi_HTH_NC_model, color="b", zorder=1)#, label="IC")
  ax1.plot(T_HTH_NC_assum, phi_HTH_NC_assum, color="b", zorder=1)#, label="IC")
  ax1.plot(T_SHH_model   , phi_mod_SHH_model   , color="m", zorder=1)#, label="IN")
  ax1.plot(T_SHH_NC_model, phi_mod_SHH_NC_model, color="m", zorder=1)#, label="IC")

  # SHH
  one = max(len(phi_SHH_scat)-2, 1)
  model_SHH = np.poly1d(np.polyfit(phi_SHH_scat, T_SHH_scat, 1))
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

  ax0.plot(T_HTH_model   , phi_HTH_model       , color="b", zorder=1)#, label="IN")
  ax0.plot(T_HTH_NC_model, phi_HTH_NC_model    , color="b", zorder=1)#, label="IC")
  ax0.plot(T_HTH_NC_assum, phi_HTH_NC_assum    , color="b", zorder=1)#, label="IC")
  ax0.plot(T_SHH_model   , phi_SHH_model   , color="m", alpha=1, zorder=1)#, label="IN")
  ax0.plot(T_SHH_NC_model, phi_SHH_NC_model, color="m", alpha=1, zorder=1)#, label="IC")
#  ax0.plot(T_SHH_NC_line, phi_SHH_NC_line, color="m", alpha=1, zorder=1)#, label="IC")

ax1.set_xlabel(r"$T_{r}$", fontsize=12, labelpad=5)
ax1.set_ylabel(r"$\phi_{\mathrm{eff}}$", fontsize=12, labelpad=2)
ax1.tick_params(axis="both", labelsize=10, pad=0)
ax1.set_xlim(T_min-0.004, T_max)
ax1.set_ylim(phi_min, phi_max)
ax1.legend(loc="lower right", fontsize=10, handletextpad=0.01)
ax1.set_yticks([0.25, 0.3, 0.35, 0.4, 0.45, 0.5])
ax1.set_yticklabels(["", "0.3", "", "0.4", "", 0.5])
ax1.set_xticks([0.0,0.05, 0.1, 0.15])

ax0.set_xlabel(r"$T_{r}$", fontsize=12, labelpad=5)
ax0.set_ylabel(r"$\phi$", fontsize=12, labelpad=2)
ax0.tick_params(axis="both", labelsize=10, pad=0)
ax0.set_xlim(T_min-0.004, T_max)
ax0.set_ylim(phi_min, phi_max)
ax0.legend(loc="lower right", fontsize=10, handletextpad=0.01)
ax0.set_yticks([0.25, 0.3, 0.35, 0.4, 0.45, 0.5])
ax0.set_yticklabels(["", "0.3", "", "0.4", "", 0.5])
ax0.set_xticks([0.0,0.05, 0.1, 0.15])
#
#ax0.text(-0.16, 0.95, r"a)", fontsize=12, transform=ax0.transAxes)
#ax1.text(-0.16, 0.95, r"b)", fontsize=12, transform=ax1.transAxes)

if test == 0:
  fig0.subplots_adjust(left=0.16, top=0.996, bottom=0.14, right=0.996)
  fig1.subplots_adjust(left=0.16, top=0.996, bottom=0.14, right=0.996)

#plt.show()
#sys.exit()
fig0.savefig("fig-phase_diag.pdf")
#fig1.savefig("fig-phase_diag_phi_eff.pdf")
plt.close()
