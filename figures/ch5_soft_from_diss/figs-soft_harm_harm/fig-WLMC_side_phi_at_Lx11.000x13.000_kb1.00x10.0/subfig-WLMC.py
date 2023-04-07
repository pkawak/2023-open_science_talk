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
label_prefix = r'$k_{b}=$'

names_in_WL = ["T", "Em", "Cv", "q6", "P2", "n6", "r2e", "r2g", "sms"]

WL_result_files = np.array([
                     "../Lx11.000_kb0.10_WLMC_results.out", "../Lx11.000_kb1.00_WLMC_results.out", "../Lx11.000_kb10.0_WLMC_results.out",
                     "../Lx11.436_kb0.10_WLMC_results.out", "../Lx11.436_kb1.00_WLMC_results.out", "../Lx11.436_kb10.0_WLMC_results.out",
                     "../Lx13.000_kb0.10_WLMC_results.out", "../Lx13.000_kb1.00_WLMC_results.out", "../Lx13.000_kb10.0_WLMC_results.out",
                     "../Lx15.000_kb0.10_WLMC_results.out", "../Lx15.000_kb1.00_WLMC_results.out", "../Lx15.000_kb10.0_WLMC_results.out"
                 ,    "../Lx11.200_kb1.00_WLMC_results.out", "../Lx11.800_kb1.00_WLMC_results.out", "../Lx12.500_kb1.00_WLMC_results.out", "../Lx13.500_kb0.10_WLMC_results.out"
                    ])

Lx_      = [11, 11.436, 13, 15]
Lx_      = np.repeat(Lx_, 3)
Lx_      = np.append(Lx_, [11.2, 11.8, 12.5, 13.5])
phi_     = Nc*Nb*sigma**3/Lx_**3*np.pi/6
kb_      = [0.1, 1, 10]
kb_      = np.tile(kb_, 4)
kb_      = np.append(kb_, [1,1,1,1])

cutT = 0.012
upT = 0.2
input_df = pd.DataFrame({'result_files': WL_result_files, 'Lx': Lx_, 'phi': phi_, 'kb': kb_})

Lx_A = 13.000
kb_A = 1.00
phi_A         = np.round(Nc*Nb*sigma**3/Lx_A**3*np.pi/6, 3)
WL_A_file     = input_df.loc[(input_df['kb'] == kb_A) & (input_df['Lx'] == Lx_A)]['result_files'].iat[0]
WL_A_df       = pd.read_csv(WL_A_file, index_col=False, delimiter=' ', names=names_in_WL)
WL_A_df['Tr'] = WL_A_df['T']/kb_A
#WL_A_df       = WL_A_df.loc[WL_A_df['Tr'] > cutT]
WL_A_df       = WL_A_df.loc[WL_A_df['Tr'] < upT]

Lx_B = 11.436
kb_B = 1.00
phi_B         = np.round(Nc*Nb*sigma**3/Lx_B**3*np.pi/6, 3)
WL_B_file     = input_df.loc[(input_df['kb'] == kb_B) & (input_df['Lx'] == Lx_B)]['result_files'].iat[0]
WL_B_df       = pd.read_csv(WL_B_file, index_col=False, delimiter=' ', names=names_in_WL)
WL_B_df['Tr'] = WL_B_df['T']/kb_B
#WL_B_df       = WL_B_df.loc[WL_B_df['Tr'] > cutT]
WL_B_df       = WL_B_df.loc[WL_B_df['Tr'] < upT]

Lx_C = 13.000
kb_C = 10.00
phi_C         = np.round(Nc*Nb*sigma**3/Lx_C**3*np.pi/6, 3)
WL_C_file     = input_df.loc[(input_df['kb'] == kb_C) & (input_df['Lx'] == Lx_C)]['result_files'].iat[0]
WL_C_df       = pd.read_csv(WL_C_file, index_col=False, delimiter=' ', names=names_in_WL)
WL_C_df['Tr'] = WL_C_df['T']/kb_C
#WL_C_df       = WL_C_df.loc[WL_C_df['Tr'] > cutT]
WL_C_df       = WL_C_df.loc[WL_C_df['Tr'] < upT]

Lx_D = 11.436
kb_D = 10.00
phi_D         = np.round(Nc*Nb*sigma**3/Lx_D**3*np.pi/6, 3)
WL_D_file     = input_df.loc[(input_df['kb'] == kb_D) & (input_df['Lx'] == Lx_D)]['result_files'].iat[0]
WL_D_df       = pd.read_csv(WL_D_file, index_col=False, delimiter=' ', names=names_in_WL)
WL_D_df['Tr'] = WL_D_df['T']/kb_D
#WL_D_df       = WL_D_df.loc[WL_D_df['Tr'] > cutT]
WL_D_df       = WL_D_df.loc[WL_D_df['Tr'] < upT]

