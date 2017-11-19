# -*- coding: utf-8 -*-
"""
Created on Fri Nov 17 22:22:03 2017

@author: evan
"""
import pandas as pd
import numpy as np
import scipy.spatial
import xlsxwriter
import platform
import time

import sys
import os
sys.path.append(os.path.abspath("Python/"))
import FNC_model_build_Pd
import FNC_model_build_TD

#sets the working directory for the os that we are in
#this way once the directory is known for an os, we can
#let it set itself up automatically
#----This probably needs to be updated for the pixelbook and Flux
def Set_WD():
    def winset():
        os.chdir(r'D:/Programing/TKA_T-C_Matching')
    def linset():
        os.chdir(r'/home/evan/TKA_T-C_Matching')
    setdir = {'Windows' : winset,
              'Linux'   : linset}
    setdir[platform.system()]()

#Import the specified dataset (1, 2, or 3) from the data folder into 
#C_pop_full and T_pop_full
def Import_DataSets(dataSet): 
    Set_WD()
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

#calculate the min weights, mean_T_pop, and bray curtis distance
def Pop_Calcuations(C_pop, T_pop):
    weights = np.tile(len(T_pop)*.1,len(T_pop.columns))
    weights = pd.Series(weights, index = list(T_pop))
    mean_T_pop = T_pop.mean()
    dist = scipy.spatial.distance.cdist(T_pop, C_pop, 'braycurtis')
    return weights, mean_T_pop, dist

#start time of some timer
def timerStart():
    timer = time.clock()
    return timer
#end time of some timer
def timerStop(timer, sig):
    timer = time.clock()-timer
    timer = round(timer, sig)
    return timer
#prints a message with time header
def printMessage(message):
    tm = time.localtime()
    timeStr = '%i:%i:%i'%(tm.tm_hour, tm.tm_min, tm.tm_sec)
    print ('%s %s' %(timeStr, message))
    
#export the timing data to an excel file
def build_writer(fileName):
    filePath = "Data/"
    fileName_out = "/%s"%(fileName)
    writer  = pd.ExcelWriter("%s%s%s"%(filePath, fileName_out, '.xlsx'),
                             engine = 'xlsxwriter')
    return writer
def write_set(TimingData, dataSet, writer):
    TimingData.to_excel(writer, "Data Set %i Timings"%(dataSet))
def write_out(writer):
    writer.save()
    print "data exported to excel"


# models are defined in their own files, this is just meant as a pass 
# through to FNC so FNC can be a one stop shop
def Build_Pd_Model(C_pop, T_pop, matches, weights):
    
    m, assign, Timings = FNC_model_build_Pd.Build(C_pop, T_pop,
                                                  matches, weights)
    return m, assign, Timings

def Build_TD_Model(C_pop, T_pop, matches, weights):
    
    m, assign, Timings = FNC_model_build_TD.Build(C_pop, T_pop, 
                                                  matches, weights)
    return m, assign, Timings

#allows you to select the which model you want to create 
def Build_Model(model_base, C_pop, T_pop, matches, weights):
    selectM = {'Pd': Build_Pd_Model,
               'TD': Build_TD_Model}
    m, assign, Timings = selectM[model_base](C_pop, T_pop, matches, weights)
    return m, assign, Timings



























