"""
 This file is meant to be ran to generate the initial state of 
 the traffic lights.
"""

from petri_nets import *
from mplus import *


def main() -> None:
    N = 10
    places = [Place(i) for i in range(N)]
    transitions = [Transition(i) for i in range(N // 2)]
    for transition in transitions:
        transition.set_fire_condition(lambda x: x >= 1)
    arcs = []
    for i in range(N):
        arcs.append(Arc(i, 1, places[(i + 1) // 2],
                        transitions[i // 2],
                        ArcDirection({0: 'input', 1: 'output'}[i % 2])))
    net = Net(places, transitions, arcs)

    places[0].token_count += 5

    for step in range(N):
        print('step {}'.format(step))
        net.print_connections()
        net.step()

    A = [
        [1, 2, 2, 2],
        [3, 4, -4, 4],
        [5, -6, 6, -6]
    ]
    B = [
        [2, 1, -2],
        [0, 3, 2],
        [1, -1, 1],
    ]
    C = [
        [5, 1, 5, 1],
        [-2, 8, 8, 8],
        [0, 1, 7, 7],
    ]
    print(minplus_add_matrices(maxplus_mult_matrices(A, B), C))


if __name__ == '__main__':
    main()
