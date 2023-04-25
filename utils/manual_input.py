# -*- coding: utf-8 -*-
"""
RPi Alkalinity
Version: v1.0
Licensed under GPL-3.0 for general use with attribution.
For works using this code please cite:
    Sandborn, D.E., Minor E.C., Hill, C. (2023)
"""
import os
from pathlib import Path
import numpy as np
import pandas as pd


def digit_input():
    digits = 0
    while digits == 0:
        try:
            digits = np.float64(input("Hach reading after acid addition --> "))
        except ValueError:
            digits = 0
            print("This is not a valid input.  Please input an integer or float.")
    return digits


def mass_input():
    mass = 0
    while mass == 0:
        try:
            mass = np.float64(input("Sample Mass (g) --> "))
        except ValueError:
            mass = 0
            print("This is not a valid mass.  Please input an integer or float.")
    return mass


def Eo_input():
    Eo = 0
    while Eo == 0:
        try:
            Eo = np.float64(input("Approximate Eo (V, typically 0.92) --> "))
        except ValueError:
            Eo = 0
            print("This is not a valid value.  Please input an integer or float.")
    return Eo


def k_input():
    Eo = 0
    while Eo == 0:
        try:
            Eo = np.float64(input("Approximate Slope Factor (try 1) --> "))
        except:
            Eo = 0
            print("This is not a valid value.  Please input an integer or float.")
    return Eo


def salinity_input():
    sal = -1
    while sal < 0 or sal > 40:
        try:
            sal = np.float64(input("Sample Salinity (psu) --> "))
        except ValueError:
            sal = -1
            print("This is not a valid salinity.  0 < salinity < 40 accepted.")
    return sal


def filename_input():
    filename = ""
    filepath = Path(os.getcwd()+"/data/")
    while filename == "":
        try:
            filename = str(
                input("Filename (including filetype) in data folder --> "))
        except:
            print("You have entered an invalid input.")
        if '.' not in filename:
            print("Invalid filename.  Did you forget the filename suffix (e.g. '.txt'?)")
            filename = ""
        elif os.path.isfile(filepath/filename):
            print("File located.")
        else:
            print("The file could not be found in " + str(filepath))
            filename = ""
    return filename


