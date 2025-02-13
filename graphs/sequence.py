import math
import numpy as np
import matplotlib.pyplot as plt
import sys

import labels

from mplus import *
from load_file import load_atrp
from intersections import get_all_system_variants


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
    for _ in range(k_0 - 1):
        Z = -minplus.add_matrices(minplus.modulo_matrices(A + P + minplus.mult_matrices(e, np.transpose(x_k)), T), R)
        B = C + Z
        Bs.append(B)
        x_k = minplus.mult_matrices(B, x_k)
    Bj = Bs[0]
    for B in Bs[1:]:
        Bj = minplus.mult_matrices(Bj, B)
    result = minplus.mult_matrices(Bj, x_0)
    order = []
    partition = np.partition(result, result.shape[0] - 1, axis=0)
    for _ in range(result.shape[0]):
        i = np.where(np.isclose(result, partition[_]))[0]
        order.append(int(i[0]))
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

    swaps = [(0, 5), (5, 0)]

    figure, axes = plt.subplots(1, 2)
    for i, (swap, system) in enumerate(zip(swaps, variant_systems)):
        exits, order = modified_shortest_signal_solve(
            system[0],
            system[1],
            system[2],
            system[3],
            system[0].shape[0]
        )
        axes[i].set_aspect('equal')
        axes[i].set_xlim([0, np.max(exits)])
        axes[i].set_ylim([0, np.max(exits)])
        axes[i].set_ylabel(labels.SEQUENCE_Y_LABEL)
        print([str(_) for _ in order])
        axes[i].set_xticks([_[0] for _ in exits], [str(_) for _ in order], fontsize=14)
        axes[i].set_xlabel(labels.SEQUENCE_X_LABEL)
        lines = {float(_exit[0]): [] for _exit in np.sort(exits, axis=0)}
        for j in range(1, len(exits)):
            Tj = float(base_system[1][j][0])
            Rj = base_system[2][j, j - 1]
            Pj = base_system[3][j, j - 1]
            if Rj > 0:
                axes[i].vlines(
                    exits[j],
                    0,
                    np.max(exits),
                    color='k',
                    linewidth=0.5,
                    linestyles=(0, (5, 10))
                )
            for k in range(-1, 10):
                lines[exits[j][0]].append((Tj * k - Pj, Tj * k - Pj + Rj))
                axes[i].vlines(
                    exits[j],
                    Tj * k - Pj,
                    Tj * k - Pj + Rj,
                    color='k',
                    linewidth=5
                )
        delay = 0
        exits = np.sort(exits, axis=0)
        for j in range(len(exits[1:]) + 1):
            for (ymin, ymax) in lines[exits[j - 1][0]]:
                if exits[j - 1] + delay < ymax and exits[j - 1] + delay > ymin:
                    delay = float(ymax - exits[j - 1][0])
            axes[i].plot(
                range(int(exits[j - 1][0]), int(exits[j][0] + 1)),
                [_ + delay for _ in range(int(exits[j - 1][0]), int(exits[j][0] + 1))],
                color='k'
            )

    plt.show()


if __name__ == '__main__':
    main()
