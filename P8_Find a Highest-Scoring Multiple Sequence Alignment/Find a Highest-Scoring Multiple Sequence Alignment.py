f = open('rosalind_ba5m.txt', 'r')
f = f.read()
f = f.splitlines()

v = f[0]
w = f[1]
u = f[2]


n = len(v) + 1
m = len(w) + 1
t = len(u) + 1
s = [[[0 for i in range(t)] for j in range(m)] for k in range(n)]
backtrace = [[[0 for i in range(t)] for j in range(m)] for k in range(n)]

# initializing backtrace table
for i in range(n):
    backtrace[i][0][0] = 4

for j in range(m):
    backtrace[0][j][0] = 6

for k in range(t):
    backtrace[0][0][k] = 7

for i in range(n):
    for j in range(m):
        backtrace[i][j][0] = 2

for i in range(n):
    for k in range(t):
        backtrace[i][0][k] = 3

for j in range(m):
    for k in range(t):
        backtrace[0][j][k] = 5


def cal_score(a, b, c):
    if a == b == c:
        return 1
    return 0


for i in range(1, n):
    for j in range(1, m):
        for k in range(1, t):
            score = cal_score(v[i-1], w[j-1], u[k-1])
            s[i][j][k] = max(s[i-1][j-1][k-1] + score,
                             s[i-1][j-1][k],
                             s[i-1][j][k-1],
                             s[i-1][j][k],
                             s[i][j-1][k-1],
                             s[i][j-1][k],
                             s[i][j][k-1])

            if s[i][j][k] == (s[i-1][j-1][k-1] + score):
                backtrace[i][j][k] = 1
            elif s[i][j][k] == s[i-1][j-1][k]:
                backtrace[i][j][k] = 2
            elif s[i][j][k] == s[i-1][j][k-1]:
                backtrace[i][j][k] = 3
            elif s[i][j][k] == s[i-1][j][k]:
                backtrace[i][j][k] = 4
            elif s[i][j][k] == s[i][j-1][k-1]:
                backtrace[i][j][k] = 5
            elif s[i][j][k] == s[i][j-1][k]:
                backtrace[i][j][k] = 6
            elif s[i][j][k] == s[i][j][k-1]:
                backtrace[i][j][k] = 7

i = n-1
j = m-1
k = t-1

v1, w1, u1 = '','',''


while i > 0 or j > 0 or k > 0:
    if backtrace[i][j][k] == 1:
        v1 = v[i-1] + v1
        w1 = w[j-1] + w1
        u1 = u[k-1] + u1
        i -= 1
        j -= 1
        k -= 1
    elif backtrace[i][j][k] == 2:
        v1 = v[i - 1] + v1
        w1 = w[j - 1] + w1
        u1 = '-' + u1
        i -= 1
        j -= 1
    elif backtrace[i][j][k] == 3:
        v1 = v[i - 1] + v1
        w1 = '-' + w1
        u1 = u[k - 1] + u1
        i -= 1
        k -= 1
    elif backtrace[i][j][k] == 5:
        v1 = '-' + v1
        w1 = w[j - 1] + w1
        u1 = u[k - 1] + u1
        j -= 1
        k -= 1
    elif backtrace[i][j][k] == 4:
        v1 = v[i - 1] + v1
        w1 = '-' + w1
        u1 = '-' + u1
        i -= 1
    elif backtrace[i][j][k] == 6:
        v1 = '-' + v1
        w1 = w[j-1] + w1
        u1 = '-' + u1
        j -= 1
    elif backtrace[i][j][k] == 7:
        v1 = '-' + v1
        w1 = '-' + w1
        u1 = u[k-1] + u1
        k -= 1


print(s[n-1][m-1][t-1])
print(v1)
print(w1)
print(u1)
