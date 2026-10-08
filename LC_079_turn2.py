class Solution:
    def exist(self, board: list[list[str]], word: str) -> bool:
        """Determine whether a word can be formed by moving horizontally or vertically

        through adjacent cells in a character grid without reusing a cell.
        """
        if not board or not board[0]:
            return False

        rows, cols = len(board), len(board[0])

        def dfs(r, c, index):
            if index == len(word):
                return True
            if (
                r < 0
                or r >= rows
                or c < 0
                or c >= cols
                or board[r][c] != word[index]
            ):
                return False

            # Temporarily mark the cell as visited
            temp = board[r][c]
            board[r][c] = "#"

            # Explore all 4 directions: up, down, left, right
            found = (
                dfs(r + 1, c, index + 1)
                or dfs(r - 1, c, index + 1)
                or dfs(r, c + 1, index + 1)
                or dfs(r, c - 1, index + 1)
            )

            # Restore the cell
            board[r][c] = temp
            return found

        for r in range(rows):
            for c in range(cols):
                if board[r][c] == word[0] and dfs(r, c, 0):
                    return True

        return False

def exist(board: list[list[str]], word: str) -> bool:
    return Solution().exist(board, word)

# --- DYNAMIC AUTOMATED TEST HARNESS ---
if __name__ == '__main__':
    import inspect
    sol = Solution()
    # Find the user's defined method on Solution (skipping dunder methods)
    methods = [m for m in dir(sol) if not m.startswith('_') and callable(getattr(sol, m))]
    if not methods:
        raise AttributeError("No solution method found in class Solution")
    target_method = getattr(sol, methods[0])

    assert target_method(board=[['A', 'B', 'C', 'E'], ['S', 'F', 'C', 'S'], ['A', 'D', 'E', 'E']], word='ABCCED') == True
    assert target_method(board=[['A', 'B', 'C', 'E'], ['S', 'F', 'C', 'S'], ['A', 'D', 'E', 'E']], word='SEE') == True
    assert target_method(board=[['A', 'B', 'C', 'E'], ['S', 'F', 'C', 'S'], ['A', 'D', 'E', 'E']], word='ABCB') == False
