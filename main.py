import math
import sys
import time
import numpy as np
import matplotlib.pyplot as plt

from mplus import *
from solver import *
from intersections import get_all_swap_variants
from algorithms import *
from load_file import load_graphml, load_atrp


def main() -> None:

    args = sys.argv
    args = args[3:]
    paired_args = {args[i][1:]: args[i + 1] for i in range(0, len(args), 2)}
    mappings = {
        'sa_temperature': (float, ['sa_temperature', 'sat']),
        'cooling_rate': (float, ['cooling_rate', 'sa_cooling_rate', 'cr', 'sacr']),
        'sa_iterations': (int, ['sa_iterations', 'sai']),
        'output': (str, ['output', 'o']),
    }
    settings = {
        'sa_temperature': 100,
        'cooling_rate': 0.9,
        'sa_iterations': 100,
        'output': 'result.atrp'
    }
    for key, (func, values) in mappings.items():
        for value in values:
            if value in paired_args.keys():
                settings[key] = func(paired_args[value])

    mode = sys.argv[1]
    file_path = sys.argv[2]

    if mode == 'graphml':
        base_system = load_graphml(file_path)
    if mode == 'atrp':
        base_system = load_atrp(file_path)

    t = time.time()

    swaps = get_all_swap_variants(base_system[0])
    annealing_result, annealing_score, annealing_history = simulated_annealing(
        base_system,
        swaps,
        shortest_signal_solve,
        settings['sa_temperature'],
        settings['cooling_rate'],
        settings['sa_iterations']
    )

    print('\nTotal runtime: {runtime:.2f}s'.format(runtime=time.time() - t))
    print('Best score: {score:.2f}'.format(score=annealing_score))

    annealing_history.dump('results')

    with open(settings['output'], 'w') as f:
        for matrix in annealing_result:
            for i in range(matrix.shape[0]):
                for j in range(matrix.shape[1]):
                    f.write('{:.2f} '.format(matrix[i, j]))
                f.write('\n')


if __name__ == '__main__':
    main()
