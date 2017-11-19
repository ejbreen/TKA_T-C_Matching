# -*- coding: utf-8 -*-
"""
Created on Sat Nov 11 19:20:44 2017

@author: Evan
"""

import pandas as pd
import numpy as np
import scipy 
import xlsxwriter
from gurobipy import *
import time

D_sets   = [1, 2, 3]
T_n_sets =          [   2,     4]
rounds  = pd.Series([1000,  1000], index = T_n_sets)
Matches = pd.Series([   5,     5], index = T_n_sets)

Timing_Cols = ['T_n', 'matches', 'Setup Time',
               'c1_t','c2_t','c3_t','c4_t', 'reps', 'Solve Time']

filePath  = "T:\Programing\IOE_413\TKA"
fileName_C = "\C_pop "
fileName_T = "\T_pop "
fileName_out = "\\timing_data_out_TD"
dataSet = D_sets[0]
fileExt = " .csv"
writer  = pd.ExcelWriter("%s%s%s"%(filePath, fileName_out, '.xlsx'),
                         engine = 'xlsxwriter')

for dataSet in D_sets:
    C_pop_full = pd.read_csv("%s%s%i%s"%(filePath, fileName_C, dataSet, fileExt), 
                             index_col = 0)
    T_pop_full = pd.read_csv("%s%s%i%s"%(filePath, fileName_T, dataSet, fileExt), 
                             index_col = 0)
    
    td=0
    TimingData = pd.DataFrame(0, index = list(range(len(T_n_sets)*len(Matches))),
                              columns = Timing_Cols, dtype = np.float)
    
    for T_n in T_n_sets:
        for matches in list(range(1, Matches[T_n]+1)):
            
            C_pop = C_pop_full.head(T_n*30)
            T_pop = T_pop_full.head(T_n)
            
            #set weights for covariates to their min
            weights = np.tile(len(T_pop)*.1,len(T_pop.columns))
            
            #set population means to dataframes
            #mean_C_pop = C_pop.mean()
            mean_T_pop = T_pop.mean()
            
            #create distance matrix
            dist = scipy.spatial.distance.cdist(T_pop, C_pop, 'braycurtis')
            
            
            setup_time = time.clock()
            #start creating model elements
            Ctrl  = list(range(len(C_pop)))
            C_pop.index = Ctrl
            Treat = list(range(len(T_pop)))
            T_pop.index = Treat
            T_n = len(T_pop)
            
            Covar = list(T_pop)
            
            distance = { (t,c) : dist[m][n] for n,c in enumerate(Ctrl)
                                            for m,t in enumerate(Treat)}
            
            Ctrl_pop = { (c,i) : C_pop.loc[m].values[n] for n,i in enumerate(Covar)
                                                        for m,c in enumerate(Ctrl)}
            
            T_avg = { i : mean_T_pop[n] for n,i in enumerate (Covar)}
            weight= { i : weights[n] for n,i in enumerate (Covar)}
            
            
            #define the model
            m = Model('match')
            m.Params.OutputFlag = 0
            
            #create variables
            tm = time.localtime()
            print "%i:%i:%i"%(tm.tm_hour,tm.tm_min,tm.tm_sec), "Creating Gurobi Variables"
            assign = m.addVars(distance.keys(), vtype = GRB.BINARY, name = "assign")
            z      = m.addVars(T_avg.keys(), vtype = GRB.CONTINUOUS, name = "z")
            
            
            m.update()
            
            #objective fuction
            tm = time.localtime()
            print "%i:%i:%i"%(tm.tm_hour,tm.tm_min,tm.tm_sec), "Creating Gurobi Objective Function"
            m.setObjective(quicksum(dist[t,c]*assign[t,c] for [t,c] in distance) + 
                           quicksum(weight[i]*z[i] for i in Covar),
                           sense = GRB.MINIMIZE)
            
            #define the constraints
            tm = time.localtime()
            print "%i:%i:%i"%(tm.tm_hour,tm.tm_min,tm.tm_sec),"Creating Gurobi Constraints"
            c1_t = time.clock()
            m.addConstrs(matches <= quicksum(assign[t,c] for c in Ctrl) for t in Treat)
            tm = time.localtime()
            print "%i:%i:%i"%(tm.tm_hour,tm.tm_min,tm.tm_sec), "Constraint 1 done"
            c1_t = round(time.clock()-c1_t,3)
            
            c2_t = time.clock()
            m.addConstrs(1 >= quicksum(assign[t,c] for t in Treat) for c in Ctrl)
            tm = time.localtime()
            print "%i:%i:%i"%(tm.tm_hour,tm.tm_min,tm.tm_sec), "Constraint 2 done"
            c2_t = round(time.clock()-c2_t,3)
        
            c3_t = time.clock()
            m.addConstrs(z[i] >= quicksum((Ctrl_pop[c,i]*assign[t,c])/(matches*T_n) 
                        for t,c in distance) + T_avg[i] for i in Covar)    
            tm = time.localtime()
            print "%i:%i:%i"%(tm.tm_hour,tm.tm_min,tm.tm_sec), "Constraint 3 done"
            c3_t = round(time.clock()-c3_t,3)
        
            c4_t = time.clock()
            m.addConstrs(z[i] >= -quicksum((Ctrl_pop[c,i]*assign[t,c])/(matches*T_n) 
                        for t,c in distance) - T_avg[i] for i in Covar)    
            tm = time.localtime()
            print "%i:%i:%i"%(tm.tm_hour,tm.tm_min,tm.tm_sec), "Constraint 4 done"
            c4_t = round(time.clock()-c4_t,3)
            
            m.update()
            
            setup_time = round(time.clock() - setup_time, 3)
            
            tm = time.localtime()
            print "%i:%i:%i"%(tm.tm_hour,tm.tm_min,tm.tm_sec), "Start Presolve"
            m.presolve()
            
            runTimes = pd.Series(range(rounds[T_n]), dtype = np.float)
            for r in range(rounds[T_n]):
        #        print "Start Gurobi Optimization"
                m.optimize()
                            
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
    print 'For', T_n, 'treatments using touple dicts, the timing data is:'
    print TimingData
    
    TimingData.to_excel(writer, 'Data Set %i Timings'%(dataSet))


writer.close()
