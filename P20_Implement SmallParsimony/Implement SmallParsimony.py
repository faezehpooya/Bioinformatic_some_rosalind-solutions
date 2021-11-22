import random

alphabet = ['A', 'T', 'C', 'G']


class Node:
    def __init__(self, label):
        self.label = label
        self.is_leaf = False
        self.alignment = ''


class Graph:
    def __init__(self, m):
        self.nodes = {node_i: None for node_i in range(m)}
        self.edges = {node_i: [] for node_i in range(m)}
        self.labels = {i: '' for i in range((m + 1)//2)}
        self.assignments = {node_i: '' for node_i in range(m)}


def get_ripe(T, tag):
    for v in T.nodes:
        if not tag[v] and v in T.edges:
            for e in T.edges[v]:
                if e > v:
                    continue
                if not tag[e]:
                    break
            return v
    return None


def calc_s(symbol, v, s, T):
    def delta(i):
        return 0 if symbol == alphabet[i] else 1

    def get_min(e):
        return min(s[e][i] + delta(i) for i in range(len(alphabet)))

    return sum([get_min(e) for e in T.edges[v] if e < v])


def update_assignments(v, s):
    index = 0
    min_s = float('inf')
    for i in range(len(s)):
        if s[i] < min_s:
            min_s = s[i]
            index = i
    T.assignments[v] += alphabet[index]
    return alphabet[index]


def backtrack(v, s, current_assignment):
    for v_next in T.edges[v]:
        if v_next < v:
            if T.nodes[v_next].is_leaf:
                continue
            if not v_next in T.assignments:
                T.assignments[v_next] = ''
            min_score = min(s[v_next])
            indices = [i for i in range(len(alphabet)) if s[v_next][i] == min_score]
            matched = False
            for i in indices:
                if alphabet[i] == current_assignment:
                    matched = True
                    T.assignments[v_next] += current_assignment
                    backtrack(v_next, s, current_assignment)
            if not matched:
                next_assignment = alphabet[indices[random.randrange(0, (len(indices)))]]
                T.assignments[v_next] += next_assignment
                backtrack(v_next, s, next_assignment)


def small_parsimony_1(T, character):
    global alphabet
    tag = {}
    s = {}

    for v in T.nodes:
        tag[v] = 0
        if T.nodes[v].is_leaf:
            tag[v] = 1
            s[v] = [0 if symbol == character[v] else float('inf') for symbol in alphabet]

    v = get_ripe(T, tag)
    while v is not None:
        tag[v] = True
        s[v] = [calc_s(symbol, v, s, T) for symbol in alphabet]
        v_last = v
        v = get_ripe(T, tag)

    backtrack(v_last, s, update_assignments(v_last, s[v_last]))
    return min([s[v_last][c] for c in range(len(alphabet))])


def small_parsimony(T):
    scores = [small_parsimony_1(T, [v[i] for l, v in T.labels.items()]) for i in range(len(T.labels[0]))]
    return sum(scores), scores


def hamming_distance(s1, s2):
    hamdis = 0
    for i in range(len(s1)):
        if s1[i] != s2[i]:
            hamdis += 1
    return hamdis


f = open('input.txt', 'r')
f = f.read()
f = f.splitlines()

n = int(f[0])
node_num = 2 * n - 1

T = Graph(node_num)

nodes_info = []
for i in range(1, len(f)):
    line = f[i]
    line = line.replace("->", ":")
    line = line.split(":")
    if i < n + 1:
        internal = int(line[0])
        internal_node = Node(internal)

        leaf = str(line[1])
        leaf_node = Node(i - 1)
        leaf_node.is_leaf = True
        leaf_node.alignment = leaf
        T.assignments[i - 1] = leaf

        T.labels[i - 1] = leaf

        T.nodes[internal] = internal_node
        T.nodes[i - 1] = leaf_node

        T.edges[internal].append(i - 1)
        T.edges[i - 1].append(internal)
    else:
        node1_ind = int(line[0])
        node1 = Node(node1_ind)

        node2_ind = int(line[1])
        node2 = Node(node2_ind)

        T.nodes[node1_ind] = node1

        T.edges[node1_ind].append(node2_ind)
        T.edges[node2_ind].append(node1_ind)


score, _ = small_parsimony(T)

result = str(score) + '\n'

for v in T.nodes:
    for e in T.edges[v]:
        result += T.assignments[v] + '->' + T.assignments[e] + ':' + str(hamming_distance(T.assignments[v], T.assignments[e])) + '\n'

f = open('output.txt', 'w')
f = f.write(result)






