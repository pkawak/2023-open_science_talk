#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

f = open("lng_summary.out")
lines = f.readlines()
f.close()

rangel_a = np.zeros(len(lines)-1)
rangeh_a = np.zeros(len(lines)-1)
time_a = np.zeros(len(lines)-1) #last iter done time
count_a = np.zeros(len(lines)-1, dtype=int) #count of days
last_iter_a = np.zeros(len(lines)-1, dtype=int)
first_iter_a = np.zeros(len(lines)-1, dtype=int)

num = 0
for line in lines[1:]:
  #first line is empty
  line_list = line.split()
  rangel_a[num] = line_list[0]
  rangeh_a[num] = line_list[1]
  time_a[num]   = float(line_list[-1])/3600.
  count_a[num]  = len(line_list)-3
  last_iter_a[num]   = line_list[-2]
  first_iter_a[num]  = int(line_list[2])

  num += 1

np.savetxt("lng_2summary.out", np.c_[rangel_a, count_a, last_iter_a, time_a], fmt="%.2e %i %i %f")

days_a    = np.zeros(len(time_a))
converged = np.zeros(len(time_a), dtype=int)
color     = []
for i in range(len(time_a)):
  days_a[i] = count_a[i]
  if days_a[i] == 1:
    days_a[i] = time_a[i]/24.
  elif days_a[i] == 2:
    days_a[i] += 3+time_a[i]/24.
  elif days_a[i] == 3:
    days_a[i] += 6+time_a[i]/24.
  else:
    days_a[i] *= 3

  if last_iter_a[i] == 26:
    converged[i] = 1
  else:
    converged[i] = 0

  if converged[i]:
    color.append([0,0,1,1])
  else:
    color.append([1,0,0,1])

np.savetxt("lng_3summary.out", np.c_[rangel_a, days_a, converged], fmt="%.2e %.1f %d")

rangel_a = np.flip(rangel_a)
rangeh_a = np.flip(rangeh_a)
x_pos = [i for i, _ in enumerate(rangel_a)]
days_a   = np.flip(days_a)
color.reverse()
alpha = np.resize([0.6,0.6], len(rangel_a))
for i in range(len(rangel_a)): 
  color[i][3] = alpha[i]
#width = rangel_a[0] - rangel_a[1]

fontsize = 12
pt = 1/72 #in/pt

first_few = 30
if first_few == -1:
  first_few = len(rangel_a)
width = rangeh_a-rangel_a

fig, ax = plt.subplots(figsize=(5, 3.4), constrained_layout=True)
#plt.bar(x_pos, days_a, color=color)
ax.bar(rangel_a[:first_few]+width[:first_few]/2, days_a[:first_few], width=width[:first_few], color=color, edgecolor='k')
#plt.bar(rangel_a[:first_few]+width[:first_few]/2, days_a[:first_few], width=width[:first_few], color=color, edgecolor='k', alpha=alpha[:first_few])
#plt.xticks([],[])
ax.set_xlabel("Energy range", fontsize=fontsize, labelpad=5)
ax.set_ylabel("Clock time (days)", fontsize=fontsize, labelpad=5)
custom_bar = [ Line2D([0], [0], color=[0,0,1,0.6], lw=4), Line2D([0], [0], color=[1,0,0,0.6], lw=4) ]
plt.legend(custom_bar, ["converged", "unconverged"], fontsize=fontsize, markerfirst=True, handlelength=0.8, handletextpad=0.3, borderpad=0.3, frameon=False)
plt.locator_params(axis='x', nbins=5)
ax.set_yticks([0,10,20,30,40])
#plt.subplots_adjust(left=0.1, right=0.97, bottom=0.1, top=0.965)
#fig.savefig("duration_bar.png", dpi=1200)
fig.savefig("fig-duration_bar.pdf")

first_iter_a = np.flip(first_iter_a)
goal_a = np.ones(len(first_iter_a), dtype=int)*26
fig, ax = plt.subplots(figsize=(5, 2.75), constrained_layout=True)
plt.scatter(rangel_a, first_iter_a, s=6.)
plt.plot(rangel_a, goal_a, label="converged", linewidth=3, color="r")
plt.xlabel("Temperature", fontsize=fontsize)
plt.ylabel("Iteration # (after 3 days)", fontsize=fontsize)
plt.xticks([],[])
plt.ylim(0,27)
fig.savefig("iter_num_3day_plt.pdf")
