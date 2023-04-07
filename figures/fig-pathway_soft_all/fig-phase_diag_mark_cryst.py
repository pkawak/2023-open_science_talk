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

Lx_reg=np.array([10.80, 10.85, 10.90, 10.95, 11.00, 11.20, 11.436, 11.80, 12.50, 13.00, 13.50])
phi_reg=np.array([.36738580410297206293, .36233010756915599929, .35736675090531806108, .35249363552190808253, .34770871980327809415, .32941211653420185469, .30943625579083324058, .28167455415242255982, .23695375670177952937, .21065102688127589590, .18810153170072169621])
phi_nosigmareg=np.array([.51956198678576816871, .51241215218040284445, .50539290587150835336, .49850128000528099655, .49173438730118226246, .46585908281269473691, .43760894962934654607, .39834797465775078716, .33510321638291127876, .29790553914331979578, .26601573723431330238])
Tin_reg=np.array([0.14207507507507505, 0.14357057057057054, 0.14307207207207207, 0.13983183183183182, 0.13758858858858858, 0.12437837837837837, 0.11137137137137137, 0.09172672672672672, 0.056831831831831825, 0.041571571571571576, 0.025426426426426424])
Tc_reg=np.array([0.10568468468468467, 0.10194594594594594, 0.09048048048048048, 0.07502702702702702, 0.0658048048048048, 0.0633123123123123, 0.044044044044044044, 0.016204204204204202, 0, 0, 0])

# the linregress fit line of data
slope, intercept, r_value, p_value, std_err = stats.linregress(phi_reg, Tin_reg)
phi_min = 0.15
phi_max = 0.4
phi_line = np.linspace(phi_min, phi_max, 1000)
Tin_line   = phi_line*slope + intercept

no_Tc_idx = np.where(Tc_reg != 0)
phi_c = phi_reg[no_Tc_idx]
Tc_reg = Tc_reg[no_Tc_idx]
# the linregress fit line of data
slope, intercept, r_value, p_value, std_err = stats.linregress(phi_c, Tc_reg)
Tc_line   = phi_line*slope + intercept

phi_scat = phi_reg
T_scat   = Tin_reg

T_min = 0.0
T_max = 0.15
#pt=1/72
#fig, ax = plt.subplots(1, figsize=(398*0.6*pt,210*pt), constrained_layout=True)
fig, ax = plt.subplots(1, figsize=(1.65,1.43))

# paint regions

phi_nem_bot=[]
phi_nem_top=[]
region_nem = np.linspace(T_min, T_max, 100)
for i in range(len(region_nem)):
  idx = (np.abs(Tin_line-region_nem[i])).argmin()
  phi_nem_bot.append(phi_line[idx])
  idx = (np.abs(Tc_line-region_nem[i])).argmin()
  phi_nem_top.append(phi_line[idx])
ax.fill_between(region_nem, phi_nem_bot, phi_nem_top, color=['#FFC947'], alpha=0.7)
#ax.text(0.33, 0.58, 'Nematic', weight='bold', color='g', fontsize=12, fontname='dejavusans', transform = ax.transAxes)

#for i in range(len(region_2)):
#  if region_2[i] < T_quad[0]:
#    phi_below_2.append(phi_trip)
#  else:
#    idx = (np.abs(T_quad-region_2[i])).argmin()
#    phi_quad_i = phi_quad[idx]
#    if phi_quad_i < phi_trip:
#      phi_below_2.append(phi_trip)
#    else:
#      phi_below_2.append(phi_quad_i)
ax.fill_between(region_nem, phi_nem_top, phi_max, color=['#185ADB'], alpha=0.5)
#ax.text(0.1, 0.82, 'Crystal', weight='bold', color='b', fontsize=12, fontname='dejavusans', transform = ax.transAxes)

ax.fill_between(region_nem, phi_min, phi_nem_bot, color=['#EFEFEF'], alpha=0.5)
#ax.text(0.63, 0.3, 'Melt'   , weight='bold', color='r', fontsize=12, fontname='dejavusans', transform = ax.transAxes)
#like S and P
T_SandP = np.linspace(0.01,0.6,1000)
th_s = np.arccos(0.9) #stepwise stiffness cutoff
th_m = 2.*np.pi/3. #max theta due to hard core restrictions
l = 1.0 #bond length
N = 10 #chain length
cos_theta_avg = 0.5*(np.exp(1./T_SandP)*np.sin(th_s)**2 + np.cos(th_s)**2 - np.cos(th_m)**2) / (np.exp(1./T_SandP)*(1-np.cos(th_s)) + np.cos(th_s) - np.cos(th_m)) #formula for thermal average for an isolated bond angle doi:10.1103/PhysRevE.97.042501
lk_by_l = ( (1+cos_theta_avg)/(1-cos_theta_avg) - 2./(N-1.) * (1-cos_theta_avg**(N-1))/(1-cos_theta_avg)**2 )
phi_SandP = 1.4/lk_by_l
#ax.plot(T_SandP, phi_SandP, color='m', ls=':', alpha=0.7, label='Shakirov and Paul')

ax.plot(Tin_line, phi_line, color='k', zorder=1)
ax.plot(Tc_line, phi_line, color='k', zorder=1)
#ax.plot([T_min, model(phi_trip)], [phi_trip, phi_trip], ls='--', color='k', zorder=1)
#ax.scatter(T_scat, phi_scat, color='m', zorder=2)
#ax.scatter(Tc_reg, phi_c, color='k', zorder=2)
ax.set_xlabel(r"$T_{r}$", fontsize=8, labelpad=3)#, labelpad=0.3)
ax.set_ylabel(r"$\phi$", fontsize=8, labelpad=2)
ax.tick_params(axis='both', labelsize=6)
ax.set_xlim(T_min, T_max)
ax.set_ylim(phi_min, phi_max)
ax.set_xticks([])
ax.set_yticks([])
Tin_trans = 0.111
Tc_trans  = 0.044
phi_trans = 0.309
ax.hlines(phi_trans, T_min, T_max, linestyles='dashdot', color='k')
c_color  = 'darkorange'
in_color = 'lime'
ax.scatter(Tc_trans, phi_trans, s=30, c=c_color)
ax.scatter(Tin_trans, phi_trans, s=30, c=in_color)
t = ax.text(Tc_trans-0.05, phi_trans+0.06, "("+str(Tc_trans)+","+str(phi_trans)+")", fontsize=8, color='w')
t.set_bbox(dict(facecolor=c_color, alpha=0.7))
t = ax.text(Tin_trans-0.043, phi_trans-0.06, "("+str(Tin_trans)+","+str(phi_trans)+")", fontsize=8, color='w')
t.set_bbox(dict(facecolor='g', alpha=0.7))
plt.savefig("fig-phase_diag_mark_cryst.pdf")
