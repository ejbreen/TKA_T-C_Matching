#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 12 18:41:31 2017

@author: evan
"""

import pandas as pd
from sklearn import linear_model as linReg

import sys
import os
sys.path.append(os.path.abspath("Python/"))
import FNC

Timings = pd.read_excel("Data/timings_both_models_4-128_treatments.xlsx", 2)

m_setup = linReg.LinearRegression()
m_c1 = linReg.LinearRegression()
m_c2 = linReg.LinearRegression()
m_c3 = linReg.LinearRegression()
m_c4 = linReg.LinearRegression()
m_solve = linReg.LinearRegression()

Params = Timings[['model', 'T_n', 'matches']]

Params = Params.assign(sqrt_T_n = lambda x: x.T_n**.5)
Params = Params.assign(T_n_sqrd = lambda x: x.T_n**2)

m_setup.fit(Params, Timings['Setup Time'])