using JuMP
using Gurobi
using DataArrays
using DataFrames
using CSV
using Gadfly
using Distances
using PyCall


T_pop_full = CSV.read("T_pop.csv")[:,2:end]
C_pop_full = CSV.read("C_pop.csv")[:,2:end]

covars = size(T_pop_full,2)

function shrink_pop(T_pop_full, C_pop_full, T_n)
    T_pop = T_pop_full[1:T_n, :]
    C_pop = C_pop_full[1:T_n*30, :]
    return T_pop, C_pop
end

T_n = 16
T_pop, C_pop = shrink_pop(T_pop_full, C_pop_full, T_n)
matches = 5

m = Model(solver = GurobiSolver())

# i=treatment case, j=potential control case, k=covariate number
# I, J, K = iterables over their domains
I = 1:T_n
J = 1:T_n*30
K = 1:covars
weight = ones(covars)

@variable(m, assign[I, J], Bin)
@variable(m, z[K])

@objective(m, Min, sum(assign.*dist)) + sum(weight[k]*z[k] for k=K))

@constraint(m, c1[i=I], sum(assign[i, j] for j=J) >= matches)
@constraint(m, c2[j=J], sum(assign[i, j] for i=I) <= 1)

@constraint(m, c3[k=K], sum() >= z[k] )
