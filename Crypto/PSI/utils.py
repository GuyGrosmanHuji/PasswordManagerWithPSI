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
    private_context = ts.context(ts.SCHEME_TYPE.BFV, poly_modulus_degree=poly_modulus_degree, plain_modulus=plain_modulus)
    public_context = ts.context_from(private_context.serialize())
    public_context.make_context_public()
    return private_context, public_context

def windowing(y, modulus):
    return [[pow(y, (i+1) * base ** j, modulus) for j in range(log_windowing_param)] for i in range(base - 1)]

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
    base_coefficient = convert_base(power, base)
    powers = []
    j = 0
    for x in base_coefficient:
        if x >= 1:
            powers.append(powers_window[x - 1][j])
        j = j + 1
    return low_depth_mult(powers)

def low_depth_mult(vec):
    depth = len(vec)
    if depth == 1:
        return vec[0]
    if depth == 2:
        return vec[0] * vec[1]
    else:
        if depth % 2:
            vec = []
            for i in range(int(depth / 2)):
                vec.append(vec[2 * i] * vec[2 * i + 1])
            vec.append(vec[depth - 1])
            return low_depth_mult(vec)
        else:
            vec = []
            for i in range(int(depth / 2)):
                vec.append(vec[2 * i] * vec[2 * i + 1])
            return low_depth_mult(vec)
