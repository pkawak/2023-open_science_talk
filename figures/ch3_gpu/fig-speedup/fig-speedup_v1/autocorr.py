#!/usr/bin/env python3

import numpy as np
#import matplotlib
#matplotlib.use('Agg')
import matplotlib.pyplot as plt

np.random.seed(123456)

filename='ESpaced.out' #'Energy_66k_800k.txt' # 'Energy_118k_1m.txt' #
with open("ESpaced.out") as f:
    ncols = len(f.readline().split(','))
Nmca = np.loadtxt(filename, delimiter=' ', skiprows=1, usecols=(0,))
coresp = np.loadtxt(filename, delimiter=' ', skiprows=1, usecols=(1,))
E = np.loadtxt(filename, delimiter=' ', skiprows=1, usecols=(2,))
Npts = len(E) # number of points in the energy file
Nmc = Nmca[0] # number of MC moves per data point in file
Ncut = int(0.5*Npts) # cutoff to drop data that is still relaxing
fullE = E
E = E[Ncut:]
def next_pow_two(n):
    i = 1
    while i < n:
        i = i << 1
    return i

def autocorr_func_1d(x, norm=True):
    x = np.atleast_1d(x)
    if len(x.shape) != 1:
        raise ValueError("invalid dimensions for 1D autocorrelation function")
    n = next_pow_two(len(x))

    # Compute the FFT and then (from that) the auto-correlation function
    f = np.fft.fft(x - np.mean(x), n=2*n)
    acf = np.fft.ifft(f * np.conjugate(f))[:len(x)].real
    acf /= 4*n
    
    # Optionally normalize
    if norm:
        acf /= acf[0]

    return acf

# Automated windowing procedure following Sokal (1989)
def auto_window(taus, c):
    m = np.arange(len(taus)) < c * taus
    if np.any(m):
        return np.argmin(m)
    return len(taus) - 1

# Following the suggestion from Goodman & Weare (2010)
#def autocorr_gw2010(y, c=5.0):
#    f = autocorr_func_1d(np.mean(y, axis=0))
#    taus = 2.0*np.cumsum(f)-1.0
#    window = auto_window(taus, c)
#    return taus[window]

def autocorr_new(y, c=5.0):
    f = np.zeros(len(y))
    f += autocorr_func_1d(y)
    taus = 2.0*np.cumsum(f)-1.0
    window = auto_window(taus, c)
    return taus[window]

# Compute the estimators for a few different chain lengths



theta = autocorr_new(E)
theta_MC = Nmca[int(np.ceil(theta))]
theta_act = coresp[int(np.ceil(theta))]

skip = int(np.ceil(theta_MC/Nmc))
Eforavg = []
for i in range(int(len(E)/skip)):
	Eforavg.append(E[i*skip])
Eforavg = np.asarray(Eforavg)
Emean_ind = np.mean(Eforavg)
#print(Emean_ind)
#tau=Nmc*np.linspace(0,Npts-Ncut-1,Npts-Ncut)              #Establish range of tau values to solve
#tau_max = np.amax(tau,axis=None) # pick the max tau in the range to fit the data (ignore data at large tau with really bad statistics)
#tau_fit = tau[tau<tau_max, np.newaxis] # get only tau < tau_max, need to be a column vector to use in lstsq
#ln_Eavg_plt = -1./theta_MC*tau_fit # the linear fit

plt.subplot(2,1,1)
plt.plot(Nmca, fullE, 'b-', label='Data')                           #Plot the data and the fit
plt.title("Full data file")
plt.xlabel("MC sweeps")
plt.ylabel("E")
plt.subplot(2,1,2)
plt.plot(Nmca[int(0.5*len(Nmca)):], E, label='focus')
plt.title("Used data")
plt.xlabel("MC sweeps")
plt.ylabel("E")


#plt.axvline(x=Nmca[Ncut])
#plt.axvline(x=Nmca[-Ncutend])
#plt.tight_layout()

plt.savefig('Energy_plot.png')                            #Save plot
print("   ")
print('theta in MC step units =',"{:.6e}".format(theta_MC))                   #Display theta value solved for in curve_fit
print(theta_act)
f = open("autocorr_result.out","w+")
f.write("AutoCorrelationTime %f\n" % theta_act)
f.write("R2 0\n")
f.write("Emean %.12f\n" % Emean_ind)
f.write("num_ind_points %d\n" % len(Eforavg))
print("Plot saved as 'Energy_plot.png'")
print("   ")
#plt.show()
