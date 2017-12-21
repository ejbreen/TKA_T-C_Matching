using JuMP
using Gurobi
using DataArrays
using DataFrames
using Gadfly

T_pop_full = readcsv("T_pop.csv")
C_pop_full = readcsv("C_pop.csv")

covars = size(T_pop_full,2)-1

T_pop = convert(DataFrame,T_pop_full[2:size(T_pop_full,1),2:size(T_pop_full,2)])

function shrink_pop(T_pop_full, C_pop_full, T_n)
    T_pop = T_pop_full[1:T_n, :]
    C_pop = C_pop_full[1:T_n*30, :]
    return T_pop, C_pop

T_n = 16
T_pop, C_pop = shrink_pop(T_pop_full, C_pop_full, T_n)
matches = 5

m = Model(solver = GurobiSolver())

# i=treatment case, j=potential control case, k=covariate number
# I, J, K = iterables over their domains
I = 1:T_n
J = 1:T_n*30
K = 1:covars

@variable(m, assign[I, J], Bin)
@variable(m, z[k])

@objective(m, Min, sum(assign.*dist)) + sum(weight[k]*z[k] for k=K))

@constraint(m, c1[i=I], sum(assign[i, j] for j=J) >= matches)
@constraint(m, c2[j=J], sum(assign[i, j] for i=I) <= 1)

@constraint(m, c3[k=K], sum() >= z[k] )
