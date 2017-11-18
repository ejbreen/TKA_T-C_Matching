# -*- coding: utf-8 -*-
"""
Created on Tue Nov  7 20:32:25 2017

@author: Evan
"""

import pandas as pd
import numpy as np
import scipy 
#import xlsxwriter
from gurobipy import *
#from matchModel import match_maker

T_n = 1


C_pop_full = pd.read_csv(
        'T:\Programing\IOE_413\TKA\C_pop 1 .csv', index_col = 0)
T_pop_full = pd.read_csv(
        'T:\Programing\IOE_413\TKA\T_pop 1 .csv', index_col = 0)

C_pop = C_pop_full.head(T_n*30)
T_pop = T_pop_full.head(T_n)

matches = 1


#set weights for covariates to their min
weights = np.tile(len(T_pop)*.1,len(T_pop.columns))


#set population means to dataframes
#mean_C_pop = C_pop.mean()
mean_T_pop = T_pop.mean()


#create distance matrix
dist = scipy.spatial.distance.cdist(T_pop, C_pop, 'braycurtis')

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


