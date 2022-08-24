import random
import sys
from hashlib import sha256
from typing import *
import tenseal as ts
import numpy as np
from params import *

def get_dummy_str():
    return f"dummy{random.randint(0, 256)}"

def rand_point(bound, i):
    """
    :param bound: an integer
    :param i: an integer less than bound
    :return: a uniform integer from [0, bound - 1], distinct from i
    """
    value = random.randint(0, bound - 1)
    while value == i:
        value = random.randint(0, bound - 1)
    return value


def sha256_to_int32(s: str) -> int:
    """
    returns an integer corresponding to the sha-256 value of s
    :param s: a string
    :return: integer value of sha256(s)
    """
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
    """
    :param y: an integer
    :param modulus: a modulus integer
    :return: a matrix associated to y, where we put y ** (i+1)*base ** j mod modulus in the (i,j) entry
    """
    return [[pow(y, (i+1) * base ** j, modulus) for j in range(logB_ell)] for i in range(base-1)]

def roots_to_coeffs(roots: List[int], modulus: int):
    """
    :param roots: an array of integers
    :param modulus: an integer
    :return: coefficients of a polynomial whose roots are roots modulo modulus
    """
    coefficients = np.array(1, dtype=np.int64)
    for r in roots:
        coefficients = np.convolve(coefficients, [1, -r]) % modulus
    return coefficients

def int2base(n, b):
    """
    :param n: an integer
    :param b: a base
    :return: an array of coefficients from the base decomposition of an integer n with coeff[i] being the coeff of b ** i
    """
    if n < b:
        return [n]
    else:
        return [n % b] + int2base(n // b, b)

def low_depth_multiplication(vector):
    """
    :param: vector: a vector of integers
    :return: an integer representing the multiplication of all the integers from vector
    """
    L = len(vector)
    if L == 1:
        return vector[0]
    if L == 2:
        return vector[0] * vector[1]
    else:
        if L % 2 == 1:
            vec = []
            for i in range(int(L / 2)):
                vec.append(vector[2 * i] * vector[2 * i + 1])
            vec.append(vector[L-1])
            return low_depth_multiplication(vec)
        else:
            vec = []
            for i in range(int(L / 2)):
                vec.append(vector[2 * i] * vector[2 * i + 1])
            return low_depth_multiplication(vec)


def get_all_powers(powers_window, power):
    """
    :param: window: a matrix of integers as powers of y; in the protocol is the matrix with entries window[i][j] = [y ** i * base ** j]
    :param: exponent: an integer, will be an exponent <= logB_ell
    :return: y ** exponent
    """
    e_base_coef = int2base(power, base)
    necessary_powers = []   # len(necessary_powers) <= 2 ** HE.depth
    j = 0
    for x in e_base_coef:
        if x >= 1:
            necessary_powers.append(powers_window[x - 1][j])
        j = j + 1
    return low_depth_multiplication(necessary_powers)
