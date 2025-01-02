import math
import sys
import xml.etree.ElementTree as et
import numpy as np
import matplotlib.pyplot as plt

from mplus import *
from solver import *
from intersections import *
from algorithms import *


def main() -> None:

    mode = sys.argv[1]

    if mode == '--graphml':
        file_path = sys.argv[2]
        f = open(file_path, 'r')
        root = et.parse(f).getroot()
        # if len(root) != 4:
        #     raise ValueError('The given GraphML file does not contain all 4 graphs.')
        values = {key: {'nodes': [], 'edges': []} for key in ('A', 'T', 'R', 'P')}
        for child in root:
            if child.tag[-5:] == 'graph':
                graph_id = child.attrib['id']
                for grandchild in child:
                    if grandchild.tag[-4:] == 'node':
                        values[graph_id]['nodes'].append(grandchild.attrib['id'])
                    if grandchild.tag[-4:] == 'edge':
                        values[graph_id]['edges'].append((grandchild.attrib['source'],
                                                          grandchild.attrib['target'],
                                                          grandchild.attrib['weight']))
        for key, value in values.items():
            if key == 'A':
                pass
            if key == 'T':
                pass
            if key == 'R':
                pass
            if key == 'P':
                pass
        return

    if mode == '--atrp':
        file_path = sys.argv[2]
        base_system = []
        with open(file_path, 'r') as f:
            j = 0; matrix_size = 1
            for i, line in enumerate(f):
                values = line.split()
                if not i % matrix_size:
                    print(values)
                    j += 1
                if not base_system and not i:
                    j = 0
                    matrix_size = len(values)
                    base_system = [
                        np.eye(matrix_size, matrix_size),
                        np.ones((matrix_size, 1)),
                        np.zeros((matrix_size, matrix_size)),
                        np.zeros((matrix_size, matrix_size))
                    ]
                    base_system[0][base_system[0] == 0] = math.inf
                    base_system[0][base_system[0] == 1] = 0
                for k, value in enumerate(values):
                    base_system[j][i % matrix_size, k] = int(value) if value != 'inf' else math.inf

    annealing_result, annealing_score = simulated_annealing(base_system, shortest_signal_solve, 100, 0.9, 1000)
    for system in get_all_variants_system(*annealing_result):
        print(shortest_signal_solve(*system, system[0].shape[0]))


if __name__ == '__main__':
    main()
