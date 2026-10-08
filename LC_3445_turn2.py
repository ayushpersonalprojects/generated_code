from math import inf


class Solution:

    def maxDifference(self, s: str, k: int) -> int:
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

        distinct_chars = set(arr)
        present_list = list(distinct_chars)

        # Precompute prefix counts for all 26 characters
        pref = [[0] * (n + 1) for _ in range(26)]
        for c in range(26):
            for i in range(n):
                pref[c][i + 1] = pref[c][i] + (1 if arr[i] == c else 0)

        for x in present_list:
            for y in present_list:
                if x == y:
                    continue

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


def max_difference(s: str, k: int) -> int:
    return Solution().maxDifference(s, k)

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
