#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt

def rotateByTheta(vec, th):
  return vec[0] * np.cos(th) - vec[1] * np.sin(th), vec[0] * np.sin(th) + vec[1] * np.cos(th)
def getDist(vec0, vec1):
  return np.sqrt( (vec0[0]-vec1[0])**2 + (vec0[1]-vec1[1])**2 )

l_CC = 1.55 # Ang
l_CH = 1.094 # Ang
theta = 115*np.pi/180
sig_CH2 = 4.000 # Ang
sig_HS = 5.2285 # Ang
bond_color = 'k' #plt.get_cmap('tab10')(0)
HS_color = '#ecb9984d'
HSbound_color = '#ecb998ff'
HSbond_color = '#05b2dcff'

x = []
y = []
#z = []

#1
x.append(0.0)
y.append(0.0)
#2
theta_init = np.pi/2/3.29672325179
x.append(l_CC*np.cos(theta_init))
y.append(l_CC*np.sin(theta_init))
#print(x[-1], y[-1])
#3
rot = rotateByTheta([x[-2]-x[-1], y[-2]-y[-1]], theta)
x.append(x[-1]+rot[0])
y.append(y[-1]+rot[1])
#4
rot = rotateByTheta([x[-2]-x[-1], y[-2]-y[-1]], -theta)
x.append(x[-1]+rot[0])
y.append(y[-1]+rot[1])
#5
rot = rotateByTheta([x[-2]-x[-1], y[-2]-y[-1]], theta)
x.append(x[-1]+rot[0])
y.append(y[-1]+rot[1])
#6
rot = rotateByTheta([x[-2]-x[-1], y[-2]-y[-1]], -theta)
x.append(x[-1]+rot[0])
y.append(y[-1]+rot[1])
#7
rot = rotateByTheta([x[-2]-x[-1], y[-2]-y[-1]], theta)
x.append(x[-1]+rot[0])
y.append(y[-1]+rot[1])
#8
rot = rotateByTheta([x[-2]-x[-1], y[-2]-y[-1]], -theta)
x.append(x[-1]+rot[0])
y.append(y[-1]+rot[1])

figsize1 = (2.2333333333, 0.918193)
figsize2 = (2.2333333333, 1.262866)
fontsize = 8
fig00, ax00 = plt.subplots(figsize=figsize2)
fig01, ax01 = plt.subplots(figsize=figsize2)
fig10, ax10 = plt.subplots(figsize=figsize2)
fig11, ax11 = plt.subplots(figsize=figsize2)
ax00.plot(x, y, c=bond_color)
ax01.plot(x, y, c=bond_color)
ax10.plot(x, y, c=bond_color)
ax11.plot(x, y, c=bond_color)
#for i in range(len(x)-1):
##  print(getDist([x[i], y[i]],  [x[i+1], y[i+1]]))
#  ax.plot([x[i], x[i+1]],  [y[i], y[i+1]], label=str(i+1))
for i in range(len(x)):
#  ax11.text(x[i],  y[i]     , "("+str(round(x[i], 2))+","+str(round(y[i], 2))+")", fontsize=fontsize, horizontalalignment="center", verticalalignment="center", bbox=dict(facecolor="white"))
  ax00.text(x[i],  y[i]     , "C"                                                , fontsize=fontsize, horizontalalignment="center", verticalalignment="center", bbox=dict(boxstyle="circle", facecolor="white", edgecolor="none"))
  ax00.text(x[i],  y[i]-l_CH, "H"                                                , fontsize=fontsize, horizontalalignment="center", verticalalignment="center", bbox=dict(boxstyle="circle", facecolor="white", edgecolor="none"))
  ax00.text(x[i],  y[i]+l_CH, "H"                                                , fontsize=fontsize, horizontalalignment="center", verticalalignment="center", bbox=dict(boxstyle="circle", facecolor="white", edgecolor="none"))
  ax01.text(x[i],  y[i]     , "C"                                                , fontsize=fontsize, horizontalalignment="center", verticalalignment="center", bbox=dict(boxstyle="circle", facecolor="white", edgecolor="none"))
  ax01.text(x[i],  y[i]-l_CH, "H"                                                , fontsize=fontsize, horizontalalignment="center", verticalalignment="center", bbox=dict(boxstyle="circle", facecolor="white", edgecolor="none"))
  ax01.text(x[i],  y[i]+l_CH, "H"                                                , fontsize=fontsize, horizontalalignment="center", verticalalignment="center", bbox=dict(boxstyle="circle", facecolor="white", edgecolor="none"))
