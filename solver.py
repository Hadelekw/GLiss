import numpy as np

from mplus import *


# TODO:
# 1. Error handling in no_signal_solve function
# 2. Handle signal_solve method


def no_signal_solve(A : np.ndarray,
                    k_0 : int,
                    end : int = None,
                    x_0 : np.ndarray = None) -> float:
    result = minplus.power_matrix(A, k_0)
    print(result)
    result = minplus.mult_matrices(result, x_0)
    return result[end]
