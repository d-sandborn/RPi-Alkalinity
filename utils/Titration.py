# -*- coding: utf-8 -*-
"""
RPi Alkalinity
Version: v0.6 Beta
Licensed under {License info} for general use with attribution.
For works using this code please cite:
    Sandborn, D.E., Minor E.C., Hill, C. (2021)
"""

import numpy as np
import pandas as pd
import time
import os
from pathlib import Path
import calkulate as calk
import sys
import matplotlib.pyplot as plt
from utils.admin import countdown

#Instruments
from utils.Get_MCC128 import get_mV
from utils.Get_DS18B20 import get_temp
from utils.manual_input import mass_input, salinity_input, digit_input

def mV_to_pH(mV, Eo, TC = 25.0):
    pH = -1*np.log10(np.exp((mV/1000-Eo)*96485.33212/8.3144621/(TC+273.15)))
    return pH

def pH_to_mV(pH, Eo, TC = 25.0):
    mV = (np.log(10**-pH)*8.3144621*298.15/96485.33212+Eo)*1000
    return mV

class RunTitration:
    def __init__(self):
        mass = mass_input()
        self.mass = mass
        SampleID = input("Sample ID? --> ")
        self.SampleID = SampleID
        salinity = salinity_input()
        self.salinity = salinity
        table = pd.DataFrame(
            {"Vol" : [],
             "mV" : [],
             "TC" : []})
        self.datasheet = table
        
    def Analyze(self): #Humphreys, M. P. and Matthews, R. S. (2020). Calkulate: total alkalinity from titration data in Python. Zenodo. doi:10.5281/zenodo.2634304.
        data = calk.read_csv(Path(os.getcwd()+"/data/Alkalinity_Meta.csv"))
        data.solve()
        return data
    
    def Titrate(self):
        """
        Text-based user interface for alkalinity titration using temperature
        and pH (EMF) probes on a Raspberry Pi-based DAQ system.  
        A Hach digital titrator is implemented in the present design, which 
        outputs "Digits" = mL*800.  
        
        Three titration phases occur:
            1) System setup.  Instruments are inserted into reaction system and temperature should stabilize.
            2) Titration to pH 3.8.  Acid is added until the sample pH is < 3.6.
            3) Titration to pH 3.  Acid is added in small intervals until the sample pH is < 3.  
    
        Returns
        -------
        titrant_concentration : float
            Molinity of HCl titrant.  
        datasheet : Pandas dataframe
            Three columns: Vol, mV, and TC.

        """
        system = pd.read_csv(Path(os.getcwd()+"/utils/System_Info.csv"))
        Eo = system['probe_Eo'][0]
        titrant_concentration = system['titrant_HCl_molinity'][0]
        print("Please ensure that pH probe and thermistor\nare submersed, temperature is stable, and stir bar is spinning at max speed.")
        input("Press Enter to continue.")
        mV = get_mV()
        TC = get_temp()
        datasheet = pd.DataFrame( #needs 2-row buffer for Calkulate: one row of column labels, another of 0s
            {"Vol" : [0],
             "mV" : [0],
             "TC" : [0]})
        print("Initial Temperature: ", TC, "°C")
        print("Initial Voltage: ", mV, "mV")
        print("Initial pH: ", np.round(mV_to_pH(mV, Eo, TC),3))
        print("Add acid with digital titrator until pH is less than 3.8.")
        sigmas = np.array([0,0,0,0,0,0,0,0])
        while mV < pH_to_mV(3.8, Eo, TC): 
            mV = get_mV(boxcarnum = 100) #more frequent readings, not saved
            TC = get_temp()
            sigmas = np.delete(sigmas, [0])
            sigmas = np.append(sigmas, mV_to_pH(mV, Eo, TC))
            sys.stdout.write('\r'+"pH: "+ str(np.round(mV_to_pH(mV, Eo, TC),3))+"T (°C): " + str(np.round(TC,2)) + "pH σ: " + str(np.round(sigmas.std(), 4)))
        print("\nStop titration.")
        print("System accepts titrator readings in Digits = mL*800.")
        digits = digit_input()        
        print("Continue stirring for 6 minutes for degassing.")
        countdown(6)
        input("Degassing completed.  Press Enter to continue. -->")
        mV = get_mV()
        TC = get_temp()
        newrow = pd.DataFrame(
            {"Vol" : [digits/800], #digits/800 = mL titrant
             "mV" : [mV],
             "TC" : [TC]})
        datasheet = datasheet.append(newrow)
        print("\nResume titration.  Add acid every time you are prompted until pH = 3.")
        print("If an error is made, continue with the titration.\nCorrections can be made manually to the .txt file. /nMinimize vibration during titration phase!")
        while mV < pH_to_mV(3, Eo, TC):
            digits = digit_input()
            time.sleep(5)
            mV = get_mV()
            TC = get_temp()
            newrow = pd.DataFrame(
                {"Vol" : [digits/800], #digits/800 = mL titrant
                 "mV" : [mV],
                 "TC" : [TC]})
            datasheet = datasheet.append(newrow)
            print("Present pH: ", np.round(mV_to_pH(mV, Eo, TC),3))
        print("Titration Completed.")
        return titrant_concentration, datasheet