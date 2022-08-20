from math import log2

plain_modulus = 536903681
poly_modulus_degree = 2 ** 13

number_of_hashes = 3
output_bits = 13

hash_seeds = (5194815923, 1847875896, 2348657587)   # each seed defines a unique murmur hash function.
                                                    # since number_of_hashes = 3,
alpha = 4  # partitioning parameter

bin_capacity = 176

ell = 3     # windowing parameter
base = 2 ** ell
minibin_capacity = int(bin_capacity / alpha)        # minibin_capacity = B / alpha
logB_ell = int(log2(minibin_capacity) / ell) + 1    # <= 2 ** HE.depth = 16
log_no_hashes = int(log2(number_of_hashes)) + 1

