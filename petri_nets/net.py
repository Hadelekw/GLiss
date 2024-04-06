"""
 This file contains the class definition of Petri net and
 basic functions related to it.
"""

from enum import Enum
from types import FunctionType


class Place:
    """ Class definition of a place in Petri net. """

    identifier : int = None
    token_count : int = 0

    def __init__(self, identifier : int) -> None:
        self.identifier = identifier
        self.token_count = 0

    def __str__(self) -> None:
        return 'Place {} ({} tokens)'.format(self.identifier, self.token_count)


class Transition:
    """ Class definition of a transition in Petri net. """

    identifier : int = None
    input_place : Place = None
    output_place : Place = None
    fire_condition : FunctionType = lambda self, x: x == 1
    firing : bool = False

    def __init__(self, identifier : int) -> None:
        self.identifier = identifier
        self.firing : bool = False

    def __str__(self) -> None:
        return 'Transition {}'.format(self.identifier)

    def fire(self) -> None:
        if self.fire_condition(self.input_place.token_count):
            self.output_place.token_count += 1
            self.input_place.token_count -= 1

    def set_fire_condition(self, condition : FunctionType) -> None:
        self.fire_condition = condition


class ArcDirection(Enum):
    """ Enumeration of possible arc directions. """
    TO_TRANSITION = 'input'  # P -> T  -- input of transition
    TO_PLACE = 'output'      # T -> P  -- output of transition


class Arc:
    """ Class definition of an arc in Petri net. """

    identifier : int = None
    weight : float = 1
    place : Place = None
    transition : Transition = None
    direction : ArcDirection = None

    def __init__(self,
                 identifier : int,
                 weight : float,
                 place : Place,
                 transition : Transition,
                 direction : ArcDirection) -> None:
        self.identifier = identifier
        self.weight = weight
        self.direction = direction
        if direction == ArcDirection('input'):
            transition.input_place = place
        elif direction == ArcDirection('output'):
            transition.output_place = place
        self.place = place
        self.transition = transition

    def __str__(self) -> None:
        return 'Arc ({}) {}'.format(self.direction.value, self.identifier)


class Net:
    """ Class definition of Petri net. """

    places : list[Place] = []
    transitions : list[Transition] = []
    arcs : list[Arc] = []

    def __init__(self,
                 places : list[Place] = [],
                 transitions : list[Transition] = [],
                 arcs : list[Arc] = []) -> None:
        self.places = places
        self.transitions = transitions
        self.arcs = arcs

    def print_connections(self) -> None:
        for transition in self.transitions:
            print('{} -> {}'.format(transition.input_place, transition))
            print('{} -> {}'.format(transition, transition.output_place))

    def step(self) -> None:
        for transition in self.transitions[::-1]:
            transition.fire()
