import itertools


def find_kmers(dna, k):
    mer = {}
    for i in range(len(dna) - k + 1):
        if dna[i:i + k] not in mer.keys():
            mer[dna[i:i + k]] = 1
        else:
            mer[dna[i:i + k]] += 1
    return mer


def reverse_compliment(s):
    compliments = {'A': 'T', 'C': 'G', 'G': 'C', 'T': 'A'}
    rc = ''
    for i in range(len(s) - 1, -1, -1):
        rc += compliments[s[i]]
    return rc


def hamming_distance(s1, s2):
    hamdis = 0
    for i in range(len(s1)):
        if s1[i] != s2[i]:
            hamdis += 1
    return hamdis


f = open('rosalind_ba1j.txt', 'r')
f = f.read()
f = f.splitlines()

dna = f[0]
k, d = map(int, f[1].split(" "))

nucleotide = ['A', 'C', 'G', 'T']

kmers_all = [''.join(x) for x in itertools.product('ACGT', repeat=k)]
dna_kmers = find_kmers(dna, k)
count = {}

for km in kmers_all:
    count[km] = 0
    km_rc = reverse_compliment(km)
    for key in dna_kmers.keys():
        if hamming_distance(km, key) <= d:
            count[km] += dna_kmers[key]
        if hamming_distance(km_rc, key) <= d:
            count[km] += dna_kmers[key]

maxcount = max(count.values())
for key, value in count.items():
    if count[key] == maxcount:
        print(key, end=" ", flush=True)
