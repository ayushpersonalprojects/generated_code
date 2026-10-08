from collections import Counter
from math import inf


def max_difference(s: str, k: int) -> int:
    """Given a string `s` and a minimum substring length `k`,

    maximize the difference (frequency of an odd-frequency character -
    frequency of an even-frequency character) over all substrings of length >= k.

    An even-frequency character must have a frequency > 0 (i.e., it actually
    appears in the substring).
    """
    n = len(s)
    # Convert characters to 0-25 integers
    arr = [ord(c) - ord("a") for c in s]

    max_diff = -inf

    # There are 26 possible odd frequency characters and 26 possible even frequency characters.
    # To make the difference (odd - even) as large as possible, we can iterate over all
    # pairs of character types (odd_char, even_char) that could appear in the substring.
    # Note: odd_char and even_char can be the same if a character has an even frequency,
    # but the problem asks for "an odd frequency and an even frequency", which usually implies
    # distinct characters or just any pair. Let's assume they can be any two characters (or the same,
    # though usually they are distinct). Wait, if odd_char == even_char, its frequency is both odd and even,
    # which is impossible. So odd_char != even_char.

    distinct_chars = set(arr)
    present_list = list(distinct_chars)

    # Prefix sums for counts and parity
    # Since we need to optimize for a specific pair of characters (x, y),
    # let's fix character x to have odd frequency and character y to have even frequency.
    # Let cnt[c][i] be the count of character c in prefix of length i.
    # We want to maximize (cnt[x][j] - cnt[x][i]) - (cnt[y][j] - cnt[y][i])
    # = (cnt[x][j] - cnt[y][j]) - (cnt[x][i] - cnt[y][i])
    # Subject to:
    # 1. j - i >= k
    # 2. (cnt[x][j] - cnt[x][i]) % 2 == 1
    # 3. (cnt[y][j] - cnt[y][i]) % 2 == 0
    # 4. (cnt[y][j] - cnt[y][i]) > 0

    # Precompute prefix counts for all 26 characters
    pref = [[0] * (n + 1) for _ in range(26)]
    for c in range(26):
        for i in range(n):
            pref[c][i + 1] = pref[c][i] + (1 if arr[i] == c else 0)

    for x in present_list:
        for y in present_list:
            if x == y:
                continue

            # We need to find 0 <= i <= j - k <= n - k
            # such that:
            # (pref[x][j] - pref[x][i]) is odd  -> pref[x][j] % 2 != pref[x][i] % 2
            # (pref[y][j] - pref[y][i]) is even -> pref[y][j] % 2 == pref[y][i] % 2
            # pref[y][j] - pref[y][i] > 0     -> pref[y][j] > pref[y][i]

            # Let's categorize the index i by:
            # - parity of pref[x][i] (0 or 1)
            # - parity of pref[y][i] (0 or 1)
            # - value of pref[y][i] (to handle > 0 constraint, or we can use a Fenwick tree / RMQ)

            # Since pref[y][j] - pref[y][i] > 0, we need pref[y][i] < pref[y][j].
            # For a fixed j, we want to minimize (pref[x][i] - pref[y][i])
            # over all valid i <= j - k.

            # We can maintain the minimums of (pref[x][i] - pref[y][i])
            # grouped by (pref[x][i] % 2, pref[y][i] % 2, pref[y][i]).
            # But pref[y][i] can range from 0 to n.
            # We can use a data structure (like a Fenwick tree or array of minimums)
            # because as j increases, new indices i become valid (i = j - k).

            # Let's use an array of minimum values for each (parity_x, parity_y, val_y).
            # Since val_y goes up to n, we can maintain min_val[p_x][p_y][v_y].
            # To query efficiently for < pref[y][j], we can use a Fenwick tree for each (p_x, p_y)
            # storing the minimum of (pref[x][i] - pref[y][i]) at index v_y = pref[y][i].

            # Initialize Fenwick trees:
            # We have 2 * 2 = 4 combinations of parities for (p_x, p_y).
            # p_x = pref[x][i] % 2
            # p_y = pref[y][i] % 2

            # We need:
            # p_x_i != p_x_j  =>  p_x_i = 1 - (pref[x][j] % 2)
            # p_y_i == p_y_j  =>  p_y_i = pref[y][j] % 2
            # val_y_i < pref[y][j]

            # So for a fixed j, we need the minimum (pref[x][i] - pref[y][i])
            # over all i <= j - k such that:
            # pref[x][i] % 2 == 1 - (pref[x][j] % 2)
            # pref[y][i] % 2 == pref[y][j] % 2
            # pref[y][i] < pref[y][j]

            # We can implement this with 4 Fenwick trees, each of size n + 2.
            # Fenwick tree stores minimums.

            class FenwickMin:

                def __init__(self, size):
                    self.size = size
                    self.tree = [inf] * (size + 1)

                def update(self, idx, val):
                    idx += 1  # 1-based indexing
                    while idx <= self.size:
                        if val < self.tree[idx]:
                            self.tree[idx] = val
                        idx += idx & (-idx)

                def query_prefix(self, idx):
                    # returns min in range [0, idx]
                    idx += 1
                    res = inf
                    while idx > 0:
                        if self.tree[idx] < res:
                            res = self.tree[idx]
                        idx -= idx & (-idx)
                    return res

            fenwicks = [[FenwickMin(n + 1) for _ in range(2)] for _ in range(2)]

            # As j goes from k to n, we can add i = j - k to the Fenwick trees.
            for j in range(k, n + 1):
                i_add = j - k
                px_i = pref[x][i_add] % 2
                py_i = pref[y][i_add] % 2
                val_i = pref[y][i_add]
                val_diff = pref[x][i_add] - pref[y][i_add]
                fenwicks[px_i][py_i].update(val_i, val_diff)

                px_j = pref[x][j] % 2
                py_j = pref[y][j] % 2
                val_j = pref[y][j]

                target_px = 1 - px_j
                target_py = py_j

                # We need val_y_i < val_j, so query prefix val_j - 1
                if val_j > 0:
                    min_prev = fenwicks[target_px][target_py].query_prefix(
                        val_j - 1
                    )
                    if min_prev != inf:
                        current_diff = (pref[x][j] - pref[y][j]) - min_prev
                        if current_diff > max_diff:
                            max_diff = current_diff

    return int(max_diff) if max_diff != -inf else -1

# --- DYNAMIC AUTOMATED TEST HARNESS ---
if __name__ == '__main__':
    import inspect
    sol = Solution()
    # Find the user's defined method on Solution (skipping dunder methods)
    methods = [m for m in dir(sol) if not m.startswith('_') and callable(getattr(sol, m))]
    if not methods:
        raise AttributeError("No solution method found in class Solution")
    target_method = getattr(sol, methods[0])

    assert target_method(s='12233', k=4) == -1
    assert target_method(s='112221', k=3) == 1
