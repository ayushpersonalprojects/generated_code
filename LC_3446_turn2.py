class Solution:

    def diagonalSort(self, mat: list[list[int]]) -> list[list[int]]:
        import collections

        m, n = len(mat), len(mat[0])
        diags = collections.defaultdict(list)

        for i in range(m):
            for j in range(n):
                diags[i - j].append(mat[i][j])

        # Sort each diagonal in non-increasing order
        for key in diags:
            diags[key].sort(reverse=True)

        for i in range(m):
            for j in range(n):
                mat[i][j] = diags[i - j].pop()

        return mat

# --- DYNAMIC AUTOMATED TEST HARNESS ---
if __name__ == '__main__':
    import inspect
    sol = Solution()
    # Find the user's defined method on Solution (skipping dunder methods)
    methods = [m for m in dir(sol) if not m.startswith('_') and callable(getattr(sol, m))]
    if not methods:
        raise AttributeError("No solution method found in class Solution")
    target_method = getattr(sol, methods[0])

    assert target_method(grid=[[1, 2, 3], [4, 5, 6], [7, 8, 9]]) == [[9, 6, 3], [8, 5, 2], [7, 4, 1]]
