import math
import numpy as np

from mplus import *
from solver import *
from intersections import *
from algorithms import *


TAU = math.inf

def main() -> None:
    # systems = [generate_random_intersection_system(10)]
    # # systems = [get_all_variants_system(system[0], system[1], system[2], system[3])[0] for system in systems]
    # for system in systems:
    #     A, T, R, P = system
    #     print(A, T, R, P)
    #     print(shortest_signal_solve(A, T, R, P, A.shape[0]))
    #     A, T, R, P = simulated_annealing(system, shortest_signal_solve, 100, 0.95, 1000)[0]
    #     print(A, T, R, P)
    #     print(shortest_signal_solve(A, T, R, P, A.shape[0]))

    # TODO:
    # 1. Create an example system of intersections.
    # 2. Add limitations to what the simulated annealing can change.

    A = np.array([
        [0, 5, TAU, TAU, TAU, TAU],
        [5, 0, 10, 15, TAU, TAU],
        [TAU, 10, 0, TAU, 15, TAU],
        [TAU, 15, TAU, 0, 20, TAU],
        [TAU, TAU, 15, 20, 0 , 5],
        [TAU, TAU, TAU, TAU, 5, 0],
    ])
    T = np.array([
        [TAU],
        [8],
        [20],
        [16],
        [12],
        [TAU],
    ])
    R = np.array([
        [0, 0, 0, 0, 0, 0],
        [16, 0, 16, 16, 0, 0],
        [0, 15, 0, 0, 15, 0],
        [0, 12, 0, 0, 12, 0],
        [0, 0, 9, 9, 0, 0],
        [0, 0, 0, 0, 0, 0],
    ])
    P = np.array([
        [0, 0, 0, 0, 0, 0],
        [5, 0, 1, 3, 0, 0],
        [0, 2, 0, 0, 7, 0],
        [0, 6, 0, 0, 10, 0],
        [0, 0, 0, 3, 0, 0],
        [0, 0, 0, 0, 0, 0],
    ])
    system = [A, T, R, P]
    print(shortest_signal_solve(A, T, R, P, A.shape[0]))
    results = []
    for _ in range(1000):
        # _A, _T, _R, _P = simulated_annealing(system, shortest_signal_solve, 100, 0.9, 100)[0]
        # print('\n'.join([str(_A), str(_T), str(_R), str(_P)]))
        # results.append(shortest_signal_solve(_A, _T, _R, _P, A.shape[0]))
        results.append(simulated_annealing(system, shortest_signal_solve, 100, 0.9, 100))
        print(results[-1][1])
    # print(sum(results) / len(results))
    _scores = [result[1] for result in results]
    print(sum(_scores) / len(_scores))
    print(len([result for result in results if result[1] == min(_scores)]))

if __name__ == '__main__':
    main()
