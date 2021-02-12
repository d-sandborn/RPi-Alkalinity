# -*- coding: utf-8 -*-
"""
Created on Mon Feb  8 09:29:33 2021
@author: Daniel Sandborn

Run_RPi_Alkalinity.py
Version: v0.1 (Pre-alpha)
Licensed under {License info} for general use with attribution.
For works using this code please cite:
    Sandborn, D.E., Minor E.C., Hill, C. (2021)
"""

#Startup
import numpy as np
import pandas as pd
from Titration import RunTitration
import calkulate as calk
import os
from datetime import date
from Titration_Alkalinity_Meta import AlkalinityMetadata

titrant_molinity = 0.26784 # mol/kg

header = "Alkalinity titration with RPi_Alkalinity system on "+str(date.today())

def get_mV():
    return (np.random.rand()-0.5)/10+0.2

def get_temp():
    return (np.random.rand()-0.5)+20

#Initialize UI
print("Welcome to RPi_Alkalinity.\nPre-Alpha Build v0.1")
print("Please select an option:\n1) Begin Titration\n2) Analyze Previous Datasheets\n3) Check Instrument Connections\n4) Check Instrument/Sample Metadata\n5) Quit")

choice = 0

while choice != 5:
    choice = int(input("--> "))
    if choice == 1:
        titration = RunTitration()
        datasheet = titration.Titrate()
        titration.datasheet = titration.datasheet.append(datasheet)
        #File Export
        filename = titration.SampleID+".csv"
        datasheet.to_csv(filename, index = False)
        print(".csv titration file created.")
        Alk_meta = AlkalinityMetadata(filename, titration.mass, titration.salinity, titrant_molinity)
        Alk_meta.Metadata_Export()
        results = titration.Analyze()
        print("TA: ", results['alkalinity'], " μmol/kg")
        input("Titration completed.  Press any key to return to the home screen.")
    elif choice == 2:
        print("This option is not yet implemented.\nPlease use Calkulate for this task.\n ")
    elif choice == 3:
        print("DUMMY RESPONSES!  Instruments not yet connected.")
        print("pH meter:", round(get_mV(),5), "mV")
        print("Thermistor 1", round(get_temp(),1), "°C")
        print(" ")
    elif choice == 4:
        print("This function not fully supported.")
        #Check metadata
        Alk_meta = AlkalinityMetadata("Undetermined", 0, "Undetermined", titrant_molinity)
        print(Alk_meta.new_meta)
        print("These options can be changed in Titration_Alkalinity_Meta.py")
    elif choice == 5:
        break
    print("Please select an option:\n1) Begin Titration\n2) Analyze Previous Datasheets\n3) Check Instrument Connections\n4) Check Instrument/Sample Metadata\n5) Quit")

