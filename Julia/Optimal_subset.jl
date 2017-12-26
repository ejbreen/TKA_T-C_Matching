using JuMP
using Gurobi
using DataArrays
using DataFrames
using CSV
using Gadfly
using Distances
using PyCall


function get_pops(T_n, dataset)
    T_pop_full = CSV.read("T_pop_$dataset.csv")[:,2:end]
    C_pop_full = CSV.read("C_pop_$dataset.csv")[:,2:end]
    # until I can figure out a way to get the distance calculation in julia, I am
    # doing it in python then transfering it over in a csv
    dist_full = readcsv("dist_$dataset.csv")
    T_pop = T_pop_full[1:T_n, :]
    C_pop = C_pop_full[1:T_n*30, :]
    dist = dist_full[1:T_n, 1:T_n*30]
    return T_pop, C_pop, dist
end

function shrink_pop(T_pop, C_pop, dist, T_n)
    T_pop = T_pop[1:T_n, :]
    C_pop = C_pop[1:T_n*30, :]
    dist = dist[1:T_n, 1:T_n*30]
    return T_pop, C_pop, dist
end

function subset_match(T_pop, C_pop, dist, matches)

    covars = size(T_pop,2)
    T_n = size(T_pop, 1)

    T_pop_mean = ones(covars)
    for col in 1:covars
        T_pop_mean[col] = mean(convert(Array, T_pop[:,col]))
    end

    m = Model(solver = GurobiSolver())

    # i=treatment case, j=potential control case, k=covariate number
    # I, J, K = iterables over their domains
    I = 1:T_n
    J = 1:T_n*30
    K = 1:covars
    weight = ones(covars)

    @variable(m, assign[I, J], Bin)
    @variable(m, z[K])

    @objective(m, Min, sum(assign[i,j]*dist[i,j] for i=I, j=J) +
                        sum(weight[k]*z[k] for k=K))

    @constraint(m, c1[i=I], sum(assign[i, j] for j=J) >= matches)
    @constraint(m, c2[j=J], sum(assign[i, j] for i=I) <= 1)

    @constraint(m, c3[k=K],  sum((get(C_pop[j,k])*assign[i,j])/(matches*T_n)
                        for j=J, i=I) - T_pop_mean[k] <= z[k] )
    @constraint(m, c4[k=K], -sum((get(C_pop[j,k])*assign[i,j])/(matches*T_n)
                        for j=J, i=I) + T_pop_mean[k] <= z[k] )

    status = solve(m)
    matched = ones(J)
    for j = J
    matched[j] = sum(getvalue(assign[i,j]) for i = I)
    end

    C_matched = C_pop[1,:]
    for x=1:T_n*matches
    push!(C_matched, zeros(21))
    end
    deleterows!(C_matched,1)
    C_matched = copy(C_matched)
    p = 1
    for j = J
        if matched[j]==1
            C_matched[p,:] = C_pop[j,:]
            p = p+1
        end
    end

    CSV.write("Results/C_1_matched_$T_n.csv", C_matched)
    return T_pop, C_pop, C_matched
end

function main()
    T_n_max = 500
    T_pop_max, C_pop_max, dist_max = get_pops(T_n_max, 1)
    T_n, matches = 4, 5
    T_pop, C_pop, dist = shrink_pop(T_pop_max, C_pop_max, dist_max, T_n)
    T_pop, C_pop, C_matched = subset_match(T_pop, C_pop, dist, matches)
end
