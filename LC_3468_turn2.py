class Solution:
    def countArrays(self, n: int, l: list[int], r: list[int], diffs: list[int]) -> int:
        pass

def count_arrays(n: int, l: int, r: int, diffs: list[int]) -> int:
    """Counts the number of arrays of length n satisfying lower and upper bounds

    [l, r] for each element and the adjacent difference constraints
    a[i+1] - a[i] = diffs[i].

    The condition a[i+1] - a[i] = diffs[i] means a[i+1] = a[i] + diffs[i].
    Therefore, once a[0] = x is chosen, the entire array is uniquely determined
    by a[i] = x + prefix_sum[i], where prefix_sum[i] = sum(diffs[0...i-1]) with prefix_sum[0] = 0.

    We need l <= a[i] <= r for all 0 <= i < n.
    This translates to:
    l <= x + p[i] <= r  for all i,
    where p[i] is the cumulative sum of diffs up to index i (p[0] = 0).

    So:
    l - p[i] <= x <= r - p[i]  for all i.

    This means x must fall within the intersection of intervals [l - p[i], r - p[i]]
    for all i from 0 to n-1.
    Let L = max(l - p[i]) for all i.
    Let R = min(r - p[i]) for all i.
    The number of valid choices for x is max(0, R - L + 1).
    """
    current_p = 0
    L = l
    R = r

    for d in diffs:
        current_p += d
        L = max(L, l - current_p)
        R = min(R, r - current_p)

    return max(0, R - L + 1)


class Solution:
    def countArrays(self, original: list[int], bounds: list[list[int]], diff: list[int]) -> int:
        pass
    
    def countArrays2(self, n: int, l: int, r: int, diffs: list[int]) -> int:
        return count_arrays(n, l, r, diffs)


if __name__ == "__main__":
    sol = Solution()
    print(sol.countArrays2(3, 1, 5, [1, -1]))  # Output: 4

# --- DYNAMIC AUTOMATED TEST HARNESS ---
if __name__ == '__main__':
    import inspect
    sol = Solution()
    # Find the user's defined method on Solution (skipping dunder methods)
    methods = [m for m in dir(sol) if not m.startswith('_') and callable(getattr(sol, m))]
    if not methods:
        raise AttributeError("No solution method found in class Solution")
    target_method = getattr(sol, methods[0])

    assert target_method(original=[1, 2, 3], bounds=[[1, 3], [2, 4], [3, 5]]) == 3
    assert target_method(original=[1, 1], bounds=[[1, 1], [1, 1]]) == 1
