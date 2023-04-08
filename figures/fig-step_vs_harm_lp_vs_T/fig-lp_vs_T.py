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
import pandas as pd
import math
from scipy.interpolate import make_interp_spline

l  = 1.0 #bond length
N  = 10 #chain length
Nc = 125

# file names
step_lp_file_name                 = "step_avg-lpvsT.out"
harm_lp_file_name                 = "harm_avg-lpvsT.out"
step_wkappa_lp_file_name          = "step_wkappa_avg-lpvsT.out"
harm_wkappa_lp_file_name          = "harm_wkappa_avg-lpvsT.out"
harm_wkappa_2_lp_file_name        = "harm_wkappa_2_avg-lpvsT.out"

# get lp data
step_lp_df                        = pd.read_csv(step_lp_file_name, index_col=False, delimiter=" ", keep_default_na=False, na_values=['_'])
harm_lp_df                        = pd.read_csv(harm_lp_file_name, index_col=False, delimiter=" ", keep_default_na=False, na_values=['_'])
step_wkappa_lp_df                 = pd.read_csv(step_wkappa_lp_file_name, index_col=False, delimiter=" ", keep_default_na=False, na_values=['_'])
harm_wkappa_lp_df                 = pd.read_csv(harm_wkappa_lp_file_name, index_col=False, delimiter=" ", keep_default_na=False, na_values=['_'])
harm_wkappa_2_lp_df               = pd.read_csv(harm_wkappa_2_lp_file_name, index_col=False, delimiter=" ", keep_default_na=False, na_values=['_'])

step_lp_df['costheta_s']          = np.round(np.cos(step_lp_df['theta_s'])       , 3)
step_wkappa_lp_df['costheta_s']   = np.round(np.cos(step_wkappa_lp_df['theta_s']), 3)
step_lp_df['kappa']               = 1
harm_lp_df['kappa']               = 1
harm_lp_df['costheta_s']          = 0.9
harm_wkappa_lp_df['costheta_s']   = 0.9
harm_wkappa_2_lp_df['costheta_s'] = 0.9

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
figsize   = (3.15, 2.75)
fontsize  = 10
labelsize = 8
test = 0
if test:
  fig, ax = plt.subplots(1, figsize=figsize, sharex=True, constrained_layout=True)
else:
  fig, ax = plt.subplots(1, figsize=figsize, sharex=True)

ax.scatter(step_kb1_kappa1_lp_df["Tr"]    , step_kb1_kappa1_lp_df["lp"]   , s=30, marker='^', facecolors='none', edgecolors='m', label='stepwise')
ax.scatter(harm_kb1_kappa1_lp_df["Tr"]    , harm_kb1_kappa1_lp_df["lp"]   , s=30, marker='^', facecolors='none', edgecolors='b', label='harmonic')
ax.scatter(step_kb1_kappa600_lp_df["Tr"]  , step_kb1_kappa600_lp_df["lp"] , s=30, marker='o', facecolors='none', edgecolors='m', label=r'$\kappa^{*}=600$')
ax.scatter(harm_kb1_kappa600_lp_df["Tr"]  , harm_kb1_kappa600_lp_df["lp"] , s=30, marker='o', facecolors='none', edgecolors='b', label=r'$\kappa^{*}=600$')
ax.scatter(step_kb20_kappa600_lp_df["Tr"] , step_kb20_kappa600_lp_df["lp"], s=20, marker='s', facecolors='none', edgecolors='m', label=r'$k_b=20$')
ax.scatter(harm_kb20_kappa600_lp_df["Tr"] , harm_kb20_kappa600_lp_df["lp"], s=20, marker='s', facecolors='none', edgecolors='b', label=r'$k_b=20$')

T = np.linspace(0.00025,1.0,10000, dtype=np.float128)
th_m = math.pi #maximum angle allowed
th_s = np.arccos(0.9) #stepwise stiffness cutoff

# theoretical stepwise lp
cosT = 0.5*(np.exp(1./T)*np.sin(th_s)**2 + np.cos(th_s)**2 - np.cos(th_m)**2) / (np.exp(1./T)*(1-np.cos(th_s)) + np.cos(th_s) - np.cos(th_m)) #formula for thermal average for an isolated bond angle doi:10.1103/PhysRevE.97.042501
lp = 0.5 * l * ( (1+cosT)/(1-cosT) )
ax.plot(T, lp     , lw=0.8, color='m')

