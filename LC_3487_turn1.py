class Solution:
    def maxSum(self, nums: list[int]) -> int:
        # To maximize the sum of a subsequence with unique values,
        # we should include every positive unique number in `nums`.
        # Negative numbers and duplicates (if we only want max sum of unique elements)
        # should be excluded, except that for duplicates of positive numbers,
        # we only include each distinct positive value once (since all instances
        # of the same number cannot be in a subsequence of *unique* values).
        # Wait, the problem says "subsequence whose values are unique". 
        # This means no two elements in the chosen subsequence can have the same *value*.
        # Therefore, we can pick each unique positive number at most once.
        # To maximize the sum, we should pick all distinct positive numbers.
        
        return sum(x for x in set(nums) if x > 0)

# Example usage:
# sol = Solution()
# print(sol.maxSum([1, 2, 3, 2])) # Output: 6 (1 + 2 + 3)

# --- DYNAMIC AUTOMATED TEST HARNESS ---
if __name__ == '__main__':
    import inspect
    sol = Solution()
    # Find the user's defined method on Solution (skipping dunder methods)
    methods = [m for m in dir(sol) if not m.startswith('_') and callable(getattr(sol, m))]
    if not methods:
        raise AttributeError("No solution method found in class Solution")
    target_method = getattr(sol, methods[0])

    assert target_method(nums=[1, 2, 2, 3, 1]) == 6
    assert target_method(nums=[5, 4, -1, 0]) == 9
