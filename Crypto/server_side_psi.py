import pickle
import random
import tenseal as ts
import numpy as np

from typing import List, Set, Tuple, Union

from params import *
from hash_table import HashTable

import tools

def insert_to_hash_table(passwords: List[str]) -> HashTable:
    hash_table = HashTable(hash_seeds, bin_capacity)
    [hash_table.insert(item) for item in passwords]

    # simple_hashed_data is padded with dummy_msg_server
    number_of_bins = 2 ** output_bits
    for i in range(number_of_bins):
        for j in range(bin_capacity):
            if hash_table.simple_hashed_data[i][j] is None:
                dummy_val = 's' + tools.get_dummy_str()
                hash_table.simple_hashed_data[i][j] = tools.sha256_to_int32(dummy_val)

    return hash_table

def get_poly_coefficients(hashed_passes: HashTable):
    poly_coeffs = []
    for i in range(hashed_passes.number_of_bins):
        # we create a list of coefficients of all minibins from concatenating the list of coefficients of each minibin
        coeffs_from_bin = []
        # we have alpha polynomials - the hash table is partitioned into alpha parts
        for j in range(alpha):
            roots = [hashed_passes.simple_hashed_data[i][minibin_capacity * j + r] for r in range(minibin_capacity)]
            coeffs_from_bin = coeffs_from_bin + tools.roots_to_coeffs(roots, plain_modulus).tolist()
        poly_coeffs.append(coeffs_from_bin)

    return poly_coeffs

def deserialize_client_powers(serialized_client_msg: bytes) -> List[List[Union[ts.BFVVector, None]]]:
    received_data = pickle.loads(serialized_client_msg)
    srv_context = ts.context_from(received_data[0])
    received_enc_query_serialized = received_data[1]
    received_enc_query = [[None for _ in range(logB_ell)] for _ in range(base - 1)]
    for i in range(base - 1):
        for j in range(logB_ell):
            if (i + 1) * base ** j - 1 < minibin_capacity:
                received_enc_query[i][j] = ts.bfv_vector_from(srv_context, received_enc_query_serialized[i][j])
    return received_enc_query

def calculate_encrypted_powers(encrypted_query):
    query_powers = [None for _ in range(minibin_capacity)]
    for i in range(base - 1):
        for j in range(logB_ell):
            if (i + 1) * base ** j - 1 < minibin_capacity:
                query_powers[(i + 1) * base ** j - 1] = encrypted_query[i][j]

    for k in range(minibin_capacity):
        if query_powers[k] is None:
            query_powers[k] = tools.power_reconstruct(encrypted_query, k + 1)
    query_powers = query_powers[::-1]
    return query_powers

def get_server_response(query_powers, poly_coefficients):
    srv_answer = []
    transposed_poly_coeffs = np.transpose(poly_coefficients).tolist()
    for i in range(alpha):
        # the rows with index multiple of (B/alpha+1) have only 1's
        dot_product = query_powers[0]
        for j in range(1, minibin_capacity):
            dot_product = dot_product + transposed_poly_coeffs[(minibin_capacity + 1) * i + j] * query_powers[j]
        dot_product = dot_product + transposed_poly_coeffs[(minibin_capacity + 1) * i + minibin_capacity]
        srv_answer.append(dot_product.serialize())

    # The answer to be sent to the client is prepared
    response = pickle.dumps(srv_answer, protocol=None)
    return response
