import random
import sys
from hashlib import sha256
from typing import *
import tenseal as ts
import numpy as np

from Crypto.PSI.params import *

def get_dummy_str():
    return f"dummy{random.randint(0, 256)}"

def rand_point(bound, i):
    value = random.randint(0, bound - 1)
    while value == i:
        value = random.randint(0, bound - 1)
    return value


def sha256_to_int32(s: str) -> int:
    s_hash = sha256(s.encode()).digest()[0:4]       # cut the 32 first bits
    return int.from_bytes(s_hash, byteorder=sys.byteorder)

PRIVATE = 0
PUBLIC = 1
def get_context() -> Tuple[ts.Context, ts.Context]:
    private_context = ts.context(ts.SCHEME_TYPE.BFV, poly_modulus_degree=POLY_MODULUS_DEGREE, plain_modulus=PLAIN_MODULUS)
    public_context = ts.context_from(private_context.serialize())
    public_context.make_context_public()
    return private_context, public_context

def windowing(y, modulus):
    return [[pow(y, (i+1) * BASE ** j, modulus)
             if ((i+1) * BASE ** j - 1 < MINIBIN_CAPACITY) else None
             for j in range(LOG_WINDOWING_PARAM)] for i in range(BASE - 1)]

def convert_base(n, b):
    if n < b:
        return [n]
    else:
        return [n % b] + convert_base(n // b, b)

def roots_to_coeffs(roots: List[int], modulus: int):
    coefficients = np.array(1, dtype=np.int64)
    for r in roots:
        coefficients = np.convolve(coefficients, [1, -r]) % modulus
    return coefficients

def get_all_powers(powers_window, power):
    base_coefficient = convert_base(power, BASE)
    powers = []
    j = 0
    for x in base_coefficient:
        if x >= 1:
            powers.append(powers_window[x - 1][j])
        j = j + 1
    return np.prod(np.array(powers))