import sys


def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    n = int(input_data[0])
    m = int(input_data[1])

    idx = 2
    pairs = []
    for _ in range(m):
        u = int(input_data[idx])
        v = int(input_data[idx + 1])
        idx += 2
        if u > v:
            u, v = v, u
        pairs.append((u - 1, v - 1))

    total_subarrays = n * (n + 1) // 2

    if m == 0:
        print(total_subarrays)
        return

    # Events for sweep-line over l from 0 to n-1.
    # A pair (u, v) is active for l in [0, u].
    # We collect additions and removals at each l.
    # Since all start at l=0, we can add them initially.
    events_remove = [[] for _ in range(n)]
    for i, (u, v) in enumerate(pairs):
        if u + 1 < n:
            events_remove[u + 1].append((v, i))

    # Iterative Segment Tree over v (0 to n-1).
    # Each leaf v maintains:
    # - count: number of active rectangles with this v
    # - id: the single rectangle id if count == 1, else -1
    size = n
    tree_v1 = [-1] * (2 * size)
    tree_c1 = [0] * (2 * size)
    tree_id1 = [-1] * (2 * size)
    tree_v2 = [-1] * (2 * size)

    leaf_active_ids = [[] for _ in range(size)]

    def merge_nodes(
        v1_l, c1_l, id1_l, v2_l, v1_r, c1_r, id1_r, v2_r
    ):
        if v1_l == -1:
            return v1_r, c1_r, id1_r, v2_r
        if v1_r == -1:
            return v1_l, c1_l, id1_l, v2_l

        if v1_l < v1_r:
            cand_v2 = v2_l if v2_l != -1 else v1_r
            if v1_r < cand_v2:
                cand_v2 = v1_r
            return v1_l, c1_l, id1_l, cand_v2
        else:
            cand_v2 = v2_r if v2_r != -1 else v1_l
            if v1_l < cand_v2:
                cand_v2 = v1_l
            return v1_r, c1_r, id1_r, cand_v2

    def update(idx, rect_id, is_add):
        if is_add:
            leaf_active_ids[idx].append(rect_id)
        else:
            leaf_active_ids[idx].remove(rect_id)

        c = len(leaf_active_ids[idx])
        pos = idx + size
        if c == 0:
            tree_v1[pos] = -1
            tree_c1[pos] = 0
            tree_id1[pos] = -1
            tree_v2[pos] = -1
        elif c == 1:
            tree_v1[pos] = idx
            tree_c1[pos] = 1
            tree_id1[pos] = leaf_active_ids[idx][0]
            tree_v2[pos] = -1
        else:
            tree_v1[pos] = idx
            tree_c1[pos] = c
            tree_id1[pos] = -1
            tree_v2[pos] = -1

        pos //= 2
        while pos > 0:
            left = 2 * pos
            right = 2 * pos + 1
            v1, c1, id1, v2 = merge_nodes(
                tree_v1[left],
                tree_c1[left],
                tree_id1[left],
                tree_v2[left],
                tree_v1[right],
                tree_c1[right],
                tree_id1[right],
                tree_v2[right],
            )
            tree_v1[pos] = v1
            tree_c1[pos] = c1
            tree_id1[pos] = id1
            tree_v2[pos] = v2
            pos //= 2

    # Initialize segment tree with all pairs active at l = 0
    for i, (u, v) in enumerate(pairs):
        leaf_active_ids[v].append(i)

    for v in range(size):
        c = len(leaf_active_ids[v])
        pos = v + size
        if c == 1:
            tree_v1[pos] = v
            tree_c1[pos] = 1
            tree_id1[pos] = leaf_active_ids[v][0]
            tree_v2[pos] = -1
        elif c > 1:
            tree_v1[pos] = v
            tree_c1[pos] = c
            tree_id1[pos] = -1
            tree_v2[pos] = -1

    for pos in range(size - 1, 0, -1):
        left = 2 * pos
        right = 2 * pos + 1
        v1, c1, id1, v2 = merge_nodes(
            tree_v1[left],
            tree_c1[left],
            tree_id1[left],
            tree_v2[left],
            tree_v1[right],
            tree_c1[right],
            tree_id1[right],
            tree_v2[right],
        )
        tree_v1[pos] = v1
        tree_c1[pos] = c1
        tree_id1[pos] = id1
        tree_v2[pos] = v2

    base_invalid = 0
    exclusive_area = [0] * m

    for l in range(n):
        if l > 0:
            for v, i in events_remove[l]:
                update(v, i, False)

        v1 = tree_v1[1]
        if v1 != -1:
            base_invalid += n - v1
            c1 = tree_c1[1]
            id1 = tree_id1[1]
            v2 = tree_v2[1]
            if c1 == 1 and id1 != -1:
                length = (v2 - v1) if v2 != -1 else (n - v1)
                exclusive_area[id1] += length

    base_valid = total_subarrays - base_invalid
    max_exclusive = max(exclusive_area) if exclusive_area else 0
    print(base_valid + max_exclusive)


if __name__ == "__main__":
    solve()

# --- DYNAMIC AUTOMATED TEST HARNESS ---
if __name__ == '__main__':
    import inspect
    sol = Solution()
    # Find the user's defined method on Solution (skipping dunder methods)
    methods = [m for m in dir(sol) if not m.startswith('_') and callable(getattr(sol, m))]
    if not methods:
        raise AttributeError("No solution method found in class Solution")
    target_method = getattr(sol, methods[0])

    assert target_method(n=4, conflictingPairs=[[2, 3], [1, 4]]) == 7
    assert target_method(n=3, conflictingPairs=[[1, 2]]) == 5
