######################################################
#                                                    #
#             Author: Shankar Ramharack              #
#                                                    #
######################################################
#                                                    #
#    [Description]:                                  #
#    Implements a RMI model for Coral Reef           #
#                                                    #
######################################################


import numpy as np

def calculate_interaction_count(P_ij, P_kl, I_jl):
    return P_ij * P_kl * I_jl

def calculate_matrices(num_coordinates, num_species, reproduction_coeff, mortality_coeff, interaction_coeff):
    # Reproduction rate matrix R
    R = np.full((num_coordinates, num_species), reproduction_coeff)

    # Mortality rate matrix M
    M = np.full((num_coordinates, num_species), mortality_coeff)

    # Interaction matrix I
    I = np.full((num_species, num_species), interaction_coeff)

    # Set the diagonal elements of the interaction matrix to zero
    np.fill_diagonal(I, 0)

    return R, M, I

def simulate_ecosystem(P, R, M, I):
    num_coordinates, num_species = P.shape
    P_new = np.copy(P)

    for i in range(num_coordinates):
        for j in range(num_species):
            # Step 1: Reproduction
            P_new[i, j] += np.round(R[i, j] * P_new[i, j])

            # Step 2: Mortality
            if P_new[i, j] <= np.round(M[i, j] * P_new[i, j]):
                P_new[i, j] = 0
            else:
                P_new[i, j] -= np.round(M[i, j] * P_new[i, j])

            # Step 3: Interactions
            for k in range(num_coordinates):
                if k != i:
                    for l in range(num_species):
                        interaction_count = calculate_interaction_count(P[i, j], P[k, l], I[j, l])
                        P_new[i, j] -= np.round(interaction_count)
                        P_new[k, l] += np.round(interaction_count)

    return P_new

# Example usage
num_coordinates = 3
num_species = 3
reproduction_coeff = 0.2
mortality_coeff = 0.1
interaction_coeff = 0.5

P = np.array([
    [100, 50, 200],
    [150, 80, 120],
    [90, 70, 180]
])

R, M, I = calculate_matrices(num_coordinates, num_species, reproduction_coeff, mortality_coeff, interaction_coeff)
P_new = simulate_ecosystem(P, R, M, I)

print("Initial population:")
print(P)
print("\nUpdated population:")
print(P_new)
