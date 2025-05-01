import math
import sys
import time
import numpy as np
import matplotlib.pyplot as plt

from solver import shortest_signal_solve
from intersections import get_all_swap_variants
from algorithms import simulated_annealing
from load_file import load_graphml, load_atrp


def main(mode : str,
         file_path : str,
         results_path : str,
         starting_times : str) -> None:

    starting_times = [float(value) for value in starting_times.split(',')]

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
        starting_times=starting_times
    )

    print('\nTotal runtime: {runtime:.2f}s'.format(runtime=time.time() - t))
    print('Best score: {score:.2f}'.format(score=annealing_score))

    annealing_history.dump(results_path)

    with open(results_path + '/result.atrp', 'w') as f:
        for matrix in annealing_result:
            for i in range(matrix.shape[0]):
                for j in range(matrix.shape[1]):
                    f.write('{:.2f} '.format(matrix[i, j]))
                f.write('\n')


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
