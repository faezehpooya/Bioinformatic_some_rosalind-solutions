def hamming_distance(s1, s2):
    hamdis = 0
    for i in range(len(s1)):
        if s1[i] != s2[i]:
            hamdis += 1
    return hamdis


f = open('input.txt', 'r')
f = f.read()
f = f.splitlines()
text = f[0]
patterns = f[1].split()
d = int(f[2])

result = []

for pattern in patterns:
    for i in range(len(text) - len(pattern) + 1):
        if hamming_distance(pattern, text[i: i + len(pattern)]) <= d:
            result.append(i)

for i in range(len(result)):
    print(result[i], end=' ', flush=True)

