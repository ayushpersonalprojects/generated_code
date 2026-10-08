class Solution:
    def countArrays(self, n: int, l: int, r: int, diffs: list[int]) -> int:
        """Counts the number of arrays of length n satisfying lower and upper bounds

        [l, r] for each element and the adjacent difference constraints
        a[i+1] - a[i] = diffs[i].
        """
        current_p = 0
        L = l
        R = r

        for d in diffs:
            current_p += d
            L = max(L, l - current_p)
            R = min(R, r - current_p)

        return max(0, R - L + 1)


if __name__ == "__main__":
    sol = Solution()
    print(sol.countArrays(3, 1, 5, [1, -1]))  # Output: 4

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
