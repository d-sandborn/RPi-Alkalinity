# -*- coding: utf-8 -*-
"""
RPi Alkalinity
Version: v0.82 Beta
Licensed under {License info} for general use with attribution.
For works using this code please cite:
    Sandborn, D.E., Minor E.C., Hill, C. (2022)
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from utils.conversions import mV_to_pH, pH_to_mV
from sklearn import linear_model
from sklearn.metrics import r2_score

def gran_plot(datasheet, mass, k, Eo):
    """
    Plots diagnostic titration figures.  Matplotlib backend.

    Parameters
    ----------
    datasheet : TYPE
        DESCRIPTION.
    mass : TYPE
        DESCRIPTION.
    k : TYPE
        DESCRIPTION.
    Eo : TYPE
        DESCRIPTION.

    Returns
    -------
    fig : TYPE
        DESCRIPTION.

    """
    datasheet = datasheet.drop([0])  # drop first filler row
    datasheet['x'] = datasheet.Vol
    datasheet['y'] = (mass+datasheet.Vol) * \
        10**(-mV_to_pH(datasheet.mV, Eo, k, datasheet.TC))  # gran function
    for i in datasheet.index:
        datasheet.loc[i, 'pH'] = mV_to_pH(datasheet.loc[i, 'mV'], Eo, k, datasheet.loc[i, 'TC'])
    regr = linear_model.LinearRegression()
    regr.fit(np.array(datasheet.x).reshape(-1, 1), np.array(datasheet.y))
    datasheet['y_pred'] = regr.predict(np.array(datasheet.x).reshape(-1, 1))
    r2 = round(r2_score(datasheet.y, datasheet.y_pred), 4)
    fig, axs = plt.subplots(3,1)
    scatter = axs[0].scatter(datasheet.x, datasheet.y, c = datasheet.TC, cmap = 'coolwarm')
    axs[0].plot(datasheet.x, datasheet.y_pred, ls = ':', c = 'k')
    axs[0].set_ylabel('Gran Function')
    axs[0].annotate('$r^2$ = ' +str(r2), xy = ((datasheet.x.min()+datasheet.x.mean())/2, (datasheet.y.max()+datasheet.y.mean())/2))
    plt.colorbar(scatter, ax = axs[0])
    resid = axs[1].scatter(datasheet.x, datasheet.y-datasheet.y_pred, c = datasheet.TC, cmap = 'coolwarm')
    axs[1].axhline(y = 0, c = 'k', ls = ':')
    axs[1].set_ylabel('Gran Function Residuals')
    plt.colorbar(resid, ax = axs[1])
    titrate = axs[2].scatter(datasheet.x, datasheet.pH, c = datasheet.TC, cmap = 'coolwarm')
    plt.colorbar(titrate, ax = axs[2])
    axs[2].set_xlabel('Titrant Volume (mL)')
    axs[2].set_ylabel('pH')
    fig.tight_layout()
    return fig
