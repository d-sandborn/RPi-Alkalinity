# -*- coding: utf-8 -*-
"""
Created on Mon Feb  8 18:42:53 2021

@author: Daniel Sandborn
"""
import pandas as pd
from datetime import date

class AlkalinityMetadata:
    def __init__(self, filename, mass, salinity, molinity):
        self.filename = filename
        self.mass = mass/1000 #convert to kg for Calkulate
        self.salinity = salinity
        self.molinity = molinity
        self.new_meta = pd.DataFrame( #See https://calkulate.readthedocs.io/en/latest/metadata/
            {"file_name" : [self.filename],
             "salinity" : [self.salinity], #psu
             "analyte_mass" : [self.mass], #Must be kg
             "date" : [str(date.today())],
             "file_good" : [True], #Where set to False, Calkulate does not attempt to import the corresponding titration file.
             "opt_total_borate" : [2], #Sets whether total borate is estimated from salinity by PyCO2SYS following: 1 : U74 (default), or 2 : LKB10.
             "opt_k_carbonic" : [8], #Sets which carbonic acid constants to use from PyCO2SYS, can be any integer from 1 to 16 inclusive. See the PyCO2SYS docs on opt_k_carbonic for details.
             "opt_k_fluoride" : [2], #Sets whether the HF dissociation constant is estimated from salinity and temperature by PyCO2SYS following: 1 : DR79 (default), or 2 : PF87.
             "opt_k_bisulfate" : [1], #Sets whether the bisulfate dissociation constant is estimated from salinity and temperature by PyCO2SYS following: 1 : D90a (default), or 2 : KRCB77.
             "measurement_type" : ["emf"], #Use "emf" (default) for potentiometric measurements, or "pH" for direct pH measurements.
             "molinity_HCl" : [self.molinity],
             "molinity_NaCl" : [0],
             "titrant_molinity" : [self.molinity]})
        
    def Metadata_Export(self):
        #open existing metadata file, create if it doesn't exist
        self.new_meta.to_csv(self.filename, mode='a', header=False)
        print("Metadata exported to Alkalinity_Meta.csv")