# -*- coding: utf-8 -*-
"""
RPi Alkalinity
Version: v0.7 Beta
Licensed under {License info} for general use with attribution.
For works using this code please cite:
    Sandborn, D.E., Minor E.C., Hill, C. (2021)
    
    
    EMF = Eo + RT/F * ln(H+)
    pH = -log10(e^((EMF-Eo)F/RT))
"""
import numpy as np

R = 8.3144621
F = 96485.33212

def mV_to_pH(mV, Eo, TC = 25.0):
    pH = -1*np.log10(np.exp((mV/1000-Eo)*F/R/(TC+273.15)))
    return pH

def pH_to_mV(pH, Eo, TC = 25.0):
    mV = (Eo+R*(TC+273.15)/F*np.log(10**-pH))*1000
    return mV