nucleotide = ['A', 'C', 'G', 'T']


def Neighbors(pattern, d):
    global nucleotide
    if d == 0:
        return [pattern]
    if len(pattern) == 1:
        return nucleotide

    neighborhood = []
    suffix_neighbors = Neighbors(pattern[1:], d)
    for text in suffix_neighbors:
        if hamming_distance(pattern[1:], text) < d:
            for x in nucleotide:
                neighborhood.append(str(x + text))
        else:
            neighborhood.append(str(pattern[0] + text))
    return neighborhood


def hamming_distance(s1, s2):
    hamdis = 0
    for i in range(len(s1)):
        if s1[i] != s2[i]:
            hamdis += 1
    return hamdis


f = open('rosalind_ba1n.txt', 'r')
f = f.read()
f = f.splitlines()
pattern = f[0]
d = int(f[1])

# pattern = 'CGCAGGTCAT'
# d = 3

d_neighborhood = Neighbors(pattern, d)
for i in range(len(d_neighborhood)):
    print(d_neighborhood[i])

