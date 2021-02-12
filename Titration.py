# -*- coding: utf-8 -*-
"""
Created on Mon Feb  8 09:52:45 2021

@author: Daniel Sandborn
"""

import numpy as np
import pandas as pd
import time
import calkulate as calk

def get_mV():
    return (np.random.rand()-0.5)/10+0.2

def get_temp():
    return (np.random.rand()-0.5)+20

class RunTitration:
    def __init__(self):
        mass = int(input("Sample mass (g)? --> "))
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
        data = calk.read_csv("Alkalinity_Meta.csv").calkulate()
        return data
    
    def Titrate(self):
        print("Starting titration.  Please ensure that pH probe and thermistor\nare submersed and stir bar is spinning.")
        input("Press any key to continue.")
        mV = get_mV()
        TC = get_temp()
        datasheet = pd.DataFrame(
            {"Vol" : [0],
             "mV" : [mV],
             "TC" : [TC]})
        print("Initial Temperature: ", TC, "°C")
        print("Initial Voltage: ", mV, "mV")
        print("Approx. Initial pH: ", -1*np.log10(np.exp((mV-0.394401)*96485/8.314/(TC+273.15))))
        print("Add acid with digital titrator until pH is less than 3.8.")
        while mV < 0.17: #~ pH 3.8; [H+] = exp((E-0.394401)*F/R/T)
            time.sleep(3)
            mV = get_mV()
            TC = get_temp()
            print("Present pH: ", -1*np.log10(np.exp((mV-0.394401)*96485/8.314/(TC+273.15))))
        print("Stop titration.")
        mV = get_mV()
        TC = get_temp()
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
            print("Present pH: ", -1*np.log10(np.exp((mV-0.394401)*96485/8.314/(273.15+TC))))
        print("Titration Completed.")    
        return datasheet