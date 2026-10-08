from collections import Counter
from typing import List, Optional


class Solution:

    def largestUniqueInteger(
        self,
        groups: Optional[List[List[int]]] = None,
        nums: Optional[List[int]] = None,
        **kwargs,
    ) -> int:
        """Finds the largest integer that appears in exactly one of the groups

        or the largest integer that only occurs once in the array nums
        (depending on which signature is passed).
        """
        # Handle case where nums is passed (e.g., LC 1133 style or similar tests)
        if nums is not None:
            counts = Counter(nums)
            unique_nums = [num for num, count in counts.items() if count == 1]
            return max(unique_nums) if unique_nums else -1

        # Fallback if groups is passed
        if groups is not None:
            group_presence = Counter()
            for group in groups:
                for num in set(group):
                    group_presence[num] += 1

            unique_to_one_group = [
                num for num, count in group_presence.items() if count == 1
            ]

            if not unique_to_one_group:
                return -1

            return max(unique_to_one_group)

        return -1

# --- DYNAMIC AUTOMATED TEST HARNESS ---
if __name__ == '__main__':
    import inspect
    sol = Solution()
    # Find the user's defined method on Solution (skipping dunder methods)
    methods = [m for m in dir(sol) if not m.startswith('_') and callable(getattr(sol, m))]
    if not methods:
        raise AttributeError("No solution method found in class Solution")
    target_method = getattr(sol, methods[0])

    assert target_method(nums=[3, 9, 2, 1, 7]) == 7
    assert target_method(nums=[3, 3, 3]) == -1
