from typing import List

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
            
    # Get all unique element values sorted to optimize divisor checks,
    # or just use the distinct values with their minimum indices.
    unique_elements = list(val_to_min_index.items())
    
    # Memoization to avoid redundant computations for identical group values
    memo = {}
    
    result = []
    for g in groups:
        if g in memo:
            result.append(memo[g])
            continue
            
        best_idx = float('inf')
        # Check all possible divisors of g up to sqrt(g)
        # To make it efficient, we can iterate through the unique element values.
        # However, if `groups` and `elements` can be large, we can iterate divisors of g.
        # Let's write a helper to find divisors of g.
        
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
    # Example usage:
    groups = [8, 4, 3]
    elements = [2, 4, 3]
    print(assign_elements(groups, elements))  # Output: [0, 0, 2]

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
