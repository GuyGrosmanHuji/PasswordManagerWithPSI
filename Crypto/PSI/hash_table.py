from Crypto.PSI.basic_hash_structure import BasicHashStructure

class HashTable(BasicHashStructure):
    def __init__(self, hash_seed, bin_size):
        super().__init__(hash_seed)
        self.simple_hashed_data = [[None for _ in range(bin_size)] for _ in range(self.number_of_bins)]
        self.appearances = [0 for _ in range(self.number_of_bins)]
        self.bin_size = bin_size

    #  insert item using hash i on position given by location
    def insert(self, str_item: str):
        item = super().insert(str_item)
        for i, seed in enumerate(self.hash_seed):
            loc = self.location(seed, item)
            if self.appearances[loc] < self.bin_size:
                self.simple_hashed_data[loc][self.appearances[loc]] = self.wrap_left_with_idx(item, i)
                self.appearances[loc] += 1
            else:
                raise self.failure_exception
