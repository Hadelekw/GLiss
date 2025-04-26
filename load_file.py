import xml.etree.ElementTree as et
import numpy as np
import math


# TODO:
# 1. Fix GraphML loading


def load_graphml(file_path : str) -> list:
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


def load_atrp(file_path : str) -> list:
    base_system = []
    with open(file_path, 'r') as f:
        j = 0; matrix_size = 1
        for i, line in enumerate(f):
            values = line.split()
            if not i % matrix_size:
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
            for k, value in enumerate(values):
                base_system[j][i % matrix_size, k] = float(value) if value not in ['inf', 't'] else math.inf
    return base_system


def save_transposed(initial_file_path : str, file_path : str):
    base_system = load_atrp(initial_file_path)
    with open(file_path, 'w') as f:
        for matrix in base_system:
            if matrix.shape[0] == matrix.shape[1]:
                matrix = matrix.T
            for i in range(matrix.shape[0]):
                for j in range(matrix.shape[1]):
                    f.write('{:.2f} '.format(matrix[i, j]))
                f.write('\n')
