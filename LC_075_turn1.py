def sort_colors(nums: list[int]) -> None:
    """
    Do not return anything, modify nums in-place instead.
    Sorts an array containing only 0, 1, and 2 in-place (Dutch National Flag problem).
    """
    low = 0
    mid = 0
    high = len(nums) - 1

    while mid <= high:
        if nums[mid] == 0:
            nums[low], nums[mid] = nums[mid], nums[low]
            low += 1
            mid += 1
        elif nums[mid] == 1:
            mid += 1
        else:  # nums[mid] == 2
            nums[mid], nums[high] = nums[high], nums[mid]
            high -= 1

# --- DYNAMIC AUTOMATED TEST HARNESS ---
if __name__ == '__main__':
    import inspect
    sol = Solution()
    # Find the user's defined method on Solution (skipping dunder methods)
    methods = [m for m in dir(sol) if not m.startswith('_') and callable(getattr(sol, m))]
    if not methods:
        raise AttributeError("No solution method found in class Solution")
    target_method = getattr(sol, methods[0])

    assert target_method(nums=[2, 0, 2, 1, 1, 0]) == [0, 0, 1, 1, 2, 2]
    assert target_method(nums=[2, 0, 1]) == [0, 1, 2]
