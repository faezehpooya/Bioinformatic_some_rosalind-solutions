class Node:
    def __init__(self, label):
        self.label = label
        self.adj = []
        self.indegree = 0
        self.outdegree = 0


f = open('input.txt', 'r')
f = f.read()
f = f.splitlines()

nodes_info = []
nodes_num = 0

for i in range(len(f)):
    line = f[i]
    line = line.split(" -> ")
    node = int(line[0])
    adj_list = list(map(int, line[1].split(",")))
    nodes_info.append([node, adj_list])
    nodes_num = max(nodes_num, node, max(adj_list))

n = nodes_num + 1
nodes = [Node(i) for i in range(n)]
for v in nodes_info:
    for u in v[1]:
        nodes[v[0]].adj.append(nodes[u])
        nodes[v[0]].outdegree += 1
        nodes[u].indegree += 1

a = nodes[0]
b = nodes[1]
for node in nodes:
    if node.indegree + 1 == node.outdegree:
        a = node
    elif node.indegree == node.outdegree + 1:
        b = node

b.adj.append(a)
b.outdegree += 1
a.indegree += 1

stack = [b]
eulerian_path = []
while len(stack) > 0:
    u = stack[-1]
    if len(u.adj) > 0:
        v = u.adj.pop()
        stack.append(v)
    else:
        eulerian_path.append(stack.pop())

eulerian_path.reverse()
path = ''
for i in range(1, len(eulerian_path)):
    path += str(eulerian_path[i].label) + '->'

print(path[:-2])

f = open('output.txt', 'w')
f = f.write(path[:-2])





