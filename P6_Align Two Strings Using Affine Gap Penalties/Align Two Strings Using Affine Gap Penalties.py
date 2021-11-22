from Bio.SubsMat import MatrixInfo
import math


def insert_indel(word, x):
    return word[:x] + '-' + word[x:]


f = open('rosalind_ba5j.txt', 'r')
f = f.read()
f = f.splitlines()

v = f[0]
w = f[1]

opening_penalty = -11
extension_penalty = -1
blosum = MatrixInfo.blosum62

n = len(v) + 1
m = len(w) + 1

middle = [[0 for i in range(m)] for j in range(n)]
lower = [[0 for i in range(m)] for j in range(n)]
upper = [[0 for i in range(m)] for j in range(n)]
backtrack = [[[0 for j in range(m)] for i in range(n)] for k in range(3)]

# initializing tables
for i in range(1, n):
    upper[i][0] = opening_penalty + (i - 1) * extension_penalty
    middle[i][0] = opening_penalty + (i - 1) * extension_penalty
    lower[i][0] = -1 * math.inf

for i in range(1, m):
    upper[0][i] = -1 * math.inf
    middle[0][i] = opening_penalty + (i - 1) * extension_penalty
    lower[0][i] = opening_penalty + (i - 1) * extension_penalty


for i in range(1, n):
    for j in range(1, m):
        lower_scores = [lower[i - 1][j] + extension_penalty, middle[i - 1][j] + opening_penalty]
        lower[i][j] = max(lower_scores)
        backtrack[0][i][j] = lower_scores.index(lower[i][j])

        upper_scores = [upper[i][j - 1] + extension_penalty, middle[i][j - 1] + opening_penalty]
        upper[i][j] = max(upper_scores)
        backtrack[2][i][j] = upper_scores.index(upper[i][j])

        score = [v[i - 1], w[j - 1]]
        try:
            blosum[(score[0], score[1])]
        except:
            score.reverse()

        middle_scores = [lower[i][j], middle[i - 1][j - 1] + blosum[(score[0], score[1])], upper[i][j]]
        middle[i][j] = max(middle_scores)
        backtrack[1][i][j] = middle_scores.index(middle[i][j])

i = n - 1
j = m - 1

v_aligned = v
w_aligned = w

final_scores = [lower[i][j], middle[i][j], upper[i][j]]
max_score = max(final_scores)
backtrack_pointer = final_scores.index(max_score)

while i * j != 0:
    if backtrack_pointer == 0:
        if backtrack[0][i][j] == 1:
            backtrack_pointer = 1
        i -= 1
        w_aligned = insert_indel(w_aligned, j)

    elif backtrack_pointer == 1:
        if backtrack[1][i][j] == 0:
            backtrack_pointer = 0
        elif backtrack[1][i][j] == 2:
            backtrack_pointer = 2
        else:
            i -= 1
            j -= 1

    else:
        if backtrack[2][i][j] == 1:
            backtrack_pointer = 1
        j -= 1
        v_aligned = insert_indel(v_aligned, i)

for x in range(i):
    w_aligned = insert_indel(w_aligned, 0)

for x in range(j):
    v_aligned = insert_indel(v_aligned, 0)


print(max_score)
print(v_aligned)
print(w_aligned)

