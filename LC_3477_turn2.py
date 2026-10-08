from typing import List


class Solution:

    def countUnplacedFruits(self, fruits: List[int], baskets: List[int]) -> int:
        """Processes fruit quantities against basket capacities from left to right,

        placing each fruit in the first unused basket that can hold it,
        and returns the count of fruits that cannot be placed.
        """
        unplaced_count = 0
        used_baskets = [False] * len(baskets)

        for fruit in fruits:
            placed = False
            for j, capacity in enumerate(baskets):
                if not used_baskets[j] and capacity >= fruit:
                    used_baskets[j] = True
                    placed = True
                    break
            if not placed:
                unplaced_count += 1

        return unplaced_count

# --- DYNAMIC AUTOMATED TEST HARNESS ---
if __name__ == '__main__':
    import inspect
    sol = Solution()
    # Find the user's defined method on Solution (skipping dunder methods)
    methods = [m for m in dir(sol) if not m.startswith('_') and callable(getattr(sol, m))]
    if not methods:
        raise AttributeError("No solution method found in class Solution")
    target_method = getattr(sol, methods[0])

    assert target_method(fruits=[4, 2, 5], baskets=[3, 5, 4]) == 1
    assert target_method(fruits=[3, 6, 1], baskets=[6, 4, 7]) == 0