def system_set():
    print("Be careful changing instrument settings.  Only select PyCO2SYS\noptions listed for each variable.  More information is available\nat https://pyco2sys.readthedocs.io/en/latest/co2sys_nd/")
    choice = 0
    while choice != 10:
        print(")`'-.,_)`'-.,_)`'-.,_)`'-.,_)`'-.,_\nChoose a setting:")
        system = pd.read_csv(Path(os.getcwd()+"/utils/System_Info.csv"))
        print("1) Titrant NaCl molinity: " +
              str(system["titrant_NaCl_molinity"][0]))
        print("2) Titrant HCl molinity: " +
              str(system["titrant_HCl_molinity"][0]))
        print("3) pH probe Eo (V): "+str(system["probe_Eo"][0]))
        print("4) pH probe slope factor: " +
              str(system["probe_slope_factor"][0]))
        print("5) Probe last calibrated: " +
              str(system["probe_last_calibrated"][0]))
        print("6) PyCO2SYS total borate option: " +
              str(system["opt_total_borate"][0]))
        print("7) PyCO2SYS K1, K2 option: "+str(system["opt_k_carbonic"][0]))
        print("8) PyCO2SYS K fluoride option: " +
              str(system["opt_k_fluoride"][0]))
        print("9) PyCO2SYS K bisulfate option: " +
              str(system["opt_k_bisulfate"][0]))
        print("10) Return to main menu.")
        try:
            choice = int(input("--> "))
        except ValueError:
            print("You have entered an invalid input.")
        if choice == 1:
            try:
                newvalue = np.float64(
                    input("New titrant NaCl concentration (mol/kg) --> "))
                system.loc[0, "titrant_NaCl_molinity"] = newvalue
                system.to_csv(
                    Path(os.getcwd()+"/utils/System_Info.csv"), mode='w', index=False)
                print("System_Info.csv updated.")
            except ValueError:
                print("ERROR You have entered an invalid input.")
        if choice == 2:
            try:
                newvalue = np.float64(
                    input("New titrant HCl concentration (mol/kg) --> "))
                system.loc[0, "titrant_HCl_molinity"] = newvalue
                system.to_csv(
                    Path(os.getcwd()+"/utils/System_Info.csv"), mode='w', index=False)
                print("System_Info.csv updated.")
            except ValueError:
                print("ERROR You have entered an invalid input.")
        if choice == 3:
            try:
                newvalue = np.float64(input("New probe Eo (V) --> "))
                system.loc[0, "probe_Eo"] = newvalue
                system.to_csv(
                    Path(os.getcwd()+"/utils/System_Info.csv"), mode='w', index=False)
                print("System_Info.csv updated.")
            except ValueError:
                print("ERROR You have entered an invalid input.")
        if choice == 4:
            try:
                newvalue = np.float64(input("New probe slope factor --> "))
                system.loc[0, "probe_slope_factor"] = newvalue
                system.to_csv(
                    Path(os.getcwd()+"/utils/System_Info.csv"), mode='w', index=False)
                print("System_Info.csv updated.")
            except ValueError:
                print("ERROR You have entered an invalid input.")
        if choice == 5:
            print("This value must be set via probe calibration.")
        if choice == 6:
            print("Available constants:\n1) Uppström 1974\n2) Lee et al. 2010 (default)")
            try:
                newvalue = int(
                    input("New PyCO2SYS borate option (integer) --> "))
                system.loc[0, "opt_total_borate"] = newvalue
                system.to_csv(
                    Path(os.getcwd()+"/utils/System_Info.csv"), mode='w', index=False)
                print("System_Info.csv updated.")
            except ValueError:
                print("ERROR You have entered an invalid input.")
        if choice == 7:
            print("Available constants:\n1) RRV93\n2) GP89\n3) H73 refit by DM87\n4) MCHP73 refit by DM87\n5) H73 and MCHP73 refit by DM87\n6) MCHP7373 'GEOSECS'\n7) MCHP73 'Peng'\n8) M79 'freshwater'\n9) CW98\n10) LDK00\n11) MM02\n12) MPL02\n13) MGH06\n14) M10\n15) WMW14\n16) SLH20\n17) SB21")
            try:
                newvalue = np.float64(
                    input("New carbonic acid dissociation K1, K2 (integer) --> "))
                system.loc[0, "opt_k_carbonic"] = newvalue
                system.to_csv(
                    Path(os.getcwd()+"/utils/System_Info.csv"), mode='w', index=False)
                print("System_Info.csv updated.")
            except ValueError:
                print("ERROR You have entered an invalid input.")
        if choice == 8:
            print(
                "Available constants:\n1) Dickson and Riley 1979\n2) Perez and Fraga 1987")
            try:
                newvalue = np.float64(
                    input("New fluoride option (integer) --> "))
                system.loc[0, "opt_k_fluoride"] = newvalue
                system.to_csv(
                    Path(os.getcwd()+"/utils/System_Info.csv"), mode='w', index=False)
                print("System_Info.csv updated.")
            except ValueError:
                print("ERROR You have entered an invalid input.")
        if choice == 9:
            print("Available constants:\n1) Dickson 1990 (default)\n2) Khoo et al. 1977\n3) Waters and Millero 2014")
            try:
                newvalue = np.float64(input("New bisulfate option --> "))
                system.loc[0, "opt_k_bisulfate"] = newvalue
                system.to_csv(
                    Path(os.getcwd()+"/utils/System_Info.csv"), mode='w', index=False)
                print("System_Info.csv updated.")
            except ValueError:
                print("ERROR You have entered an invalid input.")
        if choice == 0:
            print("Hey!  Who gave you the idea of hitting zero on my keyboard?\nDon't you know zero isn't an option?  The nerve of this user!\nDo you think I just sit around all day waiting for you to type\nnonsense?  If this keeps up I'm gonna... well...\nYou know, I don't really have any means of recourse...")
