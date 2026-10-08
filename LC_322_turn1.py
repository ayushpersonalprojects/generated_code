def min_coins(coins: list[int], target: int) -> int:
    """Returns the minimum number of coins needed to form the target amount,

    or -1 if impossible.
    """
    # dp[i] will store the minimum coins needed to get amount i
    # Initialize with infinity for all amounts up to target
    dp = [float("inf")] * (target + 1)
    dp[0] = 0

    for i in range(1, target + 1):
        for coin in coins:
            if i - coin >= 0:
                dp[i] = min(dp[i], dp[i - coin] + 1)

    return dp[target] if dp[target] != float("inf") else -1


if __name__ == "__main__":
    # Example usage:
    coins = [1, 2, 5]
    target = 11
    print(f"Coins: {coins}, Target: {target}")
    print(f"Minimum coins needed: {min_coins(coins, target)}")  # Expected: 3 (5 + 5 + 1)

# --- DYNAMIC AUTOMATED TEST HARNESS ---
if __name__ == '__main__':
    import inspect
    sol = Solution()
    # Find the user's defined method on Solution (skipping dunder methods)
    methods = [m for m in dir(sol) if not m.startswith('_') and callable(getattr(sol, m))]
    if not methods:
        raise AttributeError("No solution method found in class Solution")
    target_method = getattr(sol, methods[0])

    assert target_method(coins=[1, 2, 5], amount=11) == 3
    assert target_method(coins=[2], amount=3) == -1
    assert target_method(coins=[1], amount=0) == 0
