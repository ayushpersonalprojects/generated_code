def is_match(s: str, p: str) -> bool:
    """
    Returns whether the whole string `s` matches the pattern `p` containing
    ordinary letters plus '.' (matches any single character) and 
    '*' (matches zero or more of the preceding element).
    """
    memo = {}

    def dp(i: int, j: int) -> bool:
        if (i, j) in memo:
            return memo[(i, j)]
        
        # If we've reached the end of the pattern, we must also have reached
        # the end of the string for a successful match.
        if j == len(p):
            return i == len(s)

        # Check if the first characters match
        first_match = i < len(s) and (p[j] == s[i] or p[j] == '.')

        # If the next character in pattern is '*', we have two choices:
        # 1. Zero occurrences of the preceding element (skip pattern by 2)
        # 2. One or more occurrences (advance string index `i` if first_match)
        if j + 1 < len(p) and p[j + 1] == '*':
            ans = dp(i, j + 2) or (first_match and dp(i + 1, j))
        else:
            # Otherwise, just check current match and advance both indices
            ans = first_match and dp(i + 1, j + 1)

        memo[(i, j)] = ans
        return ans

    return dp(0, 0)

# --- DYNAMIC AUTOMATED TEST HARNESS ---
if __name__ == '__main__':
    import inspect
    sol = Solution()
    # Find the user's defined method on Solution (skipping dunder methods)
    methods = [m for m in dir(sol) if not m.startswith('_') and callable(getattr(sol, m))]
    if not methods:
        raise AttributeError("No solution method found in class Solution")
    target_method = getattr(sol, methods[0])

    assert target_method(s='aa', p='a') == False
    assert target_method(s='aa', p='a*') == True
    assert target_method(s='ab', p='.*') == True
