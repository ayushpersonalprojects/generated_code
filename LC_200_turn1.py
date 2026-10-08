def count_islands(grid: list[list[int]]) -> int:
    """Counts connected groups of land (1s) in a grid of land (1) and water (0)

    cells using four-directional adjacency.
    """
    if not grid or not grid[0]:
        return 0

    rows, cols = len(grid), len(grid[0])
    visited = [[False for _ in range(cols)] for _ in range(rows)]
    island_count = 0

    def dfs(r: int, c: int) -> None:
        # Stack for iterative DFS to avoid recursion limit issues on large grids
        stack = [(r, c)]
        visited[r][c] = True

        while stack:
            curr_r, curr_c = stack.pop()
            # Four directions: up, down, left, right
            directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

            for dr, dc in directions:
                nr, nc = curr_r + dr, curr_c + dc
                if (
                    0 <= nr < rows
                    and 0 <= nc < cols
                    and grid[nr][nc] == 1
                    and not visited[nr][nc]
                ):
                    visited[nr][nc] = True
                    stack.append((nr, nc))

    for r in range(rows):
        for c in range(cols):
            # If we find an unvisited land cell, it's the start of a new island
            if grid[r][c] == 1 and not visited[r][c]:
                island_count += 1
                dfs(r, c)

    return island_count


if __name__ == "__main__":
    # Example usage:
    # 1 represents land, 0 represents water
    grid = [
        [1, 1, 0, 0, 0],
        [1, 1, 0, 0, 1],
        [0, 0, 0, 1, 1],
        [0, 0, 0, 0, 0],
        [1, 0, 1, 1, 0],
    ]

    print(f"Number of islands: {count_islands(grid)}")  # Expected output: 4

# --- DYNAMIC AUTOMATED TEST HARNESS ---
if __name__ == '__main__':
    import inspect
    sol = Solution()
    # Find the user's defined method on Solution (skipping dunder methods)
    methods = [m for m in dir(sol) if not m.startswith('_') and callable(getattr(sol, m))]
    if not methods:
        raise AttributeError("No solution method found in class Solution")
    target_method = getattr(sol, methods[0])

    assert target_method(grid=[['1', '1', '0', '0', '0'], ['1', '1', '0', '0', '0'], ['0', '0', '1', '0', '0'], ['0', '0', '0', '1', '1']]) == 3
    assert target_method(grid=[['1', '1', '1'], ['0', '1', '0'], ['1', '1', '1']]) == 1
