# -*- coding: utf-8 -*-
"""
RPi Alkalinity
Version: v0.6 Beta
Licensed under {License info} for general use with attribution.
For works using this code please cite:
    Sandborn, D.E., Minor E.C., Hill, C. (2021)
"""

import pandas as pd
from datetime import date
from os import path
import numpy as np
from pathlib import Path

class AlkalinityMetadata:
    def __init__(self, filename, filepath, mass, salinity):
        system = pd.read_csv(Path("utils/System_Info.csv"))
        self.filename = filename
        self.filepath = filepath
        self.mass = mass/1000 #convert to kg for Calkulate
        self.salinity = salinity
        self.molinity = system['titrant_HCl_molinity'][0]
        self.opt_total_borate = system['opt_total_borate'][0]
        self.opt_k_carbonic = system['opt_k_carbonic'][0]
        self.opt_k_fluoride = system['opt_k_fluoride'][0]
        self.opt_k_bisulfate = system['opt_k_bisulfate'][0]
        self.dic = system['dic'][0]
        self.new_meta = pd.DataFrame( #See https://calkulate.readthedocs.io/en/latest/metadata/
            {"analysis_batch" : [np.nan],
             "file_name" : [self.filename],
             "file_path" : [str(self.filepath)+str(Path('/'))],
             "salinity" : [self.salinity], #psu
             "analyte_mass" : [self.mass], #Must be kg
             "date" : [str(date.today())],
             "file_good" : [True], #Where set to False, Calkulate does not attempt to import the corresponding titration file.
             "opt_total_borate" : [self.opt_total_borate], #Sets whether total borate is estimated from salinity by PyCO2SYS following: 1 : U74 (default), or 2 : LKB10.
             "opt_k_carbonic" : [self.opt_k_carbonic], #Sets which carbonic acid constants to use from PyCO2SYS, can be any integer from 1 to 16 inclusive. See the PyCO2SYS docs on opt_k_carbonic for details.
             "opt_k_fluoride" : [self.opt_k_fluoride], #Sets whether the HF dissociation constant is estimated from salinity and temperature by PyCO2SYS following: 1 : DR79 (default), or 2 : PF87.
             "opt_k_bisulfate" : [self.opt_k_bisulfate], #Sets whether the bisulfate dissociation constant is estimated from salinity and temperature by PyCO2SYS following: 1 : D90a (default), or 2 : KRCB77.
             "measurement_type" : ["EMF"], #Use "emf" (default) for potentiometric measurements, or "pH" for direct pH measurements.
             "molinity_HCl" : [self.molinity],
             "molinity_NaCl" : [0],
             "titrant_molinity" : [self.molinity],
             "alkalinity_certified" : [np.nan],
             "dic" : [self.dic],
             "total_borate" : [np.nan],
             "total_fluoride" : [np.nan],
             "total_sulfate" : [np.nan]})
        
    def Metadata_Export(self):
        #add to existing metadata file, create with headers if it doesn't exist
        if path.exists(self.filepath/"Alkalinity_Meta.csv"):
            self.new_meta.to_csv(self.filepath/"Alkalinity_Meta.csv", mode='a', header=False, index = False)
        else:
            self.new_meta.to_csv(self.filepath/"Alkalinity_Meta.csv", mode='a', header=True, index = False)
       
        print("Metadata exported to Alkalinity_Meta.csv")