import sys


def solve():
    # Read all inputs from standard input
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    n = int(input_data[0])
    A = [int(x) for x in input_data[1 : n + 1]]

    A.sort()

    if n == 1:
        print(0)
        return

    M = max(A)
    LIMIT = max(M * 2, 200000)

    divs = [[] for _ in range(LIMIT + 1)]
    for i in range(1, LIMIT + 1):
        for j in range(i, LIMIT + 1, i):
            divs[j].append(i)

    inf = float("inf")
    dp = [inf] * (LIMIT + 1)
    for v in range(A[0], LIMIT + 1):
        dp[v] = v - A[0]

    for i in range(1, n):
        target = A[i]
        new_dp = [inf] * (LIMIT + 1)

        for v in range(target, LIMIT + 1):
            min_prev = inf
            for u in divs[v]:
                if dp[u] < min_prev:
                    min_prev = dp[u]
            if min_prev != inf:
                new_dp[v] = min_prev + (v - target)

        dp = new_dp

    ans = min(dp)
    print(ans if ans != inf else -1)


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

    assert target_method(nums=[1, 2, 3], target=[2, 3]) == 1
    assert target_method(nums=[1, 1], target=[3]) == 4
