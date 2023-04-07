#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 29 17:32:10 2019

@author: pierrekawak
"""
#--------------------------------------------
#THIS FILE PLOTS COMMON THERMODYNAMIC DISTROS GIVEN A PARAMS.DAT FILE AND A LNG.OUT FILE
#IT ALSO OUTPUTS THE CANONICAL DISTRO AND THE POTENTIAL ENERGY AT GIVEN TEMPERATURE RANGE
#--------------------------------------------
import numpy as np
import matplotlib.pyplot as plt
import os
import sys
#peakTs = np.array([ i for i, f in zip(peakTs, filter_ids) if f == 1 ])
#peaks = np.array([ i for i, f in zip(peaks[0], filter_ids) if f == 1 ])
#peakUs = np.array([ i for i, f in zip(peakUs, filter_ids) if f == 1 ])
#peak_strength = np.array([ i for i, f in zip(peak_strength, filter_ids) if f == 1 ])
#idx = np.argsort(peak_strength)
#peakTs = peakTs[idx]
#peakUs = peakUs[idx]
#peak_strength = peak_strength[idx]
#[ print(t, p, u)  for t,p,u in zip(peakTs, peak_strength, peakUs) ]
#conc = np.c_[T, U, C]
#for i in range(op_num):
#  conc = np.c_[conc, op[i]]
#np.savetxt(

data = np.loadtxt('ext_canon_distro.out')
T = data[:,0]
U = data[:,1]
C = data[:,2]
Q6 = data[:,3]
P2 = data[:,4]
n6 = data[:,5]
R2e = data[:,6]
R2g = data[:,7]
SMS = data[:,8]
#op_name = [r"$Q_{6}$", r"$P_{2}$", r"$n_{Q_{6}}$", r"$R^{2}_{e}$", r"$R^{2}_{g}$", r"$S_{MS}$" ]
#op = np.array([Q6,P2,n6,R2e,R2g,SMS])
op_name = [r"$P_{2}$", r"$n_{Q_{6}}$"]
op = np.array([P2,n6])
op_num = len(op)
plt.rcParams['font.size'] = '11'
peakTs = []
with open("Ts.real.out") as f:
  lines=f.readlines()
  peakTs.append(float(lines[1].split(' ')[0]))
  peakTs.append(float(lines[2].split(' ')[0]))
peakLocs = []
peakLocs.append(np.abs(T - peakTs[0]).argmin())
peakLocs.append(np.abs(T - peakTs[1]).argmin())
howmany_peaks_label = min(5, len(peakTs))
h = 200
w = 390*0.6
pt = 1/72
fig = plt.figure(figsize=(w*pt, h*pt), constrained_layout=True)

ax1 = plt.subplot()
#ax1.set_ylabel(op_name[0], rotation=0, labelpad=10)
l1 = ax1.plot(T, op[0], label=op_name[0])
l2 = ax1.plot(T, op[1], label=op_name[1])

peakOp = []
peakNames = [r"$T_{C}$",r"$T_{IN}$"]
for i in range(howmany_peaks_label):
  peakOp.append(np.array(op[0])[peakLocs[i]].astype('float64'))
#  ax1.vlines(peakTs[i], 0, peakOp[i], linestyles='dashed', color='k')
  ax1.vlines(peakTs[i], 0, 1, linestyles='dashed', color='k')
  ax1.text(peakTs[i], -0.1, peakNames[i])
#print(peakTs

lowT = 0.00
highT = 0.25
ax1.set_xlim(lowT, highT)
ax1.set_ylim(-0.001,1.)
ax1.set_xlabel(r"$T$")
ax1.set_xticks([])
ax1.set_yticks([])

#from PIL import Image
#import fitz
#import io
##im = Image.open("cryst.pdf")
#pdf_file = fitz.open("cryst.pdf")
## in case there is a need to loop through multiple PDF pages
#for page_number in range(len(pdf_file)):
#    page = pdf_file[page_number]
#    rgb = page.get_pixmap()
#    pil_image = Image.open(io.BytesIO(rgb.tobytes()))
#
    # display code or image manipulation here for each page #
#im = plt.imread("cryst.pdf")
#height = im.size[1]
#im = np.array(im).astype(np.float) / 255
#fig.figimage(im, 0, fig.bbox.ymax, dpi=80)
#ax1.imshow(pil_image.convert('RGB'))

plt.legend()
#plt.subplots_adjust(left=0.2, bottom=0.08, right=0.95, top=0.97, wspace=None, hspace=None)
plt.savefig("subfig-soft_WLMC_P2_Q6.pdf")
