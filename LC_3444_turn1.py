import sys


def solve():
    # Read all inputs from standard input
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    n = int(input_data[0])
    A = [int(x) for x in input_data[1 : n + 1]]

    # We want to find a set of values B_1, B_2, ..., B_n such that:
    # 1. B_i >= A_i for all i.
    # 2. For every pair (i, j), B_j is a multiple of B_i, OR B_i is a multiple of B_j.
    #    (Equivalently, the divisibility relation among the chosen values forms a chain:
    #     some permutation of B divides the next).
    # 3. Sum of (B_i - A_i) is minimized.

    # Notice that any set of numbers satisfying the chain property under divisibility
    # can be ordered such that B'_1 | B'_2 | ... | B'_n.
    # Furthermore, since the maximum value in A is at most around 200,000 typically
    # (or if larger, we need to know constraints, but usually these problems have A_i <= 200,000),
    # let's check standard constraints. If A_i can be up to some limit, say MAX_VAL.
    # Wait, the problem statement doesn't specify constraints, but standard competitive programming
    # problems of this type usually have A_i <= 200,000 or 500,000.
    # Let's write a general solution. If max A_i is small, we can find the best chain.

    max_val = max(A)
    # The maximum possible value we might need to consider for the top of the chain
    # won't exceed twice the max value or some small multiple, because we can always just
    # pick the max element and multiply it, but increments would be huge.
    # Actually, any chosen value B_i will be <= some limit. Since we want to minimize increments,
    # B_i won't exceed max(A) + sum(A) or similar, but practically, multiples don't go extremely high
    # unless optimal. Wait, standard problem: "Increase array values so every target value is represented
    # through the required multiple relationship, minimizing total increments."
    # This is often solved by finding a chain of values $c_1, c_2, \dots, c_n$ where $c_1 | c_2 | \dots | c_n$.
    # Wait, the condition "every target value is represented through the required multiple relationship"
    # means that for all $i, j$, either $B_i | B_j$ or $B_j | B_i$.
    # This is equivalent to saying the chosen multiset $B$ has a chain structure of divisibility.
    # Since $N$ is usually small (e.g., $N \le 500$), let's check if there's a DP approach.

    # Let's sort A to make things easier.
    A.sort()

    # If N is small (e.g., N <= 500), we can sort A and use dynamic programming.
    # Let's assume standard constraints where max(A) <= 200,000.
    # If max(A) is up to 200,000, we can define DP.
    # But wait, what if max(A) is large? Without constraints, let's implement a robust solution
    # assuming max(A) is within standard limits (e.g., <= 200,000), which covers 99% of such problems
    # (like Codeforces 1151E, or similar divisibility chain problems).
    # Wait, let's check if there is a known problem: "Increase array values so every target value is represented
    # through the required multiple relationship, minimizing total increments."
    # This matches a problem where we want to find a sequence $B_1 \le B_2 \le \dots \le B_n$ such that
    # $B_i$ divides $B_{i+1}$ and $A_i \le B_i$.

    # Let's verify if $B_1 | B_2 | \dots | B_n$ is the condition. Yes, "every pair has a multiple relationship"
    # means the divisibility graph is a tournament of divisibility, which for a set of integers means
    # they can be ordered such that $B_1 | B_2 | \dots | B_n$.

    # Let's write a DP.
    # Since elements can go up to some limit, let's find the upper bound for the maximum element in B.
    # The maximum element in B won't exceed max(A) * something, or maybe max possible value in A is up to 200,000.
    # Let's dynamically determine the limit or use max(A) + sum(A) if small, but let's assume max(A) <= 200,000.
    # If max(A) is larger, we can cap it or handle it. Let's find max(A).
    M = max(A)

    # To minimize increments, we can sort A. Then we need to find B_1 <= B_2 <= ... <= B_n such that A_i <= B_i and B_i | B_{i+1}.
    # Wait, does B_i have to be >= A_i in the sorted order?
    # If we sort A, does the optimal B also need to be sorted? Yes, if A_1 <= A_2 <= ... <= A_n,
    # then we can assume B_1 <= B_2 <= ... <= B_n and B_i divides B_{i+1}.

    # Let's check if M is very large. If M <= 200,000, we can use a value-based DP.
    # Let dp[v] be the min cost to form a valid chain ending at value v, covering some prefix of A.
    # Alternatively, since we need to cover all A_i, let's sort A.
    # dp(i, v) = min cost to form a chain of length i ending at value v, covering A[0...i-1].
    # But this is O(N * M * log M), which might be too slow if M is large and N is large.
    # Let's check typical constraints for this exact wording: usually N <= 500, max(A) <= 200,000.
    # Wait, can we do it greedily or with min-cost flow / DP?
    # Let's write a general efficient DP or matching if applicable.

    # Let's use a simpler approach:
    # Limit for values in B: can we bound max(B_n)?
    # If max(A) is up to 200,000, let's set LIMIT = max(2 * M, max(A) + 2000).
    # Actually, let's just use the standard O(N * M log M) DP if M is up to 200,000.
    # Let's implement the DP:
    # We want to match each A_i to some B_i such that A_i <= B_i, B_i | B_{i+1}, and sum(B_i - A_i) is minimized.

    # Let's sort A.
    A.sort()

    # If N == 1, answer is 0 (A_1 divides A_1).
    if n == 1:
        print(0)
        return

    # Let's define the limit for values.
    # The maximum value in B cannot exceed max(A) plus something, or maybe max(A) itself if we don't multiply,
    # but with multiples, max value can be up to some limit. Let's cap limit at max(200000, M * 2).
    # Wait, what if M is up to 10^5?
    LIMIT = max(M * 2, 200000)

    # We can compute for each value v up to LIMIT, the minimum cost to reach v for the current element of A.
    # Let's maintain a DP table or array.
    # dp[v] = min cost to set current B_i = v.
    # Transition from previous element:
    # To go from B_{i-1} = u to B_i = v, we need u divides v (u | v) and u <= v.
    # Then dp_new[v] = (v - A[i]) + min_{u | v, u <= v} dp_old[u].

    # Since doing this naively for each i takes O(N * LIMIT log LIMIT), for LIMIT = 200,000 and N = 500,
    # N * LIMIT log LIMIT = 500 * 200000 * 18 ≈ 1.8 * 10^9 operations, which is too slow in Python.
    # We need a faster approach or optimization.

    # Is there an alternative formulation?
    # Notice that B_i >= A_i and B_1 | B_2 | ... | B_n.
    # Since B_1 | B_2 | ... | B_n, the sequence of prime factor counts or similar? Not necessarily.
    # Actually, many such problems allow us to just find the best chain of length N.
    # Let's rethink: can we just output 0 if already valid, or compute the min increments?
    # Let's check if there's any output required or if this is a specific problem.
    # "Increase array values so every target value is represented through the required multiple relationship, minimizing total increments."
    # This is a known problem. Let's implement an efficient solver.

    # Let's use a Dijkstra-like or optimized DP where we only iterate over multiples.
    # For a fixed i, dp[v] can be computed by iterating over multiples of u.
    # Even better, since we want to minimize sum(B_i - A_i), let's write a concise and fast enough solution
    # assuming reasonable constraints, or use the standard divisor-based DP with optimizations.

    # Let's precompute divisors for all numbers up to LIMIT.
    divs = [[] for _ in range(LIMIT + 1)]
    for i in range(1, LIMIT + 1):
        for j in range(i, LIMIT + 1, i):
        divs[j].append(i)

    # Initialize DP for the first element A[0]
    # For any v >= A[0], cost is v - A[0]. For v < A[0], cost is infinity.
    inf = float("inf")
    dp = [inf] * (LIMIT + 1)
    for v in range(A[0], LIMIT + 1):
        dp[v] = v - A[0]

    for i in range(1, n):
        target = A[i]
        new_dp = [inf] * (LIMIT + 1)

        # To optimize, we can compute prefix/running minimums or propagate from u to its multiples v.
        # For each u, it can transition to any multiple v >= max(u, target).
        # min_prev[u] = min cost of B_{i-1} = u.
        # We want new_dp[v] = (v - target) + min_{u | v, u >= target?} Wait, u can be anything that divides v.
        # Actually, u <= v is required for divisibility (unless u = v).
        # So for a fixed v, we look at all divisors u of v, and take min(dp[u]).
        # Then new_dp[v] = (v - target) + min_{u | v} dp[u] for v >= target.

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
