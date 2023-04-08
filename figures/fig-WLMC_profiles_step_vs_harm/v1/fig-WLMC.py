#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
created on Tue June 14 08:41:00 2021

@author: pierrekawak
"""

import sys
import numpy as np
import matplotlib.pyplot as plt
import random
import pandas as pd
import json

Nc    = 125
Nb    = 10
sigma = 1

WL_step_file_name   = "hard-step-rods-lx11.224_ext_canon_distro.out"
WL_harm_file_name   = "hard-harm-rods-lx11.224_ext_canon_distro.out"

WL_step_file_params = "hard-step-rods-lx11.224_params.json"
WL_harm_file_params = "hard-harm-rods-lx11.224_params.json"

usecols          = (0,1,2,3,4,5)
names            = ['T', 'Em', 'Cv', 'q6', 'P2', 'n6']

WL_step_df          = pd.read_csv(WL_step_file_name, index_col=False, delimiter=' ', 
                                   usecols=usecols, names=names)
WL_harm_df          = pd.read_csv(WL_harm_file_name, index_col=False, delimiter=' ', 
                                   usecols=usecols, names=names)

Lx_step             = 11.224
Lx_harm             = 11.224

phi_step            = np.round(Nc*Nb*sigma**3/Lx_step**3*np.pi/6, 3)
phi_harm            = np.round(Nc*Nb*sigma**3/Lx_harm**3*np.pi/6, 3)

fig, ax0 = plt.subplots(1, 1, sharex=True, figsize=(3.13,2.0), constrained_layout=True)
cutT = 0.005

what_is_x = "T"
#pu, = ax0.plot(WL_step_df[what_is_x], (WL_step_df["Em"])/Nbond, c=plt.get_cmap('tab10')(0), label=r"$\langle U \rangle_{\mathrm{norm}}$")
pp, = ax0.plot(WL_step_df[what_is_x], WL_step_df["P2"]              , c=plt.get_cmap('tab10')(0), label=r"$P_{2}$")
pq, = ax0.plot(WL_step_df[what_is_x], WL_step_df["n6"]              , c=plt.get_cmap('tab10')(2), label=r"$f_{\mathrm{cryst}}$")
ax2 = ax0.twinx()
pc, = ax2.plot(np.array(WL_step_df[what_is_x])[WL_step_df[what_is_x]>cutT]  , np.array(WL_step_df["Cv"])[WL_step_df[what_is_x]>cutT]/Nc/(Nb-2)    , c=plt.get_cmap('tab10')(3), label=r"$C_{V}/kN_{c}$")
ax2ylim1 = 0.5
ax2ylim2 = 300
ax2yticks = [1,10,100]
ax2.set_ylim(ax2ylim1, ax2ylim2)
ax2.tick_params(axis='y', labelsize=8, labelcolor=plt.get_cmap('tab10')(3), pad=0)
ax2.set_yscale('log')
#ax2.set_ylabel(r"$\frac{C_{V}}{kN_{\mathrm{bonds}}}$", fontsize=12, color=plt.get_cmap('tab10')(3), labelpad=-3)
ax2.set_ylabel(r"$C_{V}/kN_{\mathrm{bonds}}$", fontsize=10, color=plt.get_cmap('tab10')(3), labelpad=10)
ax2.set_yticks(ax2yticks)
#from matplotlib.ticker import ScalarFormatter, NullFormatter
#ax2.yaxis.set_major_formatter(ScalarFormatter())
#ax2.yaxis.set_minor_formatter(NullFormatter())
ax0.tick_params(axis='both', labelsize=8, pad=0)
#ax0.legend(handles=[pu, pp, pq, pc], loc='best', fontsize=8)#, prop={'size': 6})
ax0.set_xlabel(r"$T_{r}$", fontsize=10, labelpad=5)

from matplotlib.offsetbox import AnchoredOffsetbox, TextArea, HPacker, VPacker

#ybox1 = TextArea(r"$\langle U \rangle_{\mathrm{norm}}$", textprops=dict(color=plt.get_cmap('tab10')(0), size=10, rotation=90,ha='left',va='bottom'))
ybox2 = TextArea(r"$P_{2}$"                            , textprops=dict(color=plt.get_cmap('tab10')(0), size=10, rotation=90,ha='left',va='bottom'))
ybox3 = TextArea(r"$f_{\mathrm{cryst}}$"               , textprops=dict(color=plt.get_cmap('tab10')(2), size=10, rotation=90,ha='left',va='bottom'))

ybox = VPacker(children=[ybox2, ybox3], align="bottom", pad=0, sep=10)

anchored_ybox = AnchoredOffsetbox(loc=8, child=ybox, pad=0., frameon=False, bbox_to_anchor=(-0.175, 0.3), 
                                  bbox_transform=ax0.transAxes, borderpad=0.)
ax0.add_artist(anchored_ybox)
ylim1 = -.01
ylim2 = 1
ax0.set_ylim(ylim1, ylim2)
xlim1 = 0
xlim2 = 0.50
ax0.set_xlim(xlim1, xlim2)
import os
basename = os.path.splitext(__file__)[0]
plt.savefig(basename+"_1.pdf")

#Nbond = np.amax(WL_harm_df["Em"])
#pu, = ax1.plot(WL_harm_df[what_is_x], (WL_harm_df["Em"])/Nbond, c=plt.get_cmap('tab10')(0), label=r"$\langle U \rangle_{\mathrm{norm}}$")
fig, ax1 = plt.subplots(1, 1, sharex=True, figsize=(3.13,2.0), constrained_layout=True)
pp, = ax1.plot(WL_harm_df[what_is_x], WL_harm_df["P2"]              , c=plt.get_cmap('tab10')(0), label=r"$P_{2}$")
pq, = ax1.plot(WL_harm_df[what_is_x], WL_harm_df["n6"]              , c=plt.get_cmap('tab10')(2), label=r"$f_{\mathrm{cryst}}$")
ax2 = ax1.twinx()
pc, = ax2.plot(np.array(WL_harm_df[what_is_x])[WL_step_df[what_is_x]>cutT]  , np.array(WL_harm_df["Cv"])[WL_step_df[what_is_x]>cutT]/Nc/(Nb-2)    , c=plt.get_cmap('tab10')(3), label=r"$C_{V}/kN_{c}$")
ax2.set_ylim(ax2ylim1, ax2ylim2)
ax2.tick_params(axis='y', labelsize=8, labelcolor=plt.get_cmap('tab10')(3), pad=0)
ax2.set_yscale('log')
ax2.set_ylabel(r"$C_{V}/kN_{\mathrm{bonds}}$", fontsize=10, color=plt.get_cmap('tab10')(3), labelpad=10)
ax2.set_yticks(ax2yticks)
ax1.tick_params(axis='both', labelsize=8, pad=0)
#ax1.legend(handles=[pu, pp, pq, pc], loc='best', fontsize=8)#, prop={'size': 6})

#ybox1 = TextArea(r"$\langle U \rangle_{\mathrm{norm}}$", textprops=dict(color=plt.get_cmap('tab10')(0), size=10, rotation=90,ha='left',va='bottom'))
ybox2 = TextArea(r"$P_{2}$"                            , textprops=dict(color=plt.get_cmap('tab10')(0), size=10, rotation=90,ha='left',va='bottom'))
ybox3 = TextArea(r"$f_{\mathrm{cryst}}$"               , textprops=dict(color=plt.get_cmap('tab10')(2), size=10, rotation=90,ha='left',va='bottom'))

ybox = VPacker(children=[ybox2, ybox3], align="bottom", pad=0, sep=10)

anchored_ybox2 = AnchoredOffsetbox(loc=8, child=ybox, pad=0., frameon=False, bbox_to_anchor=(-0.175, 0.3), 
                                  bbox_transform=ax1.transAxes, borderpad=0.)
ax1.add_artist(anchored_ybox2)

ax1.set_xlabel(r"$T_{r}$", fontsize=10, labelpad=5)

#plt.subplots_adjust(left=0.155, top=0.985, bottom=0.088, right=0.874, hspace=0.08)

ylim1 = -.01
ylim2 = 1
ax1.set_ylim(ylim1, ylim2)
ax1.set_xticks([0, 0.1, 0.2, 0.3])
xlim1 = 0
xlim2 = 0.3
ax1.set_xlim(xlim1, xlim2)
import os
basename = os.path.splitext(__file__)[0]
plt.savefig(basename+"_2.pdf")

fig, ax = plt.subplots(1, 1, sharex=True, figsize=(3.13,2.0), constrained_layout=True)
pp, = ax.plot(WL_step_df[what_is_x], WL_step_df["P2"]              , c=plt.get_cmap('tab10')(0), ls='--', marker='|', markevery=400, label=r"$P_{2}$")
pq, = ax.plot(WL_step_df[what_is_x], WL_step_df["n6"]              , c=plt.get_cmap('tab10')(2), ls='--', marker='|', markevery=400, label=r"$f_{\mathrm{cryst}}$")
ax2 = ax.twinx()
pc, = ax2.plot(np.array(WL_step_df[what_is_x])[WL_step_df[what_is_x]>cutT]  , np.array(WL_step_df["Cv"])[WL_step_df[what_is_x]>cutT]/Nc/(Nb-2)    , c=plt.get_cmap('tab10')(3), ls='--', marker='|', markevery=400, label=r"$C_{V}/kN_{c}$")
ax2ylim1 = 0.5
ax2ylim2 = 300
ax2yticks = [1,10,100]
ax2.set_ylim(ax2ylim1, ax2ylim2)
ax2.tick_params(axis='y', labelsize=8, labelcolor=plt.get_cmap('tab10')(3), pad=0)
ax2.set_yscale('log')
ax2.set_ylabel(r"$C_{V}/kN_{\mathrm{bonds}}$", fontsize=10, color=plt.get_cmap('tab10')(3), labelpad=10)
ax2.set_yticks(ax2yticks)
ax.tick_params(axis='both', labelsize=8, pad=0)
ax.set_xlabel(r"$T_{r}$", fontsize=10, labelpad=5)

pp, = ax.plot(WL_harm_df[what_is_x], WL_harm_df["P2"]              , c=plt.get_cmap('tab10')(0), ls='-', marker='_', markevery=400, label=r"$P_{2}$")
pq, = ax.plot(WL_harm_df[what_is_x], WL_harm_df["n6"]              , c=plt.get_cmap('tab10')(2), ls='-', marker='_', markevery=400, label=r"$f_{\mathrm{cryst}}$")
ax2 = ax.twinx()
pc, = ax2.plot(np.array(WL_harm_df[what_is_x])[WL_step_df[what_is_x]>cutT]  , np.array(WL_harm_df["Cv"])[WL_step_df[what_is_x]>cutT]/Nc/(Nb-2)    , c=plt.get_cmap('tab10')(3), ls='-', marker='_', markevery=400, label=r"$C_{V}/kN_{c}$")
ax2.set_ylim(ax2ylim1, ax2ylim2)
ax2.tick_params(axis='y', labelsize=8, labelcolor=plt.get_cmap('tab10')(3), pad=0)
ax2.set_yscale('log')
ax2.set_ylabel(r"$C_{V}/kN_{\mathrm{bonds}}$", fontsize=10, color=plt.get_cmap('tab10')(3), labelpad=10)
ax2.set_yticks(ax2yticks)
ax.tick_params(axis='both', labelsize=8, pad=0)
#ax1.legend(handles=[pu, pp, pq, pc], loc='best', fontsize=8)#, prop={'size': 6})

from matplotlib.offsetbox import AnchoredOffsetbox, TextArea, HPacker, VPacker
#ybox1 = TextArea(r"$\langle U \rangle_{\mathrm{norm}}$", textprops=dict(color=plt.get_cmap('tab10')(0), size=10, rotation=90,ha='left',va='bottom'))
ybox2 = TextArea(r"$P_{2}$"                            , textprops=dict(color=plt.get_cmap('tab10')(0), size=10, rotation=90,ha='left',va='bottom'))
ybox3 = TextArea(r"$f_{\mathrm{cryst}}$"               , textprops=dict(color=plt.get_cmap('tab10')(2), size=10, rotation=90,ha='left',va='bottom'))

ybox = VPacker(children=[ybox2, ybox3], align="bottom", pad=0, sep=10)

anchored_ybox2 = AnchoredOffsetbox(loc=8, child=ybox, pad=0., frameon=False, bbox_to_anchor=(-0.175, 0.3), 
                                  bbox_transform=ax.transAxes, borderpad=0.)
ax.add_artist(anchored_ybox2)

ax.set_xlabel(r"$T_{r}$", fontsize=10, labelpad=5)

#plt.subplots_adjust(left=0.155, top=0.985, bottom=0.088, right=0.874, hspace=0.08)

ylim1 = -.01
ylim2 = 1
ax.set_ylim(ylim1, ylim2)
ax.set_xticks([0, 0.1, 0.2, 0.3])
xlim1 = 0
xlim2 = 0.5
ax.set_xlim(xlim1, xlim2)
plt.savefig(basename+".pdf")
