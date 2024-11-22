import numpy as np
import random
import math
import copy
from typing import Callable


# TODO:
# 1. Minimum green light duration
# 2. Multiple green lines consideration


def simulated_annealing(initial_system : np.ndarray,
                        func : Callable,
                        initial_temperature : float,
                        cooling_rate : float,
                        number_of_iterations : int) -> float:
    """
    Simulated annealing algorithm for improvement of an intersection
    system given as A, T, R, P matrices. Because we are considering the
    traffic system to be collision-free, we assume that the times of
    red light duration (matrix R) are fixed as they would always change
    to 0 without limitations imposed by collision probability.
    To be precise, the matrices undergoing changes are matrices T and P.
    """

    # Initial values for the initial system
    result = copy.deepcopy(initial_system)
    value = func(result[0], result[1], result[2], result[3], result[0].shape[0])
    temperature = initial_temperature

    # Initial best results (for improving via annealing)
    best_result = result
    best_value = value

    for _ in range(number_of_iterations):
        potential_result = result
        for matrix in (potential_result[1], potential_result[3]):
            for i in range(matrix.shape[0]):
                for j in range(matrix.shape[1]):
                    if math.inf > matrix[i, j] > 0:
                        matrix[i, j] += random.randint(-1, 1)
        potential_value = func(potential_result[0], potential_result[1], potential_result[2], potential_result[3], potential_result[0].shape[0])
        if potential_value == math.inf:
            break
        dv = potential_value - value
        if dv < 0:
            result = potential_result
            value = potential_value
        else:
            probability = math.exp(-dv / temperature)
            if random.random() < probability:
                result = potential_result
                value = potential_value

        if value < best_value:
            best_result = result
            best_value = value

        # temperature *= cooling_rate
        temperature = initial_temperature * (10 / initial_temperature)**(_ / number_of_iterations)

    return best_result, best_value
