import numpy as np
import random
import math
from typing import Callable


def simulated_annealing(initial_system : np.ndarray,
                        func : Callable,
                        initial_temperature : float,
                        cooling_rate : float,
                        number_of_iterations : int) -> float:
    result = initial_system
    value = func(result[0], result[1], result[2], result[3], result[0].shape[0])
    temperature = initial_temperature

    best_result = result
    best_value = value

    for _ in range(number_of_iterations):
        potential_result = result
        for matrix in potential_result[1:]:
            for i in range(matrix.shape[0]):
                for j in range(matrix.shape[1]):
                    if math.inf > matrix[i, j] > 0:
                        matrix[i, j] += random.randint(-1, 1)
        potential_value = func(potential_result[0], potential_result[1], potential_result[2], potential_result[3], potential_result[0].shape[0])
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

        temperature *= cooling_rate

    return best_result, best_value
