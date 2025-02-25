"""
 Generates a diagram showing the vehicle's movement between red lights.
 This is a very rough version of this graph which works only for specific data.
"""


import math
import numpy as np
import matplotlib.pyplot as plt
import sys

import labels

sys.path.append('../')
from mplus import *
from load_file import load_atrp
from intersections import get_all_system_variants, get_all_swap_variants


COLORS = ['r', 'b', 'm', 'g', 'k', 'y', 'k']


def modified_shortest_signal_solve(A : np.ndarray,
                                   T : np.ndarray,
                                   R : np.ndarray,
                                   P : np.ndarray,
                                   k_0 : int,
                                   x_0_0 : int = 0,
                                   x_0 : np.ndarray = None) -> float:
    if A.shape[0] != A.shape[1]:
        raise ValueError('No_signal_solve: matrix A is not square.')
    if A.shape[0] != T.shape[0] or T.shape[1] != 1:
        raise ValueError('Signal_solve: matrix T is not an Nx1 vector.')
    if A.shape != R.shape:
        raise ValueError('Signal_solve: matrix R is not NxN like matrix A.')
    if A.shape != P.shape:
        raise ValueError('Signal_solve: matrix P is not NxN like matrix A.')
    if x_0 is None:
        _ = [x_0_0,]
        _.extend([math.inf for _ in range(A.shape[0] - 1)])
        x_0 = np.transpose(np.array([_]))
    e = np.transpose(np.array([[0 for _ in range(A.shape[0])]]))
    x_k = x_0
    Bs = []
    C = A + R
    x_k_size = sum(x_k < math.inf)[0]
    former_x_k = x_k.copy()
    order = []
    for _ in range(k_0 - 1):
        Z = -minplus.add_matrices(minplus.modulo_matrices(A + P + minplus.mult_matrices(e, np.transpose(x_k)), T), R)
        B = C + Z
        Bs.append(B.copy())
        x_k = minplus.mult_matrices(B, x_k)
        if sum(x_k < math.inf) - x_k_size > 1:
            order.append(int(np.where(np.isclose(x_k, np.min(x_k[int(x_k_size):int(sum(x_k < math.inf)[0])])))[0][0]))
        else:
            try:
                order.append(int(np.where(x_k != former_x_k)[0][0]))
            except:
                pass
        x_k_size = sum(x_k < math.inf)[0]
        former_x_k = x_k.copy()
    order = [0] + order
    Bj = Bs[0]
    for B in Bs[1:]:
        Bj = minplus.mult_matrices(B, Bj)
    result = minplus.mult_matrices(Bj, x_0)
    result = {i: float(result[i][0]) for i in order}
    return result, order


def main() -> None:
    file_path = sys.argv[1]

    base_system = load_atrp(file_path)

    variant_systems = get_all_system_variants(
        base_system[0],
        base_system[1],
        base_system[2],
        base_system[3]
    )

    swaps = get_all_swap_variants(base_system[0])

    figure, axes = plt.subplots(1, len(swaps))
    for i, (swap, system) in enumerate(zip(swaps, variant_systems)):
        exits, order = modified_shortest_signal_solve(
            system[0],
            system[1],
            system[2],
            system[3],
            system[0].shape[0]
        )

        axes[i].set_aspect('equal')
        axes[i].set_xlim([0, max(exits.values())])
        axes[i].set_ylim([0, max(exits.values())])
        axes[i].set_ylabel(labels.SEQUENCE_Y_LABEL)
        axes[i].set_xlabel(labels.SEQUENCE_X_LABEL)

        accumulates = [0]
        accumulate = 0
        for j, k in zip(order[1:], order[:-1]):
            accumulate += system[0][j, k]
            accumulates.append(accumulate)
            Tj = float(system[1][j][0])
            Rj = system[2][j, k]
            Pj = system[3][j, k]
            axes[i].vlines(
                accumulate,
                0,
                max(exits.values()),
                color='k',
                linewidth=0.5,
                linestyles=(0, (5, 10))
            )
            for l in range(-1, 10):
                axes[i].vlines(
                    accumulate,
                    Tj * l - Pj,
                    Tj * l - Pj + Rj,
                    color='k',
                    linewidth=5
                )

        axes[i].set_xticks(
            [_ for _ in accumulates],
            [swap[0]] + [str(_) for _ in order[1:-1]] + [swap[1]],
            fontsize=14
        )

        for (prev_accumulate, next_accumulate), (prev_exit, next_exit) in zip(
                zip(accumulates[:-1], accumulates[1:]),
                zip(list(exits.values())[:-1], list(exits.values())[1:])):
            axes[i].plot(
                [prev_accumulate, next_accumulate],
                [prev_exit, next_accumulate if next_accumulate != accumulates[-1] else next_exit],
                color='k'
            )

    plt.show()


if __name__ == '__main__':
    main()
