class TrieNode:
    def __init__(self, label):
        self.children = [None] * 26
        self.is_leaf = False
        self.label = label


class Trie:
    def __init__(self):
        self.last_i = 0
        self.root = self.get_node()

    def get_node(self):
        new_node = TrieNode(self.last_i)
        self.last_i += 1
        return new_node

    def char_to_index(self, char):
        return ord(char) - ord('A')


def trie_costruction(patterns):
    node_list = []
    trie = Trie()
    for pattern in patterns:
        cur_node = trie.root
        for i in range(len(pattern)):
            cur_symbol = pattern[i]
            cur_index = trie.char_to_index(cur_symbol)
            if cur_node.children[cur_index] is None:
                new_node = trie.get_node()
                cur_node.children[cur_index] = new_node
                node_list.append((cur_node.label, new_node.label, cur_symbol))

            cur_node = cur_node.children[cur_index]
        cur_node.is_leaf = True
    return trie, node_list


def prefix_trie_matching(text, trie):
    i = 1
    symbol = text[0]
    v = trie.root
    while True:
        if v.is_leaf:
            return True
        w = v.children[trie.char_to_index(symbol)]
        if w is not None and i < len(text):
            symbol = text[i]
            i += 1
            v = w
        elif w is not None and i == len(text):
            v = w
        else:
            return False


def trie_matching(text, trie):
    i = 0
    results = []
    while len(text) > 0:
        res = prefix_trie_matching(text, trie)
        if res:
            results.append(i)
        i += 1
        text = text[1:]
    return results


f = open('input.txt', 'r')
f = f.read()
f = f.splitlines()
text = f[0]
patterns = f[1:]

trie, _ = trie_costruction(patterns)

output = trie_matching(text, trie)
for i in range(len(output)):
    print(output[i], end=' ', flush=True)

