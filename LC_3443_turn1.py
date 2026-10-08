from collections import Counter


def maxManhattanDistance(moves: str, k: int) -> int:
    """Calculates the maximum Manhattan distance from the origin achieved at any

    prefix of the movement string, assuming we can change at most k moves.
    """
    # Directions: 'N', 'S', 'E', 'W'
    # Track the count of each move seen so far in the prefix
    counts = Counter()
    max_dist = 0

    for char in moves:
        counts[char] += 1

        # Current net displacement without changes
        vertical = counts["N"] - counts["S"]
        horizontal = counts["E"] - counts["W"]

        # Current prefix length
        prefix_len = counts["N"] + counts["S"] + counts["E"] + counts["W"]

        # Maximum possible Manhattan distance with at most k changes:
        # Distance = |N - S| + |E - W|
        # To maximize this, we want to increase the dominant directions and decrease the weaker ones.
        # However, we can at most add +2 to the distance for each change (turning a 'S' into an 'N', etc.),
        # bounded by the number of available moves we can change and the prefix length.
        # Specifically, the maximum possible distance for a prefix of length L with k changes
        # is min(L, net_dist + 2 * k). Wait, let's be precise:
        # The true max distance achievable by optimally flipping up to k characters in a prefix
        # is min(prefix_len, abs(N - S) + abs(E - W) + 2 * k).
        # Actually, let's verify if we can always reach this upper bound:
        # We can increase the net vertical/horizontal by changing opposing directions.
        # Each change of a 'S' to an 'N' increases vertical by 2.
        # We have a total of prefix_len moves. The maximum Manhattan distance on a grid of length L is L.
        # Also, we can increase the distance by min(k, number of non-dominant moves we can flip) * 2?
        # No, any flip of a non-dominant move to a dominant one increases the distance by 2.
        # The total number of non-dominant moves available in the prefix is:
        # total_moves - (|N - S| + |E - W|)?
        # Actually, the formula for max distance with k flips in a sequence of length L
        # where current coordinates are (y, x) is:
        # abs(y) + abs(x) + 2 * min(k, L - (abs(y) + abs(x)) equivalents?
        # Simpler: The maximum distance is min(prefix_len, abs(N - S) + abs(E - W) + 2 * k).
        # Let's double check this bound. Can we always achieve it?
        # Suppose we have N, S counts. The number of "wasted" moves is S (if N > S).
        # We can flip up to k of these S's to N's. Each flip reduces S by 1 and increases N by 1,
        # changing N - S by +2. Thus Manhattan distance increases by 2.
        # If we run out of S's, we can flip other directions, which decreases their contribution and increases N,
        # still netting +2 per flip as long as we don't exceed prefix_len and parity constraints.
        # Parity constraint: Manhattan distance parity must match prefix_len parity (though here we can just change
        # any move, so parity changes by 2, maintaining the parity of prefix_len).
        # Thus, the maximum distance is indeed min(prefix_len, abs(N - S) + abs(E - W) + 2 * k).

        current_dist = abs(vertical) + abs(horizontal)
        potential_dist = current_dist + 2 * k
        max_dist = max(max_dist, min(prefix_len, potential_dist))

    return max_dist


if __name__ == "__main__":
    # Example usage:
    moves = "NWSE"
    k = 1
    print(
        f"Max distance for '{moves}' with k={k}: {maxManhattanDistance(moves, k)}"
    )

# --- DYNAMIC AUTOMATED TEST HARNESS ---
if __name__ == '__main__':
    import inspect
    sol = Solution()
    # Find the user's defined method on Solution (skipping dunder methods)
    methods = [m for m in dir(sol) if not m.startswith('_') and callable(getattr(sol, m))]
    if not methods:
        raise AttributeError("No solution method found in class Solution")
    target_method = getattr(sol, methods[0])

    assert target_method(s='NWSE', k=1) == 3
    assert target_method(s='NSWWEW', k=3) == 6
