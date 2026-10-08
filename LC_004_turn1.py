class Solution:
    def findMedianSortedArrays(self, nums1: list[int], nums2: list[int]) -> float:
        # Ensure nums1 is the smaller array to minimize the binary search range
        if len(nums1) > len(nums2):
            nums1, nums2 = nums2, nums1
            
        m, n = len(nums1), len(nums2)
        total_left = (m + n + 1) // 2
        
        low, high = 0, m
        
        while low <= high:
            i = (low + high) // 2
            j = total_left - i
            
            # nums1[i-1] and nums2[j-1] are elements on the left side of the partition
            # nums1[i] and nums2[j] are elements on the right side of the partition
            
            max_left1 = nums1[i - 1] if i > 0 else float('-inf')
            min_right1 = nums1[i] if i < m else float('inf')
            
            max_left2 = nums2[j - 1] if j > 0 else float('-inf')
            min_right2 = nums2[j] if j < n else float('inf')
            
            # Check if we have partitioned correctly
            if max_left1 <= min_right2 and max_left2 <= min_right1:
                # If total length is odd, the median is the max of the left elements
                if (m + n) % 2 == 1:
                    return float(max(max_left1, max_left2))
                # If total length is even, the median is the average of max of left and min of right
                else:
                    return (max(max_left1, max_left2) + min(min_right1, min_right2)) / 2.0
                    
            elif max_left1 > min_right2:
                # We are too far right in nums1, move left
                high = i - 1
            else:
                # We are too far left in nums1, move right
                low = i + 1
                
        raise ValueError("Input arrays are not sorted or invalid.")

# --- DYNAMIC AUTOMATED TEST HARNESS ---
if __name__ == '__main__':
    import inspect
    sol = Solution()
    # Find the user's defined method on Solution (skipping dunder methods)
    methods = [m for m in dir(sol) if not m.startswith('_') and callable(getattr(sol, m))]
    if not methods:
        raise AttributeError("No solution method found in class Solution")
    target_method = getattr(sol, methods[0])

    assert target_method(nums1=[1, 3], nums2=[2]) == 2.0
    assert target_method(nums1=[1, 2], nums2=[3, 4]) == 2.5
