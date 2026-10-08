class Solution:
    def sumOfGoodNumbers(self, nums: list[int], k: int) -> int:
        return self.sum_special_values(nums, k)

    def sum_special_values(self, arr: list[int | float], k: int) -> int | float:
        """
        Sum every array value whose neighbors at distance k, when they exist, 
        are both strictly smaller than the value.
        
        Parameters:
        arr (list): The input list of numbers.
        k (int): The distance to the neighbors.
        
        Returns:
        int/float: The sum of the values meeting the condition.
        """
        if k < 0:
            raise ValueError("Distance k must be non-negative.")
        
        total_sum = 0
        n = len(arr)
        
        for i in range(n):
            val = arr[i]
            
            # Check left neighbor at distance k
            left_exists = (i - k >= 0)
            left_smaller = (not left_exists) or (arr[i - k] < val)
            
            # Check right neighbor at distance k
            right_exists = (i + k < n)
            right_smaller = (not right_exists) or (arr[i + k] < val)
            
            # If both existing neighbors are smaller (or don't exist), include the value
            if left_smaller and right_smaller:
                total_sum += val
                
        return total_sum

# --- DYNAMIC AUTOMATED TEST HARNESS ---
if __name__ == '__main__':
    import inspect
    sol = Solution()
    # Find the user's defined method on Solution (skipping dunder methods)
    methods = [m for m in dir(sol) if not m.startswith('_') and callable(getattr(sol, m))]
    if not methods:
        raise AttributeError("No solution method found in class Solution")
    target_method = getattr(sol, methods[0])

    assert target_method(nums=[1, 3, 2, 1, 5, 4], k=2) == 8
    assert target_method(nums=[2, 1], k=1) == 2
