from typing import List

class Solution:
    def assignElements(self, groups: List[int], elements: List[int]) -> List[int]:
        return assign_elements(groups, elements)

def assign_elements(groups: List[int], elements: List[int]) -> List[int]:
    """
    Assigns each group the smallest-indexed element satisfying its divisibility requirement.
    Returns the chosen element index, or -1 when none works.
    
    Args:
        groups: List of integers representing the groups.
        elements: List of integers representing the available elements.
        
    Returns:
        List of integers where the i-th element is the smallest index in `elements`
        that divides `groups[i]`, or -1 if no such element exists.
    """
    # Precompute the minimum index for each element value.
    # Since we want the smallest index, if a value appears multiple times,
    # we only care about its first occurrence.
    val_to_min_index = {}
    for j, val in enumerate(elements):
        if val not in val_to_min_index:
            val_to_min_index[val] = j
            
    # Memoization to avoid redundant computations for identical group values
    memo = {}
    
    result = []
    for g in groups:
        if g in memo:
            result.append(memo[g])
            continue
            
        best_idx = float('inf')
        
        divisors = []
        i = 1
        while i * i <= g:
            if g % i == 0:
                divisors.append(i)
                if i * i != g:
                    divisors.append(g // i)
            i += 1
            
        for d in divisors:
            if d in val_to_min_index:
                idx = val_to_min_index[d]
                if idx < best_idx:
                    best_idx = idx
                    
        ans = best_idx if best_idx != float('inf') else -1
        memo[g] = ans
        result.append(ans)
        
    return result

if __name__ == "__main__":
    sol = Solution()
    groups = [8, 4, 3]
    elements = [2, 4, 3]
    print(sol.assignElements(groups, elements))  # Output: [0, 0, 2]

# --- DYNAMIC AUTOMATED TEST HARNESS ---
if __name__ == '__main__':
    import inspect
    sol = Solution()
    # Find the user's defined method on Solution (skipping dunder methods)
    methods = [m for m in dir(sol) if not m.startswith('_') and callable(getattr(sol, m))]
    if not methods:
        raise AttributeError("No solution method found in class Solution")
    target_method = getattr(sol, methods[0])

    assert target_method(groups=[8, 4, 3, 2], elements=[4, 2]) == [0, 0, -1, 0]
    assert target_method(groups=[5, 10], elements=[3, 5]) == [1, 1]
