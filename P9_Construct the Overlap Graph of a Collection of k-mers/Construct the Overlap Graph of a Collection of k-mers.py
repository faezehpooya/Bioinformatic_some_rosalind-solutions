class Node:
    def __init__(self, label):
        self.label = label
        self.adj = []


def suffix(s):
    return s[1:]


def prefix(s):
    return s[:-1]


f = open('rosalind_ba3c.txt', 'r')
f = f.read()
patterns = f.splitlines()
n = len(patterns)
nodes = [Node(patterns[i]) for i in range(n)]

k = len(f[0])

for i in range(n):
    for j in range(n):
        if i != j and suffix(patterns[i]) == prefix(patterns[j]):
            nodes[i].adj.append(nodes[j])

for i in range(n):
    if len(nodes[i].adj) > 0:
        print(nodes[i].label + " -> " + nodes[i].adj[0].label)







