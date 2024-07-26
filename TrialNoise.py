#Importing all needed modules to run the code
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from math import sqrt
from scipy.optimize import minimize
from scipy.interpolate import make_interp_spline
import time
start_time = time.time()

#Asks for the file name
flnm = input("Enter the name of the file you need to analyze.\n")
#Asks for the first pulse of data
istart = int(input("Enter the number of the first pulse of data.\n"))
#Asks for the last pulse of data
iend = int(input("Enter the number of the last pulse of data.\n"))

Cs = 5 #Estimated current scaling factor
Hs = 200#2V/T #Estimated magnetic field scaling factor

xs = np.arange(1,112,1)

df = pd.read_excel('%s.xlsx'%flnm,header=None)

rowi = 14*(istart-1)
rowf = 14*iend
data = df.iloc[rowi:rowf]

j = 0
srow = 0
C_t = np.zeros(111)
H_t = np.zeros(111)
tmp = np.zeros(111)

htemp = []

delay = 0

print(str(len(data)/14)+" pulses detected\n")

fig,axs = plt.subplots(2,2,sharex=True,sharey=True)
axs[0][0].set_xlim([0,111])
axs[0][0].set_ylim([0,28])

background = df.iloc[14*(51-1):14*100]
for i in range(0,50):
    erow = srow+14
    pulse = background.iloc[srow:erow]

    for a,b,c in zip(pulse.iloc[7],pulse.iloc[8],pulse.iloc[9]):
        htemp.append(Hs*sqrt(a**2+b**2+c**2))

    axs[0][0].plot(xs,htemp,'m')
    axs[0][1].plot(xs,htemp,'m')
    axs[1][0].plot(xs,htemp,'m')
    axs[1][1].plot(xs,htemp,'m')
    
    htemp = []
    srow +=14

srow = 0
tmp = np.zeros(111)
for i in range(0,10):
    erow = srow+14
    pulse = data.iloc[srow:erow]

    C_t += Cs*(pulse.iloc[0]+pulse.iloc[1]+pulse.iloc[2]+pulse.iloc[3])
    ind = np.argmax(pulse.iloc[0]+pulse.iloc[1]+pulse.iloc[2]+pulse.iloc[3])+delay
    
    for a,b,c in zip(pulse.iloc[7],pulse.iloc[8],pulse.iloc[9]):
        htemp.append(Hs*sqrt(a**2+b**2+c**2))

    tmp = np.vstack([tmp,htemp])
    
    axs[0][0].plot(xs,htemp,'-.k',alpha=0.1)
    axs[0][0].plot(ind,htemp[ind],'*r',alpha=0.2)
    
    htemp = []
    srow +=14

    C_t = np.zeros(111)
    H_t = np.zeros(111)

tmp = np.delete(tmp,0,0)
means = tmp.mean(axis=0)
stds = tmp.std(axis=0, ddof=1)
axs[0][0].set_title('10 Iterations')
axs[0][0].plot(xs,means,'--r')
axs[0][0].fill_between(xs,means-stds,means+stds,alpha=0.5)
axs[0][0].plot(xs,.4*(data.iloc[0]+data.iloc[1]+data.iloc[2]+data.iloc[3]))\

srow = 0
tmp = np.zeros(111)
for i in range(0,25):
    erow = srow+14
    pulse = data.iloc[srow:erow]

    C_t += Cs*(pulse.iloc[0]+pulse.iloc[1]+pulse.iloc[2]+pulse.iloc[3])
    ind = np.argmax(pulse.iloc[0]+pulse.iloc[1]+pulse.iloc[2]+pulse.iloc[3])+delay
    
    for a,b,c in zip(pulse.iloc[7],pulse.iloc[8],pulse.iloc[9]):
        htemp.append(Hs*sqrt(a**2+b**2+c**2))

    tmp = np.vstack([tmp,htemp])
    
    axs[0][1].plot(xs,htemp,'-.k',alpha=0.1)
    axs[0][1].plot(ind,htemp[ind],'*r',alpha=0.2)
    
    htemp = []
    srow +=14

    C_t = np.zeros(111)
    H_t = np.zeros(111)

tmp = np.delete(tmp,0,0)
means = tmp.mean(axis=0)
stds = tmp.std(axis=0, ddof=1)
axs[0][1].set_title('25 Iterations')
axs[0][1].plot(xs,means,'--r')
axs[0][1].fill_between(xs,means-stds,means+stds,alpha=0.5)
axs[0][1].plot(xs,.4*(data.iloc[0]+data.iloc[1]+data.iloc[2]+data.iloc[3]))

srow = 0
tmp = np.zeros(111)
for i in range(0,50):
    erow = srow+14
    pulse = data.iloc[srow:erow]

    C_t += Cs*(pulse.iloc[0]+pulse.iloc[1]+pulse.iloc[2]+pulse.iloc[3])
    ind = np.argmax(pulse.iloc[0]+pulse.iloc[1]+pulse.iloc[2]+pulse.iloc[3])+delay
    
    for a,b,c in zip(pulse.iloc[7],pulse.iloc[8],pulse.iloc[9]):
        htemp.append(Hs*sqrt(a**2+b**2+c**2))

    tmp = np.vstack([tmp,htemp])
    
    axs[1][0].plot(xs,htemp,'-.k',alpha=0.1)
    axs[1][0].plot(ind,htemp[ind],'*r',alpha=0.2)
    
    htemp = []
    srow +=14

    C_t = np.zeros(111)
    H_t = np.zeros(111)

tmp = np.delete(tmp,0,0)
means = tmp.mean(axis=0)
stds = tmp.std(axis=0, ddof=1)
axs[1][0].set_title('50 Iterations')
axs[1][0].plot(xs,means,'--r')
axs[1][0].fill_between(xs,means-stds,means+stds,alpha=0.5)
axs[1][0].plot(xs,.4*(data.iloc[0]+data.iloc[1]+data.iloc[2]+data.iloc[3]))

srow = 0
tmp = np.zeros(111)
for i in range(0,100):
    erow = srow+14
    pulse = data.iloc[srow:erow]

    C_t += Cs*(pulse.iloc[0]+pulse.iloc[1]+pulse.iloc[2]+pulse.iloc[3])
    ind = np.argmax(pulse.iloc[0]+pulse.iloc[1]+pulse.iloc[2]+pulse.iloc[3])+delay
    
    for a,b,c in zip(pulse.iloc[7],pulse.iloc[8],pulse.iloc[9]):
        htemp.append(Hs*sqrt(a**2+b**2+c**2))

    tmp = np.vstack([tmp,htemp])
    
    axs[1][1].plot(xs,htemp,'-.k',alpha=0.1)
    axs[1][1].plot(ind,htemp[ind],'*r',alpha=0.2)
    
    htemp = []
    srow +=14

    C_t = np.zeros(111)
    H_t = np.zeros(111)

tmp = np.delete(tmp,0,0)
means = tmp.mean(axis=0)
stds = tmp.std(axis=0, ddof=1)
axs[1][1].set_title('100 Iterations')
axs[1][1].plot(xs,means,'--r')
axs[1][1].fill_between(xs,means-stds,means+stds,alpha=0.5)
axs[1][1].plot(xs,.4*(data.iloc[0]+data.iloc[1]+data.iloc[2]+data.iloc[3]))

plt.show()
