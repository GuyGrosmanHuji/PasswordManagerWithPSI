import pickle
import tenseal as ts
import numpy as np

from typing import List, Union
from tqdm import tqdm

from Crypto.PSI.params import *
from Crypto.PSI.hash_table import HashTable
import Crypto.PSI.utils as tools


def insert_to_hash_table(passwords: List[str], _print=True) -> HashTable:
    hash_table = HashTable(HASH_SEEDS, BIN_CAPACITY)
    [hash_table.insert(item) for item in passwords]

    # the hash table is padded with dummy_msg_server
    number_of_bins = 2 ** OUTPUT_BITS
    with tqdm(total=number_of_bins * BIN_CAPACITY,
              disable=(not _print),
              bar_format="{desc}: {percentage:.3f}%|{bar}|") as pbar:
        for i in range(number_of_bins):
            for j in range(BIN_CAPACITY):
                if hash_table.data[i][j] is None:
                    dummy_val = 's' + tools.get_dummy_str()
                    hash_table.data[i][j] = tools.sha256_to_int32(dummy_val)
                pbar.update(1)

    return hash_table

def get_poly_coefficients(hashed_passes: HashTable, _print=True):
    poly_coeffs = []
    with tqdm(total=hashed_passes.number_of_bins * NUM_PARTS,
              disable=not _print,
              bar_format="{desc}: {percentage:.3f}%|{bar}|") as pbar:
        for i in range(hashed_passes.number_of_bins):
            coeffs_from_bin = []
            # we have alpha polynomials - the hash table is partitioned into alpha parts
            for j in range(NUM_PARTS):
                roots = [hashed_passes.data[i][MINIBIN_CAPACITY * j + r] for r in range(MINIBIN_CAPACITY)]
                coeffs_from_bin = coeffs_from_bin + tools.roots_to_coeffs(roots, PLAIN_MODULUS).tolist()
                pbar.update(1)
            poly_coeffs.append(coeffs_from_bin)
    return poly_coeffs

def deserialize_client_powers(serialized_client_msg: bytes) -> List[List[Union[ts.BFVVector, None]]]:
    received_data = pickle.loads(serialized_client_msg)
    client_public_context = ts.context_from(received_data[0])
    received_enc_query_serialized = received_data[1]
    received_enc_query = [[None for _ in range(LOG_WINDOWING_PARAM)] for _ in range(BASE - 1)]
    for i in range(BASE - 1):
        for j in range(LOG_WINDOWING_PARAM):
            if (i + 1) * BASE ** j - 1 < MINIBIN_CAPACITY:
                received_enc_query[i][j] = ts.bfv_vector_from(client_public_context,
                                                              received_enc_query_serialized[i][j])
    return received_enc_query

def calculate_encrypted_powers(encrypted_query):
    powers_query = [None for _ in range(MINIBIN_CAPACITY)]
    for i in range(BASE - 1):
        for j in range(LOG_WINDOWING_PARAM):
            if (i + 1) * BASE ** j - 1 < MINIBIN_CAPACITY:
                powers_query[(i + 1) * BASE ** j - 1] = encrypted_query[i][j]

    for k in range(MINIBIN_CAPACITY):
        if powers_query[k] is None:
            powers_query[k] = tools.get_all_powers(encrypted_query, k + 1)
    powers_query = powers_query[::-1]
    return powers_query

def get_server_response(powers_query, poly_coefficients):
    server_response = []
    transposed_coeff_matrix = np.transpose(poly_coefficients).tolist()
    for i in range(NUM_PARTS):
        dot_product = powers_query[0]
        for j in range(1, MINIBIN_CAPACITY):
            dot_product = dot_product + transposed_coeff_matrix[(MINIBIN_CAPACITY + 1) * i + j] * powers_query[j]
        dot_product = dot_product + transposed_coeff_matrix[(MINIBIN_CAPACITY + 1) * i + MINIBIN_CAPACITY]
        server_response.append(dot_product.serialize())

    response = pickle.dumps(server_response, protocol=None)
    return response
