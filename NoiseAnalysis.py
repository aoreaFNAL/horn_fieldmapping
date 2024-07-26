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

Cs = 0.15#5 #Estimated current scaling factor
Hs = 200#2V/T #Estimated magnetic field scaling factor

xs = np.arange(1,112,1)

df = pd.read_excel('%s.xlsx'%flnm,header=None)

C_n = np.zeros(111)
H_n = np.zeros(111)
temp_H = []

C_d = np.zeros(111)
H_d = np.zeros(111)

for i in range(0,11):
    srow = 14*i+15330
    erow = srow+14
    pulse = df.iloc[srow:erow]
    C_n = Cs*pulse.iloc[0]+pulse.iloc[1]+pulse.iloc[2]+pulse.iloc[3]

    for a,b,c in zip(pulse.iloc[7],pulse.iloc[8],pulse.iloc[9]):
        temp_H.append(Hs*sqrt(a**2+b**2+c**2))
    H_n = temp_H

    plt.plot(xs,C_n,'-b')
    plt.plot(xs,H_n,'-r')
    C_n = np.zeros(111)
    H_n = np.zeros(111)
    temp_H = []

for i in range(0,10):
    srow = 14*i+13986
    erow = srow+14
    pulse = df.iloc[srow:erow]
    C_d = Cs*pulse.iloc[0]+pulse.iloc[1]+pulse.iloc[2]+pulse.iloc[3]

    for a,b,c in zip(pulse.iloc[7],pulse.iloc[8],pulse.iloc[9]):
        temp_H.append(Hs*sqrt(a**2+b**2+c**2))
    H_d = temp_H

    plt.plot(xs,.4*C_d,'k')
    plt.plot(xs,H_d,'g')
    C_d = np.zeros(111)
    H_d = np.zeros(111)
    temp_H = []

plt.ylim([0,28])        
plt.show()

##x_max, y_max, z_max = [], [], []
##
##Hs = 0.2
##for i in range(0,int((len(df)/14))):
##    srow = 14*i
##    erow = srow+14
##    pulse = df.iloc[srow:erow]
##
##    x_max.append(Hs*max(abs(pulse.iloc[7])))
##    y_max.append(Hs*max(abs(pulse.iloc[8])))
##    z_max.append(Hs*max(abs(pulse.iloc[9])))
##
##fig, axs = plt.subplots(3,sharex=True)
##axs[0].plot(x_max,'r')
##axs[0].set_title(r'$H_{x}$')
##axs[0].set_xlim([0,1105])
##axs[0].set_xticks([0,100,200,300,400,500,600,700,800,900,1000,1105,956,1050])
##axs[0].set_ylim([.001,0.011])
##axs[0].set_yticks([0.001,0.002,0.003,0.004,0.005,0.006,0.007,0.008,0.009,0.010,0.011])
##
##axs[1].plot(y_max,'y')
##axs[1].set_title(r'$H_{y}$')
##axs[1].set_ylim([.002,0.018])
##axs[1].set_yticks([0.002,0.004,0.006,0.008,0.010,0.012,0.014,0.016,0.018])
##
##axs[2].plot(z_max,'g')
##axs[2].set_title(r'$H_{z}$')
##axs[2].set_ylim([.002,0.018])
##axs[2].set_yticks([0.002,0.004,0.006,0.008,0.010,0.012,0.014,0.016,0.018])
##plt.show()
