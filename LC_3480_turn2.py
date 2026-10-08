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

    # Coordinate compression or events for sweep line:
    # Instead of a full segment tree which might have high overhead in Python for 200k,
    # let's use events sorted by l.
    # A pair (u, v) forbids l <= u and r >= v.
    # At each l from 0 to n-1, we have a set of active pairs (those with u >= l).
    # Their v values are active.
    # Since N, M <= 200,000, let's optimize the segment tree operations or use a simpler structure.
    # Actually, Python segment tree with flat arrays (lists) is very fast if implemented iteratively or cleanly.

    # Let's use an iterative segment tree or optimized recursive segment tree over v (0 to n-1).
    # To avoid list allocation overhead per leaf, we can store counts in an array and use a Fenwick tree or Segment tree.
    # But wait, we need the 1st and 2nd minimums. A segment tree over v is required.

    size = n
    tree_v1 = [-1] * (4 * size)
    tree_c1 = [0] * (4 * size)
    tree_id1 = [-1] * (4 * size)
    tree_v2 = [-1] * (4 * size)
    leaf_counts = [0] * size
    leaf_id = [-1] * size  # if count == 1, stores the single id

    def merge_info(v1_l, c1_l, id1_l, v2_l, v1_r, c1_r, id1_r, v2_r):
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

    # To handle multiple IDs at the same leaf without heavy lists:
    # Notice that if a leaf has multiple rectangles, its count > 1, so id1 is -1 and it can never be exclusive.
    # We only need the ID when count goes from 1 to 0 or 2 to 1.
    # But wait, if multiple rectangles have the same v, when one is removed, count drops from 2 to 1.
    # Which one is remaining? If there are duplicates, we can store a dictionary or a custom stack/list for leaves with count > 1.
    leaf_active_ids = [[] for _ in range(size)]

    def update_leaf(node, l, r, idx, rect_id, is_add):
        if l == r:
            if is_add:
                leaf_active_ids[idx].append(rect_id)
            else:
                leaf_active_ids[idx].remove(rect_id)

            c = len(leaf_active_ids[idx])
            if c == 0:
                tree_v1[node] = -1
                tree_c1[node] = 0
                tree_id1[node] = -1
                tree_v2[node] = -1
            elif c == 1:
                tree_v1[node] = l
                tree_c1[node] = 1
                tree_id1[node] = leaf_active_ids[idx][0]
                tree_v2[node] = -1
            else:
                tree_v1[node] = l
                tree_c1[node] = c
                tree_id1[node] = -1
                tree_v2[node] = -1
            return

        mid = (l + r) // 2
        if idx <= mid:
            update_leaf(2 * node, l, mid, idx, rect_id, is_add)
        else:
            update_leaf(2 * node + 1, mid + 1, r, idx, rect_id, is_add)

        left_res = (
            tree_v1[2 * node],
            tree_c1[2 * node],
            tree_id1[2 * node],
            tree_v2[2 * node],
        )
        right_res = (
            tree_v1[2 * node + 1],
            tree_c1[2 * node + 1],
            tree_id1[2 * node + 1],
            tree_v2[2 * node + 1],
        )
        v1, c1, id1, v2 = merge_info(*left_res, *right_res)
        tree_v1[node] = v1
        tree_c1[node] = c1
        tree_id1[node] = id1
        tree_v2[node] = v2

    events_remove = [[] for _ in range(n)]
    for i, (u, v) in enumerate(pairs):
        update_leaf(1, 0, n - 1, v, i, True)
        if u + 1 < n:
            events_remove[u + 1].append((v, i))

    base_invalid = 0
    exclusive_area = [0] * m

    for l in range(n):
        if l > 0:
            for v, i in events_remove[l]:
                update_leaf(1, 0, n - 1, v, i, False)

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
