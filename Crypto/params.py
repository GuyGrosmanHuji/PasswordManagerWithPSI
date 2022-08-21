from math import log2

# modulus parameters for SEAL homomorphic-encryption:
plain_modulus = 536903681                               # 29-bit length - reduces false-positives probability
poly_modulus_degree = 2 ** 13

output_bits = 13

hash_seeds = (5194815923, 1847875896, 2348657587)       # each seed defines a unique murmur hash function.

num_parts = 4       # partitioning parameter - alpha in the article

bin_capacity = 176                                      # assuming server-size is about 60000 ~= 2^16
                                                        # reduces probability for the simple-hashing to fail

windowing_param = 3                                     # ell in the article
base = 2 ** windowing_param
minibin_capacity = int(bin_capacity / num_parts)        # minibin_capacity = B / alpha
logB_ell = int(log2(minibin_capacity) / windowing_param) + 1    # <= 2 ** HE.depth = 16
log_no_hashes = int(log2(len(hash_seeds))) + 1

