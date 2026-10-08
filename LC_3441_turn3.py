import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    caption = input_data[0]
    L = int(input_data[1])
    n = len(caption)
    
    # Problem: Transform caption into a valid good-caption form 
    # under the required run-length rule (no more than L consecutive identical characters)
    # while minimizing the total character-change cost.
    
    # dp[i][c][length] can be too slow if L is large.
    # Notice that for a fixed end position i and character c, we want to find 
    # the best previous state.
    # Since L is typically small or we can use a deque/sliding window for optimization,
    # let's write an efficient DP or greedy/backtracking approach depending on L.
    # If L >= n, cost is 0 and caption is already valid.
    
    if L >= n:
        print(caption)
        print(0)
        return

    # Let's implement the standard DP with O(n * 26 * L) or optimized to O(n * 26).
    # dp[i][c] = min cost to form prefix of length i ending with character c.
    # We can maintain the run length as well.
    
    # If L is small (e.g. L <= n), let's use a 1D DP array for each character:
    # dp[i][c] = cost
    # run[i][c] = length of the ending run of character c
    
    # To reconstruct the string efficiently:
    parent = {} # (i, c, run) -> (prev_i, prev_c, prev_run)
    
    # Infinity
    INF = float('inf')
    
    # dp[i][c][run] -> min cost
    # i from 0 to n
    # c from 0 to 25
    # run from 1 to L
    
    # Optimization: store only necessary states or use tabulated DP.
    # Given Python's speed, let's keep it concise and efficient.
    
    # Let's define dp[i][c][r] as min cost for prefix i, ending with char c with run length r.
    # Base case: i = 0, cost = 0.
    
    # To avoid memory/TLE issues for large L, if L is large, it's just n. But usually L is small in such problems (e.g., L <= n).
    # Let's write the DP table:
    # cur[c][r] = cost
    
    # Initialize for i = 0
    # We can use a 1D array of size 26 * (L + 1) for current and previous to save memory and time.
    
    # But wait, reconstructing the string requires keeping history or backtracking.
    # Let's store DP states compactly.
    
    # Let's use an array of size n+1 where each element is a list/dict of (c, r) -> (cost, parent_state).
    
    # Since standard competitive programming problems with this exact phrasing 
    # (like Codeforces / HackerRank string transformation with run-length L) 
    # usually have L <= n, let's implement an optimized DP.
    
    # If L == 1, no two adjacent characters can be the same.
    if L == 1:
        res = []
        cost = 0
        last_c = ''
        for i in range(n):
            orig = caption[i]
            # pick a char != last_c
            # to minimize cost, if orig != last_c, keep orig. Else pick any other char (e.g., 'a' if orig != 'a' else 'b')
            best_c = ''
            min_c = INF
            for c_code in range(97, 123):
            # ...
                pass

    # Let's write a general DP for any L >= 1:
    # dp[i][c] = min cost for prefix i ending with char c (with valid run length 1..L)
    # To track run length, we can store best run length for each (i, c).
    
    # Let's use standard DP table:
    # dp[i][c] = min cost, run[i][c] = corresponding run length
    
    dp = [[INF] * 26 for _ in range(n + 1)]
    run_len = [[0] * 26 for _ in range(n + 1)]
    par = [[None] * 26 for _ in range(n + 1)] # stores (prev_c, prev_run)
    
    # Base case: i = 0
    for c in range(26):
        dp[0][c] = 0
        run_len[0][c] = 0
        
    for i in range(1, n + 1):
        orig_c = ord(caption[i-1]) - 97
        for c in range(26):
            cost_to_change = 0 if c == orig_c else 1
            
            # Option 1: Continue the run from same character c
            if i > 1 and run_len[i-1][c] < L:
                prev_cost = dp[i-1][c]
                if prev_cost + cost_to_change < dp[i][c]:
                    dp[i][c] = prev_cost + cost_to_change
                    run_len[i][c] = run_len[i-1][c] + 1
                    par[i][c] = (c, run_len[i-1][c])
            
            # Option 2: Start a new run with character c from any different character prev_c
            for prev_c in range(26):
                if prev_c == c:
                    continue
                prev_cost = dp[i-1][prev_c]
                if prev_cost != INF:
                    if prev_cost + cost_to_change < dp[i][c]:
                        dp[i][c] = prev_cost + cost_to_change
                        run_len[i][c] = 1
                        par[i][c] = (prev_c, run_len[i-1][prev_c])
                        
    # Find best ending character at i = n
    best_cost = INF
    best_c = -1
    for c in range(26):
        if dp[n][c] < best_cost:
            best_cost = dp[n][c]
            best_c = c
            
    # Reconstruct string
    curr_i = n
    curr_c = best_c
    ans = []
    
    while curr_i > 0:
        ans.append(chr(curr_c + 97))
        prev_state = par[curr_i][curr_c]
        if prev_state is None:
            # must be i=1 starting run
            break
        prev_c, prev_r = prev_state
        curr_i -= 1
        curr_c = prev_c
        
    ans.reverse()
    print("".join(ans))
    print(best_cost)

if __name__ == '__main__':
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
