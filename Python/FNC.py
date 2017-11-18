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
import sys
import platform
import time

#sets the working directory for the os that we are in
#this way once the directory is known for an os, we can
#let it set itself up automatically
#----This probably needs to be updated for the pixelbook and Flux
def Set_WD():
    def winset():
        os.chdir(r'D:/Programing/TKA_T-C_Matching')
    def linset():
        os.chdir(r'/home/evan/TKA_T-C_Matching')
    def fluxset():
        os.chdir(r'/home/evan/TKA_T-C_Matching')
    setdir = {'Windows' : winset,
              'Linux'   : linset,
              'Flux'    : fluxset}
    setdir[platform.system()]()

#Import the specified dataset (1, 2, or 3) from the data folder into 
#C_pop_full and T_pop_full
def Import_DataSets(dataSet):  
    filePath = "Data/"
    fileName_C = "C_pop "
    fileName_T = "T_pop "
    fileExt = " .csv"
    C_pop_full = pd.read_csv("%s%s%i%s"%(filePath, fileName_C, dataSet, fileExt), 
                             index_col = 0)
    T_pop_full = pd.read_csv("%s%s%i%s"%(filePath, fileName_T, dataSet, fileExt), 
                             index_col = 0)
    return C_pop_full, T_pop_full

#shrink the full datasets to down to T_n for T_pop and T_n*30 for C_pop
#for the shrink, it takes the top of the list
def Shrink_pop(C_pop_full, T_pop_full, T_n):
    C_pop = C_pop_full.head(T_n*30)
    T_pop = T_pop_full.head(T_n)
    return C_pop, T_pop
    
def Pop_Calcuations(C_pop, T_pop):
    #set weights for covariates to their min
    weights = np.tile(len(T_pop)*.1,len(T_pop.columns))
    weights = pd.DataFrame(weights, index = T_pop.columns)
    weights = weights.T
    
    
    mean_T_pop = T_pop.mean()
    
    
    #create distance matrix
    dist = scipy.spatial.distance.cdist(C_pop, T_pop, 'braycurtis')
    
    return weights, mean_T_pop, dist

def timerStart():
    timer = time.clock()
    return timer
def timerStop(timer, sig):
    timer = time.clock()-timer
    timer = round(timer, sig)
    return timer
def printMessage(message):
    tm = time.localtime()
    timeStr = '%i:%i:%i'%(tm.tm_hour, tm.tm_min, tm.tm_sec)
    print ('%s %s' %(timeStr, message))