#  ax11.text(x[i],  y[i]     , "C"                                                , fontsize=fontsize, horizontalalignment="center", verticalalignment="center", bbox=dict(boxstyle="circle", facecolor="white", edgecolor="none"))
#  ax11.text(x[i],  y[i]-l_CH, "H"                                                , fontsize=fontsize, horizontalalignment="center", verticalalignment="center", bbox=dict(boxstyle="circle", facecolor="white", edgecolor="none"))
#  ax11.text(x[i],  y[i]+l_CH, "H"                                                , fontsize=fontsize, horizontalalignment="center", verticalalignment="center", bbox=dict(boxstyle="circle", facecolor="white", edgecolor="none"))
  ax00.plot([x[i], x[i]], [y[i], y[i]-l_CH], c=bond_color)
  ax00.plot([x[i], x[i]], [y[i], y[i]+l_CH], c=bond_color)
  ax01.plot([x[i], x[i]], [y[i], y[i]-l_CH], c=bond_color)
  ax01.plot([x[i], x[i]], [y[i], y[i]+l_CH], c=bond_color)
  ax11.plot([x[i], x[i]], [y[i], y[i]-l_CH], c=bond_color)
  ax11.plot([x[i], x[i]], [y[i], y[i]+l_CH], c=bond_color)
  circle2 = plt.Circle((x[i], y[i]), sig_CH2/2, color='b', fill=False)
  ax01.add_patch(circle2)
#  circle2 = plt.Circle((x[i], y[i]), sig_CH2/2, color='b', fill=False)
#  ax10.add_patch(circle2)
  circle2 = plt.Circle((x[i], y[i]), sig_CH2/2, color='b', fill=False)
  #ax11.add_patch(circle2)
xcom_ = []
ycom_ = []
for i in range(int(len(x)/4)):
  xcom = np.mean(x[i*4:i*4+4])
  ycom = np.mean(y[i*4:i*4+4])
  circle2 = plt.Circle((xcom, ycom), sig_HS/2, facecolor=HS_color, edgecolor=HSbound_color, linewidth=3.2)
  ax11.add_patch(circle2)
  circle2 = plt.Circle((xcom, ycom), sig_HS/2, facecolor=HS_color, edgecolor=HSbound_color, linewidth=3.2)
  ax10.add_patch(circle2)
  xcom_.append(xcom)
  ycom_.append(ycom)
ax10.plot(xcom_, ycom_, color=HSbond_color, linewidth=1)
ax11.plot(xcom_, ycom_, color=HSbond_color, linewidth=1.8)
min_lim = np.ceil(min(min(x), min(y)))
max_lim = np.ceil(max(max(x), max(y)))
#ax.set_xlim(-2.0+min_lim, 2.0+max_lim)
#ax.set_ylim(-2.0+min_lim, 2.0+max_lim)

def emptyAx (ax, lims=1):
  ax.tick_params(axis='both', labelsize=8)
  ax.get_xaxis().set_visible(False)
  ax.get_yaxis().set_visible(False)
  ax.spines.left.set_visible(False)
  ax.spines.right.set_visible(False)
  ax.spines.top.set_visible(False)
  ax.spines.bottom.set_visible(False)
  ax.axis('equal')
  if lims:
    ax.set_xlim(-sig_HS/2+xcom_[0]-0.15,xcom_[1]+sig_HS/2+0.15)
    ax.set_ylim(-0.71-sig_CH2/2,0.71+sig_CH2/2)

emptyAx(ax00)
emptyAx(ax01)
emptyAx(ax10)
emptyAx(ax11)

fig00.subplots_adjust(left=0.00, bottom=0.00, right=1.00, top=1.00, wspace=0.0, hspace=0.0)
fig01.subplots_adjust(left=0.00, bottom=0.00, right=1.00, top=1.00, wspace=0.0, hspace=0.0)
fig10.subplots_adjust(left=0.00, bottom=0.00, right=1.00, top=1.00, wspace=0.0, hspace=0.0)
fig11.subplots_adjust(left=0.00, bottom=0.00, right=1.00, top=1.00, wspace=0.0, hspace=0.0)
fig00.savefig("subfig-AA_PE.pdf")
fig01.savefig("subfig-UA_PE.pdf")
#fig10.savefig("10.pdf")
fig11.savefig("subfig-CG_PE.pdf")
#plt.legend()
#plt.show()

print("ylims:", min(y)-2, max(y)+2, max(y)-min(y)+4, max(y)+min(y))
print("xlims:", min(x)-2, max(x)+2, max(x)-min(x)+0.4, max(x)+min(x))

# repeat but rando
theta_orig = theta
#np.random.seed(999)
#seedo = int(np.random.rand()*999999)
#print(seedo)
#np.random.seed(seedo)
#np.random.seed(673603)
#np.random.seed(506886)
#np.random.seed(24117)
np.random.seed(885167)
#np.random.seed(183567)
#np.random.seed(210121774)
#np.random.seed(2109911990)
x = []
y = []
#z = []