test = 1
if test:
  fig, ax = plt.subplots(3, 1, sharex=True, figsize=(3.25,2.0*3), constrained_layout=True)
else:
  fig, ax = plt.subplots(3, 1, sharex=True, figsize=(3.25,2.0*3))#, constrained_layout=True)

what_is_x = "Tr"
Nbond = np.amax(WL_A_df["Em"])

pu, = ax[0].plot(WL_A_df[what_is_x], (WL_A_df["Em"])/Nbond, c=plt.get_cmap('tab10')(0), label=r"$\langle U \rangle_{\mathrm{norm}}$")
pp, = ax[0].plot(WL_A_df[what_is_x], WL_A_df["P2"]              , c=plt.get_cmap('tab10')(1), label=r"$P_{2}$")
pq, = ax[0].plot(WL_A_df[what_is_x], WL_A_df["n6"]              , c=plt.get_cmap('tab10')(2), label=r"$f_{\mathrm{cryst}}$")
ax2 = ax[0].twinx()
pc, = ax2.plot(np.array(WL_A_df[what_is_x])[WL_A_df[what_is_x]>cutT]  , np.array(WL_A_df["Cv"])[WL_A_df[what_is_x]>cutT]/Nc/(Nb-2)    , c=plt.get_cmap('tab10')(3), label=r"$C_{V}/kN_{c}$")
ax2ylim1 = 1
ax2ylim2 = 6
ax2ytick1 = 1
ax2ytick2 = 5
ax2.set_ylim(ax2ylim1, ax2ylim2)
ax2.tick_params(axis='y', labelsize=8, labelcolor=plt.get_cmap('tab10')(3))
ax2.set_yscale('log')
ax2.set_ylabel(r"$\frac{C_{V}}{kN_{\mathrm{bonds}}}$", fontsize=12, color=plt.get_cmap('tab10')(3), labelpad=-3)
ax2.set_yticks([ax2ytick1, ax2ytick2])
from matplotlib.ticker import ScalarFormatter, NullFormatter
ax2.yaxis.set_major_formatter(ScalarFormatter())
ax2.yaxis.set_minor_formatter(NullFormatter())
ax[0].tick_params(axis='both', labelsize=8)
#ax[0].legend(handles=[pu, pp, pq, pc], loc='best', fontsize=8)#, prop={'size': 6})

from matplotlib.offsetbox import AnchoredOffsetbox, TextArea, HPacker, VPacker

ybox1 = TextArea(r"$\langle U \rangle_{\mathrm{norm}}$", textprops=dict(color=plt.get_cmap('tab10')(0), size=10, rotation=90,ha='left',va='bottom'))
ybox2 = TextArea(r"$P_{2}$"                            , textprops=dict(color=plt.get_cmap('tab10')(1), size=10, rotation=90,ha='left',va='bottom'))
ybox3 = TextArea(r"$f_{\mathrm{cryst}}$"               , textprops=dict(color=plt.get_cmap('tab10')(2), size=10, rotation=90,ha='left',va='bottom'))

ybox = VPacker(children=[ybox1, ybox2, ybox3], align="bottom", pad=0, sep=10)

anchored_ybox = AnchoredOffsetbox(loc=8, child=ybox, pad=0., frameon=False, bbox_to_anchor=(-0.2, 0.1), 
                                  bbox_transform=ax[0].transAxes, borderpad=0.)

ax[0].add_artist(anchored_ybox)

