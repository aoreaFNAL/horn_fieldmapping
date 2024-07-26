#Importing all needed modules to run the code
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from math import sqrt

#Asks for the file name
flnm = input("Enter the name of the file you need to analyze.\n")
#Asks for the first pulse of data
istart = int(input("Enter the number of the first pulse of data.\n"))
#Asks for the last pulse of data
iend = int(input("Enter the number of the last pulse of data.\n"))

Cs = 5 #Estimated current scaling factor
Hs = 200#200mT/V or 1T/5V #Estimated magnetic field scaling factor
iC = 200 #Ideal current of 200kA

#pulsesper = [11,11,11,11,11,10,10,10,10] #Pre-Capacitor Plane 1
#pulsesper = [10,10,11,11,11,11,11,11,11] #Post-Capacitor Plane 1
#pulsesper = [10,10,11,11,11,11,11,11,11] #Post-Capacitor Plane 2
#pulsesper = [11,11,11,11,11,11,11,11,11] #Post-Capacitor Plane 3
pulsesper = [11,11,11,11,11,11,10,11,11] #Post-Capacitor Plane 4
xs = np.arange(1,112,1)

df = pd.read_excel('%s.xlsx'%flnm,header=None)

rowi = 14*(istart-1)
rowf = 14*iend
data = df.iloc[rowi:rowf] #Defines the data we want to focus on

j = 0
srow = 0
loc = 0
C_t = np.zeros(111)
H_t = np.zeros(111)
htemp, H_max = [], [] 
max_t, max_h, max_std = [], [], []#Initializing all of the arrays

print(str(len(data)/14)+" pulses counted\n")

fig,axs = plt.subplots(3,3,sharex=True,sharey=True)#Sharing x and y axes on the plots
x = [0,0,0,1,1,1,2,2,2]
y = [0,1,2,0,1,2,0,1,2] #Indicies for the subplot placements on the subplot figure
axs[0][0].set_xlim([0,111])
axs[0][0].set_ylim([0,28])#Setting the bounds to match with all the data

while j < len(data)/14:
    for k in pulsesper:
        for l in range(0,k):
            erow = srow+14 #Each pulse is 14 lines
            pulse = data.iloc[srow:erow] #Narrows out the data pulse by pulse
            C_t += Cs*(pulse.iloc[0]+pulse.iloc[1]+pulse.iloc[2]+pulse.iloc[3])
            for a,b,c in zip(pulse.iloc[7],pulse.iloc[8],pulse.iloc[9]):
                htemp.append(Hs*sqrt(a**2+b**2+c**2)) #Calculates the array of magnetic field magnitudes

            axs[x[loc]][y[loc]].plot(xs,htemp,'-.k',alpha=0.1) #Plots each individual set of data (usually 10 per location)
            
            H_t += htemp #Adding up each data array to average out later on with a red line
            max_t.append(max(htemp)) #Taking the max over the entire individual data array
            ind = np.argmax(htemp) #Finds the index of where the max is

            axs[x[loc]][y[loc]].plot(ind,max(htemp),'*r',alpha=0.2)  #Plotting the max with a red star
            
            htemp = []
            srow +=14 #Moving on to the next pulse

        max_h.append(np.mean(max_t)) #Making the arrays of maxes per location
        max_std.append(np.std(max_t,ddof=1)/np.sqrt(len(max_t))) #Making the arrays of standard errors per corresponding max
        
        max_t = []
        C_t = [a/(k) for a in C_t]
        H_t = [a/(k) for a in H_t] #Could use the 'mean' function instead, but this was done before I learned about using axis arguments
        H_max.append(max(H_t))

        axs[x[loc]][y[loc]].plot(xs,H_t,'--r')
        axs[x[loc]][y[loc]].set_title('Location '+str(loc+1))
        axs[x[loc]][y[loc]].plot(xs,.4*(data.iloc[0]+data.iloc[1]+data.iloc[2]+data.iloc[3])) #plotting the current pulse for reference
        
        C_t = np.zeros(111)
        H_t = np.zeros(111) #Resetting the arrays to zero. C_t isn't used, but it doesn't hurt to calulate
        loc += 1
        j+=k

plt.figure(10)
plt.errorbar([1,2,3,4,5,6,7,8,9],max_h,yerr=max_std,capsize=10,fmt='o',markersize=5)
plt.ylim([0,16])
plt.yticks([0,2,4,6,8,10,12,14,16])
plt.xlabel('Location')
plt.ylabel('Magnetic Field (mT)')
plt.show()
