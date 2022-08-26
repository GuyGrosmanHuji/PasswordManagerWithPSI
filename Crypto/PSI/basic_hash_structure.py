from collections import defaultdict
import mmh3
import math

from Crypto.PSI.utils import sha256_to_int32
from Crypto.PSI.params import *

LOG_NUM_OF_HASHES = int(math.log(len(HASH_SEEDS)) / math.log(2)) + 1
MASK = 2 ** OUTPUT_BITS - 1

class BasicHashStructure:
    def __init__(self, hash_seed):
        self.hash_seed = hash_seed
        self.int_to_value_map = defaultdict(lambda: set())     # maps an integer to a set with the corresponding values
        self.number_of_bins = 2 ** OUTPUT_BITS
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
        :return: mmh_seed(left_part) xor right_part, where item = left_part || right_part
        """
        left_part = item >> OUTPUT_BITS
        right_part = item & MASK
        hash_left_part = mmh3.hash(str(left_part), seed, signed=False) >> (32 - OUTPUT_BITS)
        return hash_left_part ^ right_part

    @staticmethod
    def wrap_left_with_idx(item, index) -> int:
        """
        :return: left_part || index
        """
        return ((item >> OUTPUT_BITS) << LOG_NUM_OF_HASHES) + index