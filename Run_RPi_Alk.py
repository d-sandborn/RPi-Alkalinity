# -*- coding: utf-8 -*-
"""
RPi Alkalinity
Version: v1.0
Licensed under GPL-3.0 for general use with attribution.
For works using this code please cite:
    Sandborn, D.E., Minor E.C., Hill, C. (2023)
"""

# Basics
import numpy as np
import pandas as pd
import calkulate as calk
import os
from datetime import date
from pathlib import Path

# Utilities
from utils.Titration import RunTitration
from utils.conversions import mV_to_pH
from utils.Titration_Alkalinity_Meta import AlkalinityMetadata
from utils.Probe_Calibration import ProbeCalibration
from utils.admin import say_hello, chess
from utils.plotting import gran_plot, TicTacToe
from utils.manual_input import filename_input, mass_input, Eo_input, k_input, system_set

# Instruments
from utils.Get_MCC128 import get_mV
from utils.Get_DS18B20 import get_temp

pd.set_option('display.max_rows', None) #tell Pandas not to abridge tables.
header = "Alkalinity titration with RPi_Alkalinity system on " + \
    str(date.today())

# Initialize UI
say_hello()
print("Please select an option:\n1) Begin titration\n2) Analyze previous titrations\n3) Check instruments\n4) Check sample metadata\n5) Calibrate pH probe\n6) View RPi-Alk credits\n7) Plot previous titrations\n8) Change system settings\n9) Quit")

choice = 0

while choice != 9:
    try:
        choice = int(input("--> "))
    except ValueError:
        print("You have not entered a valid input.")
    if choice == 1:
        """Initialize and conduct titration"""
        titration = RunTitration()
        titrant_molinity, datasheet = titration.Titrate()

        # File Export
        filename = titration.SampleID+".txt"
        filepath = Path(os.getcwd()+"/data/")
        datasheet.to_csv(filepath/filename, index=False, sep='\t')
        print(".txt titration file created.")
        Alk_meta = AlkalinityMetadata(
            filename, filepath, titration.mass, titration.salinity)
        Alk_meta.Metadata_Export()
        results = titration.Analyze()
        try:
            print(gran_plot(pd.read_csv(filepath/filename, sep='\t'), titration.mass, pd.read_csv(Path(os.getcwd()+"/utils/System_Info.csv"))
                  ['probe_slope_factor'][0], pd.read_csv(Path(os.getcwd()+"/utils/System_Info.csv"))['probe_Eo'][0]))
        except:
            print("Plotting is presently kaput.")
        print("TA: \n", results[["file_name",
              "analyte_mass", "alkalinity"]])
        input("Titration completed.  Press Enter to return to the home screen.")

    elif choice == 2:
        """Calkulate all previous runs stored in Alkalinity_Meta.csv."""
        data = calk.read_csv(Path(os.getcwd()+"/data/Alkalinity_Meta.csv"))
        data.get_total_salts().solve()
        print(data[["file_name", "analyte_mass", "alkalinity"]])

    elif choice == 3:
        """Acquire pH and temperature probe(s) current readings."""
        EMF = get_mV()
        TC = get_temp()
        Eo = pd.read_csv(
            Path(os.getcwd()+"/utils/System_Info.csv"))['probe_Eo'][0]
        k = pd.read_csv(Path(os.getcwd()+"/utils/System_Info.csv")
                        )['probe_slope_factor'][0]
        print("pH probe:", round((EMF), 2), "mV / pH",
              np.round(mV_to_pH(EMF, Eo, k, TC), 3))
        print("Thermistor:", round(TC, 3), "°C")

    elif choice == 4:
        """Output an example metadata row, indicative of the values in System_Info.csv."""
        Alk_meta = AlkalinityMetadata("Undetermined", Path(
            os.getcwd()+"/data"), 0, "Undetermined")
        print(Alk_meta.new_meta.transpose())
        print("These options can be changed in Titration_Alkalinity_Meta.py\n ")

    elif choice == 5:
        print("Beginning pH Probe Calibration.")
        calib = ProbeCalibration
        calib.calibrate()

    elif choice == 6:
        """Logo and credits"""
        say_hello()

    elif choice == 7:
        """Plotting for previous titrations"""
        filename = filename_input()
        filepath = Path(os.getcwd()+"/data/")
        mass = mass_input()
        Eo = Eo_input()
        k = k_input()
        try:
            print(gran_plot(pd.read_csv(filepath/filename, sep='\t'), mass, k, Eo))
        except:
            print("Plotting is presently kaput.")

    elif choice == 8:
        """Scripted way to change System_Info.csv settings."""
        system_set()

    elif choice == 9:
        break

    elif choice == 32:
        chess()
    
    elif choice == 1983:
        TicTacToe().start()
        
    elif choice == 88224646:
        print("Sorry, the Konami Code will not improve your titrations.")

    print(")`'-.,_)`'-.,_)`'-.,_)`'-.,_)`'-.,_)`'-.,_)`'-.,_)`'-.,_)`'-.,_")
    print("Please select an option:\n1) Begin titration\n2) Analyze previous titrations\n3) Check instruments\n4) Check sample metadata\n5) Calibrate pH probe\n6) View RPi-Alk credits\n7) Plot previous titrations\n8) Change system settings\n9) Quit")
