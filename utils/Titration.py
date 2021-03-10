# -*- coding: utf-8 -*-
"""
RPi Alkalinity
Version: v0.2 (Pre-alpha)
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

#Instruments
from utils.Get_MCC128 import get_mV
from utils.Get_DS18B20 import get_temp

class RunTitration:
    def __init__(self):
        mass = float(input("Sample mass (g)? --> "))
        self.mass = mass
        SampleID = input("Sample ID? --> ")
        self.SampleID = SampleID
        salinity = float(input("Sample Salinity (psu/S)? --> "))
        self.salinity = salinity
        table = pd.DataFrame(
            {"Vol" : [],
             "mV" : [],
             "TC" : []})
        self.datasheet = table
        
    def Analyze(self): #Humphreys, M. P. and Matthews, R. S. (2020). Calkulate: total alkalinity from titration data in Python. Zenodo. doi:10.5281/zenodo.2634304.
        data = calk.read_csv(Path(os.getcwd()+"/data/Alkalinity_Meta.csv")).calkulate()
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
        print("Approx. Initial pH: ", np.round(-1*np.log10(np.exp((mV-Eo)*96485/8.314/(TC+273.15))),3))
        print("Add acid with digital titrator until pH is less than 3.6.")
        while mV < (np.log(10**-3.6)*8.314*298.15/96485+Eo): #~ pH 3.6, neglecting temperature
            time.sleep(3) #wait 3 seconds for homogenization
            mV = get_mV()
            TC = get_temp()
            print("Present pH: ", np.round(-1*np.log10(np.exp((mV-Eo)*96485/8.314/(TC+273.15))),3))
        print("Stop titration.")
        mV = get_mV()
        TC = get_temp()
        print("System accepts titrator readings in Digits = mL*800.")
        digits = float(input("Input digital titrator reading --> "))
        newrow = pd.DataFrame(
            {"Vol" : [digits/800], #digits/800 = mL titrant
             "mV" : [mV],
             "TC" : [TC]})
        datasheet.append(newrow)
        print("Continue stirring for 6 minutes for degassing.")
        #time.sleep(60*5)
        print("One minute left until resuming titration.")
        #time.sleep(60)
        print("Resume titration.  Add ~25 digits at a time until pH = 3.00.")
        print("If an error is made, continue with the titration.\nCorrections can be made manually to the .csv file.")
        while mV < 0.217:
            digits = float(input("Titrator reading --> "))
            time.sleep(3)
            mV = get_mV()
            TC = get_temp()
            newrow = pd.DataFrame(
                {"Vol" : [digits/800], #digits/800 = mL titrant
                 "mV" : [mV],
                 "TC" : [TC]})
            datasheet.append(newrow)
            print("Present pH: ", np.round(-1*np.log10(np.exp((mV-Eo)*96485/8.314/(273.15+TC))),3))
        print("Titration Completed.")    
        return titrant_concentration, datasheet