"""
 This file contains the definition of (max, +) algebra operations and constants.
"""

from enum import Enum
from numbers import Number


class MaxPlusConst(Enum):
    IDENTITY_UNIT_ADD = ''   # it will be named after the consonant
    IDENTITY_UNIT_MULT = ''  # it will be named after the consonant


def maxplus_add(*args : Number):
    return max(args)


def maxplus_mult(*args : Number):
    return sum(args)


def maxplus_add_matrices(A : list[list[Number]],
                         B : list[list[Number]]) -> list[list[Number]]:
    if len(A) != len(B):
        raise Exception('Maxplus Add Error: Matrices are of different sizes.')
    for k in range(len(A)):
        if len(A[k]) != len(B[k]):
            raise Exception('Maxplus Add Error: Matrices are of different sizes.')
    result = [[None for _ in range(len(A[0]))] for __ in range(len(A))]
    for i in range(len(A)):
        for j in range(len(A[i])):
            result[i][j] = maxplus_add(A[i][j], B[i][j])
    return result


def maxplus_mult_matrices(A : list[list[Number]],
                          B : list[list[Number]]) -> list[list[Number]]:
    for k in range(len(B)):
        if len(A) != len(B[k]):
            raise Exception('Maxplus Mult Error: Matrices aren\'t of size MxN and NxP.')
    result = [[None for _ in range(len(A[0]))] for __ in range(len(B))]
    for i in range(len(B)):
        for j in range(len(A[0])):
            result[i][j] = maxplus_add(*[maxplus_mult(A[k][j], B[i][k]) for k in range(len(A))])
    return result
