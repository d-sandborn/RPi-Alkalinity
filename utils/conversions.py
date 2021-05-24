# -*- coding: utf-8 -*-
"""
RPi Alkalinity
Version: v0.4 (Beta)
Licensed under {License info} for general use with attribution.
For works using this code please cite:
    Sandborn, D.E., Minor E.C., Hill, C. (2021)
"""
import numpy as np

R = 8.3144621
F = 96485

def mV_to_pH(mV, Eo, TC = 25.0):
    pH = -1*np.log10(np.exp((mV/1000-Eo)*96485/8.3144621/(TC+273.15)))
    return pH

def pH_to_mV(pH, Eo, TC = 25.0):
    mV = (np.log(10**-pH)*8.3144621*298.15/96485+Eo)*1000
    return mV