import random
import math
from typing import Set, Optional, List

import mmh3

from Crypto.PSI.params import *
from Crypto.PSI.basic_hash_structure import BasicHashStructure
import Crypto.PSI.utils as tools

def extract_index(item_left_and_index):
    """
    extracts the index chosen for an item according the the entry value
    """
    return item_left_and_index & (2 ** LOG_NO_HASHES - 1)

def reconstruct_item(wrapped_item, current_location, seed):
    """
    reconstructs an item from the cuckoo hash table according to its index
    in the intersection vector and entry in the cuckoo hash
    """
    left_part = wrapped_item >> LOG_NO_HASHES
    hashed_left_part = mmh3.hash(str(left_part), seed, signed=False) >> (32 - OUTPUT_BITS)
    right_part = hashed_left_part ^ current_location
    return (left_part << OUTPUT_BITS) + right_part

class Cuckoo(BasicHashStructure):
    def __init__(self, hash_seed):
        super().__init__(hash_seed)
        self.recursion_depth = int(8 * math.log(self.number_of_bins) / math.log(2))
        self.data: List[Optional[int]] = [None for _ in range(self.number_of_bins)]
        self.insert_index = random.randint(0, len(HASH_SEEDS) - 1)
        self.depth = 0

        self.hash_seed = hash_seed


    def insert(self, str_item: str):
        # map string to int32 and adds to mapping:
        item = super().insert(str_item)

        current_location = self.location(self.hash_seed[self.insert_index], item)
        current_item = self.data[current_location]
        self.data[current_location] = self.wrap_left_with_idx(item, self.insert_index)

        if current_item is None:
            self.insert_index = random.randint(0, len(HASH_SEEDS) - 1)
            self.depth = 0
        else:
            unwanted_index = extract_index(current_item)
            self.insert_index = tools.rand_point(len(HASH_SEEDS), unwanted_index)
            if self.depth < self.recursion_depth:
                self.depth += 1
                jumping_item = reconstruct_item(current_item, current_location, self.hash_seed[unwanted_index])
                self.insert(jumping_item)
            else:
                raise self.failure_exception

    def reconstruct_item_from_intersection(self, i) -> Set:
        """
        :param i: The index i is the location of the element in the intersection
        :return: The element matching element
        """
        int_val = reconstruct_item(self.data[i], i, HASH_SEEDS[self.data[i] % (2 ** LOG_NO_HASHES)])
        return self.int_to_value_map[int_val]