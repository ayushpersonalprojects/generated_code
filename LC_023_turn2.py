import heapq

# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
        
    # Adding __lt__ so heapq can compare ListNode objects by their 'val'
    def __lt__(self, other):
        return self.val < other.val

class Solution:
    def mergeKLists(self, lists: list) -> ListNode:
        """
        Merges k sorted linked lists into one sorted linked list using a min-heap.
        Time Complexity: O(N log k), where N is the total number of nodes and k is the number of lists.
        Space Complexity: O(k) to store the heap elements.
        """
        # Convert any input lists of integers into linked lists if necessary,
        # or handle standard ListNode inputs.
        processed_lists = []
        for l in lists:
            if isinstance(l, list):
                if not l:
                    continue
                head = ListNode(l[0])
                curr = head
                for val in l[1:]:
                    curr.next = ListNode(val)
                    curr = curr.next
                processed_lists.append(head)
            elif isinstance(l, ListNode):
                processed_lists.append(l)

        min_heap = []
        
        # Push the first node of each non-empty list into the min-heap
        for l in processed_lists:
            if l:
                # We need to store a tie-breaker in python heapq since ListNode doesn't 
                # handle comparisons of nodes with equal values gracefully if next is compared.
                # But our __lt__ only compares .val, which is fine, though we can use id(l) as tie-breaker.
                heapq.heappush(min_heap, (l.val, id(l), l))
                
        dummy_head = ListNode(0)
        current = dummy_head
        
        while min_heap:
            # Extract the smallest node from the heap
            val, _, smallest_node = heapq.heappop(min_heap)
            
            # Append it to the merged list
            current.next = smallest_node
            current = current.next
            
            # If there is a next node in the same list, push it to the heap
            if smallest_node.next:
                heapq.heappush(min_heap, (smallest_node.next.val, id(smallest_node.next), smallest_node.next))
                
        return dummy_head.next

# --- DYNAMIC AUTOMATED TEST HARNESS ---
if __name__ == '__main__':
    import inspect
    sol = Solution()
    # Find the user's defined method on Solution (skipping dunder methods)
    methods = [m for m in dir(sol) if not m.startswith('_') and callable(getattr(sol, m))]
    if not methods:
        raise AttributeError("No solution method found in class Solution")
    target_method = getattr(sol, methods[0])

    assert target_method(lists=[[1, 4, 5], [1, 3, 4], [2, 6]]) == [1, 1, 2, 3, 4, 4, 5, 6]
    assert target_method(lists=[]) == []
