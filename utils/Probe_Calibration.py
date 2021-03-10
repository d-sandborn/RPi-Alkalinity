# -*- coding: utf-8 -*-
"""
RPi Alkalinity
Version: v0.2 (Pre-alpha)
Licensed under {License info} for general use with attribution.
For works using this code please cite:
    Sandborn, D.E., Minor E.C., Hill, C. (2021)
"""

import pandas as pd
import numpy as np
from datetime import date
import time
import os
from sklearn.linear_model import LinearRegression
from pathlib import Path

#Instruments
from utils.Get_MCC128 import get_mV
from utils.Get_DS18B20 import get_temp

class ProbeCalibration:
     def __init__(self):
         system = pd.read_csv(Path(os.getcwd()+"utils/System_Info.csv"))
         self.Eo = system['probe_Eo'][0]
         self.last_cal = pd.to_datetime(system['probe_last_calibrated'][0])
         
     def calibrate():
         """
         Runs through multi-buffer pH probe calibration with text-based prompts.
         Calibration outputs include a new Eo (standard potential) and calibration date.
         Eo determined via a linear regression based on the equation:
             EMF(probe) = ln(10**-pH)*RT/F + Eo
             --> Such that Eo is the intercept of the regression.  
         Outputs calibration results to utils/System_Info.csv
         THE ACCURACY OF Eo IS NOT ESSENTIAL TO ALKALINITY DETERMINATION.  
         See Dickson (2007) SOP 3b.  

         Returns
         -------
         None.

         """
         print("Beginning pH probe calibration./nInsert probe into first buffer.")
         num_buffers = int(input("How many buffers will you use? --> "))
         X = np.array([])
         Y = np.array([])
         for i in range(num_buffers):
             pH = float(input("What is the pH of the buffer? -->"))
             print("Wait > 4 minutes for measurement stabilization.")
             time.sleep(60*4) #Disabled for development.
             EMF = get_mV()
             X = np.append(X,EMF)
             Y = np.append(Y,np.log(10**-pH))
             print("Proceed to next buffer.")
         model = LinearRegression().fit(X.reshape(-1, 1),Y.reshape(-1, 1))
         TC = get_temp()
         new_Eo = model.intercept_[0]/-96485*8.314*(TC + 273.15)
         new_date = date.today()
         system = pd.read_csv(Path(os.getcwd()+"utils/System_Info.csv"))
         system.loc[0, 'probe_Eo'] = new_Eo
         system.loc[0, 'probe_last_calibrated'] = new_date
         system.to_csv(Path(os.getcwd()+"utils/System_Info.csv"), mode='w', index = False)
         print("System_Info.csv updated.  Probe calibration completed.  ")
         