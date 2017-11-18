# -*- coding: utf-8 -*-
"""
Created on Tue Nov  7 20:32:25 2017

@author: Evan
"""

import pandas as pd
import numpy as np
import scipy 
import xlsxwriter
from gurobipy import *
import os
#from matchModel import match_maker

os.chdir(r'/home/evan/TKA_T-C_Matching')

D_sets   = [1, 2, 3]
T_n_sets =          [   2,     4]
rounds  = pd.Series([1000,  1000], index = T_n_sets)
Matches = pd.Series([   5,     5], index = T_n_sets)

Timing_Cols = ['T_n', 'matches', 'Setup Time',
               'c1_t','c2_t','c3_t','c4_t', 'reps', 'Solve Time']

fileName_C = "C_pop "
fileName_T = "T_pop "
fileName_out = "timing_data_out_Pd"
dataSet = D_sets[0]
fileExt = " .csv"
writer  = pd.ExcelWriter("%s%s"%(fileName_out, '.xlsx'),
                         engine = 'xlsxwriter')

def Import_DataSets(dataset, file_name_C, file_name_T, fileExt):  
    C_pop_full = pd.read_csv("%s%i%s"%(fileName_C, dataSet, fileExt), 
                             index_col = 0)
    T_pop_full = pd.read_csv("%s%i%s"%(fileName_T, dataSet, fileExt), 
                             index_col = 0)
    return C_pop_full, T_pop_full
   
C_pop_full, T_pop_full = Import_DataSets(D_sets[0], fileName_C, fileName_T, fileExt)

C_pop = C_pop_full.head(T_n_sets[0]*30)
T_pop = T_pop_full.head(T_n_sets[0])

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

#m_vars = 0
#match_maker(C_pop, T_pop, matches, weights, mean_T_pop, dist, m_vars)

# =============================================================================
# #make everything a dataframe
# weights_df = pd.DataFrame(weights)
# weights_df = weights_df.T
# weights_df.columns = T_pop.columns
# mean_C_pop_df = pd.DataFrame(mean_C_pop)
# mean_C_pop_df = mean_C_pop_df.T
# mean_C_pop_df.columns = C_pop.columns
# mean_T_pop_df = pd.DataFrame(mean_T_pop)
# mean_T_pop_df = mean_T_pop_df.T
# mean_T_pop_df.columns = T_pop.columns
# dist_df = pd.DataFrame(dist)
# =============================================================================

# =============================================================================
# writer = pd.ExcelWriter("T:\Programing\IOE_413\TKA\pandas_out.xlsx",
#                         engine = 'xlsxwriter')
# 
# params.to_excel(writer, 'params')
# C_pop.to_excel(writer, 'C_pop')
# mean_T_pop_df.to_excel(writer, 'mean_T_pop')
# weights_df.to_excel(writer, 'weights')
# dist_df.to_excel(writer, 'dist')
# 
# writer.save()
# =============================================================================


