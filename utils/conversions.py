# -*- coding: utf-8 -*-
"""
Created on Mon May 24 10:29:11 2021

@author: sandb425
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