import math

class Node:
    def __init__(self, label):
        self.label = label
        self.adj = []
        self.visited = False
        self.par = None


def dfs(u):
    global nodes, topological_order
    u.visited = True
    for v in u.adj:
        if not v[0].visited:
            dfs(v[0])
    topological_order.append(u)


def longest_path(s, n, d):
    global topological_order
    dist = [-math.inf] * n
    dist[s.label] = 0

    for u in topological_order:
        for v in u.adj:
            if dist[v[0].label] < dist[u.label] + v[1]:
                dist[v[0].label] = dist[u.label] + v[1]
                v[0].par = u

    length = dist[d.label]
    lp = []
    while d is not None:
        lp.append(d.label)
        d = d.par

    return length, lp


f = open('rosalind_ba5d.txt', 'r')
f = f.read()
f = f.splitlines()

src = int(f[0])
sink = int(f[1])

topological_order = []
nodes_info = []
nodes_num = 0
for i in range(2, len(f)):
    line = f[i]
    line = line.replace("->", ":")
    line = line.split(":")
    node1 = int(line[0])
    node2 = int(line[1])
    weight = int(line[2])
    nodes_info += [node1, node2, weight]
    nodes_num = max(nodes_num, node1)
    nodes_num = max(nodes_num, node2)

n = nodes_num + 1
nodes = [Node(i) for i in range(n)]

for i in range(0, len(nodes_info), 3):
    node1 = nodes_info[i]
    node2 = nodes_info[i + 1]
    weight = nodes_info[i + 2]
    nodes[node1].adj.append((nodes[node2], weight))


dfs(nodes[src])
topological_order.reverse()
for node in topological_order:
    print(node.label)

length, lp = longest_path(nodes[src], n, nodes[sink])
lp.reverse()
print(length)
path = ''
for node in lp:
    path += str(node) + '->'
print(path[:-2])


