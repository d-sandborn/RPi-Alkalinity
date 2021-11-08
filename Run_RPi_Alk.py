# -*- coding: utf-8 -*-
"""
RPi Alkalinity
Version: v0.7 (Beta)
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
from pathlib import Path

#Utilities
from utils.Titration import RunTitration
from utils.conversions import mV_to_pH
from utils.Titration_Alkalinity_Meta import AlkalinityMetadata
from utils.Probe_Calibration import ProbeCalibration
from utils.admin import say_hello, chess
from utils.plotting import gran_plot, residual_plot
from utils.manual_input import filename_input, mass_input, Eo_input

#Instruments
from utils.Get_MCC128 import get_mV
from utils.Get_DS18B20 import get_temp


header = "Alkalinity titration with RPi_Alkalinity system on "+str(date.today())

#Initialize UI
print("  _____  _____ _               _ _         _ _       _ _         \n |  __ \|  __ (_)        /\   | | |       | (_)     (_) |        \n | |__) | |__) | ______ /  \  | | | ____ _| |_ _ __  _| |_ _   _ \n |  _  /|  ___/ |______/ /\ \ | | |/ / _` | | | `_ \| | __| | | |\n | | \ \| |   | |     / ____ \| |   < (_| | | | | | | | |_| |_| |\n |_|  \_\_|   |_|    /_/    \_\_|_|\_\__,_|_|_|_| |_|_|\__|\__, |\n                                                            __/ |\n                                                (C)2021 des|___/ \n                                                           ")
print("Welcome to RPi-Alkalinity.\nBeta Build 0.7")
print("Please select an option:\n1) Begin Titration\n2) Analyze Previous Titrations\n3) Check Instrument Connections\n4) Check Instrument/Sample Metadata\n5) Calibrate pH Probe\n6) View RPi-Alk credits\n7) Plot previous titrations\n8) Quit")

choice = 0

while choice != 8:
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
        try:
            print(gran_plot(pd.read_csv(filepath/filename, sep = '\t'), titration.mass, pd.read_csv(Path(os.getcwd()+"/utils/System_Info.csv"))['probe_Eo'][0]))
            print(residual_plot(pd.read_csv(filepath/filename, sep = '\t'), titration.mass, pd.read_csv(Path(os.getcwd()+"/utils/System_Info.csv"))['probe_Eo'][0]))
        except:
            print("Plotting is presently kaput.")
        print("TA: \n", results[["file_name", "analyte_mass", "alkalinity"]], "\nμmol/kg")
        input("Titration completed.  Press Enter to return to the home screen.")
        
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
        filename = filename_input()
        filepath = Path(os.getcwd()+"/data/")
        mass = mass_input()
        Eo = Eo_input()
        try:
            print(gran_plot(pd.read_csv(filepath/filename, sep = '\t'), mass, Eo))
            print(residual_plot(pd.read_csv(filepath/filename, sep = '\t'), mass, Eo))
        except:
            print("Plotting is presently kaput.")
    
    elif choice == 8:
        break
    
    elif choice == 32:
        chess()
        
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("Please select an option:\n1) Begin Titration\n2) Analyze Previous Titrations\n3) Check Instrument Connections\n4) Check Instrument/Sample Metadata\n5) Calibrate pH Probe\n6) View RPi-Alk credits\n7) Plot previous titrations\n8) Quit")


