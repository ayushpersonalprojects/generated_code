import sys

def count_valid_numbers(L: int, R: int, target_balance: dict) -> int:
    """
    Counts integers in the range [L, R] whose digit frequencies satisfy a 
    specific balance property defined by `target_balance`.
    
    `target_balance` is a dictionary mapping digits (0-9) to their required counts.
    If a digit is not in the dictionary, its required count is 0.
    """
    # Convert range boundaries to string for digit DP
    s_l = str(L)
    s_r = str(R)
    
    # Pad s_l with leading zeros to match length of s_r
    s_l = s_l.zfill(len(s_r))
    
    # Total required counts across all digits
    total_len = len(s_r)
    
    # Normalize target_balance to have all keys 0-9
    req = {i: 0 for i in range(10)}
    for d, count in target_balance.items():
        req[d] = count
        
    # Check if the total required digits match the length of R
    if sum(req.values()) > total_len:
        return 0

    memo = {}

    def solve(s):
        """Counts numbers from 0 to s (represented as string) satisfying req."""
        n = len(s)
        
        # We use memoization. State: (index, tight, lead_zero, tuple of remaining counts)
        # Since the sum of counts is at most len(s), we can pack remaining counts.
        # However, to avoid negative counts during transitions, we track current counts
        # or remaining counts. Remaining counts is better for memoization.
        
        memo_local = {}
        
        def dp(index, tight, lead_zero, rem_counts):
            # If we placed all digits
            if index == n:
                # Check if all remaining counts are 0
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
                    # Leading zeros do not consume the required count for '0' 
                    # if the problem implies standard number representation 
                    # (i.e., leading zeros are not counted as digits of the number).
                    # Here we assume leading zeros are just placeholders.
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
    # Be careful with L-1 string representation and padding
    ans_r = solve(s_r)
    
    # Calculate L - 1
    if L > 0:
        s_l_minus_1 = str(L - 1).zfill(total_len)
        ans_l_minus_1 = solve(s_l_minus_1)
    else:
        ans_l_minus_1 = 0
        
    return ans_r - ans_l_minus_1

if __name__ == "__main__":
    # Example usage:
    # Count numbers between 10 and 50 where each number must contain 
    # exactly one '1' and one '2' (and 0 of others, total length up to 2).
    # Wait, for range 10 to 50, length is 2.
    # Let's define target balance: {'1': 1, '2': 1} -> numbers like 12, 21.
    L, R = 10, 100
    target = {1: 1, 2: 1}
    
    # Adjust target to match total digits if needed, 
    # but our function handles partial specifications (others default to 0).
    # Wait, the default in our function is 0 for unlisted digits. 
    # But if length of number is 2, and we specify 2 digits, the remaining 0 digits 
    # must sum up. Wait, numbers in [10, 99] have length 2. 
    # If target specifies 2 digits, total required is 2, which matches length 2.
    
    result = count_valid_numbers(L, R, target)
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
