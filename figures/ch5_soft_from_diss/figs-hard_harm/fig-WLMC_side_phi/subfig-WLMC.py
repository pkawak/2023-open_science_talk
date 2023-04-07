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

WL_A_file_name   = "lx13.00_ext_canon_distro.out"
WL_B_file_name   = "lx11.224_ext_canon_distro.out"

WL_A_file_params = "lx13.00_params.json"
WL_B_file_params = "lx11.224_params.json"

usecols          = (0,1,2,3,4,5)
names            = ['T', 'Em', 'Cv', 'q6', 'P2', 'n6']

WL_A_df          = pd.read_csv(WL_A_file_name, index_col=False, delimiter=' ', 
                                   usecols=usecols, names=names)
WL_B_df          = pd.read_csv(WL_B_file_name, index_col=False, delimiter=' ', 
                                   usecols=usecols, names=names)

Lx_A             = float(json.load(open(WL_A_file_params, "r+"))["Lx"])
Lx_B             = float(json.load(open(WL_B_file_params, "r+"))["Lx"])

phi_A            = np.round(Nc*Nb*sigma**3/Lx_A**3*np.pi/6, 3)
phi_B            = np.round(Nc*Nb*sigma**3/Lx_B**3*np.pi/6, 3)
print(phi_A, phi_B)

test = 0
if test:
  fig, ax = plt.subplots(2, 1, sharex=True, figsize=(3.13,2.0*2), constrained_layout=True)
else:
  fig, ax = plt.subplots(2, 1, sharex=True, figsize=(3.13,2.0*2))#, constrained_layout=True)
cutT = 0.005

what_is_x = "T"
#pu, = ax[0].plot(WL_A_df[what_is_x], (WL_A_df["Em"])/Nbond, c=plt.get_cmap('tab10')(0), label=r"$\langle U \rangle_{\mathrm{norm}}$")
pp, = ax[0].plot(WL_A_df[what_is_x], WL_A_df["P2"]              , c=plt.get_cmap('tab10')(0), label=r"$P_{2}$")
pq, = ax[0].plot(WL_A_df[what_is_x], WL_A_df["n6"]              , c=plt.get_cmap('tab10')(2), label=r"$f_{\mathrm{cryst}}$")
ax2 = ax[0].twinx()
pc, = ax2.plot(np.array(WL_A_df[what_is_x])[WL_A_df[what_is_x]>cutT]  , np.array(WL_A_df["Cv"])[WL_A_df[what_is_x]>cutT]/Nc/(Nb-2)    , c=plt.get_cmap('tab10')(3), label=r"$C_{V}/kN_{c}$")
ax2ylim1 = 0.5
ax2ylim2 = 6
ax2ytick1 = 1
ax2ytick2 = 5
ax2.set_ylim(ax2ylim1, ax2ylim2)
ax2.tick_params(axis='y', labelsize=8, labelcolor=plt.get_cmap('tab10')(3), pad=0)
ax2.set_yscale('log')
#ax2.set_ylabel(r"$\frac{C_{V}}{kN_{\mathrm{bonds}}}$", fontsize=12, color=plt.get_cmap('tab10')(3), labelpad=-3)
ax2.set_ylabel(r"$C_{V}/kN_{\mathrm{bonds}}$", fontsize=10, color=plt.get_cmap('tab10')(3), labelpad=10)
ax2.set_yticks([ax2ytick1, ax2ytick2])
from matplotlib.ticker import ScalarFormatter, NullFormatter
ax2.yaxis.set_major_formatter(ScalarFormatter())
ax2.yaxis.set_minor_formatter(NullFormatter())
ax[0].tick_params(axis='both', labelsize=8, pad=0)
#ax[0].legend(handles=[pu, pp, pq, pc], loc='best', fontsize=8)#, prop={'size': 6})

from matplotlib.offsetbox import AnchoredOffsetbox, TextArea, HPacker, VPacker