#1
x.append(0.0)
y.append(0.0)
#2
theta_init = np.pi/2/3.29672325179
x.append(l_CC*np.cos(theta_init))
y.append(l_CC*np.sin(theta_init))
#print(x[-1], y[-1])
#3
theta = theta_orig + (np.random.rand()-0.5)*np.pi*0.4
rot = rotateByTheta([x[-2]-x[-1], y[-2]-y[-1]], theta)
x.append(x[-1]+rot[0])
y.append(y[-1]+rot[1])
#4
theta = theta_orig + (np.random.rand()-0.5)*np.pi*0.4
rot = rotateByTheta([x[-2]-x[-1], y[-2]-y[-1]], -theta)
x.append(x[-1]+rot[0])
y.append(y[-1]+rot[1])
#5
theta = theta_orig + (np.random.rand()-0.5)*np.pi*0.4
rot = rotateByTheta([x[-2]-x[-1], y[-2]-y[-1]], theta)
x.append(x[-1]+rot[0])
y.append(y[-1]+rot[1])
#6
theta = theta_orig + (np.random.rand()-0.5)*np.pi*0.4
rot = rotateByTheta([x[-2]-x[-1], y[-2]-y[-1]], -theta)
x.append(x[-1]+rot[0])
y.append(y[-1]+rot[1])
#7
theta = theta_orig + (np.random.rand()-0.5)*np.pi*0.4
rot = rotateByTheta([x[-2]-x[-1], y[-2]-y[-1]], theta)
x.append(x[-1]+rot[0])
y.append(y[-1]+rot[1])
#8
theta = theta_orig + (np.random.rand()-0.5)*np.pi*0.4
rot = rotateByTheta([x[-2]-x[-1], y[-2]-y[-1]], -theta)
x.append(x[-1]+rot[0])
y.append(y[-1]+rot[1])
#9
theta = theta_orig + (np.random.rand()-0.5)*np.pi*0.4
rot = rotateByTheta([x[-2]-x[-1], y[-2]-y[-1]], theta)
x.append(x[-1]+rot[0])
y.append(y[-1]+rot[1])
#10
theta = theta_orig + (np.random.rand()-0.5)*np.pi*0.4
rot = rotateByTheta([x[-2]-x[-1], y[-2]-y[-1]], -theta)
x.append(x[-1]+rot[0])
y.append(y[-1]+rot[1])
#11
theta = theta_orig + (np.random.rand()-0.5)*np.pi*0.4
rot = rotateByTheta([x[-2]-x[-1], y[-2]-y[-1]], theta)
x.append(x[-1]+rot[0])
y.append(y[-1]+rot[1])
#12
theta = theta_orig + (np.random.rand()-0.5)*np.pi*0.4
rot = rotateByTheta([x[-2]-x[-1], y[-2]-y[-1]], -theta)
x.append(x[-1]+rot[0])
y.append(y[-1]+rot[1])
#13
theta = theta_orig + (np.random.rand()-0.5)*np.pi*0.4
rot = rotateByTheta([x[-2]-x[-1], y[-2]-y[-1]], theta)
x.append(x[-1]+rot[0])
y.append(y[-1]+rot[1])
#14
theta = theta_orig + (np.random.rand()-0.5)*np.pi*0.4
rot = rotateByTheta([x[-2]-x[-1], y[-2]-y[-1]], -theta)
x.append(x[-1]+rot[0])
y.append(y[-1]+rot[1])
#15
theta = theta_orig + (np.random.rand()-0.5)*np.pi*0.4
rot = rotateByTheta([x[-2]-x[-1], y[-2]-y[-1]], theta)
x.append(x[-1]+rot[0])
y.append(y[-1]+rot[1])
#16
theta = theta_orig + (np.random.rand()-0.5)*np.pi*0.4
rot = rotateByTheta([x[-2]-x[-1], y[-2]-y[-1]], -theta)
x.append(x[-1]+rot[0])
y.append(y[-1]+rot[1])
#17
theta = theta_orig + (np.random.rand()-0.5)*np.pi*0.4
rot = rotateByTheta([x[-2]-x[-1], y[-2]-y[-1]], theta)
x.append(x[-1]+rot[0])
y.append(y[-1]+rot[1])
#18
theta = theta_orig + (np.random.rand()-0.5)*np.pi*0.4
rot = rotateByTheta([x[-2]-x[-1], y[-2]-y[-1]], -theta)
x.append(x[-1]+rot[0])
y.append(y[-1]+rot[1])
#19
theta = theta_orig + (np.random.rand()-0.5)*np.pi*0.4
rot = rotateByTheta([x[-2]-x[-1], y[-2]-y[-1]], theta)
x.append(x[-1]+rot[0])
y.append(y[-1]+rot[1])
#20
theta = theta_orig + (np.random.rand()-0.5)*np.pi*0.4
rot = rotateByTheta([x[-2]-x[-1], y[-2]-y[-1]], -theta)
x.append(x[-1]+rot[0])
y.append(y[-1]+rot[1])
#21
theta = theta_orig + (np.random.rand()-0.5)*np.pi*0.4
rot = rotateByTheta([x[-2]-x[-1], y[-2]-y[-1]], theta)
x.append(x[-1]+rot[0])
y.append(y[-1]+rot[1])
#22
theta = theta_orig + (np.random.rand()-0.5)*np.pi*0.4
rot = rotateByTheta([x[-2]-x[-1], y[-2]-y[-1]], -theta)
x.append(x[-1]+rot[0])
y.append(y[-1]+rot[1])
#23
theta = theta_orig + (np.random.rand()-0.5)*np.pi*0.4
rot = rotateByTheta([x[-2]-x[-1], y[-2]-y[-1]], theta)
x.append(x[-1]+rot[0])
y.append(y[-1]+rot[1])
#24
theta = theta_orig + (np.random.rand()-0.5)*np.pi*0.4
rot = rotateByTheta([x[-2]-x[-1], y[-2]-y[-1]], -theta)
x.append(x[-1]+rot[0])
y.append(y[-1]+rot[1])
#21
theta = theta_orig + (np.random.rand()-0.5)*np.pi*0.4
rot = rotateByTheta([x[-2]-x[-1], y[-2]-y[-1]], theta)
x.append(x[-1]+rot[0])
y.append(y[-1]+rot[1])
#22
theta = theta_orig + (np.random.rand()-0.5)*np.pi*0.4
rot = rotateByTheta([x[-2]-x[-1], y[-2]-y[-1]], -theta)
x.append(x[-1]+rot[0])
y.append(y[-1]+rot[1])
#23
theta = theta_orig + (np.random.rand()-0.5)*np.pi*0.4
rot = rotateByTheta([x[-2]-x[-1], y[-2]-y[-1]], theta)
x.append(x[-1]+rot[0])
y.append(y[-1]+rot[1])
#28
theta = theta_orig + (np.random.rand()-0.5)*np.pi*0.4
rot = rotateByTheta([x[-2]-x[-1], y[-2]-y[-1]], -theta)
x.append(x[-1]+rot[0])
y.append(y[-1]+rot[1])


