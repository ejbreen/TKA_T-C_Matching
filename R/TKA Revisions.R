# Defining new data set definitions with revision risk built in
# The 
T_rev_random_def = T_pop_def 
T_rev_causal_def = T_pop_def

T_rev_random_def <- defData(T_rev_random_def,
                            varname = '5yr_Rev_Rate',
                            dist = 'binary',
                            formula = .005)

T_rev_causal_def <- defData(T_rev_causal_def,
                            varname = '5yr_Rev_Rate',
                            dist = 'nonrandom',
                            formula = 'round(1/(1+exp(-(1))))')

