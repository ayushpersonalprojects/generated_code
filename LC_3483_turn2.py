class Solution:
    def count_even_three_digit_numbers(self, digits):
        """Counts distinct three-digit even numbers that can be formed

        using the supplied digits at most once each.
        """
        from itertools import permutations

        distinct_numbers = set()

        # A 3-digit number has length 3
        for perm in permutations(digits, 3):
            # Cannot start with '0'
            if perm[0] == 0:
                continue
            # Must be even (last digit must be even)
            if perm[2] % 2 != 0:
                continue

            number = perm[0] * 100 + perm[1] * 10 + perm[2]
            distinct_numbers.add(number)

        return len(distinct_numbers)


if __name__ == "__main__":
    sol = Solution()
    # Example usage:
    # Let's test with digits [1, 2, 3, 4, 0]
    sample_digits = [1, 2, 3, 4, 0]
    print(
        f"Distinct even 3-digit numbers from {sample_digits}:",
        sol.count_even_three_digit_numbers(sample_digits),
    )

# --- DYNAMIC AUTOMATED TEST HARNESS ---
if __name__ == '__main__':
    import inspect
    sol = Solution()
    # Find the user's defined method on Solution (skipping dunder methods)
    methods = [m for m in dir(sol) if not m.startswith('_') and callable(getattr(sol, m))]
    if not methods:
        raise AttributeError("No solution method found in class Solution")
    target_method = getattr(sol, methods[0])

    assert target_method(digits=[1, 2, 3, 4]) == 6
    assert target_method(digits=[0, 2, 2]) == 2
