from collections import Counter

class Solution:
    def findValidPair(self, s: str) -> str:
        """Finds an adjacent pair of digits whose values differ and whose frequencies
        in the full string equal the corresponding digit values.

        Returns the first valid pair as a two-character string, or an empty string if none exists.
        """
        if not s or not isinstance(s, str):
            return ""

        # Count frequencies of all digits in the string
        counts = Counter(s)

        # Iterate through adjacent pairs
        for i in range(len(s) - 1):
            d1_char = s[i]
            d2_char = s[i + 1]

            # Digits must differ in value
            if d1_char == d2_char:
                continue

            d1 = int(d1_char)
            d2 = int(d2_char)

            # Check if their frequencies equal their respective values
            if counts[d1_char] == d1 and counts[d2_char] == d2:
                return d1_char + d2_char

        return ""

def find_special_adjacent_pair(s: str) -> str:
    sol = Solution()
    return sol.findValidPair(s)


if __name__ == "__main__":
    # Test cases
    print(repr(find_special_adjacent_pair("221")))  # Expected: '21' (freq('2')=2, freq('1')=1)
    print(repr(find_special_adjacent_pair("223")))  # Expected: ''
    print(repr(find_special_adjacent_pair("122")))  # Expected: '12' (freq('1')=1, freq('2')=2)
    print(repr(find_special_adjacent_pair("3331")))  # Expected: '31' (freq('3')=3, freq('1')=1)
    print(repr(find_special_adjacent_pair("55555"))) # Expected: '' (no differing adjacent digits)
    print(repr(find_special_adjacent_pair("")))     # Expected: ''

# --- DYNAMIC AUTOMATED TEST HARNESS ---
if __name__ == '__main__':
    import inspect
    sol = Solution()
    # Find the user's defined method on Solution (skipping dunder methods)
    methods = [m for m in dir(sol) if not m.startswith('_') and callable(getattr(sol, m))]
    if not methods:
        raise AttributeError("No solution method found in class Solution")
    target_method = getattr(sol, methods[0])

    assert target_method(s='2523533') == '23'
    assert target_method(s='221133') == '13'
