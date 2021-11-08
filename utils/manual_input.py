# -*- coding: utf-8 -*-
"""
RPi Alkalinity
Version: v0.7 Beta
Licensed under {License info} for general use with attribution.
For works using this code please cite:
    Sandborn, D.E., Minor E.C., Hill, C. (2021)
"""
import os
from pathlib import Path

def digit_input():
    digits = 0
    while digits == 0:
        try:
            digits = float(input("Hach reading after acid addition --> "))
        except ValueError:
            digits = 0
            print("This is not a valid input.  Please input an integer or float.")
    return digits

def mass_input():
    mass = 0
    while mass == 0:
        try:
            mass = float(input("Sample Mass (g) --> "))
        except ValueError:
            mass = 0
            print("This is not a valid mass.  Please input an integer or float.")
    return mass

def Eo_input():
    Eo = 0
    while Eo == 0:
        try:
            Eo = float(input("Approximate Eo (V, typically 0.92) --> "))
        except ValueError:
            Eo = 0
            print("This is not a valid mass.  Please input an integer or float.")
    return Eo

def salinity_input():
    sal = -1
    while sal < 0 or sal > 40:
        try:
            sal = float(input("Sample Salinity (psu) --> "))
        except ValueError:
            sal = -1
            print("This is not a valid salinity.  0 < salinity < 40 accepted.")
    return sal

def filename_input():
    filename = ""
    filepath = Path(os.getcwd()+"/data/")
    while filename == "":
        try:
            filename = str(input("Filename (including filetype) in data folder --> "))
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
        