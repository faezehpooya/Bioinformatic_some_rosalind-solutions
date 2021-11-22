import numpy as np
import math


class Node:
    def __init__(self, label):
        self.adj = []
        self.is_leaf = False
        self.label = label
        self.age = 0
        self.edge = []


def find_closest_clusters(D, clusters):
    min_dist = math.inf
    n = len(D)
    ii = -1
    jj = -1
    for i in range(n):
        for j in range(i):
            if i in clusters and j in clusters and D[i][j] < min_dist:
                ii = i
                jj = j
                min_dist = D[i][j]
    return ii, jj, min_dist


def d(i, j, clusters, D):
    if i in clusters and j in clusters:
        return sum([D[cl_i][cl_j] for cl_i in clusters[i] for cl_j in clusters[j]]) / (
                    len(clusters[i]) * len(clusters[j]))
    return None


def UPGMA(D, n):
    clusters = {cluster_i: [cluster_i] for cluster_i in range(n)}
    graph = {i: Node(i) for i in range(n)}

    while len(clusters) > 1:
        i, j, dist = find_closest_clusters(D, clusters)

        new_node = len(graph)
        graph[new_node] = Node(new_node)
        graph[new_node].age = D[i][j] / 2.0

        graph[new_node].adj.append(graph[i])
        graph[new_node].adj.append(graph[j])
        graph[i].adj.append(graph[new_node])
        graph[j].adj.append(graph[new_node])

        new_cluster = clusters[i] + clusters[j]
        clusters[new_node] = new_cluster

        del clusters[i]
        del clusters[j]

        row = [d(i, new_node, clusters, D) for i in range(len(D))] + [0.0]
        for k in range(len(D)):
            D[k].append(row[k])
        D.append(row)

    for key in graph:
        for w in graph[key].adj:
            graph[key].edge.append((w, abs(w.age - graph[key].age)))
    return graph


f = open('input.txt', 'r')
f = f.read()
f = f.splitlines()

n = int(f[0])

D = []
for i in range(n):
    f[i + 1] = f[i + 1].strip()
    row_data = list(map(int, f[i + 1].split()))
    D.append(row_data)

graph = UPGMA(D, n)
for node in graph:
    for e in graph[node].edge:
        print(str(graph[node].label) + '->' + str(e[0].label) + ':' + str("%.3f" % e[1]))
