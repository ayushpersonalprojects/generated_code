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

    # Count valid permutations starting with odd
    # To start with odd: odd, even, odd, even...
    # Number of odd positions = ceil(n / 2), number of even positions = floor(n / 2)
    num_odd_spots = (n + 1) // n_div_2_dummy = 0  # just to structure
    len_odds = len(odds)
    len_evens = len(evens)

    def count_perms(l_odds: int, l_evens: int, starts_with_odd: bool) -> int:
        if starts_with_odd:
            if l_odds != l_evens and l_odds != l_evens + 1:
                return 0
            if l_odds == 0 and l_evens == 0:
                return 1
            # Next must be even
            return math.factorial(l_odds) * math.factorial(l_evens)
        else:
            if l_evens != l_odds and l_evens != l_odds + 1:
                return 0
            if l_odds == 0 and l_evens == 0:
                return 1
            # Next must be odd
            return math.factorial(l_odds) * math.factorial(l_evens)

    # Actually, standard alternating permutation formula:
    # If n is even, len(odds) == len(evens) == n/2.
    #   Starts with odd: math.factorial(n//2) * math.factorial(n//2)
    #   Starts with even: math.factorial(n//2) * math.factorial(n//2)
    # If n is odd, len(odds) = (n+1)/2, len(evens) = (n-1)/2.
    #   Starts with odd: math.factorial((n+1)//2) * math.factorial((n-1)//2)
    #   Starts with even: 0 (since we need len_evens >= len_odds for even start, but evens has fewer)

    def total_count(n):
        o = (n + 1) // 2
        e = n // 2
        c = 0
        # Try starting with odd
        if o == e or o == e + 1:
            c += math.factorial(o) * math.factorial(e)
        # Try starting with even
        if e == o or e == o + 1:
            c += math.factorial(e) * math.factorial(o)
        return c

    # Let's dynamically construct the permutation.
    result = []
    current_odds = list(odds)
    current_evens = list(evens)

    # Check if k is within total possible permutations
    # To be precise, let's just use backtracking/lexicographical counting.

    def solve(rem_n, last_was_odd, cur_odds, cur_evens, k_val):
        if rem_n == 0:
            return []

        # Try all possible next numbers
        # If last was odd, next must be even. If last was none, can be either.
        candidates = []
        if not result:
            candidates = sorted(cur_odds + cur_evens)
        else:
            last_val = result[-1]
            if last_val % 2 != 0:
                candidates = sorted(cur_evens)
            else:
                candidates = sorted(cur_odds)

        for cand in candidates:
            # Temporarily pick cand
            is_odd = cand % 2 != 0
            if is_odd:
                cur_odds.remove(cand)
            else:
                cur_evens.remove(cand)
            result.append(cand)

            # Count how many valid permutations can be formed with current state
            sub_count = math.factorial(len(cur_odds)) * math.factorial(
                len(cur_evens)
            )
            # Wait, factorial product is only valid if alternating can strictly continue.
            # Alternating count for remaining:
            # The remaining must be partitionable into alternating sequence.
            # Specifically, |len_odds_rem - len_evens_rem| <= 1.
            valid = True
            if abs(len(cur_odds) - len(cur_evens)) > 1:
                valid = 0
            else:
                # Also, the next element parity is fixed (opposite of cand).
                # Does the count of remaining odds and evens match the required alternating pattern?
                # If next needed is odd, we need len(cur_odds) >= len(cur_evens) depending on pattern.
                # Actually, any interleaving of remaining odds and evens of sizes S_o and S_e
                # where |S_o - S_e| <= 1 has valid alternating permutations!
                # Wait, if we fix the first element of the remainder, say it needs to be Odd,
                # then if len(cur_odds) < len(cur_evens), we can't start with Odd and alternate.
                next_need_odd = cand % 2 == 0  # opposite parity
                if next_need_odd:
                    if len(cur_odds) < len(cur_evens):
                        valid = False
                else:
                    if len(cur_evens) < len(cur_odds):
                        valid = False

                if valid:
                    # Number of ways to arrange remaining
                    # If next needed is odd and len_odds == len_evens + 1, only 1 pattern (O E O E...)
                    # If len_odds == len_evens, 2 patterns (O E... and E O...) -> wait, next is fixed!
                    # If next is fixed, say Odd, and len_odds == len_evens, can we do O E O E...?
                    # Yes, starting with Odd when len_o == len_e is valid (e.g., O=2, E=2 -> O E O E).
                    # What if next is Odd and len_odds > len_e + 1? Invalid.
                    sub_count = math.factorial(len(cur_odds)) * math.factorial(
                        len(cur_evens)
                    )
                else:
                    sub_count = 0

            if k_val <= sub_count:
                res = solve(rem_n - 1, is_odd, cur_odds, cur_evens, k_val)
                if res is not None:
                    return [cand] + res
            else:
                k_val -= sub_count

            # Backtrack
            result.pop()
            if is_odd:
                cur_odds.append(cand)
                cur_odds.sort()
            else:
                cur_evens.append(cand)
                cur_evens.sort()

        return None

    # Total check
    ans = solve(n, None, current_odds, current_evens, k)
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
