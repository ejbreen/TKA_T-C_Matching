# -*- coding: utf-8 -*-
"""
Created on Tue Nov  7 20:32:25 2017

@author: Evan
"""

import pandas as pd
import numpy as np
import scipy.spatial
import xlsxwriter
from gurobipy import *
import sys
import os
sys.path.append(os.path.abspath("Python/"))
import FNC

os.chdir(r'/home/evan/TKA_T-C_Matching')

D_sets   = [1, 2, 3]
T_n_sets =          [   2,     4]
rounds  = pd.Series([1000,  1000], index = T_n_sets)
Matches = pd.Series([   5,     5], index = T_n_sets)

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

C_pop, T_pop = FNC.Shrink_pop(C_pop_full, T_pop_full, T_n_sets[0])

matches = 1


#set weights for covariates to their min
weights = np.tile(len(T_pop)*.1,len(T_pop.columns))
weights = pd.DataFrame(weights, index = T_pop.columns)
weights = weights.T


#set population means to dataframes
#mean_C_pop = C_pop.mean()
mean_T_pop = T_pop.mean()


#create distance matrix
dist = scipy.spatial.distance.cdist(C_pop, T_pop, 'braycurtis')

