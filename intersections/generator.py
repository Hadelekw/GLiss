import math
import random
import numpy as np


TAU = math.inf


def _generate_random_intersection(N : int) -> dict:
    """ Generates a semi-random system of intersections as a directional adjacency list. It assumes one Source and one Sink. """
    result = {i: ([i + 1] if i < N - 1 else []) for i in range(N)}
    for i in range(1, N - 1):
        result[i].extend(random.sample(range(N), random.choice(range(2, 5))))
        result[i] = list(set(result[i]))
        if i in result[i]:
            result[i].remove(i)
    return result


def _generate_random_A(adjacency_list : dict,
                      min_weight : int = 5,
                      max_weight : int = 30) -> np.ndarray:
    """ Uses _generate_random_intersection to create matrix A. """
    adjacency_matrix = [[TAU for __ in range(len(adjacency_list))] for _ in range(len(adjacency_list))]
    for key, adjacent in adjacency_list.items():
        adjacency_matrix[key][key] = 0
        for value in adjacent:
            adjacency_matrix[value][key] = random.randint(min_weight, max_weight)
    return np.array(adjacency_matrix)


def _generate_random_T(N : int,
                       min_weight : int = 5,
                       max_weight : int = 50) -> np.ndarray:
    """ Generates a semi-random matrix T. """
    result = [TAU for _ in range(N)]
    for i in range(1, N - 1):
        result[i] = random.randint(min_weight, max_weight)
    return np.transpose(np.array([result]))


def _generate_random_R(A : np.ndarray,
                       min_weight : int = 5,
                       max_weight : int = 50,
                       chance : float = 0.85) -> np.ndarray:
    """ Generates a semi-random matrix R based on matrix A. """
    result = np.where(math.inf > A.copy(), 1, 0)
    for i in range(A.shape[0]):
        for j in range(A.shape[1]):
            if i != j:
                result[i, j] *= random.randint(min_weight, max_weight) if random.random() < chance else 0
            else:
                result[i, j] = 0
    return result


def _generate_random_P(R : np.ndarray,
                       min_weight : int = 5,
                       max_weight : int = 50) -> np.ndarray:
    """ Generates a semi-random matrix P based on matrix R. """
    result = np.where(R.copy() > 0, 1, 0)
    for i in range(R.shape[0]):
        for j in range(R.shape[1]):
            result[i, j] *= random.randint(min_weight, max_weight)
    return result


def generate_random_intersection_system(N : int,
                                        log : bool = True) -> tuple[np.ndarray]:
    """ Generates a semi-random system of intersections given as matrices A, T, R, P. """
    adjacency_list = _generate_random_intersection(N)
    A = _generate_random_A(adjacency_list)
    T = _generate_random_T(N)
    R = _generate_random_R(A)
    P = _generate_random_P(R)
    return A, T, R, P