Nbond = np.amax(WL_B_df["Em"])
pu, = ax[1].plot(WL_B_df[what_is_x], (WL_B_df["Em"])/Nbond, c=plt.get_cmap('tab10')(0), label=r"$\langle U \rangle_{\mathrm{norm}}$")
pp, = ax[1].plot(WL_B_df[what_is_x], WL_B_df["P2"]              , c=plt.get_cmap('tab10')(1), label=r"$P_{2}$")
pq, = ax[1].plot(WL_B_df[what_is_x], WL_B_df["n6"]              , c=plt.get_cmap('tab10')(2), label=r"$f_{\mathrm{cryst}}$")
ax2 = ax[1].twinx()
pc, = ax2.plot(np.array(WL_B_df[what_is_x])[WL_B_df[what_is_x]>cutT]  , np.array(WL_B_df["Cv"])[WL_B_df[what_is_x]>cutT]/Nc/(Nb-2)    , c=plt.get_cmap('tab10')(3), label=r"$C_{V}/kN_{c}$")
ax2.set_ylim(ax2ylim1, ax2ylim2)
ax2.tick_params(axis='y', labelsize=8, labelcolor=plt.get_cmap('tab10')(3))
ax2.set_yscale('log')
ax2.set_ylabel(r"$\frac{C_{V}}{kN_{\mathrm{bonds}}}$", fontsize=12, color=plt.get_cmap('tab10')(3), labelpad=-3)
ax2.set_yticks([ax2ytick1, ax2ytick2])
from matplotlib.ticker import ScalarFormatter, NullFormatter
ax2.yaxis.set_major_formatter(ScalarFormatter())
ax2.yaxis.set_minor_formatter(NullFormatter())
ax[1].tick_params(axis='both', labelsize=8)
#ax[1].legend(handles=[pu, pp, pq, pc], loc='best', fontsize=8)#, prop={'size': 6})

from matplotlib.offsetbox import AnchoredOffsetbox, TextArea, HPacker, VPacker

ybox1 = TextArea(r"$\langle U \rangle_{\mathrm{norm}}$", textprops=dict(color=plt.get_cmap('tab10')(0), size=10, rotation=90,ha='left',va='bottom'))
ybox2 = TextArea(r"$P_{2}$"                            , textprops=dict(color=plt.get_cmap('tab10')(1), size=10, rotation=90,ha='left',va='bottom'))
ybox3 = TextArea(r"$f_{\mathrm{cryst}}$"               , textprops=dict(color=plt.get_cmap('tab10')(2), size=10, rotation=90,ha='left',va='bottom'))

ybox = VPacker(children=[ybox1, ybox2, ybox3], align="bottom", pad=0, sep=10)

anchored_ybox = AnchoredOffsetbox(loc=8, child=ybox, pad=0., frameon=False, bbox_to_anchor=(-0.2, 0.1), 
                                  bbox_transform=ax[1].transAxes, borderpad=0.)

ax[1].add_artist(anchored_ybox)

Nbond = np.amax(WL_D_df["Em"])
pu, = ax[2].plot(WL_D_df[what_is_x], (WL_D_df["Em"])/Nbond, c=plt.get_cmap('tab10')(0), label=r"$\langle U \rangle_{\mathrm{norm}}$")
pp, = ax[2].plot(WL_D_df[what_is_x], WL_D_df["P2"]              , c=plt.get_cmap('tab10')(1), label=r"$P_{2}$")
pq, = ax[2].plot(WL_D_df[what_is_x], WL_D_df["n6"]              , c=plt.get_cmap('tab10')(2), label=r"$f_{\mathrm{cryst}}$")
ax2 = ax[2].twinx()
pc, = ax2.plot(np.array(WL_D_df[what_is_x])[WL_D_df[what_is_x]>cutT]  , np.array(WL_D_df["Cv"])[WL_D_df[what_is_x]>cutT]/Nc/(Nb-2)    , c=plt.get_cmap('tab10')(3), label=r"$C_{V}/kN_{c}$")

ax2.set_ylim(ax2ylim1, ax2ylim2)
ax2.tick_params(axis='y', labelsize=8, labelcolor=plt.get_cmap('tab10')(3))
ax2.set_yscale('log')
ax2.set_ylabel(r"$\frac{C_{V}}{kN_{\mathrm{bonds}}}$", fontsize=12, color=plt.get_cmap('tab10')(3), labelpad=-3)
ax2.set_yticks([ax2ytick1, ax2ytick2])
from matplotlib.ticker import ScalarFormatter, NullFormatter
ax2.yaxis.set_major_formatter(ScalarFormatter())
ax2.yaxis.set_minor_formatter(NullFormatter())
ax[2].tick_params(axis='both', labelsize=8)
#ax[2].legend(handles=[pu, pp, pq, pc], loc='best', fontsize=8)#, prop={'size': 6})

from matplotlib.offsetbox import AnchoredOffsetbox, TextArea, HPacker, VPacker

ybox1 = TextArea(r"$\langle U \rangle_{\mathrm{norm}}$", textprops=dict(color=plt.get_cmap('tab10')(0), size=10, rotation=90,ha='left',va='bottom'))
ybox2 = TextArea(r"$P_{2}$"                            , textprops=dict(color=plt.get_cmap('tab10')(1), size=10, rotation=90,ha='left',va='bottom'))
ybox3 = TextArea(r"$f_{\mathrm{cryst}}$"               , textprops=dict(color=plt.get_cmap('tab10')(2), size=10, rotation=90,ha='left',va='bottom'))

