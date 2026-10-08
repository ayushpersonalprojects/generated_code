from collections import Counter
from typing import List


class Solution:

    def largestUniqueInteger(self, groups: List[List[int]]) -> int:
        """Finds the largest integer that appears in exactly one of the groups.

        If groups is a list of lists of integers, this function flattens the counts
        across all groups or treats the problem based on the context of array groups.
        Assuming "appears in exactly one of the relevant array groups" means:
        Count how many *groups* each integer appears in. Find the integers that
        appear in exactly *one* group, and return the maximum of those integers.
        """
        # Find which groups each number appears in (using sets to avoid counting duplicates within the same group)
        group_presence = Counter()
        for group in groups:
            for num in set(group):
                group_presence[num] += 1

        # Find numbers that appear in exactly one group
        unique_to_one_group = [
            num for num, count in group_presence.items() if count == 1
        ]

        if not unique_to_one_group:
            return -1

        return max(unique_to_one_group)

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
