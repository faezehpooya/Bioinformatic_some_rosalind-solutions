class Node:
    def __init__(self, label):
        self.label = label
        self.adj = []
        self.indegree = 0
        self.outdegree = 0


def suffix(s):
    return s[1:]


def prefix(s):
    return s[:-1]


def generate_contigs():
    global nodes, k
    paths = []
    one_in_one_out = []
    for v in nodes.values():
        if v.indegree == v.outdegree == 1:
            one_in_one_out.append(v)

    for v in nodes.values():
        if not (v.indegree == v.outdegree == 1):
            if v.outdegree > 0:
                for w in v.adj:
                    non_branching_path = v.label + w.label[k-2:]
                    while w.indegree == w.outdegree == 1:
                        one_in_one_out.remove(w)
                        u = w.adj[0]
                        non_branching_path += u.label[k-2:]
                        w = u
                    paths.append(non_branching_path)

    while len(one_in_one_out) > 0:
        v = one_in_one_out.pop()
        u = v.adj[0]
        non_branching_path = v.label
        while u != v:
            non_branching_path += u.label[k-2:]
            one_in_one_out.remove(u)
            u = u.adj[0]
        non_branching_path += u.label[k-2:]
        paths.append(non_branching_path)
    return paths


f = open('rosalind_ba3k.txt', 'r')
f = f.read()
patterns = f.splitlines()
n = len(patterns)
k = len(patterns[0])

overlaps = set()
for p in patterns:
    overlaps.add(prefix(p))
    overlaps.add(suffix(p))

nodes = {}
for s in overlaps:
    nodes[s] = Node(s)

for p in patterns:
    nodes[prefix(p)].adj.append(nodes[suffix(p)])
    nodes[prefix(p)].outdegree += 1
    nodes[suffix(p)].indegree += 1

paths = generate_contigs()

for path in paths:
    print(path)





