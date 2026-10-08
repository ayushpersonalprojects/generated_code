from collections import Counter
from typing import List, Tuple, Union


class Solution:
    def maxStudentsOnBench(
        self, pairs: List[Union[List[int], Tuple[int, int]]] = None, students: List[Union[List[int], Tuple[int, int]]] = None, **kwargs
    ) -> int:
        """Given pairs representing students sitting on benches, return the largest

        number of students sharing one bench.

        Each pair is represented as [student_id, bench_id].
        """
        data = pairs if pairs is not None else students
        if data is None and kwargs:
            data = next(iter(kwargs.values()))

        if not data:
            return 0

        # Note: A single student might sit on the same bench multiple times, 
        # or the problem might count distinct students. Usually, it's distinct students per bench.
        # Let's use set of (student_id, bench_id) to avoid double counting if a student is listed twice for the same bench,
        # or just count all records if uniqueness isn't specified. Standard is unique students per bench.
        unique_pairs = set(tuple(p) for p in data)

        bench_counts = Counter(bench for _, bench in unique_pairs)

        return max(bench_counts.values()) if bench_counts else 0


def max_students_on_bench(pairs: List[Tuple[int, int]] = None, **kwargs) -> int:
    """Given pairs representing students sitting on benches, return the largest

    number of students sharing one bench.

    Each pair is typically represented as (student_id, bench_id).
    """
    sol = Solution()
    if pairs is not None:
        return sol.maxStudentsOnBench(pairs=pairs)
    return sol.maxStudentsOnBench(**kwargs)

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
