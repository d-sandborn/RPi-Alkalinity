# -*- coding: utf-8 -*-
"""
RPi Alkalinity
Version: v0.3 (Pre-alpha)
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

#Instruments
from utils.Get_MCC128 import get_mV
from utils.Get_DS18B20 import get_temp
from utils.manual_input import mass_input, salinity_input, digit_input
from utils.plotting import gran_plot

def mV_to_pH(mV, Eo, TC = 25.0):
    pH = -1*np.log10(np.exp((mV/1000-Eo)*96485/8.3144621/(TC+273.15)))
    return pH

def pH_to_mV(pH, Eo, TC = 25.0):
    mV = (np.log(10**-pH)*8.3144621*298.15/96485+Eo)*1000
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
            2) Titration to pH 3.6.  Acid is added until the sample pH is < 3.6.
            3) Titration to pH 3.  Acid is added in small intervals until the sample pH is < 3.  
    
        Returns
        -------
        titrant_concentration : float
            Obsolete.  Molinity of HCl titrant.  
        datasheet : Pandas dataframe
            Three columns: Digits, EMF, and Temperature C.  Digits are equal to mL*800 as a result of the Hach digital titrator design.  

        """
        system = pd.read_csv(Path(os.getcwd()+"/utils/System_Info.csv"))
        Eo = system['probe_Eo'][0]
        titrant_concentration = system['titrant_HCl_molinity'][0]
        print("Starting titration.  Please ensure that pH probe and thermistor\nare submersed, temperature is stable, and stir bar is spinning.")
        input("Press any key to continue.")
        mV = get_mV()
        TC = get_temp()
        datasheet = pd.DataFrame( #needs 2-row buffer for Calkulate: one row of column labels, another of 0s
            {"Vol" : [0, 0],
             "mV" : [0, mV],
             "TC" : [0, TC]})
        print("Initial Temperature: ", TC, "°C")
        print("Initial Voltage: ", mV, "mV")
        print("Approx. Initial pH: ", np.round(mV_to_pH(mV, Eo, TC),3))
        print("Add acid with digital titrator until pH is less than 3.7.")
        while mV < pH_to_mV(3.7, Eo, TC): 
            #time.sleep(1) 
            mV = get_mV(boxcarnum = 100) #more frequent readings, not saved
            TC = get_temp()
            sys.stdout.write('\r'+"Present pH: "+ str(np.round(mV_to_pH(mV, Eo, TC),3)))
        print("\nStop titration.")
        mV = get_mV()
        TC = get_temp()
        print("System accepts titrator readings in Digits = mL*800.")
        digits = digit_input()
        newrow = pd.DataFrame(
            {"Vol" : [digits/800], #digits/800 = mL titrant
             "mV" : [mV],
             "TC" : [TC]})
        datasheet = datasheet.append(newrow)
        print("Continue stirring for 6 minutes for degassing.")
        #time.sleep(60*5) #disabled for dev
        print("One minute left until resuming titration.")
        #time.sleep(60) #disabled for dev
        print("Resume titration.  Add ~25 digits at a time until pH = 3.00.")
        print("If an error is made, continue with the titration.\nCorrections can be made manually to the .csv file.")
        while mV < pH_to_mV(3, Eo, TC):
            digits = digit_input()
            time.sleep(4)
            mV = get_mV()
            TC = get_temp()
            newrow = pd.DataFrame(
                {"Vol" : [digits/800], #digits/800 = mL titrant
                 "mV" : [mV],
                 "TC" : [TC]})
            datasheet = datasheet.append(newrow)
            try:
                gran_plot(datasheet, self.mass, Eo)
            except:
                print("Plotting is presently kaput.")
            print("Present pH: ", np.round(mV_to_pH(mV, Eo, TC),3))
        print("Titration Completed.")    
        return titrant_concentration, datasheet