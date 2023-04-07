#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 18 17:32:10 2021

@author: pierrekawak
"""
import numpy as np
import matplotlib.pyplot as plt

data = np.loadtxt("heights_phi.out")
names = data[:, 0]
start = data[:, 1]
heights = data[:, 2]
end = data[:, 3]

fig, ax = plt.subplots(figsize=(3.25,2.5))
ax.scatter(names, heights-start, marker='*', label='Forward')
ax.scatter(names, heights-end, marker='o', facecolors='none', edgecolors='r', label='Reverse')
ax.set_yscale('log')
ax.set_xlabel(r"$\phi$", fontsize=10, labelpad=6)
ax.set_ylabel(r"$\Delta F^{\dagger}/\epsilon$", fontsize=10, labelpad=5)
ax.tick_params(axis='both', which='major', labelsize=10)
plt.subplots_adjust(left=0.21, bottom=0.19, right=0.99, top=0.99)
ax.legend(loc='best')
fig.savefig("fig-heights_vs_phi.pdf")

##
#from sklearn.linear_model import LinearRegression
#from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
#import statsmodels.api as sm
#
#x = names
#y = heights-start
#logy = np.log(y)
#model = LinearRegression()
#x= x.reshape(-1, 1)
#logy= logy.reshape(-1, 1)
#model.fit(x, logy)
#print("log-linear fit for Forward barrier")
#print("y = Ca**x")
#print("ln(C)/C:", model.intercept_, np.exp(model.intercept_))
#print("ln(a)/a:", model.coef_, np.exp(model.coef_))
#print("R2:", model.score(x, logy))
##for y = c*a**x
#c = np.exp(model.intercept_)
#a = np.exp(model.coef_)
##fig, ax = plt.subplots()
##ax.scatter(x, y)
##ax.plot(x, c*a**x)
##plt.show()
##plt.close()
#
#x = names
#y = heights-end
#logy = np.log(y)
#model = LinearRegression()
#x= x.reshape(-1, 1)
#logy= logy.reshape(-1, 1)
#model.fit(x, logy)
#print("log-linear fit for Reverse barrier")
#print("y = Ca**x")
#print("ln(C)/C:", model.intercept_, np.exp(model.intercept_))
#print("ln(a)/a:", model.coef_, np.exp(model.coef_))
#print("R2:", model.score(x, logy))
##for y = c*a**x
#c = np.exp(model.intercept_)
#a = np.exp(model.coef_)
##fig, ax = plt.subplots()
##ax.scatter(x, y)
##ax.plot(x, c*a**x)
##plt.show()
##plt.close()
#
#x = np.concatenate((names, names))
#y = np.concatenate((heights-start, heights-end))
#logy = np.log(y)
#model = LinearRegression()
#x= x.reshape(-1, 1)
#logy= logy.reshape(-1, 1)
#model.fit(x, logy)
#print("log-linear fit for Average barrier")
#print("y = Ca**x")
#print("ln(C)/C:", model.intercept_, np.exp(model.intercept_))
#print("ln(a)/a:", model.coef_, np.exp(model.coef_))
#print("R2:", model.score(x, logy))
##for y = c*a**x
#c = np.exp(model.intercept_)
#a = np.exp(model.coef_)
#fig, ax = plt.subplots()
#ax.scatter(x, y)
#ax.plot(x, c*a**x)
#plt.show()
#plt.close()
