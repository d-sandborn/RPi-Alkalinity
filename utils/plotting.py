# -*- coding: utf-8 -*-
"""
RPi Alkalinity
Version: v0.5 Beta
Licensed under {License info} for general use with attribution.
For works using this code please cite:
    Sandborn, D.E., Minor E.C., Hill, C. (2021)
"""
import plotnine as p9
import pandas as pd
import numpy as np
from utils.conversions import mV_to_pH, pH_to_mV
from sklearn import linear_model
from sklearn.metrics import r2_score

def gran_plot(datasheet, mass, Eo):
    """
    Plots the the linear portion of a Gran Plot.

    Parameters
    ----------
    datasheet : pandas dataframe
        Three columns: Vol, mV, TC
    mass : float or int
        Mass in g of sample analyzed.
    Eo : float
        Value of the standard cell potential for a pH probe, determined via calibration.  

    Returns
    -------
    p1 : TYPE
        DESCRIPTION.

    """
    datasheet = datasheet.drop([0]) #drop first filler row
    datasheet['x'] = datasheet.Vol
    datasheet['y'] = (mass+datasheet.Vol)*10**(-mV_to_pH(datasheet.mV, Eo, datasheet.TC))#gran function
    regr = linear_model.LinearRegression()
    regr.fit(np.array(datasheet.x).reshape(-1,1), np.array(datasheet.y))
    datasheet['y_pred'] = regr.predict(np.array(datasheet.x).reshape(-1,1))
    r2 = round(r2_score(datasheet.y, datasheet.y_pred),4)
    p1 = (p9.ggplot(datasheet, p9.aes(x = 'x', y = 'y'))
          +p9.geom_point(p9.aes(color = 'TC'))
          +p9.geom_smooth(method = 'lm', se = False)
          +p9.annotate('text', x = np.mean(datasheet.x), y = max(datasheet.y), label = 'R^2 = ' + str(r2))
          +p9.labs(y = 'Gran Function', x = 'Acid Added (mL)', title = 'Gran Plot')
          +p9.theme_classic())
    return p1

def residual_plot(datasheet, mass, Eo):
    """
    Plots the residual values of the linear portion of a Gran Plot.

    Parameters
    ----------
    datasheet : pandas dataframe
        Three columns: Vol, mV, TC
    mass : float or int
        Mass in g of sample analyzed.
    Eo : float
        Value of the standard cell potential for a pH probe, determined via calibration.  

    Returns
    -------
    p1 : ggplot object
        Returns ggplot object (generated with Plotnine) to be passed to print().  

    """
    datasheet = datasheet.drop([0]) #drop first filler row
    datasheet['x'] = datasheet.Vol
    datasheet['Gran'] = (mass+datasheet.Vol)*10**(-mV_to_pH(datasheet.mV, Eo, datasheet.TC)) #gran function
    regr = linear_model.LinearRegression()
    regr.fit(np.array(datasheet.x).reshape(-1,1), np.array(datasheet.Gran))
    datasheet['y_pred'] = regr.predict(np.array(datasheet.x).reshape(-1,1))
    datasheet['y'] = datasheet.Gran-datasheet.y_pred
    r2 = round(r2_score(datasheet.Gran, datasheet.y_pred),4)
    p1 = (p9.ggplot(datasheet, p9.aes(x = 'x', y = 'y'))
          +p9.geom_point(p9.aes(color = 'TC'), size = 5)
          +p9.geom_area(fill = 'lightblue', alpha = 0.5)
          +p9.geom_smooth(method = 'lm', se = False)
          +p9.annotate('text', x = np.mean(datasheet.x), y = max(datasheet.y), label = 'R^2 = ' + str(r2))
          +p9.labs(y = 'Gran Residuals', x = 'Acid Added (mL)', title = 'Gran Residuals Plot')
          +p9.theme_classic())
    return p1    