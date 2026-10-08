import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    caption = input_data[0]
    L = int(input_data[1])
    n = len(caption)
    
    # dp[i][c_idx][length]
    # To avoid TLE and memory limit (26 * L can be large if L is large, but usually L <= n),
    # let's optimize. If L is up to n, state space n * 26 * L could be O(n^2 * 26) which TLEs if n is large.
    # However, standard "good caption" problems usually have small L (e.g., L <= 10 or L <= n).
    # If L is large, we can optimize using prefix minimums.
    
    # Let's use 1-based indexing for length: length from 1 to L.
    # dp[i][c] = min cost to form prefix of length i ending with char c, 
    # where the last block of char c has some valid length <= L.
    # Actually, standard definition: no run of identical characters can exceed L.
    
    # Let's implement the O(N * 26 * L) DP with optimizations.
    # If L > n, no run can exceed L is trivially satisfied by the string itself (cost 0), 
    # but maybe we need runs of length L? 
    # Wait, if L is large, let's assume standard run-length constraint: max run length <= L.
    
    # Let's write a safe, optimized DP.
    # dp[i][c] : min cost for prefix i ending in character c.
    # To keep track of run lengths, we can store for each i and c, the best cost and the run length.
    
    # Let's do standard DP:
    # dp[i][c] = min cost for prefix of length i ending with character c.
    # Since we can transition from any prev_c != c with run length 1, 
    # or from same c with run length + 1 (up to L).
    
    # Let's represent dp as an array of size 26 for the current index i:
    # current[c] = (min_cost, run_length)
    
    # To optimize, we can maintain the best prev states.
    
    pass

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

    assert target_method(caption='cdcd') == 'cccc'
    assert target_method(caption='aca') == 'aaa'
