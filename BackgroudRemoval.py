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

pulsesper = [11,11,11,11,11,10,10,10,10]
xs = np.arange(1,112,1)

df = pd.read_excel('%s.xlsx'%flnm,header=None)

srow = 0

temp_H = []
H_n_avg = np.zeros(111)
H_n = np.zeros(111)

for i in range(0,11):
    srow = 14*i+15330
    erow = srow+14
    pulse = df.iloc[srow:erow]

    for a,b,c in zip(pulse.iloc[7],pulse.iloc[8],pulse.iloc[9]):
        temp_H.append(Hs*sqrt(a**2+b**2+c**2))
    H_n += temp_H
##    plt.plot(xs,temp_H,'--r')
    temp_H = []
H_n_avg = [-1*a/10 for a in H_n]
H_n_avg = np.array(H_n_avg)
##plt.plot(H_n_avg,'g')
##plt.show()

rowi = 14*(istart-1)
rowf = 14*iend
data = df.iloc[rowi:rowf]

j = 0
srow = 0
loc = 0
C_t = np.zeros(111)
H_t = np.zeros(111)
htemp, H_max = [], []

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
            for a,b,c in zip(pulse.iloc[7],pulse.iloc[8],pulse.iloc[9]):
                htemp.append(Hs*sqrt(a**2+b**2+c**2))
            print(len(htemp))
            print(len(H_t))
            print(len(H_n_avg))
            axs[x[loc]][y[loc]].plot(xs,htemp,'-.k',alpha=0.1)

            htemp += H_n_avg
            H_t += htemp
            max_t.append(max(htemp))
            htemp = []
            srow +=14

        max_h.append(np.mean(max_t))
        max_std.append(np.std(max_t,ddof=1)/np.sqrt(len(max_t)))
        
        max_t = []
        C_t = [a/(k) for a in C_t]
        H_t = [a/(k) for a in H_t]
        H_max.append(max(H_t))

        axs[x[loc]][y[loc]].plot(xs,H_t,'--r')
        axs[x[loc]][y[loc]].set_title('Location '+str(loc+1))
        axs[x[loc]][y[loc]].plot(xs,.4*(data.iloc[0]+data.iloc[1]+data.iloc[2]+data.iloc[3]))
        
        C_t = np.zeros(111)
        H_t = np.zeros(111)
        loc += 1
        j+=k

plt.figure(10)
plt.errorbar([1,2,3,4,5,6,7,8,9],max_h,yerr=max_std,capsize=10,fmt='o',markersize=5)
plt.ylim([0,16])
plt.yticks([0,2,4,6,8,10,12,14,16])
##plt.plot(H_max,label='Option 2')
##plt.legend(loc="upper right")
plt.show()
