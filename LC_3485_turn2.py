import sys


class TrieNode:
    __slots__ = ("children", "count")

    def __init__(self):
        self.children = {}
        self.count = 0


def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    n = int(input_data[0])
    k = int(input_data[1])
    strings = input_data[2 : 2 + n]

    root = TrieNode()

    # Insert all strings into the trie
    for s in strings:
        curr = root
        curr.count += 1
        for ch in s:
            if ch not in curr.children:
                curr.children[ch] = TrieNode()
            curr = curr.children[ch]
            curr.count += 1

    ans = []
    # For each string, find the max common prefix length shared by at least k of the OTHER strings
    for s in strings:
        curr = root
        current_len = 0

        valid = True
        for ch in s:
            if not valid:
                break
            nxt = curr.children.get(ch)
            if nxt and nxt.count - 1 >= k:
                current_len += 1
                curr = nxt
            else:
                valid = False

        ans.append(str(current_len))

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
