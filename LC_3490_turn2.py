import sys

class Solution:
    def countValidNumbers(self, L: int, R: int, target_balance: dict) -> int:
        """
        Counts integers in the range [L, R] whose digit frequencies satisfy a 
        specific balance property defined by `target_balance`.
        
        `target_balance` is a dictionary mapping digits (0-9) to their required counts.
        If a digit is not in the dictionary, its required count is 0.
        """
        # Convert range boundaries to string for digit DP
        s_r = str(R)
        total_len = len(s_r)
        
        # Normalize target_balance to have all keys 0-9
        req = {i: 0 for i in range(10)}
        for d, count in target_balance.items():
            req[d] = count
            
        # Check if the total required digits exceed the length of R
        if sum(req.values()) > total_len:
            return 0

        def solve(s):
            """Counts numbers from 0 to s (represented as string) satisfying req."""
            n = len(s)
            memo_local = {}
            
            def dp(index, tight, lead_zero, rem_counts):
                # If we placed all digits
                if index == n:
                    return 1 if all(c == 0 for c in rem_counts) else 0
                    
                state = (index, tight, lead_zero, rem_counts)
                if state in memo_local:
                    return memo_local[state]
                    
                limit = int(s[index]) if tight else 9
                ans = 0
                
                for digit in range(limit + 1):
                    new_tight = tight and (digit == limit)
                    new_lead_zero = lead_zero and (digit == 0)
                    
                    if new_lead_zero:
                        # Leading zeros do not consume the required count for digits
                        ans += dp(index + 1, new_tight, True, rem_counts)
                    else:
                        # Check if we still need this digit
                        if rem_counts[digit] > 0:
                            new_rem = list(rem_counts)
                            new_rem[digit] -= 1
                            ans += dp(index + 1, new_tight, False, tuple(new_rem))
                            
                memo_local[state] = ans
                return ans

            initial_rem = tuple(req[i] for i in range(10))
            return dp(0, True, True, initial_rem)

        # Count(R) - Count(L - 1)
        ans_r = solve(s_r)
        
        # Calculate L - 1
        if L > 0:
            s_l_minus_1 = str(L - 1).zfill(total_len)
            ans_l_minus_1 = solve(s_l_minus_1)
        else:
            ans_l_minus_1 = 0
            
        return ans_r - ans_l_minus_1

if __name__ == "__main__":
    sol = Solution()
    L, R = 10, 100
    target = {1: 1, 2: 1}
    result = sol.countValidNumbers(L, R, target)
    print(f"Count of numbers in [{L}, {R}] with balance {target}: {result}")

# --- DYNAMIC AUTOMATED TEST HARNESS ---
if __name__ == '__main__':
    import inspect
    sol = Solution()
    # Find the user's defined method on Solution (skipping dunder methods)
    methods = [m for m in dir(sol) if not m.startswith('_') and callable(getattr(sol, m))]
    if not methods:
        raise AttributeError("No solution method found in class Solution")
    target_method = getattr(sol, methods[0])

    assert target_method(l=1, r=10) == 10
    assert target_method(l=10, r=20) == 10
