using JuMP
using Gurobi
using DataArrays
using DataFrames
using Gadfly

T_pop_full = readcsv("")
C_pop_full = readcsv("")

function shrink_pop(T_pop_full, C_pop_full, T_n)
    T_pop = T_pop_full[1:T_n, :]
    C_pop = C_pop_full[1:T_n*30, :]
    return T_pop, C_pop

T_n = 16
T_pop, C_pop = shrink_pop(T_pop_full, C_pop_full, T_n)

m = Model(solver = GurobiSolver())

# i=treatment case, j=potential control case, k=covariate number
# I, J, K = iterables over their domains
I = 1:T_n
J = 1:T_n*30
K = 1:size(T_pop, 0)

@variable(m, assign[I, J], Bin)

@objective(m, Min, )