#ybox1 = TextArea(r"$\langle U \rangle_{\mathrm{norm}}$", textprops=dict(color=plt.get_cmap('tab10')(0), size=10, rotation=90,ha='left',va='bottom'))
ybox2 = TextArea(r"$P_{2}$"                            , textprops=dict(color=plt.get_cmap('tab10')(0), size=10, rotation=90,ha='left',va='bottom'))
ybox3 = TextArea(r"$f_{\mathrm{cryst}}$"               , textprops=dict(color=plt.get_cmap('tab10')(2), size=10, rotation=90,ha='left',va='bottom'))

ybox = VPacker(children=[ybox2, ybox3], align="bottom", pad=0, sep=10)

anchored_ybox = AnchoredOffsetbox(loc=8, child=ybox, pad=0., frameon=False, bbox_to_anchor=(-0.175, 0.3), 
                                  bbox_transform=ax[0].transAxes, borderpad=0.)
ax[0].add_artist(anchored_ybox)

#Nbond = np.amax(WL_B_df["Em"])
#pu, = ax[1].plot(WL_B_df[what_is_x], (WL_B_df["Em"])/Nbond, c=plt.get_cmap('tab10')(0), label=r"$\langle U \rangle_{\mathrm{norm}}$")
pp, = ax[1].plot(WL_B_df[what_is_x], WL_B_df["P2"]              , c=plt.get_cmap('tab10')(0), label=r"$P_{2}$")
pq, = ax[1].plot(WL_B_df[what_is_x], WL_B_df["n6"]              , c=plt.get_cmap('tab10')(2), label=r"$f_{\mathrm{cryst}}$")
ax2 = ax[1].twinx()
pc, = ax2.plot(np.array(WL_B_df[what_is_x])[WL_A_df[what_is_x]>cutT]  , np.array(WL_B_df["Cv"])[WL_A_df[what_is_x]>cutT]/Nc/(Nb-2)    , c=plt.get_cmap('tab10')(3), label=r"$C_{V}/kN_{c}$")
ax2.set_ylim(ax2ylim1, ax2ylim2)
ax2.tick_params(axis='y', labelsize=8, labelcolor=plt.get_cmap('tab10')(3), pad=0)
ax2.set_yscale('log')
#ax2.set_ylabel(r"$\frac{C_{V}}{kN_{\mathrm{bonds}}}$", fontsize=12, color=plt.get_cmap('tab10')(3), labelpad=-3)
ax2.set_ylabel(r"$C_{V}/kN_{\mathrm{bonds}}$", fontsize=10, color=plt.get_cmap('tab10')(3), labelpad=10)
ax2.set_yticks([ax2ytick1, ax2ytick2])
from matplotlib.ticker import ScalarFormatter, NullFormatter
ax2.yaxis.set_major_formatter(ScalarFormatter())
ax2.yaxis.set_minor_formatter(NullFormatter())
ax[1].tick_params(axis='both', labelsize=8, pad=0)
#ax[1].legend(handles=[pu, pp, pq, pc], loc='best', fontsize=8)#, prop={'size': 6})

anchored_ybox = AnchoredOffsetbox(loc=8, child=ybox, pad=0., frameon=False, bbox_to_anchor=(-0.175, 0.3), 
                                  bbox_transform=ax[1].transAxes, borderpad=0.)
ax[1].add_artist(anchored_ybox)

ax[1].set_xlabel(r"$T_{r}$", fontsize=10, labelpad=5)


if test == 0:
  plt.subplots_adjust(left=0.155, top=0.985, bottom=0.088, right=0.874, hspace=0.08)

ylim1 = -.01
ylim2 = 1
ax[0].set_ylim(ylim1, ylim2)
ax[1].set_ylim(ylim1, ylim2)
xlim1 = 0
xlim2 = 0.25
ax[0].set_xlim(xlim1, xlim2)
ax[1].set_xlim(xlim1, xlim2)
import os
basename = os.path.splitext(__file__)[0]
plt.savefig(basename+".pdf")
