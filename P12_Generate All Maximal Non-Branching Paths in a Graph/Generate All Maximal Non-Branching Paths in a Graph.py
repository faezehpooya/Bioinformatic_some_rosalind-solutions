import math
class Node:
    def __init__(self, label):
        self.label = label
        self.adj = []
        self.indegree = 0
        self.outdegree = 0


def maximal_nonBranching_paths(nodes):
    paths = []
    one_in_one_out = []
    for v in nodes:
        if v.indegree == v.outdegree == 1:
            one_in_one_out.append(v)

    for v in nodes:
        if not (v.indegree == v.outdegree == 1):
            if v.outdegree > 0:
                for w in v.adj:
                    non_branching_path = str(v.label) + ' -> ' + str(w.label)
                    while w.indegree == w.outdegree == 1:
                        one_in_one_out.remove(w)
                        u = w.adj[0]
                        non_branching_path += ' -> ' + str(u.label)
                        w = u
                    paths.append(non_branching_path)

    while len(one_in_one_out) > 0:
        v = one_in_one_out.pop()
        u = v.adj[0]
        non_branching_path = str(v.label) + ' -> '
        while u != v:
            non_branching_path += str(u.label) + ' -> '
            one_in_one_out.remove(u)
            u = u.adj[0]
        non_branching_path += str(u.label)
        paths.append(non_branching_path)
    return paths


f = open('dataset_206173_2.txt', 'r')
f = f.read()
f = f.splitlines()

nodes_info = []
nodes_max = 0
nodes_min = math.inf

for i in range(len(f)):
    line = f[i]
    line = line.split(" -> ")
    node = int(line[0])
    adj_list = list(map(int, line[1].split(",")))
    nodes_info.append([node, adj_list])
    nodes_max = max(nodes_max, node, max(adj_list))
    nodes_min = min(nodes_min, node, min(adj_list))

n = nodes_max - nodes_min + 1
nodes = [Node(i + nodes_min) for i in range(n)]
for v in nodes_info:
    for u in v[1]:
        nodes[v[0] - nodes_min].adj.append(nodes[u - nodes_min])
        nodes[v[0] - nodes_min].outdegree += 1
        nodes[u - nodes_min].indegree += 1


paths = maximal_nonBranching_paths(nodes)

for path in paths:
    print(path)

