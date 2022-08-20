from collections import defaultdict

from tools import sha256_to_int32
from params import *

class BasicHashStructure:
    def __init__(self, hash_seed):
        self.FAIL = 0
        self.hash_seed = hash_seed
        self.int_to_value_map = defaultdict(lambda: set())     # maps an integer to a set with the corresponding values
        self.number_of_bins = 2 ** output_bits

    def insert(self, str_item: str) -> int:
        item = sha256_to_int32(str_item)
        self.int_to_value_map[item].add(str_item)
        return item
