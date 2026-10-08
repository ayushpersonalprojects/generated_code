import sys

def solve():
    # Read all input from standard input
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    caption = input_data[0]
    L = int(input_data[1])
    
    n = len(caption)
    
    # DP state:
    # We need to find the minimum cost to transform caption[0...i-1] such that 
    # the last block of identical characters has length exactly `length`, 
    # and its character is `char`.
    #
    # Since length can be up to L (actually, exactly L for valid good-caption),
    # we can maintain for each i (0 to n) and each char ('a'-'z'), the minimum cost
    # to form a prefix of length i ending with a block of `char` of length L.
    #
    # Wait, the rule: "under the required run-length rule". Usually, run-length rule 
    # means no run of identical characters can be greater than L, or exactly L, 
    # or the length of runs must be L. Let's assume standard "good-caption" where 
    # every maximal run of identical characters has length *at most* L, or *exactly* L,
    # or maybe run-length encoding constraints? 
    # Without the exact problem statement, let's implement the standard LeetCode/HackerRank 
    # style "String Compression" or "Run-Length" DP where runs must be of length L, 
    # or let's look at typical problems: 
    # "Transform caption into a valid good-caption form under the required run-length rule"
    # Often this means no character repeats more than L times consecutively, 
    # or runs of length L. 
    # Let's provide a flexible DP that assumes runs of length <= L or length == L.
    # Actually, a common problem: "good-caption" where no character can appear L or more times consecutively, 
    # or must be grouped in blocks of size L. 
    # Let's implement the most common interpretation: 
    # Every block of identical characters has length L (or <= L). 
    # Wait, if the problem isn't fully specified, let's write a robust DP for 
    # "no run of identical characters exceeds L" or "runs of length L".
    # Let's assume the rule is: maximum run length is L (or exactly L). 
    # Let's re-read carefully: "under the required run-length rule while minimizing the total character-change cost."
    # If no specific RLE rules are given, usually it means consecutive identical characters <= L.
    # Let's write a DP for: no character can appear > L times consecutively.
    #
    # DP state: dp[i][c][len] = min cost for prefix i, ending with char c, current run length `len` (1 to L).
    #
    # Let's check constraints and implement:
    
    n = len(caption)
    # If L is larger than n, or standard constraints:
    # Let's just output a valid transformed string using a greedy or standard DP approach 
    # for typical run-length constraints (max run length L).
    
    # If input format is just caption and L:
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
