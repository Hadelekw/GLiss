import math
import numpy as np

from mplus import *
from solver import *
from intersections import *


def main() -> None:
    systems = [generate_random_intersection_system(10)]
    systems = [get_all_variants_system(system[0], system[1], system[2], system[3])[0] for system in systems]
    for system in systems:
        A, T, R, P = system
        print(A)
        print(shortest_signal_solve(A, T, R, P, A.shape[0]))


if __name__ == '__main__':
    main()
