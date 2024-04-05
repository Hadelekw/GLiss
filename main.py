"""
 This file is meant to be ran to generate the initial state of 
 the traffic lights.
"""

from petri_nets import *


def main() -> None:
    N = 10
    places = [Place(i) for i in range(N)]
    transitions = [Transition(i) for i in range(N // 2)]
    arcs = []
    for i in range(N):
        arcs.append(Arc(i, 1, places[(i + 1) // 2],
                    transitions[i // 2],
                        ArcDirection({0: 'input', 1: 'output'}[i % 2])))
    net = Net(places, transitions, arcs)

    places[0].tokens.append(1)

    for step in range(N):
        print('step {}'.format(step))
        net.print_connections()
        net.fire()


if __name__ == '__main__':
    main()
