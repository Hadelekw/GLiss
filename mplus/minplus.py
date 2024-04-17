"""
 This file contains the definition of (min, +) algebra operations and constants.
"""

import math

from enum import Enum
from numbers import Number


class MinPlusConst(Enum):
    """
     Constants for (min, +) algebra.
     They are named after the notation.
    """
    ZERO_ELEMENT = 'tau'  # tau = inf
    IDENTITY_ELEMENT = 'e'  # e = zero


def minplus_add(*args : Number):
    return min(args)


def minplus_mult(*args : Number):
    return sum(args)


def minplus_add_matrices(A : list[list[Number]],
                         B : list[list[Number]]) -> list[list[Number]]:
    if len(A) != len(B):
        raise Exception('Minplus Add Error: Matrices are of different sizes.')
    for k in range(len(A)):
        if len(A[k]) != len(B[k]):
            raise Exception('Minplus Add Error: Matrices are of different sizes.')
    result = [[None for _ in range(len(A[0]))] for __ in range(len(A))]
    for i in range(len(A)):
        for j in range(len(A[i])):
            result[i][j] = minplus_add(A[i][j], B[i][j])
    return result


def minplus_mult_matrices(A : list[list[Number]],
                          B : list[list[Number]]) -> list[list[Number]]:
    for k in range(len(B)):
        if len(A) != len(B[k]):
            raise Exception('Minplus Mult Error: Matrices aren\'t of size MxN and NxP.')
    result = [[None for _ in range(len(A[0]))] for __ in range(len(B))]
    for i in range(len(B)):
        for j in range(len(A[0])):
            result[i][j] = minplus_add(*[minplus_mult(A[k][j], B[i][k]) for k in range(len(A))])
    return result
