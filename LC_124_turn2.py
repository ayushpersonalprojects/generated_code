class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def maxPathSum(self, root) -> int:
        # If root is given as a list, deserialize it into a binary tree first
        if isinstance(root, list):
            if not root:
                return 0
            nodes = [TreeNode(val) if val is not None else None for val in root]
            kids = nodes[::-1]
            root_node = kids.pop()
            for node in nodes:
                if node:
                    if kids: node.left = kids.pop()
                    if kids: node.right = kids.pop()
            root = root_node

        max_sum = float('-inf')
        
        def helper(node):
            nonlocal max_sum
            if not node:
                return 0
            
            # Max gain from left and right subtrees. 
            # If the gain is negative, we can choose not to include it (hence max(0, ...))
            left_gain = max(0, helper(node.left))
            right_gain = max(0, helper(node.right))
            
            # The price to start a new path where `node` is the highest node (price of path through this node)
            current_path_sum = node.val + left_gain + right_gain
            
            # Update the global maximum if the current path is greater
            max_sum = max(max_sum, current_path_sum)
            
            # For the recursion return value, we can only return the contribution of the node 
            # plus either its left or right child path (since it must be a single connected line upwards)
            return node.val + max(left_gain, right_gain)
        
        helper(root)
        return max_sum

# --- DYNAMIC AUTOMATED TEST HARNESS ---
if __name__ == '__main__':
    import inspect
    sol = Solution()
    # Find the user's defined method on Solution (skipping dunder methods)
    methods = [m for m in dir(sol) if not m.startswith('_') and callable(getattr(sol, m))]
    if not methods:
        raise AttributeError("No solution method found in class Solution")
    target_method = getattr(sol, methods[0])

    assert target_method(root=[1, 2, 3]) == 6
    assert target_method(root=[-10, 9, 20, None, None, 15, 7]) == 42