#rotate by 60 degs

figsize2 = (2.650, 2.550)
fig, ax = plt.subplots(figsize=figsize2)
ax.plot(x, y, c=bond_color, alpha=0.4)
#for i in range(len(x)):
#  ax.text(x[i],  y[i]     , "("+str(round(x[i], 2))+","+str(round(y[i], 2))+")", horizontalalignment="center", verticalalignment="center", bbox=dict(facecolor="white"))
#  ax.text(x[i],  y[i]     , "C"                                                , fontsize=fontsize, horizontalalignment="center", verticalalignment="center", bbox=dict(boxstyle="circle", facecolor="white", edgecolor="none"))
#  ax.text(x[i],  y[i]-l_CH, "H"                                                , fontsize=fontsize, horizontalalignment="center", verticalalignment="center", bbox=dict(boxstyle="circle", facecolor="white", edgecolor="none"))
#  ax.text(x[i],  y[i]+l_CH, "H"                                                , fontsize=fontsize, horizontalalignment="center", verticalalignment="center", bbox=dict(boxstyle="circle", facecolor="white", edgecolor="none"))
#  ax.plot([x[i], x[i]], [y[i], y[i]-l_CH], c=bond_color)
#  ax.plot([x[i], x[i]], [y[i], y[i]+l_CH], c=bond_color)
#  circle2 = plt.Circle((x[i], y[i]), sig_CH2/2, color='b', fill=False)
#  ax.add_patch(circle2)
xcom_ = []
ycom_ = []
for i in range(int(len(x)/4)):
  xcom = np.mean(x[i*4:i*4+4])
  ycom = np.mean(y[i*4:i*4+4])
  circle2 = plt.Circle((xcom, ycom), sig_HS/2, facecolor=HS_color, edgecolor=HSbound_color, linewidth=3)
  ax.add_patch(circle2)
  xcom_.append(xcom)
  ycom_.append(ycom)
ax.plot(xcom_, ycom_, color=HSbond_color, linewidth=1.5)
min_lim = np.ceil(min(min(x), min(y)))
max_lim = np.ceil(max(max(x), max(y)))
#ax.set_xlim(-2.0+min_lim, 2.0+max_lim)
#ax.set_ylim(-2.0+min_lim, 2.0+max_lim)

emptyAx(ax, lims=0)
fig.subplots_adjust(left=-0.00, bottom=-0.00, right=1.00, top=1.00, wspace=0.0, hspace=0.0)
#plt.legend()
#plt.show()
fig.savefig("subfig-long_CG_PE.pdf")

print(min(y), max(y), max(y)+min(y))
