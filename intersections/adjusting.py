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


def _find_sources(A : np.ndarray) -> list[int]:
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


def get_all_variants_swaps(A : np.ndarray) -> list[tuple[int, int]]:
    """ Get all possible pairs of sources and sinks. """
    result = []
    sources = _find_sources(A); sinks = _find_sinks(A)
    for source in sources:
        for sink in sinks:
            result.append((source, sink))
    return result


def get_all_variants_matrix(A : np.ndarray,
                            sources : list[tuple],
                            sinks : list[tuple]) -> list[np.ndarray]:
    """ Get all variant of source to sink of an intersection matrix. """
    result = []
    A_copy = A.copy()
    n = A.shape[0] - 1
    for source in sources:
        _swap_columns(A_copy, 0, source)
        _swap_rows(A_copy, 0, source)
        for sink in sinks:
            _swap_columns(A_copy, n, sink)
            _swap_rows(A_copy, n, sink)
            if A_copy not in result:  # Removal of unwanted duplicates.
                result.append(A_copy)
    return result


def get_all_variants_system(A : np.ndarray,
                            T : np.ndarray,
                            R : np.ndarray,
                            P : np.ndarray) -> list[tuple[np.ndarray]]:
    """
    Get all variants of source to sink of all intersection matrices.
    Because matrices A, R, and P have the same shape they get changed in the same way.
    Matrix T does not change but is included in the return for a full system.
    """
    sources = _find_sources(A)
    sinks = _find_sinks(A)
    As = get_all_variants_matrix(A, sources, sinks)
    Rs = get_all_variants_matrix(R, sources, sinks)
    Ps = get_all_variants_matrix(P, sources, sinks)
    result = [(As[i], T.copy(), Rs[i], Ps[i]) for i in range(len(As))]
    return result
