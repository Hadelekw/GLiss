import math
import numpy as np


def _swap_rows(A : np.ndarray,
              row_1 : int,
              row_2 : int) -> np.ndarray:
    """ Swaps two rows in an array. """
    A[[row_1, row_2], :] = A[[row_2, row_1], :]
    return A


def _swap_columns(A : np.ndarray,
                  column_1 : int,
                  column_2 : int) -> np.ndarray:
    """ Swaps two columns in an array. """
    A[:, [column_1, column_2]] = A[:, [column_2, column_1]]
    return A


def find_sources(A : np.ndarray) -> list[int]:
    """ 
    We assume that the source in an array may only have one outward connection. 
    We return a list of possible sources based on that assumption. An outward
    connection is defined via columns of the matrix.
    """
    result = []
    for j in range(A.shape[1]):
        count = 0
        for value in A[:, j]:
            if math.inf > value > 0:
                count += 1
            if count > 1:
                break
        else:
            if count:
                result.append(j)
    return result


def _find_sinks(A : np.ndarray) -> list[int]:
    """
    We assume that the sink in an array may only have one inward connection.
    We return a list of possible sinks based on that assumption. An inward
    connection is defined via rows of the matrix.
    """
    result = []
    for i in range(A.shape[0]):
        count = 0
        for value in A[i, :]:
            if math.inf > value > 0:
                count += 1
            if count > 1:
                break
        else:
            if count:
                result.append(i)
    return result


def get_all_variants_A(A : np.ndarray) -> list[np.ndarray]:
    """ Get all variants of source to sink of the intersection matrix A. """
    result = []
    sources = _find_sources(A); sinks = _find_sinks(A)
    A_copy = A.copy()
    n = A.shape[0] - 1
    for source in sources:
        _swap_columns(A_copy, 0, source)
        _swap_rows(A_copy, 0, source)
        for sink in sinks:
            _swap_columns(A_copy, n, sink)
            _swap_rows(A_copy, n, sink)
            result.append(A_copy)
    return result
