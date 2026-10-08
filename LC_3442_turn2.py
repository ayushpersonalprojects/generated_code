from collections import Counter


class Solution:

    def largest_frequency_difference(self, s: str) -> int:
        """Computes the largest difference between an odd character frequency

        and an even character frequency in a given string.
        Difference is defined as (odd_frequency - even_frequency).
        """
        if not s:
            return 0

        counts = Counter(s).values()

        odd_freqs = [c for c in counts if c % 2 != 0]
        even_freqs = [c for c in counts if c % 2 == 0]

        if not odd_freqs or not even_freqs:
            return 0

        # We want to maximize odd - even
        return max(odd_freqs) - min(even_freqs)


def largest_frequency_difference(s: str) -> int:
    sol = Solution()
    return sol.largest_frequency_difference(s)


# Example usage:
if __name__ == "__main__":
    sol = Solution()
    print(
        sol.largest_frequency_difference("aabbc")
    )  # 'a':2, 'b':2, 'c':1 => 1 - 2 = -1
    print(
        sol.largest_frequency_difference("aaabbc")
    )  # 'a':3, 'b':2, 'c':1 => max(3,1) - 2 = 3 - 2 = 1

# --- DYNAMIC AUTOMATED TEST HARNESS ---
if __name__ == '__main__':
    import inspect
    sol = Solution()
    # Find the user's defined method on Solution (skipping dunder methods)
    methods = [m for m in dir(sol) if not m.startswith('_') and callable(getattr(sol, m))]
    if not methods:
        raise AttributeError("No solution method found in class Solution")
    target_method = getattr(sol, methods[0])

    assert target_method(s='aaaaabbc') == 3
    assert target_method(s='abcabcab') == 1
