from collections import defaultdict
from typing import List

class Solution:
    def maxPoints(self, points: List[List[int]]) -> int:
        n = len(points)
        if n <= 2:
            return n
        
        max_points = 0
        
        for i in range(n):
            slopes = defaultdict(int)
            duplicates = 1
            verticals = 0
            curr_max = 0
            
            x1, y1 = points[i]
            
            for j in range(i + 1, n):
                x2, y2 = points[j]
                
                if x1 == x2 and y1 == y2:
                    duplicates += 1
                    continue
                
                if x1 == x2:
                    verticals += 1
                    curr_max = max(curr_max, verticals)
                else:
                    # Calculate reduced slope (dx, dy)
                    dx = x2 - x1
                    dy = y2 - y1
                    
                    import math
                    gcd = math.gcd(dx, dy)
                    dx //= gcd
                    dy //= gcd
                    
                    # Normalize the sign to avoid -0 and inconsistent signs
                    if dx < 0:
                        dx = -dx
                        dy = -dy
                    elif dx == 0:
                        dy = abs(dy)
                        
                    slopes[(dx, dy)] += 1
                    curr_max = max(curr_max, slopes[(dx, dy)])
            
            max_points = max(max_points, curr_max + duplicates)
            
        return max_points

def maxPoints(points: List[List[int]]) -> int:
    return Solution().maxPoints(points)

# --- DYNAMIC AUTOMATED TEST HARNESS ---
if __name__ == '__main__':
    import inspect
    sol = Solution()
    # Find the user's defined method on Solution (skipping dunder methods)
    methods = [m for m in dir(sol) if not m.startswith('_') and callable(getattr(sol, m))]
    if not methods:
        raise AttributeError("No solution method found in class Solution")
    target_method = getattr(sol, methods[0])

    assert target_method(points=[[1, 1], [2, 2], [3, 3]]) == 3
    assert target_method(points=[[1, 1], [3, 2], [5, 3], [4, 1], [2, 3], [1, 4]]) == 4
