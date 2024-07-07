import numpy as np

from mplus import *


def main() -> None:
    A = np.array([
        [1, 2],
        [3, 4],
        [5, 6]
    ])
    B = np.array([
        [3, 4, 5],
        [1, 2, 6]
    ])
    C = minplus.mult_matrices(A, B)
    print(C)

    a = 10
    t = 8
    print(minplus.modulo(a, t))

    A = np.array([
        [0, 2, 3],
        [1, 0, 3],
        [3, 8, 0]
    ])
    C = minplus.power_matrix(A, 5)
    print(C)


if __name__ == '__main__':
    main()
