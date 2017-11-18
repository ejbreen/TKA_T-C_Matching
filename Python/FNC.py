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


def Build_PD_Model(C_pop_full, T_pop_full, T_n, matches):
    
    C_pop, T_pop = Shrink_pop(C_pop_full, T_pop_full, T_n)
    #start the setup timer
    setup_time = timerStart()
    
    #set weights for covariates to their min
    weights, mean_T_pop,  dist = Pop_Calcuations(C_pop, T_pop) 
    
    #start creating model elements
    Ctrl  = list(range(len(C_pop)))
    C_pop.index = Ctrl
    Treat = list(range(len(T_pop)))
    T_pop.index = Treat
    T_n = len(T_pop)
    match = list(range(matches))
    
    dist = pd.DataFrame(dist, index = Treat, columns = Ctrl)
    
    Covar = list(T_pop)
    
    weights = pd.Series(weights, index = Covar)
    
    
    #define the model
    m = Model('match')
    m.Params.OutputFlag = 0
    
    #create variables
    printMessage("Creating Gurobi Variables")
    assign = [[m.addVar(vtype = GRB.BINARY, name = "%i, %i" % (t, c)) 
                for c in Ctrl] for t in Treat]
    assign = pd.DataFrame(assign, index = Treat, columns = Ctrl)
    z      = m.addVars(Covar, vtype = GRB.CONTINUOUS, name = "z")
    
    m.update()
    
    #objective fuction
    printMessage("Creating Gurobi Objective Function")
    m.setObjective((dist*assign).sum().sum() +  
            quicksum(weights[i]*z[i] for i in Covar), 
            sense = GRB.MINIMIZE)
    
    #define the constraints
    printMessage("Creating Gurobi Constraints")
    c1_t = timerStart()
    m.addConstrs(matches <= assign.T.sum()[t] for t in Treat)
    printMessage("Constraint 1 done")
    c1_t = timerStop(c1_t, 3)
    
    c2_t = timerStart()
    m.addConstrs(1 >= assign.sum()[c] for c in Ctrl)
    printMessage("Constraint 2 done")
    c2_t = timerStop(c2_t, 3)

    c3_t = timerStart()
    m.addConstrs(z[i] >= quicksum(((assign.T[t]*C_pop[i])/(matches*T_n)).sum()
            for t in Treat) + mean_T_pop[i] for i in Covar)
    printMessage("Constraint 3 done")
    c3_t = timerStop(c3_t, 3)

    c4_t = timerStart()
    m.addConstrs(z[i] >= -quicksum(((assign.T[t]*C_pop[i])/(matches*T_n)).sum()
            for t in Treat) - mean_T_pop[i] for i in Covar)    
    printMessage("Constraint 4 done")
    c4_t = timerStop(c4_t, 3)
    
    m.update()
    
    setup_time = timerStop(setup_time, 3)
    
    return m



