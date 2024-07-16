import math
import numpy as np

from mplus import *


def no_signal_solve(A : np.ndarray,
                    k_0 : int,
                    x_0_0 : int = 0,
                    x_0 : np.ndarray = None) -> float:
    """ Finds a solution to Green Light problem for system without traffic lights. """
    if A.shape[0] != A.shape[1]:
        raise ValueError('No_signal_solve: matrix A is not square.')
    if x_0 is None:
        _ = [x_0_0,]
        _.extend([math.inf for _ in range(A.shape[0] - 1)])
        x_0 = np.transpose(np.array([_]))
    result = minplus.power_matrix(A, k_0)
    result = minplus.mult_matrices(result, x_0)
    return result[result.shape[0] - 1][0]


def signal_solve(A : np.ndarray,
                 T : np.ndarray,
                 R : np.ndarray,
                 P : np.ndarray,
                 x_0_0 : int = 0,
                 x_0 : np.ndarray = None) -> float:
    """ Finds a solution to Green Light problem for system with traffic lights. """
    if A.shape[0] != A.shape[1]:
        raise ValueError('No_signal_solve: matrix A is not square.')
    if A.shape[0] != T.shape[0] or T.shape[1] != 1:
        raise ValueError('Signal_solve: matrix T is not a proper Nx1 vector.')
    if A.shape != R.shape:
        raise ValueError('Signal_solve: matrix R is not NxN like matrix A.')
    if A.shape != P.shape:
        raise ValueError('Signal_solve: matrix P is not NxN like matrix A.')
    if x_0 is None:
        _ = [x_0_0,]
        _.extend([math.inf for _ in range(A.shape[0] - 1)])
        x_0 = np.transpose(np.array([_]))
    e = np.transpose(np.array([[0 for _ in range(A.shape[0])]]))
    x_k = x_0
    for _ in range(A.shape[0]):
        C = A + R
        Z = -(minplus.add_matrices(
            minplus.modulo_matrices((A + P + minplus.mult_matrices(e, np.transpose(x_k))), T), R))
        B = C + Z
        x_k = minplus.mult_matrices(B, x_k)
    return x_k[A.shape[0] - 1][0]


def shortest_signal_solve(A : np.ndarray,
                          T : np.ndarray,
                          R : np.ndarray,
                          P : np.ndarray,
                          k_0 : int,
                          x_0_0 : int = 0,
                          x_0 : np.ndarray = None) -> float:
    """ Finds a solution to Green Light problem for system with traffic lights via shortest path. """
    if A.shape[0] != A.shape[1]:
        raise ValueError('No_signal_solve: matrix A is not square.')
    if A.shape[0] != T.shape[0] or T.shape[1] != 1:
        raise ValueError('Signal_solve: matrix T is not a proper Nx1 vector.')
    if A.shape != R.shape:
        raise ValueError('Signal_solve: matrix R is not NxN like matrix A.')
    if A.shape != P.shape:
        raise ValueError('Signal_solve: matrix P is not NxN like matrix A.')
    if x_0 is None:
        _ = [x_0_0,]
        _.extend([math.inf for _ in range(A.shape[0] - 1)])
        x_0 = np.transpose(np.array([_]))
    e = np.transpose(np.array([[0 for _ in range(A.shape[0])]]))
    x_k = x_0
    Bs = []
    for _ in range(k_0 - 1):
        C = A + R
        Z = -(minplus.add_matrices(
            minplus.modulo_matrices((A + P + minplus.mult_matrices(e, np.transpose(x_k))), T), R))
        B = C + Z
        Bs.append(B)
        x_k = minplus.mult_matrices(B, x_k)
    Bj = Bs[0]
    for B in Bs[1:]:
        Bj = minplus.mult_matrices(Bj, B)
    return (minplus.mult_matrices(Bj, x_0))[A.shape[0] - 1][0]
