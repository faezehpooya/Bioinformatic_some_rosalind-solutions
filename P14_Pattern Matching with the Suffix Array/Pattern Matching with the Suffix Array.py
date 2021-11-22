f = open('input.txt', 'r')
f = f.read()
f = f.splitlines()
text = f[0]
patterns = f[1:]

suffix_array = []
n = len(text)

for i in range(n):
    suffix_array.append([i, text])
    text = text[1:]

suffix_array = sorted(suffix_array, key=lambda x: x[1])

result = []

for pattern in patterns:
    right = n - 1
    left = 0
    m = len(pattern)
    mid = (right + left) // 2
    while left <= right:
        mid = (right + left) // 2
        suffix_mid = suffix_array[mid][1][:m]
        if pattern == suffix_mid:
            result.append(suffix_array[mid][0])
            break
        elif pattern > suffix_mid:
            left = mid + 1
        else:
            right = mid - 1
    i = mid - 1
    j = mid + 1
    while i >= 0 and suffix_array[i][1][:m] == pattern:
        result.append(suffix_array[i][0])
        i -= 1

    while j < n and suffix_array[j][1][:m] == pattern:
        result.append(suffix_array[j][0])
        j += 1


for i in range(len(result)):
    print(result[i], end=' ', flush=True)
