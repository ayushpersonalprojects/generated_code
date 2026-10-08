class Solution:
    def countDivisibleSubstrings(self, s: str) -> int:
        """
        Count substrings whose numeric value is divisible by their final digit,
        excluding substrings ending in zero.
        Optimized to handle longer strings efficiently (e.g., up to length 2000).
        """
        count = 0
        n = len(s)
        
        # We can optimize by grouping by the length of the substring or the ending digit.
        # Since last digits are 1-9, we can iterate over all possible ending indices,
        # and for each ending index, maintain the running values modulo d for each possible final digit d (1-9).
        # Actually, since lengths can be up to 10-20, standard integer parsing can become large,
        # but Python handles arbitrarily large integers. However, O(N^2) with large ints might TLE
        # if not careful. Wait, 2000^2 is 4 million operations, which is fast in Python,
        # but converting string to int inside a nested loop for every substring can be slow.
        # Let's optimize by computing `val = val * 10 + digit` on the fly.
        
        for i in range(n):
            val = 0
            for j in range(i, n):
                digit = int(s[j])
                val = val * 10 + digit
                
                if digit == 0:
                    continue
                
                if val % digit == 0:
                    count += 1
                    
        return count

def count_divisible_substrings(s: str) -> int:
    sol = Solution()
    return sol.countDivisibleSubstrings(s)

if __name__ == "__main__":
    test_str = "1234"
    sol = Solution()
    print(f"String: {test_str}, Count: {sol.countDivisibleSubstrings(test_str)}")

# --- DYNAMIC AUTOMATED TEST HARNESS ---
if __name__ == '__main__':
    import inspect
    sol = Solution()
    # Find the user's defined method on Solution (skipping dunder methods)
    methods = [m for m in dir(sol) if not m.startswith('_') and callable(getattr(sol, m))]
    if not methods:
        raise AttributeError("No solution method found in class Solution")
    target_method = getattr(sol, methods[0])

    assert target_method(s='124') == 3
    assert target_method(s='120') == 2
