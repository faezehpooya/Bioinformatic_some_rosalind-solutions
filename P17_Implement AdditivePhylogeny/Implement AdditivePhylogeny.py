import math
import numpy as np


class Node:
    def __init__(self, label):
        self.adj = []
        self.is_leaf = False
        self.label = label


def limb(D, j):
    n = D.shape[0]
    min_dist = np.inf
    for i in range(n):
        for k in range(n):
            if i != j and k != j:
                res = (D[i, j] + D[j, k] - D[i, k]) // 2
                min_dist = min(min_dist, res)
    return min_dist


def find_i_k(D):
    for k in range(D.shape[0] - 1):
        arr = D[k] - D[-1]
        index = np.where(arr == D[k, -1])
        if len(index[0]) > 0:
            return index[0][0], k
    return None


def find_nearest(edge, weight, x, i, k):
    q = [[i]]
    visited = {i}
    res_path = []
    while len(q) > 0:
        path = q.pop()
        node = path[-1]
        visited.add(node)
        if node == k:
            res_path = path
            break
        for adj_node in edge[node]:
            if adj_node not in visited:
                q.append(path + [adj_node])

    dist = 0
    for j in range(len(res_path) - 1):
        s, t = res_path[j], res_path[j + 1]
        if (dist + weight[(s, t)]) > x:
            return s, t, x - dist, dist + weight[(s, t)] - x
        dist += weight[(s, t)]


def additive_phylogeny(D, inner_edge_i):
    n = len(D)

    if n == 2:
        edge = {0: [1], 1: [0]}
        weight = {(0, 1): D[0, 1], (1, 0): D[0, 1]}
        return edge, weight, inner_edge_i

    limb_length = limb(D, n - 1)
    print(limb_length)
    D[:-1, -1] -= limb_length
    D[-1, :-1] -= limb_length

    i, k = find_i_k(D)
    x = D[i, -1]
    print(D)
    print(i, k, x)

    edge, weight, inner_edge_i = additive_phylogeny(D[:-1, :-1], inner_edge_i)
    i_near, k_near, i_x, k_x = find_nearest(edge, weight, x, i, k)
    print(i_near, k_near, i_x, k_x)

    new_node = i_near

    if k_x != 0:
        new_node = inner_edge_i
        inner_edge_i += 1

        edge[i_near].remove(k_near)
        edge[k_near].remove(i_near)

        edge[i_near].append(new_node)
        edge[k_near].append(new_node)

        edge[new_node] = [i_near, k_near]

        weight[(new_node, i_near)] = i_x
        weight[(i_near, new_node)] = i_x

        weight[(new_node, k_near)] = k_x
        weight[(k_near, new_node)] = k_x

        del weight[(i_near, k_near)]
        del weight[(k_near, i_near)]

    edge[new_node].append(n - 1)
    edge[n - 1] = [new_node]
    weight[(n - 1, new_node)] = limb_length
    weight[(new_node, n - 1)] = limb_length
    return edge, weight, inner_edge_i


f = open('input.txt', 'r')
f = f.read()
f = f.splitlines()

n = int(f[0])

matrix = np.zeros((n, n), dtype=np.int32)
for i in range(n):
    f[i + 1] = f[i + 1].strip()
    rowData = np.array(f[i + 1].split()).astype(np.int32)
    matrix[i] += rowData

edge, weight, _ = additive_phylogeny(matrix, n)

for e in edge:
    for v in edge[e]:
        print(str(e) + '->' + str(v) + ':' + str(weight[(e, v)]))



