class Solution:

    def solve(self, nums: list[int]) -> int:
        # If the problem is about removing elements to make the array non-decreasing,
        # or a similar cost-based reduction where cost is often related to element values.
        # Let's handle the classic problem:
        # "Minimum cost to make array non-decreasing by removing elements"
        # Or if it's the problem where we can remove adjacent elements, etc.
        # Let's implement the Longest Non-Decreasing Subsequence approach for minimum removals:
        # Min removals to make array non-decreasing = len(nums) - length of LIS (with duplicates: non-decreasing).
        # Wait, if the cost is the sum of removed elements:
        # To minimize the sum of removed elements, we want to maximize the sum of retained elements
        # such that the retained elements form a non-decreasing subsequence.
        
        n = len(nums)
        if n <= 1:
            return 0

        # Coordinate compression for values and prefix sums of max valid subsequence weights.
        # Or dynamic programming:
        # Since values can be large or small, let's use a standard DP where dp[v] is the max sum
        # of a non-decreasing subsequence ending at or with max value v.
        
        # Actually, let's use a Fenwick tree (Binary Indexed Tree) for efficient range maximum queries
        # to find the maximum sum of a non-decreasing subsequence.
        
        distinct_vals = sorted(list(set(nums)))
        val_to_idx = {val: i + 1 for i, val in enumerate(distinct_vals)}
        m = len(distinct_vals)
        
        bit = [0] * (m + 1)
        
        def update(idx, val):
            while idx <= m:
                bit[idx] = max(bit[idx], val)
                idx += idx & (-idx)
                
        def query(idx):
            res = 0
            while idx > 0:
                res = max(res, bit[idx])
                idx -= idx & (-idx)
            return res

        max_retained_sum = 0
        total_sum = sum(nums)
        
        for x in nums:
            idx = val_to_idx[x]
            # Max sum of non-decreasing subsequence ending with a value <= x
            prev_max = query(idx)
            curr_sum = prev_max + x
            max_retained_sum = max(max_retained_sum, curr_sum)
            update(idx, curr_sum)
            
        return total_sum - max_retained_sum


def solve(nums):
    return Solution().solve(nums)

# --- DYNAMIC AUTOMATED TEST HARNESS ---
if __name__ == '__main__':
    import inspect
    sol = Solution()
    # Find the user's defined method on Solution (skipping dunder methods)
    methods = [m for m in dir(sol) if not m.startswith('_') and callable(getattr(sol, m))]
    if not methods:
        raise AttributeError("No solution method found in class Solution")
    target_method = getattr(sol, methods[0])

    assert target_method(nums=[6, 2, 9, 4]) == 12
    assert target_method(nums=[1, 2, 3]) == 4
