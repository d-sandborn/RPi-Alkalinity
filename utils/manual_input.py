# -*- coding: utf-8 -*-
"""
RPi Alkalinity
Version: v0.3 (Pre-alpha)
Licensed under {License info} for general use with attribution.
For works using this code please cite:
    Sandborn, D.E., Minor E.C., Hill, C. (2021)
"""

def digit_input():
    digits = 0
    while digits == 0:
        try:
            digits = float(input("Hach Reading --> "))
        except ValueError:
            digits = 0
            print("This is not a valid input.  Please input an integer or float.")
    return digits

def mass_input():
    mass = 0
    while mass == 0:
        try:
            mass = float(input("Sample Mass (kg) --> "))
        except ValueError:
            mass = 0
            print("This is not a valid mass.  Please input an integer or float.")
    return mass

def salinity_input():
    sal = -1
    while sal < 0 or sal > 40:
        try:
            sal = float(input("Sample Salinity (psu) --> "))
        except ValueError:
            sal = -1
            print("This is not a valid salinity.  0 < salinity < 40 accepted.")
    return sal