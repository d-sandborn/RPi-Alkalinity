# -*- coding: utf-8 -*-
"""
RPi Alkalinity
Version: v0.2 (Pre-alpha)
Licensed under {License info} for general use with attribution.
For works using this code please cite:
    Sandborn, D.E., Minor E.C., Hill, C. (2021)
"""

#Basics
import numpy as np
import pandas as pd
import calkulate as calk
import os
from datetime import date

#Utilities
from Titration import RunTitration
from Titration_Alkalinity_Meta import AlkalinityMetadata
from Probe_Calibration import ProbeCalibration

#Instruments
from Get_MCC128 import get_mV
from Get_DS18B20 import get_temp


header = "Alkalinity titration with RPi_Alkalinity system on "+str(date.today())

#Initialize UI
print("Welcome to RPi_Alkalinity.\nPre-Alpha Build v0.2")
print("Please select an option:\n1) Begin Titration\n2) Analyze Previous Datasheets\n3) Check Instrument Connections\n4) Check Instrument/Sample Metadata\n5) Calibrate pH Probe\n6) Quit")

choice = 0

while choice != 6:
    choice = int(input("--> "))
    if choice == 1:
        #Initialize and conduct titration
        titration = RunTitration()
        titrant_molinity, datasheet = titration.Titrate()
        
        #File Export
        filename = titration.SampleID+".csv"
        filepath = os.getcwd()
        datasheet.to_csv(filename, index = False)
        print(".csv titration file created.")
        Alk_meta = AlkalinityMetadata(filename, filepath, titration.mass, titration.salinity)
        Alk_meta.Metadata_Export()
        results = titration.Analyze()
        print("TA: ", results['alkalinity'], " μmol/kg")
        input("Titration completed.  Press any key to return to the home screen.")
        
    elif choice == 2:
        data = calk.read_csv(os.getcwd()+"\\Data\\Alkalinity_Meta.csv").calkulate()
        print(data[["file_name", "analyte_mass", "alkalinity"]])
        
    elif choice == 3:
        print("DUMMY RESPONSES!  Instruments not yet connected.")
        EMF = (get_mV())
        TC = get_temp()
        Eo =  system = pd.read_csv("System_Info.csv")['probe_Eo'][0]
        print("pH probe:", round((EMF),5), "mV / pH", np.round(-1*np.log10(np.exp((EMF-Eo)*96485/8.314/(TC+273.15))),3))
        print("Titration Beaker Thermistor:", round(TC,1), "°C")
        
    elif choice == 4:
        print("This function not fully supported.")
        #Check metadata
        Alk_meta = AlkalinityMetadata("Undetermined", 0, "Undetermined")
        print(Alk_meta.new_meta.transpose())
        print("These options can be changed in Titration_Alkalinity_Meta.py\n ")
        
    elif choice == 5: 
        print("Beginning pH Probe Calibration.")
        calib = ProbeCalibration
        calib.calibrate()
        
    elif choice == 6:
        break
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("Please select an option:\n1) Begin Titration\n2) Analyze Previous Datasheets\n3) Check Instrument Connections\n4) Check Instrument/Sample Metadata\n5) Calibrate pH Probe\n6) Quit")

