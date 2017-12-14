#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 12 18:41:31 2017

@author: evan
"""

import pandas as pd
import statsmodels.api as sm

import sys
import os
sys.path.append(os.path.abspath("Python/"))
import FNC

FNC.printMessage("starting timing regression")

Timings = pd.read_excel("Data/timings_both_models_4-128_treatments.xlsx", 2)

Timings = Timings.assign(sqrt_T_n = lambda x: x.T_n**.5)
Timings = Timings.assign(T_n_sqrd = lambda x: x.T_n**2)

Timings = Timings.rename(index = str, columns = {'Setup Time':'setup_time'})
Timings = Timings.rename(index = str, columns = {'Solve Time':'solve_time'})

m_setup = sm.OLS.from_formula('setup_time ~ C(model) + T_n + matches + sqrt_T_n + T_n_sqrd', Timings)
m_c1 = sm.OLS.from_formula('c1_t ~ C(model) + T_n + matches + sqrt_T_n + T_n_sqrd', Timings)
m_c2 = sm.OLS.from_formula('c2_t ~ C(model) + T_n + matches + sqrt_T_n + T_n_sqrd', Timings)
m_c3 = sm.OLS.from_formula('c3_t ~ C(model) + T_n + matches + sqrt_T_n + T_n_sqrd', Timings)
m_c4 = sm.OLS.from_formula('c4_t ~ C(model) + T_n + matches + sqrt_T_n + T_n_sqrd', Timings)
m_solve = sm.OLS.from_formula('solve_time ~ C(model) + T_n + matches + sqrt_T_n + T_n_sqrd', Timings)

models = [m_setup, m_c1, m_c2, m_c3, m_c4, m_solve]

r = m_setup.fit()
results = [r, r, r, r, r, r]

i=0
for m in models:
    results[i]=m.fit()
    i=i+1
