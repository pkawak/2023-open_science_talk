#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
created on Sat May 22 08:41:00 2021

@author: pierrekawak
"""

import sys
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import math
from scipy.interpolate import make_interp_spline

l  = 1.0 #bond length
N  = 10 #chain length
Nc = 125

step_lp_file_name                = "step_avg-lpvsT.out"
harm_lp_file_name                = "harm_avg-lpvsT.out"
step_wkappa_lp_file_name         = "step_wkappa_avg-lpvsT.out"
harm_wkappa_lp_file_name         = "harm_wkappa_avg-lpvsT.out"
harm_wkappa_2_lp_file_name       = "harm_wkappa_2_avg-lpvsT.out"
#filter_by = { "kb": 1.0 , "costheta_s": 0.9 }

# get lp data
step_lp_df                               = pd.read_csv(step_lp_file_name, index_col=False, delimiter=" ", keep_default_na=False, na_values=['_'])
harm_lp_df                               = pd.read_csv(harm_lp_file_name, index_col=False, delimiter=" ", keep_default_na=False, na_values=['_'])
step_wkappa_lp_df                        = pd.read_csv(step_wkappa_lp_file_name, index_col=False, delimiter=" ", keep_default_na=False, na_values=['_'])
harm_wkappa_lp_df                        = pd.read_csv(harm_wkappa_lp_file_name, index_col=False, delimiter=" ", keep_default_na=False, na_values=['_'])
harm_wkappa_2_lp_df               = pd.read_csv(harm_wkappa_2_lp_file_name, index_col=False, delimiter=" ", keep_default_na=False, na_values=['_'])

step_lp_df['costheta_s']                 = np.round(np.cos(step_lp_df['theta_s']),3)
step_wkappa_lp_df['costheta_s']          = np.round(np.cos(step_wkappa_lp_df['theta_s']),3)
step_lp_df['kappa']                      = 1
harm_lp_df['kappa']                      = 1
harm_lp_df['costheta_s']                 = 0.9
harm_wkappa_lp_df['costheta_s']          = 0.9
harm_wkappa_2_lp_df['costheta_s']        = 0.9

def unique_stuff(df):
  unique_kb = pd.unique(df['kb'])
  unique_kappa = pd.unique(df['kappa'])
  unique_costheta_s = pd.unique(df['costheta_s'])
  unique_l0 = pd.unique(df['l0'])
  print("kb:", unique_kb,"kappa:", unique_kappa,"costheta_s:", unique_costheta_s,"l0:", unique_l0)

#print("step_lp_df"); unique_stuff(step_lp_df)
#print("step_wkappa_lp_df"); unique_stuff(step_wkappa_lp_df)
#print("harm_lp_df"); unique_stuff(harm_lp_df)
#print("harm_wkappa_lp_df"); unique_stuff(harm_wkappa_lp_df)
#print("harm_wkappa_2_lp_df"); unique_stuff(harm_wkappa_2_lp_df)

step_lp_combo_df = pd.concat([step_lp_df, step_wkappa_lp_df])
harm_lp_combo_df = pd.concat([harm_lp_df, harm_wkappa_lp_df, harm_wkappa_2_lp_df])

filter_by = { "kb": 1.0, "kappa": 600.0, "costheta_s": 0.9 }
harm_kb1_kappa600_lp_df = harm_lp_combo_df.loc[(harm_lp_combo_df[list(filter_by)] == pd.Series(filter_by)).all(axis=1)]
step_kb1_kappa600_lp_df = step_lp_combo_df.loc[(step_lp_combo_df[list(filter_by)] == pd.Series(filter_by)).all(axis=1)]

filter_by = { "kb": 20.0, "kappa": 600, "costheta_s": 0.9 }
harm_kb20_kappa600_lp_df = harm_lp_combo_df.loc[(harm_lp_combo_df[list(filter_by)] == pd.Series(filter_by)).all(axis=1)]
step_kb20_kappa600_lp_df = step_lp_combo_df.loc[(step_lp_combo_df[list(filter_by)] == pd.Series(filter_by)).all(axis=1)]

filter_by = { "kb": 1.0, "kappa": 1.0, "costheta_s": 0.9 }
harm_kb1_kappa1_lp_df = harm_lp_combo_df.loc[(harm_lp_combo_df[list(filter_by)] == pd.Series(filter_by)).all(axis=1)]
step_kb1_kappa1_lp_df = step_lp_combo_df.loc[(step_lp_combo_df[list(filter_by)] == pd.Series(filter_by)).all(axis=1)]

#sys.exit()
#print("harm_kb1_kappa600", harm_kb1_kappa600_lp_df['Tr'])
#print("step_kb1_kappa600", step_kb1_kappa600_lp_df['Tr'])
#print("harm_kb20_kappa600", harm_kb20_kappa600_lp_df['Tr'])
#print("step_kb20_kappa600", step_kb20_kappa600_lp_df['Tr'])
#print("harm_kb1_kappa1", harm_kb1_kappa1_lp_df['Tr'])
#print("step_kb1_kappa1", step_kb1_kappa1_lp_df['Tr'])

step_lp_df = step_lp_df.loc[step_lp_df['costheta_s'] == 0.9]
step_wkappa_lp_df = step_wkappa_lp_df.loc[step_wkappa_lp_df['costheta_s'] == 0.9]

# filter out some Ts to prettify
figsize   = (3.1,3.0)
fontsize  = 10
labelsize = 8
test = 0
if test:
  fig, ax = plt.subplots(1, figsize=figsize, sharex=True, constrained_layout=True)
else:
  fig, ax = plt.subplots(1, figsize=figsize, sharex=True)
ax.set_xlabel(r"$T_{r}$", fontsize=fontsize, labelpad=5)
ax.set_ylabel(r"$l_{p}/l_{0}$", fontsize=fontsize, labelpad=2)
ax.tick_params(axis='both', labelsize=labelsize, pad=0)
ax.scatter(step_kb1_kappa1_lp_df["Tr"]   , step_kb1_kappa1_lp_df["lp"]   , s=5, color='m', label='stepwise')
ax.scatter(harm_kb1_kappa1_lp_df["Tr"]   , harm_kb1_kappa1_lp_df["lp"]   , s=5, color='b', label='harmonic')
ax.scatter(step_kb1_kappa600_lp_df["Tr"] , step_kb1_kappa600_lp_df["lp"] , marker='+', color='m', label=r'$\kappa^{*}=600$')
ax.scatter(harm_kb1_kappa600_lp_df["Tr"] , harm_kb1_kappa600_lp_df["lp"] , marker='+', color='b', label=r'$\kappa^{*}=600$')
ax.scatter(step_kb20_kappa600_lp_df["Tr"], step_kb20_kappa600_lp_df["lp"], s=20, marker='*', color='m', label=r'$k_b=20$')
ax.scatter(harm_kb20_kappa600_lp_df["Tr"], harm_kb20_kappa600_lp_df["lp"], s=20, marker='*', color='b', label=r'$k_b=20$')
#print(harm_kb20_kappa600_lp_df["Tr"])
#print(step_kb20_kappa600_lp_df["Tr"])
#ax.errorbar(step_wkappa_lp_df["Tr"], step_wkappa_lp_df["lp"], yerr=step_wkappa_lp_df["lp_se"], fmt='.', color='m', alpha=0.5, label='kb=10')
#ax.errorbar(harm_wkappa_lp_df["Tr"], harm_wkappa_lp_df["lp"], yerr=harm_wkappa_lp_df["lp_se"], fmt='.', color='b', alpha=0.5, label='kb=10')
#ax.errorbar(harm_wkappa_2_lp_df["Tr"], harm_wkappa_2_lp_df["lp"], yerr=harm_wkappa_2_lp_df["lp_se"], fmt='.', color='b', alpha=0.5)#, label='kb=10')
ax.set_ylim(0,25)
#ax.set_yscale('log')
#ax.set_xscale('log')
# These are in unitless percentages of the figure size. (0,0 is bottom left)
T = np.linspace(0.00025,1.0,10000, dtype=np.float128)
th_m = math.pi #maximum angle allowed
th_s = np.arccos(0.9) #stepwise stiffness cutoff

# theoretical stepwise lp
cosT = 0.5*(np.exp(1./T)*np.sin(th_s)**2 + np.cos(th_s)**2 - np.cos(th_m)**2) / (np.exp(1./T)*(1-np.cos(th_s)) + np.cos(th_s) - np.cos(th_m)) #formula for thermal average for an isolated bond angle doi:10.1103/PhysRevE.97.042501
lp = 0.5 * l * ( (1+cosT)/(1-cosT) )
ax.plot(T, lp, color='m')

# theoretical harmonic lp
cosT_harm = ( np.cos(th_m) * np.exp(np.cos(th_m)/T) - np.exp(1/T) ) / ( np.exp(np.cos(th_m)/T) - np.exp(1/T) ) - T
lp_harm = 0.5 * l * ( (1+cosT_harm)/(1-cosT_harm) )
U_harm = 1-cosT
ax.plot(T, lp_harm, color='b')

from matplotlib.lines import Line2D
legend_elements = [
                   Line2D([0], [0], marker='+', color='k', markeredgewidth=1.5, label=r'$\kappa^{*} = 600$',
                          markerfacecolor='k', markersize=5),# handlelength=1),
                   Line2D([0], [0], marker='*', color='w', label=r'$k_{b} = 20$',
                          markerfacecolor='k', markersize=10),
                   Line2D([0], [0], color='b', label='harmonic'),
                   Line2D([0], [0], color='m', label='stepwise')
                  ]

ax.set_xlim(0-0.03, 1+0.03)
#ax.legend(loc='best', fontsize=labelsize)
ax.legend(loc='best', ncol=2, handles=legend_elements, handlelength=0.5, fontsize=labelsize)
#ax.legend(handles=legend_elements, loc='lower right', ncol=1, columnspacing=1.0, fontsize=7.5, handletextpad=1, handlelength=0.5, borderpad=0.5)#, bbox_to_anchor=(1.02,-0.02))
if test == 0:
  plt.subplots_adjust(left=0.125, top=0.986, bottom=0.117, right=0.997)

left, bottom, width, height = [0.5, 0.34, 0.45, 0.45]
ax2 = fig.add_axes([left, bottom, width, height])
ax2.plot(T, lp, color='m')
ax2.plot(T, lp_harm, color='b')
ax2.tick_params(axis='both'     , labelsize=labelsize-2, pad=0)
ax2.set_xlabel(r"$T_{r}$"       , fontsize=fontsize-2  , labelpad=0)
ax2.set_ylabel(r"$l_{p}/l_{0}$", fontsize=fontsize-2  , labelpad=0)
ax2.scatter(step_kb1_kappa1_lp_df["Tr"]  , step_kb1_kappa1_lp_df["lp"]  , s=5, color='m', label='stepwise')
ax2.scatter(harm_kb1_kappa1_lp_df["Tr"]  , harm_kb1_kappa1_lp_df["lp"]  , s=5, color='b', label='harmonic')
ax2.scatter(step_kb1_kappa600_lp_df["Tr"], step_kb1_kappa600_lp_df["lp"], marker='+', color='m', label=r'$\kappa^{*}=600$')
ax2.scatter(harm_kb1_kappa600_lp_df["Tr"], harm_kb1_kappa600_lp_df["lp"], marker='+', color='b', label=r'$\kappa^{*}=600$')
ax2.scatter(step_kb20_kappa600_lp_df["Tr"] , step_kb20_kappa600_lp_df["lp"] , s=20, marker='*', color='m', label=r'$k_b=20$')
ax2.scatter(harm_kb20_kappa600_lp_df["Tr"] , harm_kb20_kappa600_lp_df["lp"] , s=20, marker='*', color='b', label=r'$k_b=20$')
ax2.set_xscale('log')
ax2.set_yscale('log')
#ax2.set_xlim(0.00025, 1)
ax2.set_xlim(0.00025-0.00005, 1+0.3)

plt.savefig("fig-lp_vs_T.pdf")
plt.close()

# more analyses:
#from scipy import stats
#slope, intercept, r_value, p_value, std_err = stats.linregress(np.array(np.log10(T), dtype=np.float64), np.array(np.log10(lp_harm), dtype=np.float64))
#lp_harm_loglog   = np.log10(T)*slope + intercept
#c_star = 10**intercept
#lp_harm_ = c_star*T**slope
#print("lp_harm = ", str(round(c_star, 6)), "*T^", str(round(slope, 6)))
#
#mse = ((np.log10(lp_harm) - lp_harm_loglog)**2).mean(axis=0)
#print("mse of lp_harm and lp_harm_loglog:", mse)
#
#T_data = harm_kb1_kappa1_lp_df["Tr"]
#lp_data = harm_kb1_kappa1_lp_df["lp"]
#lp_harm_model = c_star*T_data**slope
#mse = ((lp_data - lp_harm_model)**2).mean(axis=0)
#print("mse of lp_data and lp_harm_model:", mse)
#
#lp_harm_model_divT = c_star/T_data
#mse = ((lp_data - lp_harm_model_divT)**2).mean(axis=0)
#print("mse of lp_data and lp_harm_model_divT:", mse)
#
#print("slope", "intercept", "r_value", "p_value", "std_err")
#print(slope, intercept, r_value, p_value, std_err)
#plt.plot(np.log10(T), np.log10(lp_harm))
#plt.plot(np.log10(T), lp_harm_loglog)
#plt.plot(np.log10(T), np.log10(lp_harm_))
#plt.plot(T, lp_harm)
#plt.plot(T, 10**lp_harm_loglog)
#plt.show()
