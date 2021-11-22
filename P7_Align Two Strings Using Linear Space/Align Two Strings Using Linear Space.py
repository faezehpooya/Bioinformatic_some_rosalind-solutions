from Bio.SubsMat import MatrixInfo


def get_score(score):
    global blosum
    try:
        res = blosum[(score[0], score[1])]
    except:
        res = blosum[(score[1], score[0])]
    return res


def insert_indel(word, x):
    return word[:x] + '-' + word[x:]


def middle_column_score(v, w):
    global indel_penalty
    n = len(v)
    m = len(w)

    S = [[i * j * indel_penalty for j in range(-1, 1)] for i in range(n + 1)]
    S[0][1] = -1 * indel_penalty
    backtrack = [0] * (n + 1)

    for j in range(1, m // 2 + 1):
        for i in range(n + 1):
            if i == 0:
                S[i][1] = -j * indel_penalty
            else:
                scores = [S[i-1][0] + get_score([v[i-1], w[j-1]]), S[i][0] - indel_penalty, S[i-1][1] - indel_penalty]
                S[i][1] = max(scores)
                backtrack[i] = scores.index(S[i][1])

        if j != m // 2:
            S = [[row[1]] * 2 for row in S]

    return [row[1] for row in S], backtrack


def middle_edge(v, w):
    global indel_penalty
    source_to_middle, _ = middle_column_score(v, w)

    middle_to_sink, backtrack = map(lambda l: l[::-1],
                                  middle_column_score(v[::-1], w[::-1] + ['', '$'][len(w) % 2 == 1 and len(w) > 1]))

    scores = list(map(sum, zip(source_to_middle, middle_to_sink)))
    max_middle = max(range(len(scores)), key=lambda i: scores[i])

    if max_middle == (len(scores) - 1):
        next_node = (max_middle, len(w) // 2 + 1)
    else:
        next_node = [(max_middle + 1, (len(w)) // 2 + 1), (max_middle, (len(w)) // 2 + 1),
                     (max_middle + 1, (len(w)) // 2)][backtrack[max_middle]]
    return (max_middle, (len(w)) // 2), next_node


def global_alignment(v, w):
    global indel_penalty
    n = len(v)
    m = len(w)
    S = [[0 for j in range(m + 1)] for i in range(n + 1)]
    backtrack = [[0 for j in range(m + 1)] for i in range(n + 1)]

    for i in range(1, n + 1):
        S[i][0] = -i * indel_penalty
    for j in range(1, m + 1):
        S[0][j] = -j * indel_penalty

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            scores = [S[i-1][j] - indel_penalty, S[i][j-1] - indel_penalty, S[i-1][j-1] + get_score([v[i-1], w[j-1]])]
            S[i][j] = max(scores)
            backtrack[i][j] = scores.index(S[i][j])

    v_aligned = v
    w_aligned = w
    i = n
    j = m
    max_score = str(S[i][j])

    while i * j != 0:
        if backtrack[i][j] == 0:
            i -= 1
            w_aligned = insert_indel(w_aligned, j)
        elif backtrack[i][j] == 1:
            j -= 1
            v_aligned = insert_indel(v_aligned, i)
        else:
            i -= 1
            j -= 1

    for x in range(i):
        w_aligned = insert_indel(w_aligned, 0)
    for x in range(j):
        v_aligned = insert_indel(v_aligned, 0)

    return str(max_score), v_aligned, w_aligned


def linear_space_alignment(top, bottom, left, right):
    global v, w
    if left == right:
        return [v[top:bottom], '-' * (bottom - top)]

    if top == bottom:
        return ['-' * (right - left), w[left:right]]

    if bottom - top == 1 or right - left == 1:
        return global_alignment(v[top:bottom], w[left:right])[1:]

    mid_node, next_node = middle_edge(v[top:bottom], w[left:right])
    mid_node = tuple(map(sum, zip(mid_node, [top, left])))
    next_node = tuple(map(sum, zip(next_node, [top, left])))
    cur_node = [['-', v[mid_node[0] % len(v)]][next_node[0] - mid_node[0]],
                ['-', w[mid_node[1] % len(w)]][next_node[1] - mid_node[1]]]

    A = linear_space_alignment(top, mid_node[0], left, mid_node[1])
    B = linear_space_alignment(next_node[0], bottom, next_node[1], right)
    return [A[i] + cur_node[i] + B[i] for i in range(2)]


indel_penalty = 5
blosum = MatrixInfo.blosum62

f = open('input.txt', 'r')
f = f.read()
f = f.splitlines()

v = f[0]
w = f[1]


n = len(v)
m = len(w)

v_aligned, w_aligned = linear_space_alignment(0, n, 0, m)
score = sum([-1 * indel_penalty if '-' in pair else get_score(pair) for pair in zip(v_aligned, w_aligned)])

print(score)
print(v_aligned)
print(w_aligned)
