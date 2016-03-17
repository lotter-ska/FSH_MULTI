# -*- coding: utf-8 -*-
"""
Created on Wed Mar 09 07:22:51 2016

@author: lkock

FSH Data Processing
"""
#from Tkinter import Tk
from Tkinter import *
from tkFileDialog import askopenfilename
import numpy as np
import matplotlib.pyplot as plt
import time


def convert(dut,antennaF,lna):
#    dut="/FSH Data/20160309_GEO_Equipment/asuslaptop.csv"
    data= np.genfromtxt(dut,delimiter=',',dtype=None)
    freq=(data[45:-1,0]).astype(np.float)
    dbm=(data[45:-1,1]).astype(np.float)
    dbuV=dbm+107
    
#    antennaF="/RFI Archive/Equipment_Database/Passive_Antennas/Antenna_MESA_KLPDA1.csv"
    af=np.genfromtxt(antennaF,delimiter=',',dtype=None)
    f=(af[2:-1,0]).astype(np.float)
    af1=(af[2:-1,3]).astype(np.float)
    af2=np.interp(freq,f,af1)
#    calc e field
    g=np.genfromtxt(lna,delimiter=',',dtype=None)
    ff=(g[3:-1,0]).astype(np.float)   
    gg=(g[3:-1,1]).astype(np.float)
    gg1=np.interp(freq,ff,gg)
    
    
    dbuV_m=dbuV+af2-gg1
    return freq, dbuV_m



def on_off(on,off,labels):
    f1, e1=convert(on,filename,filename_lna)
    f2, e2=convert(off,filename,filename_lna)
    plt.figure()    
    plt.plot(f1,e1,label="DUT On")
    plt.plot(f2,e2,label="DUT Off")
    plt.legend()
    plt.grid()
    plt.xlabel("frequency [Hz]")
    plt.ylabel("E Field [dBuV/m]")
    plt.title(labels)
    plt.savefig(labels)


print('=====================================================')
q = input("How many measurements to be processed and plotted? ")

Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
filename_ant = askopenfilename(title="Select Antenna Cal File") # show an "Open" dialog box and return the path to the selected file
filename_lna = askopenfilename(title="Select LNA Cal File")
fig = plt.figure(figsize=(18.8,9.8))
for x in range(q):
    txt="Select measurement %s" % str(x+1)
    filename = askopenfilename(title=txt)
    f1, e1=convert(filename,filename_ant,filename_lna)   
    plt.plot(f1,e1,label=filename)


plt.legend()
plt.grid()
plt.xlabel("frequency [Hz]")
plt.ylabel("E Field [dBuV/m]")
plt.title("Comparison of Measurements")  #change title here if required
flnm=time.strftime("%Y%m%d")+"_Measurements"
plt.savefig(flnm,dpi=100)






