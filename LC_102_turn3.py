from collections import deque
from typing import Optional, List, Union

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def levelOrder(self, root: Optional[Union[TreeNode, List]]) -> List[List[int]]:
        """
        Returns the values of a binary tree grouped by depth from the root level to the deepest level.
        Handles both TreeNode objects and LeetCode-style list representations.
        """
        if not root:
            return []
            
        # If input is given as a list (LeetCode level-order array representation)
        if isinstance(root, list):
            if not root[0] and root[0] is not None: # empty list
                return []
            
            nodes = [TreeNode(val) if val is not None else None for val in root]
            kids = nodes[::-1]
            root_node = kids.pop()
            
            for node in nodes:
                if node:
                    if kids: node.left = kids.pop()
                    if kids: node.right = kids.pop()
            root = root_node

        if not isinstance(root, TreeNode):
            return []

        result = []
        queue = deque([root])
        
        while queue:
            level_size = len(queue)
            current_level = []
            
            for _ in range(level_size):
                node = queue.popleft()
                current_level.append(node.val)
                
                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)
                    
            result.append(current_level)
            
        return result

def level_order_traversal(root: Optional[Union[TreeNode, List]]) -> List[List[int]]:
    sol = Solution()
    return sol.levelOrder(root)

# --- DYNAMIC AUTOMATED TEST HARNESS ---
if __name__ == '__main__':
    import inspect
    sol = Solution()
    # Find the user's defined method on Solution (skipping dunder methods)
    methods = [m for m in dir(sol) if not m.startswith('_') and callable(getattr(sol, m))]
    if not methods:
        raise AttributeError("No solution method found in class Solution")
    target_method = getattr(sol, methods[0])

    assert target_method(root=[3, 9, 20, None, None, 15, 7]) == [[3], [9, 20], [15, 7]]
    assert target_method(root=[]) == []
