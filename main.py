import math
import numpy as np

from mplus import *
from solver import *


TAU = math.inf


def main() -> None:
    A = np.array([
        [0, 5, TAU, TAU, TAU, TAU],
        [5, 0, 10, 15, TAU, TAU],
        [TAU, 10, 0, TAU, 15, TAU],
        [TAU, 15, TAU, 0, 20, TAU],
        [TAU, TAU, 15, 20, 0, 5],
        [TAU, TAU, TAU, TAU, 5, 0],
    ])
    print(no_signal_solve(A, 4))


if __name__ == '__main__':
    main()
