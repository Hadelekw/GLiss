import numpy as np
import matplotlib.pyplot as plt
import math
from statistics import median, kde
import sys

sys.path.append('../')

import labels
from reaction_time import alt_emg


COLORS = ['r', 'b', 'm', 'g', 'k', 'y', 'k']
HATCHES = ['||||', '----', '////', '\\\\\\\\', '++++', '....']


def load_values(file_path : str) -> tuple:
    potential_values = []
    variant_potential_values = {}
    with open(file_path, 'r') as f:
        for line in f:
            contents = line.split()
            if contents[0] == 'value':
                potential_values.append(float(contents[1]))
            elif contents[0] == 'variant':
                for swap, value in zip(contents[1::2], contents[2::2]):
                    if swap not in variant_potential_values.keys():
                        variant_potential_values[swap] = []
                    variant_potential_values[swap].append(float(value))
    return potential_values, variant_potential_values


def mean(dataset : list) -> float:
    return sum(dataset) / len(dataset)


def standard_deviation(dataset : list) -> float:
    m = mean(dataset)
    variance = sum([(x - m)**2 for x in dataset]) / len(dataset)
    return math.sqrt(variance)


def skewness(dataset : list) -> float:
    return (mean(dataset) - median(dataset)) / standard_deviation(dataset)


def main() -> None:

    mode = sys.argv[1]
    identifier = sys.argv[2]
    if len(identifier) == 2:
        system_id, delay = identifier[0], identifier[1]
        if delay == 'a':
            system_id = identifier
            delay = None
    elif len(identifier) == 1:
        system_id = identifier
        delay = None
    else:
        system_id, delay = identifier[:-2], identifier[2]

    if delay != '0' and delay is not None:
        files_paths = [f'../results/results_{system_id}_{delay}{i}/values.txt' for i in range (10)]
    elif delay is None:
        files_paths = []
        for i in range(10):
            for j in range(6):
                if j != 0:
                    files_paths.append(f'../results/results_{system_id}_{j}{i}/values.txt')
                else:
                    files_paths.append(f'../results/results_{system_id}_{i}/values.txt')
    else:
        files_paths = [f'../results/results_{system_id}_{i}/values.txt' for i in range (10)]
    # files_paths = sys.argv[2].split(',')

    potential_values = []

    for file_path in files_paths:
        potential_values.extend(load_values(file_path)[0])

    if mode == 'distribution':
        plt.rc('axes', labelsize=12)
        counts, bins = np.histogram(
            potential_values,
            bins=tuple(set([int(value) for value in potential_values]))
        )
        counts = counts.astype('float64')
        counts /= max(counts)
        plt.stairs(counts, bins)
        plt.hist(bins[:-1], bins, weights=counts, color='#cccccc', edgecolor='#cccccc')

        m = mean(potential_values)
        s = standard_deviation(potential_values)
        gamma = skewness(potential_values)
        mu = m - s * (gamma / 2)**(1/3)
        sigma = math.sqrt(s**2 * (1 - (gamma / 2)**(2/3)))
        tau = s * (gamma / 2)**(1/3)

        # print(m)
        # print(s)
        # print(gamma)

        # def poisson(l : float, k : float):
        #     return (l**k * math.exp(-l)) / (math.factorial(int(k)))

        # plt.plot(bins[:-1], [poisson(m, counts[x]) for x in range(len(counts))], color='k')

        plt.plot(range(25, 140), [alt_emg(x, mu, sigma, tau) for x in range(25, 140)], color='k')
        plt.xlabel(labels.DISTRIBUTION_X_LABEL)
        plt.ylabel(labels.DISTRIBUTION_Y_LABEL)
        plt.xlim([25, 140])
        # plt.legend(loc='upper right')
    plt.show()


if __name__ == '__main__':
    main()
