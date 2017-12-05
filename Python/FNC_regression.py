# -*- coding: utf-8 -*-
"""
Created on Tue Dec 05 14:48:06 2017

@author: Evan
"""

import pandas as pd
from sklearn import linear_model as linReg

import sys
import os
sys.path.append(os.path.abspath("Python/"))
import FNC

def compare_MLR(C_pop, T_pop, C_matched):
    
    FNC.printMessage("starting multiple linear regression")
    
    MLR_raw, MLR_sub = linReg.LinearRegression(), linReg.LinearRegression()
    
    Raw = T_pop.append(C_pop)
    Raw_feat = Raw.drop('AGE', axis=1)
    Raw_resp = Raw['AGE']
    
    Sub = T_pop.append(C_matched)
    Sub_feat = Sub.drop('AGE', axis=1)
    Sub_resp = Sub['AGE']
    
    MLR_raw.fit(Raw_feat, Raw_resp)
    MLR_sub.fit(Sub_feat, Sub_resp)
    
    temp = pd.Series(MLR_raw.coef_, index = Raw_feat.columns)
    temp = temp.append(pd.Series({"const":MLR_raw.intercept_}))
    
    temp2 = pd.Series(MLR_sub.coef_, index = Sub_feat.columns)
    temp2 = temp2.append(pd.Series({"const":MLR_sub.intercept_}))
    
    Models = pd.DataFrame({"raw data MRL":temp, "subset MRL":temp2})
    
    Scores = pd.Series({"raw data MRL":MLR_raw.score(Raw_feat, Raw_resp),
                        "subset MRL":MLR_sub.score(Sub_feat, Sub_resp)})
    Scores.name = "R^2 Score"
    
    Models = Models.append(Scores)
        
    return Models, MLR_raw, MLR_sub

