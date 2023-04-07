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

ylim1 = 1
ylim2 = 70

cmap = plt.get_cmap("tab10")
test = 0
fig, axs = plt.subplots(3, 1, figsize=(6.5, 8.1), sharex=True, constrained_layout=test)
ax = axs[0]
ax.scatter(Nc, sp_nom , color=cmap(0), s=100, label=r'$S_{p}^{\mathrm{try}}$')
ax.scatter(Nc, sp_succ, color=cmap(2), s=100, label=r'$S_{p}^{\mathrm{success}}$')
ax.scatter(Nc, sp_auto, color=cmap(3), s=100, label=r'$S_{p}^{\mathrm{auto}}$')
ax.vlines(returnNc(1792), ylim1, ylim2, color=cmap(5), ls='dashed', label="P100")
ax.set_yscale('log')
ax.set_xscale('log')
#ax.set_xlabel(r'$N_{c}$', fontsize=fontsize)
ax.set_ylabel(r'Speedup, $S_{p}$', fontsize=fontsize)#, labelpad=-5)
ax.legend(loc='upper left', fontsize=fontsize, ncol=2, columnspacing=1.0)
ax.set_yticks([1,10])
ax.set_ylim([ylim1, ylim2])

# twin object for two different y-axis on the sample plot
ax2=ax.twiny()
#ax2.scatter(df_par['proc'], sp_nom , color=cmap(0), marker='*', s=100, label=r'$S_{p}^{\mathrm{try}}$')
#ax2.scatter(df_par['proc'], sp_succ, color=cmap(2), marker='*', s=100, label=r'$S_{p}^{\mathrm{success}}')
#ax2.scatter(df_par['proc'], sp_auto, color=cmap(3), marker='*', s=100, label=r'$S_{p}^{\mathrm{auto}}$')
ax2.set_xscale('log')
ax2.set_xlabel('threads (p)', fontsize=fontsize)

Nclim1 = 80
Nclim2 = 12000
ax.set_xlim(80, 12000)
plim1  = returnThreads(Nclim1)
plim2  = returnThreads(Nclim2)
ax2.set_xlim(plim1, plim2)

ax.tick_params(axis='both', labelsize=fontsize, pad=0)
ax2.tick_params(axis='x'  , labelsize=fontsize, pad=0)

ax = axs[1]
ax.scatter(Nc, df_ser['time_per_step']*10**6, color=cmap(0), s=100, marker='+', label=r'$t^{\mathrm{try}}_{\mathrm{serial}}$')
ax.scatter(Nc, df_par['time_per_step']*10**6, color=cmap(0), s=100, marker='*', label=r'$t^{\mathrm{try}}_{\mathrm{parallel}}$')
ax.scatter(Nc, df_ser['time_per_succ']*10**6, color=cmap(2), s=100, marker='+', label=r'$t^{\mathrm{succ}}_{\mathrm{ serial}}$')
ax.scatter(Nc, df_par['time_per_succ']*10**6, color=cmap(2), s=100, marker='*', label=r'$t^{\mathrm{succ}}_{\mathrm{ parallel}}$')
ax.set_yscale('log')
ax.set_xscale('log')
#ax.set_xlabel(r'$N_{c}$', fontsize=fontsize)
ax.set_ylabel(r'time for $10^{6}$ moves (sec)', fontsize=fontsize, labelpad=5)
ax.legend(loc='best', fontsize=fontsize, ncol=2, columnspacing=1.0)
#ax.set_yticks([1,10])
#ax.set_ylim([ylim1, ylim2])
ax.set_xlim(80, 12000)
ax.tick_params(axis='both', labelsize=fontsize, pad=0)

ax = axs[2]
ax.scatter(Nc, df_ser['auto_time_sec'], color=cmap(3), s=100, marker='+', label=r'serial')
ax.scatter(Nc, df_par['auto_time_sec'], color=cmap(3), s=100, marker='*', label=r'parallel')
ax.set_yscale('log')
ax.set_xscale('log')
ax.set_xlabel(r'$N_{c}$', fontsize=fontsize)
ax.set_ylabel(r'autocorrelation time, $\tau$ (sec)', fontsize=fontsize, labelpad=5)
ax.legend(loc='best', fontsize=fontsize, ncol=2, columnspacing=1.0)
ax.set_xlim(80, 12000)
ax.tick_params(axis='both', labelsize=fontsize, pad=0)

df_ser.loc[:, 'time_per_succ'] = df_ser.loc[:, 'time_per_step']*df_ser.loc[:, 'numb_succ']/df_ser.loc[:, 'numb_try']
df_par.loc[:, 'time_per_succ'] = df_par.loc[:, 'time_per_step']*df_par.loc[:, 'numb_succ']/df_par.loc[:, 'numb_try']

if test == 0:
  plt.subplots_adjust(left=0.083, bottom=0.048, right=0.999, top=0.954, hspace=0.03)
fig.savefig('subfig-speedup.pdf')
plt.close()
