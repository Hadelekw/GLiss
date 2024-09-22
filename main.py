import math
import numpy as np

from mplus import *
from solver import *
from intersections import *
from algorithms import *


def main() -> None:
    systems = [generate_random_intersection_system(10)]
    # systems = [get_all_variants_system(system[0], system[1], system[2], system[3])[0] for system in systems]
    for system in systems:
        A, T, R, P = system
        print(A, T, R, P)
        print(shortest_signal_solve(A, T, R, P, A.shape[0]))
        A, T, R, P = simulated_annealing(system, shortest_signal_solve, 100, 0.95, 1000)[0]
        print(A, T, R, P)
        print(shortest_signal_solve(A, T, R, P, A.shape[0]))


if __name__ == '__main__':
    main()
