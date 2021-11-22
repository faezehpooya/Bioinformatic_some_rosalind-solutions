f = open('rosalind_ba1h.txt', 'r')
f = f.read()
f = f.splitlines()

s = f[1]
p = f[0]
d = int(f[2])
k = len(p)
output = []

for i in range(len(s) - k + 1):
    k_mer = s[i:(i+k)]
    mismatch = 0
    for j in range(k):
        if k_mer[j] != p[j]:
            mismatch += 1
    if mismatch <= d:
        output.append(i)

for x in output:
    print(x, end=' ', flush=True)