# theoretical harmonic lp
cosT_harm = ( np.cos(th_m) * np.exp(np.cos(th_m)/T) - np.exp(1/T) ) / ( np.exp(np.cos(th_m)/T) - np.exp(1/T) ) - T
lp_harm = 0.5 * l * ( (1+cosT_harm)/(1-cosT_harm) )
U_harm = 1-cosT_harm
ax.plot(T, lp_harm, lw=0.8, color='b')

# These are in unitless percentages of the figure size. (0,0 is bottom left)
left, bottom, width, height = [0.5, 0.34, 0.45, 0.45]
ax.tick_params(axis='both', labelsize=labelsize, pad=0)
ax.set_xlabel(r"Reduced Temperature, $T_{r}$"     , fontsize=fontsize, labelpad=3)
ax.set_ylabel(r"Persistence Length, $l_{p}/l_{0}$", fontsize=fontsize, labelpad=2)
ax.set_xscale('log')
ax.set_yscale('log')
ax.set_xlim(0.00025-0.00005, 1+0.3)
ax.set_ylim(0, 1200)

from matplotlib.lines import Line2D
legend_elements = [
                   Line2D([0], [0], color='m', label='Discrete'),
                   Line2D([0], [0], color='b', label='Continuous'),
#                   Line2D([0], [0], marker='+', color='k', markeredgewidth=1.5, label=r'$\kappa^{*} = 600$',
#                   Line2D([0], [0], marker='o', color='k', markeredgewidth=1.5, label=r'springs $\frac{\epsilon_{l}}{\epsilon_{\theta}} = 600$',
#                          markerfacecolor='k', markersize=5),# handlelength=1),
#                   Line2D([0], [0], marker='s', color='w', label=r'$k_{b}^{*} = 20$',
#                   Line2D([0], [0], marker='s', color='w', label=r'springs $\frac{\epsilon_{l}}{\epsilon_{\theta}} = 30$',
#                          markerfacecolor='k', markersize=10),
                  ]

#ax.legend(loc='lower left', ncol=1, handles=legend_elements, labelspacing=1, handlelength=0.5, fontsize=fontsize, frameon=False)
ax.legend(loc='lower left', ncol=1, handles=legend_elements, labelspacing=0.3, handlelength=1.0, fontsize=fontsize, frameon=False, title="Bending Stiffness", bbox_to_anchor=(-0.02, -0.02))
#ax.legend(handles=legend_elements, loc='lower right', ncol=1, columnspacing=1.0, fontsize=7.5, handletextpad=1, handlelength=0.5, borderpad=0.5)#, bbox_to_anchor=(1.02,-0.02))
if test == 0:
  plt.subplots_adjust(left=0.174, top=0.994, bottom=0.146, right=0.9925)

plt.savefig("fig-lp_vs_T.pdf")
plt.close()

# more analyses:
from scipy import stats
slope, intercept, r_value, p_value, std_err = stats.linregress(np.array(np.log(T), dtype=np.float64), np.array(np.log(lp_harm), dtype=np.float64))
print(slope, intercept)
lp_harm_loglog   = np.log(T)*slope + intercept
c_star = 10**intercept
lp_harm_ = c_star*T**slope
print("lp_harm = ", str(round(c_star, 6)), "* T ^", str(round(slope, 6)))
mse = ((np.log(lp_harm) - lp_harm_loglog)**2).mean(axis=0)
#print("mse of lp_harm and lp_harm_loglog:", mse)
corr_matrix = np.corrcoef(np.log(lp_harm), lp_harm_loglog)
corr_matrix = np.corrcoef(lp_harm, lp_harm_)
corr = corr_matrix[0,1]
R_sq = corr**2
print("Fitness:", R_sq)
#
#import statsmodels.api as sm
#spector_data = sm.datasets.spector.load()
#spector_data.exog = sm.add_constant(spector_data.exog, prepend=False)
#
## Fit and summarize OLS model
#mod = sm.OLS(spector_data.endog, spector_data.exog)
#res = mod.fit()
#print(res.summary())
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
#plt.plot(np.log(T), np.log(lp_harm))
#plt.plot(np.log(T), lp_harm_loglog)
#plt.plot(np.log(T), np.log(lp_harm_))
#plt.plot(T, lp_harm)
#plt.plot(T, 10**lp_harm_loglog)
#plt.show()
