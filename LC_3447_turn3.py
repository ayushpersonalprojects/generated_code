from typing import List

class Solution:
    def assignElements(self, groups: List[int], elements: List[int]) -> List[int]:
        # Find the maximum value in groups to bound our divisor/multiple precomputation
        max_val = max(groups) if groups else 0
        
        # min_index[v] will store the smallest index in elements that has value v
        # Initialize with infinity
        min_index = {}
        for idx, elem in enumerate(elements):
            if elem not in min_index:
                min_index[elem] = idx
                
        # For each element value present in elements, we can update the best index
        # for all its multiples up to max_val. 
        # To do this efficiently, we can use an array of size max_val + 1.
        best_for_val = [-1] * (max_val + 1)
        
        # We want the smallest index for each value.
        # Iterate through elements and keep the minimum index.
        # But wait, multiple elements can have the same value. We already filtered to the first occurrence in min_index.
        
        # Sieve-like approach:
        # For each unique element value present in elements, update its multiples.
        # To ensure we get the *smallest* index overall, we should process elements in their original order.
        # However, checking every multiple for every element might be too slow if elements is large (up to 10^5).
        # A better way: for each value up to max_val, find the best index among its divisors, 
        # or precalculate for each number up to max_val the minimum index of its divisors.
        
        # Let's map each value present in `elements` to its minimum index.
        # Then for each number from 1 to max_val, we can find its minimum index divisor.
        
        # Actually, an array `best_div_idx` of size max_val + 1 initialized to -1.
        best_div_idx = [-1] * (max_val + 1)
        
        # Populate with elements
        for idx, elem in enumerate(elements):
            if elem <= max_val:
                if best_div_idx[elem] == -1 or idx < best_div_idx[elem]:
                    best_div_idx[elem] = idx
                    
        # Now, for each number from 1 to max_val, if it has a valid index, 
        # propagate that index to all its multiples. But wait, if a multiple already has a smaller index, keep the minimum.
        # Wait, if we iterate from 1 to max_val:
        # If `best_div_idx[i] != -1`, this index divides `i`. Could it divide multiples of `i` with a smaller index?
        # No, because if a multiple `M` has a divisor `d` with index `idx`, then `idx` is a candidate for `M`.
        # Standard sieve:
        
        # Let's maintain `min_elem_idx` for each number up to max_val.
        # First, store the minimum index of each element value.
        val_to_idx = {}
        for idx, val in enumerate(elements):
            if val not in val_to_idx:
                val_to_idx[val] = idx
                
        # ans array for each value up to max_val
        val_ans = [-1] * (max_val + 1)
        
        # For every possible element value that appears in `elements`, 
        # we can update its multiples.
        # Wait, if we iterate through `elements` in order:
        seen = set()
        for idx, val in enumerate(elements):
            if val > max_val or val in seen:
                continue
            seen.add(val)
            # update all multiples of val
            curr = val
            while curr <= max_val:
                if val_ans[curr] == -1 or idx < val_ans[curr]:
                    val_ans[curr] = idx
                curr += val
                
        # Wait, the sieve approach above updates multiples of *each unique element*. 
        # Since we iterate `elements` in order, the first time we see a value, we update its multiples.
        # But what if a smaller index appears later for the *same* value? We handled that by `val in seen`? 
        # Wait! If `val` appears later with a *smaller* index, we skipped it because `val in seen`!
        # That's wrong: we want the *smallest* index overall for each value.
        
        # Correct precomputation for value-to-min_index:
        val_to_min_idx = {}
        for idx, val in enumerate(elements):
            if val not in val_to_min_idx:
                val_to_min_idx[val] = idx
            else:
                if idx < val_to_min_idx[val]:
                    val_to_min_idx[val] = idx
                    
        # Now we have the absolute minimum index for each distinct value in `elements`.
        # Can we use a sieve where for each number `i` from 1 to max_val, we check its divisors, 
        # or for each value in `val_to_min_idx`, we update its multiples?
        
        # If we update multiples for each `(val, idx)` in `val_to_min_idx`:
        # for val, idx in val_to_min_idx.items():
        #     curr = val
        #     while curr <= max_val:
        #         if val_ans[curr] == -1 or idx < val_ans[curr]:
        #             val_ans[curr] = idx
        #         curr += val
        # The total operations for this harmonic series is O(max_val log max_val), which is very fast! (max_val <= 10^5 typically, or up to max group value).
        
        # Let's double check constraints. Usually groups and elements values can be up to 10^5.
        # Let's implement this sieve approach:
        
        val_ans = [-1] * (max_val + 1)
        
        for val, idx in val_to_min_idx.items():
            curr = val
            while curr <= max_val:
                if val_ans[curr] == -1 or idx < val_ans[curr]:
                    val_ans[curr] = idx
                curr += val
                
        return [val_ans[g] for g in groups]

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
