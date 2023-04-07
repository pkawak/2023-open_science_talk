#!/usr/bin/env python3

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

Nb       = 100
rho      = 0.15
sigma    = 1
rc       = 2.5
fontsize = 10
in_file  = "sp_metrics.out"

pd.set_option("display.precision", 16)
df = pd.read_csv(in_file, sep=" ")

# average out reps
df = df.groupby( ['mode', 'Nc'] ).mean().reset_index()
df['acc'] = df['numb_succ']/df['numb_try']
df['time_per_succ'] = df['time_per_step']*df['numb_try']/df['numb_succ']
df['Lx'] = (df['Nc']*Nb/rho) ** (1/3)
df['ncell'] = (df['Lx']/rc).astype('int')
for i in range(len(df['ncell'])):
  while (df['ncell'].iloc[i]/2 % 2) == 1:
    df['ncell'].iloc[i] -= 1
df['rcell'] = df['Lx']/df['ncell']
df['proc'] = (df['ncell']/2) ** 3

# split into parallel and serial
df_par = df.loc[df['mode'] == "par"]
df_ser = df.loc[df['mode'] == "ser"]

# use this to simplify plotting interesting stuff
toPlot = [['time_per_step', 'numb_try', 'acc'], ['auto_time_sec', 'Emean', 'conv_crit']]
x = 'Nc'
scale  = [['log', 'linear', 'linear'], ['linear', 'linear', 'linear']]

# calculate speedup measures
Nc = df_ser['Nc'].to_numpy()
sp_nom  = df_ser['time_per_step'].to_numpy()/df_par['time_per_step'].to_numpy()
sp_succ = df_ser['time_per_succ'].to_numpy()/df_par['time_per_succ'].to_numpy()
sp_auto = df_ser['auto_time_sec'].to_numpy()/df_par['auto_time_sec'].to_numpy()

def returnThreads(Nc):
  return int( ( 100/2.5**3/0.15*Nc )**(1/3) )**3/8

def returnNc(threads):
  return 2.5**3 * 8 * threads * 0.15/100

cmap = plt.get_cmap("tab10")
test = 0
pt=1/72
ht=0.8
wt=1.0
fig, ax = plt.subplots(1, 1, figsize=(wt*199*pt, ht*243.4*pt), sharex=True, constrained_layout=test)
#ax.scatter(Nc, sp_nom , color=cmap(0), s=100, label=r'$S_{p}^{\mathrm{try}}$')
#ax.scatter(Nc, sp_succ, color=cmap(2), s=100, label=r'$S_{p}^{\mathrm{success}}$')
ax.scatter(Nc, sp_auto, color=cmap(3), s=100, label=r'$S_{p}^{\mathrm{auto}}$')
#ax.vlines(returnNc(1792), ylim1, ylim2, color=cmap(5), ls='dashed', label="P100")
ax.set_yscale('log')
ax.set_xscale('log')
#ax.set_xlabel(r'$N_{c}$', fontsize=fontsize)
ax.set_xlabel(r'Number of polymers', fontsize=fontsize)
ax.set_ylabel(r'Speedup = $t_{\mathrm{serial}}/t_{\mathrm{parallel}}$', fontsize=fontsize, labelpad=-5)
#ax.legend(loc='upper left', fontsize=fontsize, ncol=2, columnspacing=1.0)

ylim1 = 1
ylim2 = 10.75
ax.set_yticks([1,10])
ax.set_ylim([ylim1, ylim2])

Nclim1 = 80
Nclim2 = 12000
ax.set_xlim(Nclim1, Nclim2)
plim1  = returnThreads(Nclim1)
plim2  = returnThreads(Nclim2)
ax.tick_params(axis='both', labelsize=fontsize, pad=0)

## twin object for two different y-axis on the sample plot
#ax2=ax.twiny()
#ax2.set_xscale('log')
#ax2.set_xlabel('threads (p)', fontsize=fontsize)
#ax2.set_xlim(plim1, plim2)
#ax2.tick_params(axis='x'  , labelsize=fontsize, pad=0)
if test == 0:
  plt.subplots_adjust(left=0.144, bottom=0.146, right=0.991, top=0.998, hspace=0.0)
fig.savefig('fig-speedup.pdf')
plt.close()
