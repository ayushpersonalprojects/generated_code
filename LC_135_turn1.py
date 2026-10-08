def candy(ratings: list[int]) -> int:
    """Calculates the minimum number of candies needed to distribute to children

    such that each child has at least one candy, and children with higher ratings
    get more candies than their neighbors.
    """
    n = len(ratings)
    if n == 0:
        return 0

    candies = [1] * n

    # Forward pass: check left neighbor
    for i in range(1, n):
        if ratings[i] > ratings[i - 1]:
            candies[i] = candies[i - 1] + 1

    # Backward pass: check right neighbor
    for i in range(n - 2, -1, -1):
        if ratings[i] > ratings[i + 1]:
            candies[i] = max(candies[i], candies[i + 1] + 1)

    return sum(candies)

# --- DYNAMIC AUTOMATED TEST HARNESS ---
if __name__ == '__main__':
    import inspect
    sol = Solution()
    # Find the user's defined method on Solution (skipping dunder methods)
    methods = [m for m in dir(sol) if not m.startswith('_') and callable(getattr(sol, m))]
    if not methods:
        raise AttributeError("No solution method found in class Solution")
    target_method = getattr(sol, methods[0])

    assert target_method(ratings=[1, 0, 2]) == 5
    assert target_method(ratings=[1, 2, 2]) == 4
