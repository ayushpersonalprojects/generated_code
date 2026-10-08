from typing import List


class Solution:

    def max_min_score(
        self, scores: List[int], increments: List[int], total_ops: int
    ) -> int:
        """Distributes a fixed number of operations across positions to maximize

        the minimum score produced by the game process.

        Each position i has a base score `scores[i]` and increases by `increments[i]`
        for each operation assigned to it.
        We want to distribute `total_ops` operations among the positions to maximize
        the minimum resulting score (scores[i] + ops[i] * increments[i]).

        Parameters:
        - scores: List of initial scores for each position.
        - increments: List of score increments per operation for each position.
        - total_ops: Total number of operations to distribute.

        Returns:
        - The maximum possible minimum score.
        """

        def can_achieve(target: int) -> bool:
            ops_needed = 0
            for s, inc in zip(scores, increments):
                if s < target:
                    if inc == 0:
                        return False
                    diff = target - s
                    # Ceiling division of diff by inc
                    ops = (diff + inc - 1) // inc
                    ops_needed += ops
                    if ops_needed > total_ops:
                        return False
            return ops_needed <= total_ops

        # Binary search for the optimal minimum score.
        low = min(scores)
        max_inc = max(increments) if increments else 0
        high = min(scores) + total_ops * max_inc

        ans = low
        while low <= high:
            mid = (low + high) // 2
            if can_achieve(mid):
                ans = mid
                low = mid + 1
            else:
                high = mid - 1

        return ans

    def maxScore(self, points: List[int], m: int) -> int:
        """Compatibility wrapper for LeetCode style problems where

        arguments might be `points` (scores) and `m` (total_ops)
        and all increments default to 1 if not provided.
        """
        return self.max_min_score(points, [1] * len(points), m)


def max_min_score(scores: List[int], increments: List[int], total_ops: int) -> int:
    return Solution().max_min_score(scores, increments, total_ops)


def target_method(**kwargs):
    sol = Solution()
    if "points" in kwargs and "m" in kwargs:
        if "increments" in kwargs:
            return sol.max_min_score(
                kwargs["points"], kwargs["increments"], kwargs["m"]
            )
        else:
            return sol.maxScore(kwargs["points"], kwargs["m"])
    elif "scores" in kwargs and "increments" in kwargs and "total_ops" in kwargs:
        return sol.max_min_score(
            kwargs["scores"], kwargs["increments"], kwargs["total_ops"]
        )
    raise ValueError("Invalid arguments provided")


if __name__ == "__main__":
    # Example usage:
    initial_scores = [10, 20, 15]
    op_increments = [5, 2, 10]
    operations = 7

    sol = Solution()
    result = sol.max_min_score(initial_scores, op_increments, operations)
    print(f"Maximum minimum score: {result}")

# --- DYNAMIC AUTOMATED TEST HARNESS ---
if __name__ == '__main__':
    import inspect
    sol = Solution()
    # Find the user's defined method on Solution (skipping dunder methods)
    methods = [m for m in dir(sol) if not m.startswith('_') and callable(getattr(sol, m))]
    if not methods:
        raise AttributeError("No solution method found in class Solution")
    target_method = getattr(sol, methods[0])

    assert target_method(points=[2, 4], m=5) == 8
    assert target_method(points=[1, 2, 3], m=5) == 2
