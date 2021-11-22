import numpy as np
# s = open('rosalind_ba1f.txt', 'r')
# s = s.read()
s = 'CCTATCGGTGGATTAGCATGTCCCTGTACGTTTCGCCGCGAACTAGTTCACACGGCTTGATGGCAAATGGTTTTTCCGGCGACCGTAATCGTCCACCGAG'

skew = 0
prefix = np.array([0])
for c in s:
    if c == 'C':
        skew -= 1
    elif c == 'G':
        skew += 1

    prefix = np.append(prefix, skew)
print(prefix)
min_skew = np.where(prefix == prefix.min())
for x in np.nditer(min_skew):
    print(x, end=" ", flush=True)
