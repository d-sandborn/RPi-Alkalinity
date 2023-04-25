# -*- coding: utf-8 -*-
"""
RPi Alkalinity
Version: v1.0
Licensed under GPL-3.0 for general use with attribution.
For works using this code please cite:
    Sandborn, D.E., Minor E.C., Hill, C. (2023)
    
    
    EMF = Eo + RTk/F * pH
    pH = (EMF-Eo)/-(ln(10)RTk/F)
"""
import numpy as np

R = 8.3144621
F = 96485.33212

def mV_to_pH(mV, Eo, k, TC = 25.0):
    pH = -(mV/1000-Eo)/(np.log(10)*R*(TC+273.15)*k/F)
    return pH

def pH_to_mV(pH, Eo, k, TC = 25.0):
    mV = (Eo-np.log(10)*R*(TC+273.15)*k/F*pH)*1000
    return mV