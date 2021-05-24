# -*- coding: utf-8 -*-
"""
RPi Alkalinity
Version: v0.3 (Pre-alpha)
Licensed under {License info} for general use with attribution.
For works using this code please cite:
    Sandborn, D.E., Minor E.C., Hill, C. (2021)
"""

#Basics
import numpy as np
import pandas as pd
import calkulate as calk
import os
import sys
from datetime import date
from pathlib import Path

#Utilities
from utils.Titration import RunTitration, mV_to_pH
from utils.Titration_Alkalinity_Meta import AlkalinityMetadata
from utils.Probe_Calibration import ProbeCalibration
from utils.admin import say_hello, chess

#Instruments
from utils.Get_MCC128 import get_mV
from utils.Get_DS18B20 import get_temp


header = "Alkalinity titration with RPi_Alkalinity system on "+str(date.today())

#Initialize UI
print("Welcome to RPi_Alkalinity.\nPre-Alpha Build v0.3")
print("Please select an option:\n1) Begin Titration\n2) Analyze Previous Datasheets\n3) Check Instrument Connections\n4) Check Instrument/Sample Metadata\n5) Calibrate pH Probe\n6) View RPi-Alk credits\n7) Quit")

choice = 0

while choice != 7:
    try: 
        choice = int(input("--> "))
    except ValueError:
        print("You have not entered a valid input.")
    if choice == 1:
        """Initialize and conduct titration"""
        titration = RunTitration()
        titrant_molinity, datasheet = titration.Titrate()
        
        #File Export
        filename = titration.SampleID+".txt"
        filepath = Path(os.getcwd()+"/data/")
        datasheet.to_csv(filepath/filename, index = False, sep = '\t')
        print(".txt titration file created.")
        Alk_meta = AlkalinityMetadata(filename, filepath, titration.mass, titration.salinity)
        Alk_meta.Metadata_Export()
        results = titration.Analyze()
        print("TA: \n", results[["file_name", "analyte_mass", "alkalinity"]], "\nμmol/kg")
        input("Titration completed.  Press any key to return to the home screen.")
        
    elif choice == 2:
        """Calkulate all previous runs stored in Alkalinity_Meta.csv.
        This could take a while, depending on how many runs there are."""
        data = calk.read_csv(Path(os.getcwd()+"/data/Alkalinity_Meta.csv"))
        data.solve()
        print(data[["file_name", "analyte_mass", "alkalinity"]])
        
    elif choice == 3:
        """Acquire pH and temperature probe(s) current readings."""
        EMF = get_mV()
        TC = get_temp()
        Eo =  pd.read_csv(Path(os.getcwd()+"/utils/System_Info.csv"))['probe_Eo'][0]
        print("pH probe:", round((EMF),5), "mV / pH", np.round(mV_to_pH(EMF, Eo, TC),3))
        print("Titration Beaker Thermistor:", round(TC,1), "°C")
        
    elif choice == 4:
        """Output an example metadata row, indicative of the values in System_Info.csv."""
        print("This function not fully supported.")
        #Check metadata
        Alk_meta = AlkalinityMetadata("Undetermined", Path(os.getcwd()+"/data"), 0, "Undetermined")
        print(Alk_meta.new_meta.transpose())
        print("These options can be changed in Titration_Alkalinity_Meta.py\n ")
        
    elif choice == 5: 
        print("Beginning pH Probe Calibration.")
        calib = ProbeCalibration
        calib.calibrate()
        
    elif choice == 6:
        say_hello()
        
    elif choice == 7:
        break
    
    elif choice == 32:
        chess()
        
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("Please select an option:\n1) Begin Titration\n2) Analyze Previous Datasheets\n3) Check Instrument Connections\n4) Check Instrument/Sample Metadata\n5) Calibrate pH Probe\n6) View RPi-Alk credits\n7) Quit")

