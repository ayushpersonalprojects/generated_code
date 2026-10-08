import math
from typing import List


def get_kth_alternating_parity_permutation(n: int, k: int) -> List[int]:
    """Returns the k-th permutation of 1 through n (1-indexed k)

    where adjacent elements have alternating parity (even/odd), or an empty list if fewer than k exist.
    """
    if n == 0:
        return []

    odds = [i for i in range(1, n + 1) if i % 2 != 0]
    evens = [i for i in range(1, n + 1) if i % 2 == 0]

    result = []
    current_odds = list(odds)
    current_evens = list(evens)

    def solve(rem_n, cur_odds, cur_evens, k_val):
        if rem_n == 0:
            return []

        if not result:
            candidates = sorted(cur_odds + cur_evens)
        else:
            last_val = result[-1]
            if last_val % 2 != 0:
                candidates = sorted(cur_evens)
            else:
                candidates = sorted(cur_odds)

        for cand in candidates:
            is_odd = cand % 2 != 0
            if is_odd:
                cur_odds.remove(cand)
            else:
                cur_evens.remove(cand)
            result.append(cand)

            valid = True
            if abs(len(cur_odds) - len(cur_evens)) > 1:
                valid = False
            else:
                next_need_odd = cand % 2 == 0  # opposite parity
                if next_need_odd:
                    if len(cur_odds) < len(cur_evens):
                        valid = False
                else:
                    if len(cur_evens) < len(cur_odds):
                        valid = False

                if valid:
                    sub_count = math.factorial(len(cur_odds)) * math.factorial(
                        len(cur_evens)
                    )
                else:
                    sub_count = 0

            if k_val <= sub_count:
                res = solve(rem_n - 1, cur_odds, cur_evens, k_val)
                if res is not None:
                    return [cand] + res
            else:
                k_val -= sub_count

            result.pop()
            if is_odd:
                cur_odds.append(cand)
                cur_odds.sort()
            else:
                cur_evens.append(cand)
                cur_evens.sort()

        return None

    ans = solve(n, current_odds, current_evens, k)
    return ans if ans is not None else []


if __name__ == "__main__":
    print(get_kth_alternating_parity_permutation(4, 1))

# --- DYNAMIC AUTOMATED TEST HARNESS ---
if __name__ == '__main__':
    import inspect
    sol = Solution()
    # Find the user's defined method on Solution (skipping dunder methods)
    methods = [m for m in dir(sol) if not m.startswith('_') and callable(getattr(sol, m))]
    if not methods:
        raise AttributeError("No solution method found in class Solution")
    target_method = getattr(sol, methods[0])

    assert target_method(n=3, k=1) == [1, 2, 3]
    assert target_method(n=3, k=10) == []
