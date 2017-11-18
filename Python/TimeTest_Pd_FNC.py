# -*- coding: utf-8 -*-
"""
Created on Sat Nov 11 18:38:18 2017

@author: Evan
"""

import pandas as pd
import numpy as np
import scipy 
import xlsxwriter
from gurobipy import *
import time

import sys
import os
sys.path.append(os.path.abspath("Python/"))
import FNC

C_pop_full, T_pop_full = FNC.Import_DataSets(1)

D_sets   = [1]
T_n_sets =          [   2,     4]
rounds  = pd.Series([1000,  1000], index = T_n_sets)
Matches = pd.Series([   5,     5], index = T_n_sets)
weights = np.ones(len(T_pop_full.columns))

Timing_Cols = ['T_n', 'matches', 'Setup Time',
               'c1_t','c2_t','c3_t','c4_t', 'reps', 'Solve Time']
Timing_Data = pd.DataFrame(0, index = list(range(Matches.sum())),
                          columns = Timing_Cols, dtype = np.float)
dataSet = D_sets[0]

for dataSet in D_sets:
    C_pop_full, T_pop_full = FNC.Import_DataSets(dataSet)
    
    td = 0 
    
     
    for T_n in T_n_sets:
        for matches in list(range(1, Matches[T_n]+1)):
            Timing_Data.loc[td][0:2] = [T_n, matches]
            
            #set up the model and return the timings of the different element's
            m, setup_Time = FNC.Build_PD_Model(C_pop_full, T_pop_full, T_n,
                                            matches, weights)
            Timing_Data.loc[td][2:7] = setup_Time
            
            FNC.printMessage("Start Presolve")
            m.presolve()
            
            m.optimize()
            
            td = td + 1
        
    
            
           
    


































