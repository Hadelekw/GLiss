import numpy as np
import os
from typing import Callable


class History:
    """
    Class for logging the values generatred by simulated annealing.
    To be used in preparing various graphs etc.
    """

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
        self.potential_results = []
        self.potential_values = []
        self.variant_potential_values = {swap: [] for swap in self.swaps}


    def dump_settings(self, file_path : str) -> None:
        with open(file_path, 'w') as f:
            f.write('swaps {swaps}\n'.format(swaps=' '.join([str(swap) for swap in self.swaps])))
            f.write('func {func_name}\n'.format(func_name=self.func.__name__))
            f.write('initial_temperature {initial_temperature}\n'.format(initial_temperature=self.initial_temperature))
            f.write('cooling_rate {cooling_rate}\n'.format(cooling_rate=self.cooling_rate))
            f.write('number_of_iterations {number_of_iterations}\n'.format(number_of_iterations=self.number_of_iterations))


    def dump_all_values(self, file_path : str) -> None:
        with open(file_path, 'w') as f:
            for i in range(self.number_of_iterations):
                f.write('iteration {iteration}\n'.format(iteration=i))
                f.write('value {value}\nvariant '.format(value=self.potential_values[i]))
                # for swap, variant_potential_values in self.variant_potential_values.items():
                #     f.write('{swap} {value} '.format(swap=str(swap).replace(' ', ''), value=variant_potential_values[i]))
                f.write('\n')


    def dump_results(self, directory_path : str) -> None:
        if os.path.isdir(directory_path):
            pass
        else:
            os.mkdir(directory_path)
        for i, potential_result in enumerate(self.potential_results):
            with open(directory_path + '/{file_path}.atrp'.format(file_path=i), 'w') as f:
                for matrix in potential_result:
                    for j in range(matrix.shape[0]):
                        for k in range(matrix.shape[1]):
                            f.write('{:.2f} '.format(matrix[j, k]))
                        f.write('\n')


    def dump(self, directory_path : str) -> None:
        self.dump_results(directory_path)
        self.dump_all_values(directory_path + '/values.txt')
        self.dump_settings(directory_path + '/settings.txt')
