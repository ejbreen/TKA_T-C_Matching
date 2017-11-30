# Defining new data set definitions with revision risk built in
# The 
T_rev_random_def = T_pop_def 
T_rev_causal_def = T_pop_def

T_rev_random_def <- defData(T_rev_random_def,
                            varname = '5yr_Revision_Rate',
                            dist = 'nonrandom',
                            formula = '1')

