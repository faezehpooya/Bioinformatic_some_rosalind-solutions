import math


def remove(i, D):
    D_new = []
    for j in range(len(D)):
        if j != i:
            D_new.append([D[j][k] for k in range(len(D[j])) if k != i])
    return D_new


def construct_D_star(D, total_distance_D):
    n = len(D)
    D_star = [[0 for i in range(n)] for j in range(n)]
    for i in range(n):
        for j in range(n):
            if i == j:
                D_star[i][j] = 0
            else:
                D_star[i][j] = (n - 2) * D[i][j] - total_distance_D[i] - total_distance_D[j]
    return D_star


def construct_total_distance_D(D):
    n = len(D)
    total_distance_D = [0 for i in range(n)]
    for i in range(n):
        total_distance_D[i] = sum(D[i][k] for k in range(n))
    return total_distance_D


def find_min_elem(D_star):
    min_elem = math.inf
    ii = -1
    jj = -1
    for i in range(len(D_star)):
        for j in range(i):
            if D_star[i][j] <= min_elem:
                ii = i
                jj = j
                min_elem = D_star[i][j]
    return ii, jj, min_elem


def remove_row_column(D, i, j):
    i += 1
    j += 1
    row_i = D[i]
    row_j = D[j]
    D.remove(row_i)
    D.remove(row_j)

    x, y = (i, j) if i < j else (j, i)
    for k in range(len(D)):
        D[k] = D[k][:x] + D[k][x + 1:y] + D[k][y + 1:]

    return D


def neighbour_joining(D, n, node_list=None):
    if node_list is None:
        node_list = list(range(n))

    if n == 2:
        weight = {(node_list[0], node_list[1]): D[0][1], (node_list[1], node_list[0]): D[0][1]}
        return weight

    total_distance_D = construct_total_distance_D(D)
    D_star = construct_D_star(D, total_distance_D)
    i, j, min_elem = find_min_elem(D_star)
    delta = (total_distance_D[i] - total_distance_D[j]) / (n - 2)
    limb_length_i = 0.5 * (D[i][j] + delta)
    limb_length_j = 0.5 * (D[i][j] - delta)

    new_row = [0.5 * (D[k][i] + D[k][j] - D[i][j]) for k in range(n)] + [0]

    D.append(new_row)
    for l in range(n):
        D[l].append(new_row[l])

    D = remove(max(i, j), D)
    D = remove(min(i, j), D)


    new_node = node_list[-1] + 1
    node_list.append(new_node)

    node_i = node_list[i]
    node_j = node_list[j]
    node_list.remove(node_i)
    node_list.remove(node_j)

    weight = neighbour_joining(D, n-1, node_list)

    weight[(new_node, node_i)] = limb_length_i
    weight[(node_i, new_node)] = limb_length_i
    weight[(new_node, node_j)] = limb_length_j
    weight[(node_j, new_node)] = limb_length_j

    return weight


f = open('input.txt', 'r')
f = f.read()
f = f.splitlines()

n = int(f[0])

D = []
for i in range(n):
    f[i + 1] = f[i + 1].strip()
    row_data = list(map(int, f[i + 1].split()))
    D.append(row_data)


weight = neighbour_joining(D, n)
for (v, w) in weight:
    print(str(v) + '->' + str(w) + ':' + str(weight[(v, w)]))
