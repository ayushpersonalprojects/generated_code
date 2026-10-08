class Solution:

    def longestPalindrome(self, s: str, k: int) -> int:
        n = len(s)
        if n == 0:
            return 0

        memo = {}

        def get_longest(i, j, c):
            if i > j:
                return 0
            if i == j:
                return 1
            if c < 0:
                return -1000000

            state = (i, j, c)
            if state in memo:
                return memo[state]

            res = get_longest(i + 1, j, c)
            res = max(res, get_longest(i, j - 1, c))

            cost = abs(ord(s[i]) - ord(s[j]))
            if c >= cost:
                res = max(res, 2 + get_longest(i + 1, j - 1, c - cost))

            memo[state] = res
            return res

        return get_longest(0, n - 1, k)


def longest_palindrome_with_k_changes(s: str, k: int) -> str:
    """Returns the longest palindromic subsequence obtainable after at most k unit character-change operations.

    A unit character-change operation changes a character to any other character.
    The "distance" between two characters c1 and c2 is abs(ord(c1) - ord(c2)).
    """
    n = len(s)
    if n == 0:
        return ""

    memo = {}

    def get_longest(i, j, c):
        if i > j:
            return 0
        if i == j:
            return 1
        if c < 0:
            return -1000000

        state = (i, j, c)
        if state in memo:
            return memo[state]

        res = get_longest(i + 1, j, c)
        res = max(res, get_longest(i, j - 1, c))

        cost = abs(ord(s[i]) - ord(s[j]))
        if c >= cost:
            res = max(res, 2 + get_longest(i + 1, j - 1, c - cost))

        memo[state] = res
        return res

    total_len = get_longest(0, n - 1, k)
    if total_len <= 0:
        return s[0] if n > 0 else ""

    res_chars_left = []
    res_chars_right = []

    i, j, c = 0, n - 1, k
    while i <= j:
        if i == j:
            res_chars_left.append(s[i])
            break

        cost = abs(ord(s[i]) - ord(s[j]))
        if c >= cost and get_longest(i, j, c) == 2 + get_longest(
            i + 1, j - 1, c - cost
        ):
            # Choose the lexicographically smaller character or just s[j]
            chosen_char = min(s[i], s[j])
            res_chars_left.append(chosen_char)
            res_chars_right.append(chosen_char)
            c -= cost
            i += 1
            j -= 1
        elif get_longest(i, j, c) == get_longest(i + 1, j, c):
            i += 1
        else:
            j -= 1

    res_chars_right.reverse()
    return "".join(res_chars_left + res_chars_right)


if __name__ == "__main__":
    print(longest_palindrome_with_k_changes("abca", 2))

# --- DYNAMIC AUTOMATED TEST HARNESS ---
if __name__ == '__main__':
    import inspect
    sol = Solution()
    # Find the user's defined method on Solution (skipping dunder methods)
    methods = [m for m in dir(sol) if not m.startswith('_') and callable(getattr(sol, m))]
    if not methods:
        raise AttributeError("No solution method found in class Solution")
    target_method = getattr(sol, methods[0])

    assert target_method(s='abca', k=1) == 4
    assert target_method(s='abcd', k=0) == 1
