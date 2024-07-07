import math
import numpy as np

from mplus import *


# TODO:
# 1. Error handling in no_signal_solve function
# 2. Handle signal_solve method


def no_signal_solve(A : np.ndarray,
                    k_0 : int,
                    x_0_0 : int = 0,
                    x_0 : np.ndarray = None) -> float:
    if A.shape[0] != A.shape[1]:
        raise ValueError('No_signal_solve: matrix not a square.')
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
                 P : np.ndarray) -> float:
    pass
