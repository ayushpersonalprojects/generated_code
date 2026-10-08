def count_divisible_substrings(s: str) -> int:
    """Count substrings whose numeric value is divisible by their final digit,

    excluding substrings ending in zero.
    """
    count = 0
    n = len(s)

    for i in range(n):
        # Substrings must not start with '0' if we consider numeric values?
        # Actually, standard numeric value of substring: leading zeros don't change value
        # but let's parse normally.
        for j in range(i, n):
            sub = s[i : j + 1]
            last_char = sub[-1]

            # Exclude substrings ending in zero
            if last_char == "0":
                continue

            last_digit = int(last_char)
            val = int(sub)

            if val % last_digit == 0:
                count += 1

    return count


if __name__ == "__main__":
    # Test example
    test_str = "1234"
    print(f"String: {test_str}, Count: {count_divisible_substrings(test_str)}")

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
