import random
import math
from typing import Set

import mmh3

from Crypto.PSI.params import *
from Crypto.PSI.basic_hash_structure import BasicHashStructure
import Crypto.PSI.utils as tools

def extract_index(item_left_and_index):
    """
    extracts the index chosen for an item according the the entry value
    """
    return item_left_and_index & (2 ** log_no_hashes - 1)

def reconstruct_item(item_left_and_index, current_location, seed):
    """
    reconstructs an item from the cuckoo hash table according to its index
    in the intersection vector and entry in the cuckoo hash
    """
    item_left = item_left_and_index >> log_no_hashes
    hashed_item_left = mmh3.hash(str(item_left), seed, signed=False) >> (32 - output_bits)
    item_right = hashed_item_left ^ current_location
    return (item_left << output_bits) + item_right

class Cuckoo(BasicHashStructure):
    def __init__(self, hash_seed):
        super().__init__(hash_seed)
        self.recursion_depth = int(8 * math.log(self.number_of_bins) / math.log(2))
        self.data = [None for _ in range(self.number_of_bins)]
        self.insert_index = random.randint(0, len(hash_seeds) - 1)
        self.depth = 0

        self.hash_seed = hash_seed


    def insert(self, str_item: str):
        # map string to int32 and adds to mapping:
        item = super().insert(str_item)

        current_location = self.location(self.hash_seed[self.insert_index], item)
        current_item = self.data[current_location]
        self.data[current_location] = self.wrap_left_with_idx(item, self.insert_index)

        if current_item is None:
            self.insert_index = random.randint(0, len(hash_seeds) - 1)
            self.depth = 0
        else:
            unwanted_index = extract_index(current_item)
            self.insert_index = tools.rand_point(len(hash_seeds), unwanted_index)
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
        int_val = reconstruct_item(self.data[i], i, hash_seeds[self.data[i] % (2 ** log_no_hashes)])
        return self.int_to_value_map[int_val]