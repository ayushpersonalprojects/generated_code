class Solution:
    def count_even_three_digit_numbers(self, digits):
        """Counts distinct three-digit even numbers that can be formed
        using the supplied digits at most once each.
        """
        from collections import Counter
        
        digit_counts = Counter(digits)
        distinct_numbers = set()
        
        # Iterate over all possible 3-digit numbers from 100 to 998 with step 2 (even numbers)
        for num in range(100, 1000, 2):
            d1 = num // 100
            d2 = (num // 10) % 10
            d3 = num % 10
            
            needed = Counter([d1, d2, d3])
            
            # Check if we have enough of each digit in our supplied digits
            possible = True
            for d, count in needed.items():
                if digit_counts[d] < count:
                    possible = False
                    break
            
            if possible:
                distinct_numbers.add(num)
                
        return len(distinct_numbers)


if __name__ == "__main__":
    sol = Solution()
    # Example usage:
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
