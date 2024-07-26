#Should be the code to use for analysis since it gives the best visuals

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
iC = 200 #Ideal current of 200kA

#pulsesper = [11,11,11,11,11,10,10,10,10] #Pre-Capacitor Plane 1
pulsesper = [10,10,11,11,11,11,11,11,11] #Post-Capacitor Plane 1
#pulsesper = [10,10,11,11,11,11,11,11,11] #Post-Capacitor Plane 2
#pulsesper = [11,11,11,11,11,11,11,11,11] #Post-Capacitor Plane 3
pulsesper = [11,11,11,11,11,11,10,11,11] #Post-Capacitor Plane 4
xs = np.arange(1,112,1)

df = pd.read_excel('%s.xlsx'%flnm,header=None)

rowi = 14*(istart-1)
rowf = 14*iend
data = df.iloc[rowi:rowf]

j = 0
srow = 0
loc = 0
C_t = np.zeros(111)
H_t = np.zeros(111)
tmp = np.zeros(111)

htemp, H_max = [], []

inds = []
delay = 0

max_t, max_h, max_std = [], [], []
print(str(len(data)/14)+" pulses detected\n")

fig,axs = plt.subplots(3,3,sharex=True,sharey=True)
x = [0,0,0,1,1,1,2,2,2]
y = [0,1,2,0,1,2,0,1,2]
axs[0][0].set_xlim([0,111])
axs[0][0].set_ylim([0,28])

while j < len(data)/14:
    for k in pulsesper:
        for l in range(0,k):
            erow = srow+14
            pulse = data.iloc[srow:erow]
            C_t += Cs*(pulse.iloc[0]+pulse.iloc[1]+pulse.iloc[2]+pulse.iloc[3])

            c = max(pulse.iloc[0]+pulse.iloc[1]+pulse.iloc[2]+pulse.iloc[3])
            ind = np.argmax(pulse.iloc[0]+pulse.iloc[1]+pulse.iloc[2]+pulse.iloc[3])+delay
            inds.append(ind)
            
            for a,b,c in zip(pulse.iloc[7],pulse.iloc[8],pulse.iloc[9]):
                htemp.append(Hs*sqrt(a**2+b**2+c**2))

            tmp = np.vstack([tmp,htemp])
            
            axs[x[loc]][y[loc]].plot(xs,htemp,'-.k',alpha=0.1)
            axs[x[loc]][y[loc]].plot(ind,htemp[ind],'*r',alpha=0.2)
            
            H_t += htemp
            max_t.append(htemp[ind])
            htemp = []
            srow +=14

        max_h.append(np.mean(max_t))
        max_std.append(np.std(max_t,ddof=1)/np.sqrt(len(max_t)))

        tmp = np.delete(tmp,0,0)
        means = tmp.mean(axis=0)
        stds = tmp.std(axis=0, ddof=1)
        axs[x[loc]][y[loc]].plot(xs,means,'--r')
        axs[x[loc]][y[loc]].fill_between(xs,means-stds,means+stds,alpha=0.5)
            
        max_t = []
##        C_t = [a/(k) for a in C_t]
        H_t = tmp.mean(axis=0)
        H_max.append(max(H_t))

##        axs[x[loc]][y[loc]].plot(xs,H_t,'--r')
        axs[x[loc]][y[loc]].set_title('Location '+str(loc+1))
        axs[x[loc]][y[loc]].plot(xs,.4*(data.iloc[0]+data.iloc[1]+data.iloc[2]+data.iloc[3]))

        tmp = np.zeros(111)
        C_t = np.zeros(111)
        H_t = np.zeros(111)
        loc += 1
        j+=k

plt.figure(10)
plt.errorbar([1,2,3,4,5,6,7,8,9],max_h,yerr=max_std,capsize=10,fmt='o',markersize=5)
plt.ylim([0,16])
plt.yticks([0,2,4,6,8,10,12,14,16])
plt.xlabel('Location')
plt.ylabel('Magnetic Field (mT)')
##plt.plot(H_max,label='Option 2')
##plt.legend(loc="upper right")
plt.show()
