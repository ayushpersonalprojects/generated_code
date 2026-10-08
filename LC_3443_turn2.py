from collections import Counter


class Solution:

    def maxManhattanDistance(self, moves: str, k: int) -> int:
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
            prefix_len = (
                counts["N"] + counts["S"] + counts["E"] + counts["W"]
            )

            current_dist = abs(vertical) + abs(horizontal)
            potential_dist = current_dist + 2 * k
            max_dist = max(max_dist, min(prefix_len, potential_dist))

        return max_dist


def maxManhattanDistance(moves: str, k: int) -> int:
    return Solution().maxManhattanDistance(moves, k)


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
