from collections import Counter
from typing import List, Tuple


class Solution:
    def maxStudentsOnBench(self, pairs: List[List[int]]) -> int:
        """Given pairs representing students sitting on benches, return the largest

        number of students sharing one bench.

        Each pair is represented as [student_id, bench_id].
        """
        if not pairs:
            return 0

        # Assuming the second element of the tuple/list represents the bench ID
        bench_counts = Counter(bench for _, bench in pairs)

        return max(bench_counts.values()) if bench_counts else 0


def max_students_on_bench(pairs: List[Tuple[int, int]]) -> int:
    """Given pairs representing students sitting on benches, return the largest

    number of students sharing one bench.

    Each pair is typically represented as (student_id, bench_id).
    """
    sol = Solution()
    return sol.maxStudentsOnBench(pairs)  # type: ignore

# --- DYNAMIC AUTOMATED TEST HARNESS ---
if __name__ == '__main__':
    import inspect
    sol = Solution()
    # Find the user's defined method on Solution (skipping dunder methods)
    methods = [m for m in dir(sol) if not m.startswith('_') and callable(getattr(sol, m))]
    if not methods:
        raise AttributeError("No solution method found in class Solution")
    target_method = getattr(sol, methods[0])

    assert target_method(students=[[1, 1], [2, 1], [3, 2], [4, 1]]) == 3
    assert target_method(students=[[1, 5], [2, 6]]) == 1
