# -*- coding: utf-8 -*-
"""
RPi Alkalinity
Version: v0.3 (Pre-alpha)
Licensed under {License info} for general use with attribution.
For works using this code please cite:
    Sandborn, D.E., Minor E.C., Hill, C. (2021)
"""
import plotnine as p9
import pandas as pd
from Titration import mV_to_pH, pH_to_mV

def gran_plot(datasheet, mass, Eo):
    datasheet = datasheet.drop([0]) #drop first filler row
    datasheet['x'] = datasheet.Vol
    datasheet['y'] = (mass+datasheet.Vol)+10**(-mV_to_pH(datasheet.mV, Eo, datasheet.TC))#gran function
    p1 = (p9.ggplot(datasheet, p9.aes(x = 'x', y = 'y'))
          +p9.geom_point()
          +p9.labs(y = 'Gran Function', x = 'Acid Added (mL)', title = 'Gran Plot')
          +p9.theme_classic())
    return p1