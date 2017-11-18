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

D_sets   = [1]
T_n_sets =          [   2,     4]
rounds  = pd.Series([1000,  1000], index = T_n_sets)
Matches = pd.Series([   5,     5], index = T_n_sets)

Timing_Cols = ['T_n', 'matches', 'Setup Time',
               'c1_t','c2_t','c3_t','c4_t', 'reps', 'Solve Time']

fileName_C = "\C_pop "
fileName_T = "\T_pop "
fileName_out = "\\timing_data_out_Pd"
dataSet = D_sets[0]
fileExt = " .csv"
writer  = pd.ExcelWriter("%s%s"%(fileName_out, '.xlsx'),
                         engine = 'xlsxwriter')

for dataSet in D_sets:
    C_pop_full = pd.read_csv("%s%i%s"%(fileName_C, dataSet, fileExt), 
                             index_col = 0)
    T_pop_full = pd.read_csv("%s%i%s"%(fileName_T, dataSet, fileExt), 
                             index_col = 0)
    
    td = 0 
    TimingData = pd.DataFrame(0, index = list(range(len(T_n_sets)*len(Matches))),
                              columns = Timing_Cols, dtype = np.float)
     
    for T_n in T_n_sets:
        for matches in list(range(1, Matches[T_n]+1)):
        
            C_pop = C_pop_full.head(T_n*30)
            T_pop = T_pop_full.head(T_n)
            
            
            
            #set weights for covariates to their min
            weights, mean_T_pop,  dist = FNC.Pop_Calcuations(C_pop, T_pop) 
            
            setup_time = FNC.timerStart()
            
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
            FNC.printMessage("Creating Gurobi Variables")
            assign = [[m.addVar(vtype = GRB.BINARY, name = "%i, %i" % (t, c)) 
                        for c in Ctrl] for t in Treat]
            assign = pd.DataFrame(assign, index = Treat, columns = Ctrl)
            z      = m.addVars(Covar, vtype = GRB.CONTINUOUS, name = "z")
            
            m.update()
            
            #objective fuction
            FNC.printMessage("Creating Gurobi Objective Function")
            m.setObjective((dist*assign).sum().sum() +  
                    quicksum(weights[i]*z[i] for i in Covar), 
                    sense = GRB.MINIMIZE)
            
            #define the constraints
            FNC.printMessage("Creating Gurobi Constraints")
            c1_t = FNC.timerStart()
            m.addConstrs(matches <= assign.T.sum()[t] for t in Treat)
            FNC.printMessage("Constraint 1 done")
            c1_t = FNC.timerStop(c1_t, 3)
            
            c2_t = FNC.timerStart()
            m.addConstrs(1 >= assign.sum()[c] for c in Ctrl)
            FNC.printMessage("Constraint 2 done")
            c2_t = FNC.timerStop(c2_t, 3)
        
            c3_t = FNC.timerStart()
            m.addConstrs(z[i] >= quicksum(((assign.T[t]*C_pop[i])/(matches*T_n)).sum()
                    for t in Treat) + mean_T_pop[i] for i in Covar)
            FNC.printMessage("Constraint 3 done")
            c3_t = FNC.timerStop(c3_t, 3)
        
            c4_t = FNC.timerStart()
            m.addConstrs(z[i] >= -quicksum(((assign.T[t]*C_pop[i])/(matches*T_n)).sum()
                    for t in Treat) - mean_T_pop[i] for i in Covar)    
            FNC.printMessage("Constraint 4 done")
            c4_t = FNC.timerStop(c4_t, 3)
            
            m.update()
            
            setup_time = round(time.clock() - setup_time, 3)
            
            FNC.printMessage("Start Presolve")
            m.presolve()
            
            runTimes = pd.Series(range(rounds[T_n]), dtype = np.float)
            for r in range(rounds[T_n]):
        #        print "Start Gurobi Optimization"
                m.optimize()
                
                assignment = pd.DataFrame([np.zeros(len(Treat)) for mt in match])
                
                
                for t in Treat:
                    a = pd.DataFrame(np.zeros(len(match)))
        #            a.name = t
                    n=0
                    for c in Ctrl:
                        if assign[c][t].X==1:
                            #print "%i, %i" % (t, c)
                            a[n] = c
                            n = n+1
                    assignment[t] = a.T
                            
        #        print 'runtime was',m.runtime
                runTimes[r] = m.runtime
                
            print 'The setup time for the model was', setup_time
            print 'The average runtime for data set %i, %i treatments, and %i matches' % (dataSet, T_n, matches)
            print 'over %i optimizations was %5.5f seconds'%(rounds[T_n],runTimes.mean())
            print '------------------------------'
            print ''
        
            TimingData.loc[td] = (
                    [round(T_n,0), round(matches,0), 
                     setup_time, c1_t, c2_t, c3_t, c4_t,
                     rounds[T_n], round(runTimes.mean(), 5)])
            td = td+1
    
    
    print '------------------------------'
    print '------------------------------'
    print 'For', T_n, 'treatments using Pandas DataFrames, the timing data is:'
    print TimingData
    
    TimingData.to_excel(writer, 'Data Set %i Timings'%(dataSet))
    
writer.save()
