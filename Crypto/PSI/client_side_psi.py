import pickle
import tenseal as ts
from typing import List, Set, Tuple

from params import *
from cuckoo_hash import Cuckoo

import tools

WindowTensor = List[List[List[int]]]

def get_cuckoo_items(passwords: List[str]) -> Cuckoo:
    """
    :param passwords: a list of strings, each represents a password
    :return: A Cuckoo object with the passwords
    """
    cuckoo = Cuckoo(hash_seeds)
    [cuckoo.insert(pswd) for pswd in passwords]

    # Fill empty bins with a dummy password:
    for bin_ in range(len(cuckoo.array)):
        if cuckoo.array[bin_] is None:
            cuckoo.array[bin_] = tools.sha256_to_int32(tools.get_dummy_str())
    return cuckoo


def get_windowing_tensor(c: Cuckoo) -> WindowTensor:
    """
    :param c: a Cuckoo object
    :return: A tensor, each row contains window vector of c's items
    """
    return list(map(lambda pwd: tools.windowing(pwd, plain_modulus),
                    c.array))


def prepare_encrypted_message(windowing_tensor: WindowTensor, context_tuple: Tuple[ts.Context, ts.Context]) -> bytes:
    """
    :return: Encrypted message to be sent, containing the windowing tensor and the context
    """
    private_context, public_context = context_tuple
    plain_query = [None for _ in range(len(windowing_tensor))]
    enc_query = [[None for _ in range(logB_ell)] for _ in range(1, base)]

    # We create the <<batched>> query to be sent to the server
    # By our choice of parameters, number of bins = poly modulus degree (m/N =1), so we get (base - 1) * logB_ell ciphertexts
    for j in range(logB_ell):
        for i in range(base - 1):
            if (i + 1) * base ** j - 1 < minibin_capacity:
                for k in range(len(windowing_tensor)):
                    plain_query[k] = windowing_tensor[k][i][j]
                enc_query[i][j] = ts.bfv_vector(private_context, plain_query)

    enc_query_serialized = [[None for _ in range(logB_ell)] for _ in range(1, base)]
    for j in range(logB_ell):
        for i in range(base - 1):
            if (i + 1) * base ** j - 1 < minibin_capacity:
                enc_query_serialized[i][j] = enc_query[i][j].serialize()

    context_serialized = public_context.serialize()
    message_to_be_sent = [context_serialized, enc_query_serialized]
    return pickle.dumps(message_to_be_sent, protocol=None)

def decrypt_server_answer(answer: bytes, context_tuple: Tuple[ts.Context, ts.Context]) -> List[int]:
    ciphertexts = pickle.loads(answer)
    decrypts = []
    for ct in ciphertexts:
        decrypts.append(ts.bfv_vector_from(context_tuple[tools.PRIVATE], ct).decrypt())

    return decrypts

def find_intersection(decrypted_answer: List[List[int]], cuckoo: Cuckoo) -> Set[str]:
    client_intersection = set()
    for i in range(num_parts):
        for j in range(poly_modulus_degree):
            if decrypted_answer[i][j] == 0:
                common_values = cuckoo.reconstruct_item_from_intersection(j)
                client_intersection = client_intersection.union(common_values)

    return client_intersection
