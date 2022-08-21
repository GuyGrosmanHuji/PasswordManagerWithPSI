from collections import defaultdict
import mmh3
import math

from tools import sha256_to_int32
from params import *

log_no_hashes = int(math.log(len(hash_seeds)) / math.log(2)) + 1
mask_of_power_of_2 = 2 ** output_bits - 1

class BasicHashStructure:
    def __init__(self, hash_seed):
        self.hash_seed = hash_seed
        self.int_to_value_map = defaultdict(lambda: set())     # maps an integer to a set with the corresponding values
        self.number_of_bins = 2 ** output_bits
        self.failure_exception = Exception("Hashing failure, please run the PSI again")

    def insert(self, str_item: str) -> int:
        """
        inserts str_item to an internal mapping between strings and their 32-bit values
        :return: the 32bit integer value of the string
        """
        item = sha256_to_int32(str_item)
        self.int_to_value_map[item].add(str_item)
        return item

    #The hash family used for Cuckoo hashing relies on the Murmur hash family (mmh3)
    @staticmethod
    def location(seed, item) -> int:
        """
        returns a location for item according to the murmur hash algorithm corresponding to the given seed
        :return: mmh_seed(item_left) xor item_right, where item = item_left || item_right
        """
        item_left = item >> output_bits
        item_right = item & mask_of_power_of_2
        hash_item_left = mmh3.hash(str(item_left), seed, signed=False) >> (32 - output_bits)
        return hash_item_left ^ item_right

    @staticmethod
    def wrap_left_with_idx(item, index) -> int:
        """
        :return: item_left || index
        """
        return ((item >> output_bits) << log_no_hashes) + index