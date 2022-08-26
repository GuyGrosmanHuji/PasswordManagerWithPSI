from math import log2

# modulus parameters for SEAL homomorphic-encryption:
PLAIN_MODULUS = 536903681                               # 29-bit length - reduces false-positives probability
POLY_MODULUS_DEGREE = 2 ** 13

OUTPUT_BITS = 13                                        # For murmur-hashing true value retrieval

HASH_SEEDS = (5194815923, 1847875896, 2348657587)       # each seed defines a unique murmur hash function.
                                                        # The values were chosen arbitrarily

NUM_PARTS = 4                                           # partitioning parameter - alpha in the article

BIN_CAPACITY = 176                                      # assuming server-size is about 250000 ~= 2^18
                                                        # The following sizes are useful: 176 - server size 2^18,
                                                        #  536 - server size 2^20, 1832 - server size 2^22
                                                        # reduces probability for the simple-hashing to fail

WINDOWING_PARAM = 3                                     # ell in the article
BASE = 2 ** WINDOWING_PARAM
MINIBIN_CAPACITY = int(BIN_CAPACITY / NUM_PARTS)        # minibin_capacity = B / alpha
LOG_WINDOWING_PARAM = int(log2(MINIBIN_CAPACITY) / WINDOWING_PARAM) + 1    # <= 2 ** HE.depth = 16
LOG_NO_HASHES = int(log2(len(HASH_SEEDS))) + 1
