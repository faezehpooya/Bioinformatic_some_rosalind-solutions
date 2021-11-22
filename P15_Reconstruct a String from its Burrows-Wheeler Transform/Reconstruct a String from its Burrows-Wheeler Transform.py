def change_char(s, ind, c):
    return s[:ind] + c + s[ind + 1:]


def shift_right_and_add(s, c, n):
    return c + s[:n]


transform = 'TTCCTAACG$A'
n = len(transform)
text = ''
bwt_matrix = ['x'*(n-1) for j in range(n)]

sorted_transform = sorted(transform)
for i in range(n):
    bwt_matrix[i] = change_char(bwt_matrix[i], 0, sorted_transform[i])

for i in range(n-1):
    for j in range(n):
        bwt_matrix[j] = shift_right_and_add(bwt_matrix[j], transform[j], n-1)
    bwt_matrix.sort()

text = bwt_matrix[0][1:] + '$'

print(text)

