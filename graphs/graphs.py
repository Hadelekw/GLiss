import numpy as np
import matplotlib.pyplot as plt
import sys

import labels


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


def main() -> None:

    mode = sys.argv[1]
    file_path = sys.argv[2]

    potential_values, variant_potential_values = load_values(file_path)

    if mode == 'variant_distribution':
        for i, (variant, scores) in enumerate(variant_potential_values.items()):
            counts, bins = np.histogram(scores, bins=tuple(set([round(score) for score in scores])))
            plt.stairs(counts, bins)
            plt.hist(bins[:-1], bins, weights=counts, label=str(variant), edgecolor=COLORS[i], facecolor=COLORS[i], alpha=0.5)
        plt.xlabel(labels.VARIANT_DISTRIBUTION_X_LABEL)
        plt.ylabel(labels.VARIANT_DISTRIBUTION_Y_LABEL)
        plt.legend(loc='upper right')
    elif mode == 'variant_probability':
        for i, (variant, scores) in enumerate(variant_potential_values.items()):
            counts, bins = np.histogram(scores, bins=tuple(set([round(score) for score in scores])))
            counts = counts.astype('float64')
            counts /= np.max(counts)
            plt.stairs(counts, bins)
            plt.hist(bins[:-1], bins, weights=counts, label=str(variant), edgecolor=COLORS[i], facecolor=COLORS[i], alpha=0.5)
        plt.xlabel(labels.VARIANT_PROBABILITY_X_LABEL)
        plt.ylabel(labels.VARIANT_PROBABILITY_Y_LABEL)
        plt.legend(loc='upper right')
    elif mode == 'variant_evolution':
        iterations = [i for i in range(len(potential_values))]
        for i, (variant, scores) in enumerate(variant_potential_values.items()):
            plt.plot(iterations, scores, label=str(variant), color=COLORS[i], linewidth=0.5)
        plt.plot(iterations, potential_values, label=labels.VARIANT_EVOLUTION_AVERAGE_LABEL, color='k', linewidth=2)
        plt.xlabel(labels.VARIANT_EVOLUTION_X_LABEL)
        plt.ylabel(labels.VARIANT_EVOLUTION_Y_LABEL)
        plt.legend(loc='upper right')
    elif mode == 'limited_variant_evolution':
        limit = int(sys.argv[3])
        iterations = range(limit)
        for i, (variant, scores) in enumerate(variant_potential_values.items()):
            plt.plot(iterations, scores[:limit], label=str(variant), color=COLORS[i], linewidth=0.5)
        plt.plot(iterations, potential_values[:limit], label=labels.VARIANT_EVOLUTION_AVERAGE_LABEL, color='k', linewidth=2)
        plt.xlabel(labels.VARIANT_EVOLUTION_X_LABEL)
        plt.ylabel(labels.VARIANT_EVOLUTION_Y_LABEL)
        plt.legend(loc='upper right')
    plt.show()


if __name__ == '__main__':
    main()