ybox = VPacker(children=[ybox1, ybox2, ybox3], align="bottom", pad=0, sep=10)

anchored_ybox = AnchoredOffsetbox(loc=8, child=ybox, pad=0., frameon=False, bbox_to_anchor=(-0.2, 0.1), 
                                  bbox_transform=ax[2].transAxes, borderpad=0.)

ax[2].add_artist(anchored_ybox)

#Nbond = np.amax(WL_D_df["Em"])
#pu, = ax[3].plot(WL_D_df[what_is_x], (WL_D_df["Em"])/Nbond, c=plt.get_cmap('tab10')(0), label=r"$\langle U \rangle_{\mathrm{norm}}$")
#pp, = ax[3].plot(WL_D_df[what_is_x], WL_D_df["P2"]              , c=plt.get_cmap('tab10')(1), label=r"$P_{2}$")
#pq, = ax[3].plot(WL_D_df[what_is_x], WL_D_df["n6"]              , c=plt.get_cmap('tab10')(2), label=r"$f_{\mathrm{cryst}}$")
#ax2 = ax[3].twinx()
#pc, = ax2.plot(WL_D_df[what_is_x]  , WL_D_df["Cv"]/Nc/(Nb-2)    , c=plt.get_cmap('tab10')(3), label=r"$C_{V}/kN_{c}$")
#
#ax2.set_ylim(ax2ylim1, ax2ylim2)
#ax2.tick_params(axis='y', labelsize=8, labelcolor=plt.get_cmap('tab10')(3))
#ax2.set_yscale('log')
#ax2.set_ylabel(r"$\frac{C_{V}}{kN_{\mathrm{bonds}}}$", fontsize=12, color=plt.get_cmap('tab10')(3), labelpad=-3)
#ax2.set_yticks([ax2ytick1, ax2ytick2])
#from matplotlib.ticker import ScalarFormatter, NullFormatter
#ax2.yaxis.set_major_formatter(ScalarFormatter())
#ax2.yaxis.set_minor_formatter(NullFormatter())
#ax[3].tick_params(axis='both', labelsize=8)
##ax[3].legend(handles=[pu, pp, pq, pc], loc='best', fontsize=8)#, prop={'size': 6})
#
#from matplotlib.offsetbox import AnchoredOffsetbox, TextArea, HPacker, VPacker
#
#ybox1 = TextArea(r"$\langle U \rangle_{\mathrm{norm}}$", textprops=dict(color=plt.get_cmap('tab10')(0), size=10, rotation=90,ha='left',va='bottom'))
#ybox2 = TextArea(r"$P_{2}$"                            , textprops=dict(color=plt.get_cmap('tab10')(1), size=10, rotation=90,ha='left',va='bottom'))
#ybox3 = TextArea(r"$f_{\mathrm{cryst}}$"               , textprops=dict(color=plt.get_cmap('tab10')(2), size=10, rotation=90,ha='left',va='bottom'))
#
#ybox = VPacker(children=[ybox1, ybox2, ybox3], align="bottom", pad=0, sep=10)
#
#anchored_ybox = AnchoredOffsetbox(loc=8, child=ybox, pad=0., frameon=False, bbox_to_anchor=(-0.2, 0.1), 
#                                  bbox_transform=ax[3].transAxes, borderpad=0.)
#
#ax[3].add_artist(anchored_ybox)

ax[-1].set_xlabel(r"$T_{r}$", fontsize=10, labelpad=5)

if test == 0:
  plt.subplots_adjust(left=0.168, top=0.999, bottom=0.05, right=0.998, hspace=0.1)

ylim1 = -.01
ylim2 = 1
ax[0].set_ylim(ylim1, ylim2)
ax[1].set_ylim(ylim1, ylim2)
ax[2].set_ylim(ylim1, ylim2)
#ax[3].set_ylim(ylim1, ylim2)
xlim1 = 0
xlim2 = 0.2
ax[0].set_xlim(xlim1, xlim2)
ax[1].set_xlim(xlim1, xlim2)
ax[2].set_xlim(xlim1, xlim2)
#ax[3].set_xlim(xlim1, xlim2)
import os
basename = os.path.splitext(__file__)[0]
plt.savefig(basename+".pdf")
