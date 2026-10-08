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
    def mergeKLists(self, lists: list[ListNode]) -> ListNode:
        """
        Merges k sorted linked lists into one sorted linked list using a min-heap.
        Time Complexity: O(N log k), where N is the total number of nodes and k is the number of lists.
        Space Complexity: O(k) to store the heap elements.
        """
        min_heap = []
        
        # Push the first node of each non-empty list into the min-heap
        for l in lists:
            if l:
                heapq.heappush(min_heap, l)
                
        dummy_head = ListNode(0)
        current = dummy_head
        
        while min_heap:
            # Extract the smallest node from the heap
            smallest_node = heapq.heappop(min_heap)
            
            # Append it to the merged list
            current.next = smallest_node
            current = current.next
            
            # If there is a next node in the same list, push it to the heap
            if smallest_node.next:
                heapq.heappush(min_heap, smallest_node.next)
                
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
