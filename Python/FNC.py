# -*- coding: utf-8 -*-
"""
Created on Fri Nov 17 22:22:03 2017

@author: evan
"""
import pandas as pd
import numpy as np
import scipy.spatial
import xlsxwriter
from gurobipy import *
import os


def Import_DataSets(dataSet, filePath, fileName_C, fileName_T, fileExt):  
    C_pop_full = pd.read_csv("%s%s%i%s"%(filePath, fileName_C, dataSet, fileExt), 
                             index_col = 0)
    T_pop_full = pd.read_csv("%s%s%i%s"%(filePath, fileName_T, dataSet, fileExt), 
                             index_col = 0)
    return C_pop_full, T_pop_full
  
def Shrink_pop(C_pop_full, T_pop_full, T_n):
    C_pop = C_pop_full.head(T_n*30)
    T_pop = T_pop_full.head(T_n)
    return C_pop, T_pop