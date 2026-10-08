from collections import deque

def ladderLength(beginWord: str, endWord: str, wordList: list) -> int:
    wordSet = set(wordList)
    if endWord not in wordSet:
        return 0
    
    queue = deque([(beginWord, 1)])
    visited = {beginWord}
    
    while queue:
        current_word, level = queue.popleft()
        
        if current_word == endWord:
            return level
            
        for i in range(len(current_word)):
            for c in 'abcdefghijklmnopqrstuvwxyz':
                next_word = current_word[:i] + c + current_word[i+1:]
                
                if next_word in wordSet and next_word not in visited:
                    visited.add(next_word)
                    queue.append((next_word, level + 1))
                    
    return 0

# --- DYNAMIC AUTOMATED TEST HARNESS ---
if __name__ == '__main__':
    import inspect
    sol = Solution()
    # Find the user's defined method on Solution (skipping dunder methods)
    methods = [m for m in dir(sol) if not m.startswith('_') and callable(getattr(sol, m))]
    if not methods:
        raise AttributeError("No solution method found in class Solution")
    target_method = getattr(sol, methods[0])

    assert target_method(beginWord='hit', endWord='cog', wordList=['hot', 'dot', 'dog', 'lot', 'log', 'cog']) == 5
    assert target_method(beginWord='hit', endWord='cog', wordList=['hot', 'dot', 'dog', 'lot', 'log']) == 0
