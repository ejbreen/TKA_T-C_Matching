# -*- coding: utf-8 -*-
"""
Created on Tue Nov  7 20:32:25 2017

@author: Evan
"""

import pandas as pd

import sys
import os
sys.path.append(os.path.abspath("Python/"))
import FNC

FNC.Set_WD()

D_sets   = [1, 2, 3]
T_n_sets =          [   2,     4,   8,  16, 32, 64, 128, 256, 512, 1024, 2048]
rounds  = pd.Series([1000,  1000, 100, 100, 50, 50,  25,  25,  10,    5,    5], 
                    index = T_n_sets)
Matches = pd.Series([   5,     5,   5,   5,  3,  2,   1,   1,   1,    1,    1], 
                    index = T_n_sets)

Timing_Cols = ['T_n', 'matches', 'Setup Time',
               'c1_t','c2_t','c3_t','c4_t', 'reps', 'Solve Time']

filePath = "Data/"
fileName_C = "C_pop "
fileName_T = "T_pop "
fileName_out = "timing_data_out_Pd"
dataSet = D_sets[0]
fileExt = " .csv"
writer  = pd.ExcelWriter("%s%s"%(fileName_out, '.xlsx'),
                         engine = 'xlsxwriter')
   
C_pop_full, T_pop_full = FNC.Import_DataSets(D_sets[0], filePath, fileName_C, 
                                             fileName_T, fileExt)

C_pop, T_pop = FNC.Shrink_pop(C_pop_full, T_pop_full, T_n_sets[1])

weights, mean_T_pop, dist = FNC.Pop_Calcuations(C_pop, T_pop)



