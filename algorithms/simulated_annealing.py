import numpy as np
import random
import math
import copy
import sys
from typing import Callable

from intersections import get_all_system_variants

from . import sa_settings as settings
from .history import History
from .temperatures import TEMPERATURE_UPDATE_MAP


def simulated_annealing(initial_system : np.ndarray,
                        swaps : list[tuple[int]],
                        func : Callable,
                        temperature_update_method_identifier : str = settings.TEMPERATURE_UPDATE_METHOD_IDENTIFIER,
                        initial_temperature : float = settings.INITIAL_TEMPERATURE,
                        cooling_rate : float = settings.COOLING_RATE,
                        final_temperature : int = settings.FINAL_TEMPERATURE,
                        number_of_iterations : int = settings.NUMBER_OF_ITERATIONS,
                        starting_times : list[float] = settings.STARTING_TIMES) -> float:
    """
    Simulated annealing algorithm for improvement of an intersection
    system given as A, T, R, P matrices.
    """

    history = History(
        initial_system,
        swaps,
        func,
        initial_temperature,
        cooling_rate,
        number_of_iterations
    )

    # The values for the initial system
    result = copy.deepcopy(initial_system)
    value = func(result[0], result[1], result[2], result[3], result[0].shape[0])
    temperature = initial_temperature

    # Initial best results (for later improvement via annealing)
    best_result = result
    best_value = value

    for i in range(number_of_iterations):

        percentage = (i + 1) / number_of_iterations
        sys.stdout.write('\rProgress: {iteration}/{number_of_iterations} ({percentage:.2%}) [{progress}] Best score: {score:.2f}'.format(
            iteration=i + 1,
            number_of_iterations=number_of_iterations,
            percentage=percentage,
            progress=('#' * int(percentage * 20)).ljust(20, '-'),
            score=best_value
        ))

        potential_result = result

        # Generating the changes to T matrix
        for i in range(potential_result[1].shape[0]):
            for j in range(potential_result[1].shape[1]):
                if potential_result[1][i, j] != math.inf:
                    _value = potential_result[1][i, j] + random.random() * random.randint(-1, 1) * random.randint(1, 5)
                    if _value > settings.MIN_T_VALUE and _value < settings.MAX_T_VALUE:
                        potential_result[1][i, j] = _value
                    elif _value < settings.MIN_T_VALUE:
                        potential_result[1][i, j] = settings.MIN_T_VALUE
                    else:
                        potential_result[1][i, j] = settings.MAX_T_VALUE

        # Generating the changes to R matrix
        for i in range(potential_result[2].shape[0]):
            for j in range(potential_result[2].shape[1]):
                if potential_result[0][i, j] > 0 and potential_result[0][i, j] != math.inf:
                    _value = potential_result[2][i, j] + random.random() * random.randint(-1, 1) * random.randint(1, 5)
                    if potential_result[1][i, 0] - _value > settings.MIN_GREEN_LIGHT_LENGTH and _value > settings.MIN_R_VALUE:
                        potential_result[2][i, j] = _value
                    elif _value < settings.MIN_R_VALUE:
                        potential_result[2][i, j] = settings.MIN_R_VALUE

        # Generating the changes to P matrix
        for i in range(potential_result[3].shape[0]):
            for j in range(potential_result[3].shape[1]):
                if potential_result[0][i, j] > 0 and potential_result[0][i, j] != math.inf:
                    _value = potential_result[3][i, j] + random.random() * random.randint(-1, 1) * random.randint(1, 5)
                    if _value > settings.MIN_P_VALUE and _value < settings.MAX_P_VALUE:
                        potential_result[3][i, j] = _value
                    elif _value < settings.MIN_P_VALUE:
                        potential_result[3][i, j] = settings.MIN_P_VALUE
                    else:
                        potential_result[3][i, j] = settings.MAX_P_VALUE

        for matrix in potential_result:
            matrix = np.round(matrix, settings.DECIMAL_PLACES)

        history.potential_results.append(copy.deepcopy(potential_result))

        variant_potential_results = get_all_system_variants(
            potential_result[0],
            potential_result[1],
            potential_result[2],
            potential_result[3]
        )

        potential_value = 0

        for swap, variant_potential_result in zip(swaps, variant_potential_results):
            variant_potential_value = 0
            for starting_point in starting_times:
                variant_potential_value += round(func(
                    variant_potential_result[0],
                    variant_potential_result[1],
                    variant_potential_result[2],
                    variant_potential_result[3],
                    variant_potential_result[0].shape[0],
                    starting_point
                ), 2)
            variant_potential_value /= len(starting_times)
            potential_value += variant_potential_value
            history.variant_potential_values[swap].append(float(variant_potential_value))

        potential_value /= len(swaps)
        potential_value = round(potential_value, settings.DECIMAL_PLACES)
        history.potential_values.append(float(potential_value))

        # Skip if the time needed to travel through intersection is infinite
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
            best_result = copy.deepcopy(result)
            best_value = value

        if temperature_update_method_identifier == 'a':
            temperature = TEMPERATURE_UPDATE_MAP[temperature_update_method_identifier](temperature, cooling_rate)
        else:
            temperature = TEMPERATURE_UPDATE_MAP[temperature_update_method_identifier](initial_temperature, final_temperature, i, number_of_iterations)

    return best_result, best_value, history
