import math
import numpy as np

from mplus import *
from solver import *


TAU = math.inf


def main() -> None:
    print('Example 1 results')
    A = np.array([
        [0, 5, TAU, TAU, TAU, TAU],
        [5, 0, 10, 15, TAU, TAU],
        [TAU, 10, 0, TAU, 15, TAU],
        [TAU, 15, TAU, 0, 20, TAU],
        [TAU, TAU, 15, 20, 0, 5],
        [TAU, TAU, TAU, TAU, 5, 0],
    ])
    print(no_signal_solve(A, 4))
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
        [6, 0, 6, 6, 0, 0],
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
    print(signal_solve(A, T, R, P))

    print('Example 2 results')
    A = np.array([
        [0, TAU, TAU, TAU, TAU],
        [12, 0, TAU, TAU, TAU],
        [TAU, 10, 0, TAU, TAU],
        [TAU, TAU, 20, 0, TAU],
        [TAU, TAU, TAU, 10, 0],
    ])
    T = np.array([
        [TAU],
        [18],
        [30],
        [15],
        [TAU],
    ])
    R = np.array([
        [0, 0, 0, 0, 0],
        [13, 0, 0, 0, 0],
        [0, 23, 0, 0, 0],
        [0, 0, 13, 0, 0],
        [0, 0, 0, 0, 0],
    ])
    P = np.array([
        [0, 0, 0, 0, 0],
        [8, 0, 0, 0, 0],
        [0, 25, 0, 0, 0],
        [0, 0, 10, 0, 0],
        [0, 0, 0, 0, 0],
    ])
    print(signal_solve(A, T, R, P))


if __name__ == '__main__':
    main()
