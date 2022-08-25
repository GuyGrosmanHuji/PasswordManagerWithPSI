import pickle
import tenseal as ts
import numpy as np

from typing import List, Union
from tqdm import tqdm

from Crypto.PSI.params import *
from Crypto.PSI.hash_table import HashTable
import Crypto.PSI.utils as tools

tqdm_props = {"n_fmt": "", "total_fmt": ""}

def insert_to_hash_table(passwords: List[str], _print=True) -> HashTable:
    hash_table = HashTable(hash_seeds, bin_capacity)
    [hash_table.insert(item) for item in passwords]

    # the hash table is padded with dummy_msg_server
    number_of_bins = 2 ** output_bits
    with tqdm(total=number_of_bins * bin_capacity,
              disable=(not _print),
              bar_format="{desc}: {percentage:.3f}%|{bar}|") as pbar:
        for i in range(number_of_bins):
            for j in range(bin_capacity):
                if hash_table.data[i][j] is None:
                    dummy_val = 's' + tools.get_dummy_str()
                    hash_table.data[i][j] = tools.sha256_to_int32(dummy_val)
                pbar.update(1)

    return hash_table

def get_poly_coefficients(hashed_passes: HashTable, _print=True):
    poly_coeffs = []
    with tqdm(total=hashed_passes.number_of_bins*num_parts,
              disable=not _print,
              bar_format="{desc}: {percentage:.3f}%|{bar}|") as pbar:
        for i in range(hashed_passes.number_of_bins):
            coeffs_from_bin = []
            # we have alpha polynomials - the hash table is partitioned into alpha parts
            for j in range(num_parts):
                roots = [hashed_passes.data[i][minibin_capacity * j + r] for r in range(minibin_capacity)]
                coeffs_from_bin = coeffs_from_bin + tools.roots_to_coeffs(roots, plain_modulus).tolist()
                pbar.update(1)
            poly_coeffs.append(coeffs_from_bin)
    return poly_coeffs

def deserialize_client_powers(serialized_client_msg: bytes) -> List[List[Union[ts.BFVVector, None]]]:
    received_data = pickle.loads(serialized_client_msg)
    client_public_context = ts.context_from(received_data[0])
    received_enc_query_serialized = received_data[1]
    received_enc_query = [[None for _ in range(log_windowing_param)] for _ in range(base - 1)]
    for i in range(base - 1):
        for j in range(log_windowing_param):
            if (i + 1) * base ** j - 1 < minibin_capacity:
                received_enc_query[i][j] = ts.bfv_vector_from(client_public_context,
                                                              received_enc_query_serialized[i][j])
    return received_enc_query

def calculate_encrypted_powers(encrypted_query):
    powers_query = [None for _ in range(minibin_capacity)]
    for i in range(base - 1):
        for j in range(log_windowing_param):
            if (i + 1) * base ** j - 1 < minibin_capacity:
                powers_query[(i + 1) * base ** j - 1] = encrypted_query[i][j]

    for k in range(minibin_capacity):
        if powers_query[k] is None:
            powers_query[k] = tools.get_all_powers(encrypted_query, k + 1)
    powers_query = powers_query[::-1]
    return powers_query

def get_server_response(powers_query, poly_coefficients):
    server_response = []
    transposed_coeff_matrix = np.transpose(poly_coefficients).tolist()
    for i in range(num_parts):
        dot_product = powers_query[0]
        for j in range(1, minibin_capacity):
            dot_product = dot_product + transposed_coeff_matrix[(minibin_capacity + 1) * i + j] * powers_query[j]
        dot_product = dot_product + transposed_coeff_matrix[(minibin_capacity + 1) * i + minibin_capacity]
        server_response.append(dot_product.serialize())

    response = pickle.dumps(server_response, protocol=None)
    return response
