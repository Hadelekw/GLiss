import numpy as np
from typing import Callable


class History:

    def __init__(self,
                 initial_system : np.ndarray,
                 swaps : list[tuple[int]],
                 func : Callable,
                 initial_temperature : float,
                 cooling_rate : float,
                 number_of_iterations : int) -> None:
        self.initial_system = initial_system
        self.swaps = swaps
        self.func = func
        self.initial_temperature = initial_temperature
        self.cooling_rate = cooling_rate
        self.number_of_iterations = number_of_iterations
        self.potential_values = []
        self.variant_potential_values = {swap: [] for swap in self.swaps}
