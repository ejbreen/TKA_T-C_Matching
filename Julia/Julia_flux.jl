include("Optimal_subset.jl")

T_n_max = 500
T_pop_max, C_pop_max, dist_max = get_pops(T_n_max, 1)

T_n, matches = 4, 5
T_pop, C_pop, dist = shrink_pop(T_pop_max, C_pop_max, dist_max, T_n)
T_pop, C_pop, C_matched = subset_match(T_pop, C_pop, dist, matches)

T_n, matches = 500, 5
T_pop, C_pop, dist = shrink_pop(T_pop_max, C_pop_max, dist_max, T_n)
T_pop, C_pop, C_matched = subset_match(T_pop, C_pop, dist, matches)
