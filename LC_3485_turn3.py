import sys


def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    n = int(input_data[0])
    k = int(input_data[1])
    strings = input_data[2 : 2 + n]

    # Trie using arrays of size 26 for children and a list for counts to maximize performance
    # Node 0 is the root.
    trie_children = [{} for _ in range(1)]
    trie_count = [0]

    for s in strings:
        curr = 0
        trie_count[curr] += 1
        for ch in s:
            ci = ord(ch) - 97
            if ci not in trie_children[curr]:
                new_node = len(trie_count)
                trie_children[curr][ci] = new_node
                trie_children.append({})
                trie_count.append(0)
                curr = new_node
            else:
                curr = trie_children[curr][ci]
            trie_count[curr] += 1

    ans = [None] * n
    for i, s in enumerate(strings):
        curr = 0
        current_len = 0
        for ch in s:
            ci = ord(ch) - 97
            nxt = trie_children[curr].get(ci)
            if nxt is not None and trie_count[nxt] - 1 >= k:
                current_len += 1
                curr = nxt
            else:
                break
        ans[i] = str(current_len)

    sys.stdout.write(" ".join(ans) + "\n")


if __name__ == "__main__":
    solve()

# --- DYNAMIC AUTOMATED TEST HARNESS ---
if __name__ == '__main__':
    import inspect
    sol = Solution()
    # Find the user's defined method on Solution (skipping dunder methods)
    methods = [m for m in dir(sol) if not m.startswith('_') and callable(getattr(sol, m))]
    if not methods:
        raise AttributeError("No solution method found in class Solution")
    target_method = getattr(sol, methods[0])

    assert target_method(words=['abc', 'abd', 'ab', 'a'], k=2) == [2, 2, 2, 2]
    assert target_method(words=['a', 'b'], k=1) == [1, 1]
