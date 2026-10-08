class Solution:
    def transformAndSort(self, nums: list[int]) -> list[int]:
        """Replaces every positive array value by 0 (if even) or 1 (if odd),
        leaves non-positive values as they are, and returns the transformed
        array in nondecreasing order.
        """
        transformed = []
        for x in nums:
            if x > 0:
                transformed.append(0 if x % 2 == 0 else 1)
            else:
                transformed.append(x)

        transformed.sort()
        return transformed

    def transform_and_sort(self, arr: list[int]) -> list[int]:
        """Alias for compatibility with different method name naming conventions."""
        return self.transformAndSort(arr)

# --- DYNAMIC AUTOMATED TEST HARNESS ---
if __name__ == '__main__':
    import inspect
    sol = Solution()
    # Find the user's defined method on Solution (skipping dunder methods)
    methods = [m for m in dir(sol) if not m.startswith('_') and callable(getattr(sol, m))]
    if not methods:
        raise AttributeError("No solution method found in class Solution")
    target_method = getattr(sol, methods[0])

    assert target_method(nums=[4, 3, 2, 1]) == [0, 0, 1, 1]
    assert target_method(nums=[1, 5, 3]) == [1, 1, 1]
