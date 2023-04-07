#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 02 05:40:00 2022

@author: pierrekawak
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

df_MCPC = pd.read_csv('dataaggregate.out', delimiter=' ')
df_MCPC['Et'] = df_MCPC['Epair'] + df_MCPC['Ebond']
df_MCPC['Et_se'] = (df_MCPC['Epair_se']**2 + df_MCPC['Ebond_se']**2)**0.5

res = df_MCPC.groupby(['T']).mean().reset_index()
sem = df_MCPC.groupby(['T']).sem().reset_index()

#T = np.array([5., 7.5, 10.])
simp_pairE_avg = np.array([-7.8443817E+03,-6.3182585E+03,-5.1108395E+03])
simp_pairE_se = np.array([2.9740000E+01,4.7420000E+01,5.6620000E+01])
simp_bondE_avg = np.array([2.4743033E+04,3.7239809E+04,4.9805644E+04])
simp_bondE_se = np.array([1.9880000E+02,3.2620000E+02,4.5340000E+02])
simp_totalE_avg = simp_pairE_avg + simp_bondE_avg
simp_totalE_se = np.sqrt( simp_pairE_se**2 + simp_bondE_se**2 )

markersize = 8
markeredgewidth = 1.5
fig, ax = plt.subplots(figsize=(4,3), constrained_layout=True)
plt.errorbar(res['T'], simp_totalE_avg/1e4, 1.96*simp_totalE_se/1e4, marker='o', color='#2ca02c', markersize=markersize, markerfacecolor='None', markeredgewidth=markeredgewidth, linestyle='None', label='Simpatico')
plt.errorbar(res['T'], res['Et']/1e4, 1.96*res['Et_se']/1e4, marker='o', color='#9467bd', markersize=markersize, markerfacecolor='None', markeredgewidth=markeredgewidth, linestyle='None', label='GPU MCMC')
plt.legend(loc='lower right', fontsize=12, frameon=True, borderpad=0.5, markerfirst=True, handlelength=1, handletextpad=0.5)
plt.xlim([4,12])
plt.ylim([1,5])
plt.xticks(np.linspace(4, 12, 5))
plt.yticks(np.linspace(1, 5, 5))
plt.xlabel(r'$kT/\epsilon$', fontsize=12, labelpad=8)
plt.ylabel(r'$\left<U\right>/\epsilon \times 10^{-4}$', fontsize=12, labelpad=8)
fig.savefig('fig-accuracy.pdf')

import scipy.stats as st

T_t_stuff = []
t_stuff = []
for i in range(len(res['T'])):
  dff=len(df_MCPC.loc[df_MCPC['T'] == res['T'][i]])
  T_t_stuff.append(res['T'][i])
  t_stuff.append(st.t.interval(alpha=0.95, df=dff, loc=res['Et'][i], scale=res['Et_se'][i]))

for i in range(len(res['T'])):
  dff=len(df_MCPC.loc[df_MCPC['T'] == res['T'][i]])
  tval=-st.t.ppf(0.05, dff)
#  print(T_t_stuff[i], res['Et'][i], res['Et_se'][i], res['Et'][i]-tval*res['Et_se'][i], res['Et'][i]+tval*res['Et_se'][i], t_stuff[i][0], t_stuff[i][1])
  zstat = res['Et'][i]-simp_totalE_avg[i]
  zstat /= res['Et_se'][i]
  zstat = np.abs(zstat)
  pval = np.exp(-0.717*zstat -0.416*zstat**2)
#  print(zstat, pval)

