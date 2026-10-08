class Solution:
    def check_maximal_k_substring(self, s: str, k: int) -> bool:
        """Returns whether a length-k substring exists whose characters are all identical
        and which is maximal with respect to neighboring characters.
        """
        if k <= 0 or k > len(s):
            return False

        n = len(s)
        i = 0
        while i < n:
            # Find the end of the current run of identical characters
            j = i
            while j < n and s[j] == s[i]:
                j += 1

            run_length = j - i

            # Check if this run contains a maximal substring of length k.
            # A run of identical characters of length R is maximal if it cannot be extended.
            # This means the run itself must have length k, AND it must not be flanked
            # by the same character (though for the whole string, boundaries matter:
            # if the run touches the start/end of the string, it's automatically maximal on that side).
            if run_length == k:
                left_ok = i == 0 or s[i - 1] != s[i]
                right_ok = j == n or s[j] != s[i - 1]  # s[i-1] is the char of the run
                if left_ok and right_ok:
                    return True

            i = j

        return False

def check_maximal_k_substring(s: str, k: int) -> bool:
    return Solution().check_maximal_k_substring(s, k)

# --- DYNAMIC AUTOMATED TEST HARNESS ---
if __name__ == '__main__':
    import inspect
    sol = Solution()
    # Find the user's defined method on Solution (skipping dunder methods)
    methods = [m for m in dir(sol) if not m.startswith('_') and callable(getattr(sol, m))]
    if not methods:
        raise AttributeError("No solution method found in class Solution")
    target_method = getattr(sol, methods[0])

    assert target_method(s='aaabc', k=3) == True
    assert target_method(s='aaaa', k=3) == False
