import sys


def solve():
    # Read all input from standard input
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
        # We assume 1-based indexing for elements, converting to 0-based
        pairs.append((u - 1, v - 1))

    # A pair (u, v) with u < v forbids any subarray [L, R] such that L <= u and v <= R.
    # This means the forbidden start points are <= u and end points are >= v.
    # Total subarrays of length N is N * (N + 1) // 2.
    # Each pair (u, v) forbids (u + 1) * (N - v) subarrays.
    # If two pairs (u1, v1) and (u2, v2) overlap in their forbidden regions,
    # the number of doubly-forbiden subarrays is (min(u1, u2) + 1) * (N - max(v1, v2)).
    # Wait, the problem says "Remove at most one conflicting pair so the total number of valid subarrays is maximized."
    # Actually, standard problem: Given M pairs of conflicting elements, which pair removal maximizes valid subarrays?
    # Or does it mean pairs of indices that cannot be together?
    # Let's re-read carefully: "Remove at most one conflicting pair so the total number of valid subarrays is maximized."
    # A subarray is valid if it contains NO conflicting pair.
    # A conflicting pair is given as (u, v). If both u and v are in the subarray, it's invalid?
    # Usually, a pair (u, v) means u and v cannot both be present, which is equivalent to saying
    # the subarray cannot start at <= u and end at >= v (assuming u < v).
    # If we remove one pair, we add back the subarrays that were *only* forbidden by this pair.
    # More precisely, let F_i be the set of forbidden subarrays for pair i.
    # We want to maximize the size of the complement of (Union of F_j for j != i).
    # Maximize |All - Union_{j != i} F_j| = Min |Union_{j != i} F_j|.
    # Since |Union F_j| = Sum |F_j| - Intersections, removing pair i reduces the union size
    # by |F_i| minus the intersections of F_i with all other F_j.
    # Thus, to maximize the union (hence minimize it by removing i), we want to MAXIMIZE the reduction.
    # Reduction by removing i is |F_i| - sum_{j != i} |F_i int F_j| + ... (inclusion-exclusion, or if we consider pairwise overlaps).
    # Wait, usually these problems consider that each pair restricts the range [L, R].
    # Specifically, pair (u, v) forbids L <= u and R >= v.
    # Let's check if there's a standard problem: "Remove at most one restriction to maximize valid subarrays".
    # Let's implement an efficient sweep-line or interval overlap algorithm.

    # Total subarrays:
    total_subarrays = n * (n + 1) // 2

    # If M == 0, we remove nothing, answer is total_subarrays.
    if m == 0:
        print(total_subarrays)
        return

    # Each pair i has weight w_i = (u_i + 1) * (n - v_i).
    # The overlap between pair i and pair j is (min(u_i, u_j) + 1) * (n - max(v_i, v_j)) if they overlap, else 0.
    # If we remove pair i, the number of newly valid subarrays that were previously blocked ONLY by pair i
    # is complex if multiple pairs overlap. But wait!
    # Often, these problems assume we just want to remove the pair that was causing the most exclusive damage,
    # or it's about grid/intervals.
    # Let's write a robust solution. If the problem implies each pair is an interval [u, v],
    # and a valid subarray is one that doesn't contain any forbidden pair.
    # If we remove one pair, say k, the set of forbidden subarrays becomes U_{j != k} F_j.
    # We want to find k that minimizes the size of this union, which maximizes the valid subarrays.
    # |U_{j != k} F_j| = sum_{j != k} |F_j| - sum_{j < l, j != k, l != k} |F_j int F_l| + ...
    # If we only consider pairwise intersections (M is up to, say, 200,000):
    # This looks like we can compute for each pair its "exclusive" contribution, or use a sweep-line.

    # Let's output total_subarrays - (union size without i).
    # Since exact union size with up to M intervals can be computed by sweep-line:
    # A forbidden region is a rectangle in (L, R) space: L in [0, u], R in [v, n-1].
    # We have M rectangles. We want to find the union of these M rectangles.
    # Then for each i, we want the union of the other M-1 rectangles.
    # Efficiently computing union of M rectangles minus one rectangle for all i:
    # This can be done if M is small, or using persistent segment trees, or sweep-line if M is large.
    # Let's assume standard competitive programming constraints: M <= 2e5, N <= 2e5.
    # Wait, if M is large, we can't do O(M^2).
    # Let's rethink: does "conflicting pair" mean adjacent elements, or general pairs?
    # "Remove at most one conflicting pair so the total number of valid subarrays is maximized."
    # If the pairs are given, let's compute the total number of invalid subarrays (the union of rectangles [0..u_i] x [v_i..n-1]).
    # The area of the union of rectangles can be found by sweep-line on L (from 0 to n-1), maintaining R intervals.
    # Can we find the contribution of each rectangle to the union?
    # A point (l, r) is covered by multiple rectangles. If it's covered by *only* rectangle i,
    # then removing rectangle i will uncover (make valid) this point.
    # If it's covered by >= 2 rectangles, removing rectangle i leaves it covered by others, so it stays invalid.
    # Thus, the number of newly valid subarrays when removing rectangle i is EXACTLY
    # the number of points covered ONLY by rectangle i!
    # WOW. Is that true?
    # Let's check: A point is invalid if it's in the union.
    # It becomes valid if it's no longer in the union of the remaining rectangles.
    # It is in the union of all, but not in the union of remaining <=> it is covered ONLY by i.
    # So the gain in valid subarrays by removing i is precisely the area covered exclusively by rectangle i!
    # Therefore, we just need to find, for each rectangle, its exclusively covered area (number of grid points (l, r) with l <= u_i and r >= v_i such that no other rectangle covers (l, r)).
    # Maximizing valid subarrays <=> Maximizing the gain <=> Maximizing the exclusively covered area of the removed rectangle!
    # If we remove the rectangle with the maximum exclusively covered area, we maximize the valid subarrays.
    # What if we remove NO rectangle? Then valid subarrays = total - total_union.
    # Wait, the problem says "Remove AT MOST ONE conflicting pair".
    # So we can choose to remove 0 pairs (if removing 1 doesn't help, or if 0 is better? Wait, removing a pair can ONLY INCREASE or KEEP SAME the number of valid subarrays).
    # Wait, removing a pair removes constraints, so it can only INCREASE the number of valid subarrays (or keep it same if exclusive area is 0).
    # Thus, we should definitely consider removing the best pair, or 0 if no pairs. But wait, removing a pair always increases or keeps valid count same. So we just find max gain over all i, and also consider removing nothing (gain = 0). Since gain >= 0, max gain >= 0.

    # So the problem reduces to:
    # For each rectangle i = (u_i, v_i), find the number of points (l, r) with 0 <= l <= u_i and v_i <= r < n
    # that are covered by rectangle i and NO OTHER rectangle.
    # We want to find max_i (exclusive_area(i)), and the answer is (Total_Union_Area - Union_Without_Best_i) ?
    # No!
    # Valid_subarrays_with_removal_i = Total - (Union_Area - exclusive_area(i))
    # = (Total - Union_Area) + exclusive_area(i)
    # = (Valid_subarrays_with_none) + exclusive_area(i).
    # YES!
    # So Valid Subarrays with removal of i = (Base Valid Subarrays) + (Exclusive Area of i).
    # Therefore, to maximize Valid Subarrays, we just need to maximize Exclusive Area of i!
    # If max Exclusive Area is 0, we can just remove nothing (or any, doesn't matter, valid count is Base).
    # So the maximum valid subarrays = Base_Valid + max(0, max_i (Exclusive_Area_i)).

    # Now, how to compute the Exclusive Area for all rectangles efficiently?
    # Total rectangles M <= 200,000, N <= 200,000.
    # This is a classic 2D counting problem.
    # A point (l, r) is covered by rectangle i if l <= u_i and r >= v_i.
    # It is covered by EXCLUSIVELY rectangle i if it is covered by i, AND NOT covered by any j != i.
    # Since M can be large, how to compute exclusive area for each rectangle?
    # Often, this can be done using sweep-line or segment tree, or if M is small enough.
    # Wait, let's check typical constraints for this specific problem if it's from a known platform.
    # If N, M <= 200,000, $O(M \log M)$ or $O((N+M) \log N)$ is needed.
    # Let's think if we can use a segment tree or sweep-line.
    # A point (l, r) is covered by a set of rectangles.
    # We can use sweep-line over l from 0 to N-1.
    # At each l, we have a set of active rectangles (those with u_i >= l).
    # For these active rectangles, we care about their v_i values.
    # A point (l, r) is covered by rectangle i if r >= v_i.
    # It is exclusively covered by i if r is covered by i and NOT covered by any other active rectangle j.
    # This means r falls into a range of r-values where ONLY rectangle i is present among all active rectangles!
    # For a fixed l, as r goes from v_i to N-1:
    # The set of rectangles covering (l, r) is the set of active rectangles with v_j <= r.
    # We want to find the lengths of r-intervals where the coverage count is exactly 1, and that single rectangle is i.
    # This can be maintained using a Segment Tree over r (from 0 to N-1)!
    # Segment tree over r:
    # When l decreases from N-1 down to 0 (or increases from 0 to N-1):
    # Rectangles are added when l reaches u_i (or removed, depending on sweep direction).
    # Let's sweep l from 0 to N-1.
    # When l reaches u_i, rectangle i becomes active. Its r-range is [v_i, N-1].
    # Wait, the condition is l <= u_i. So as l increases, rectangles *enter* the active set at l = 0, and *leave* the active set when l > u_i.
    # So at l = 0, all rectangles with u_i >= 0 are active.
    # As l goes from 0 to N-1, rectangles with u_i == l - 1 leave the active set!
    # Let's sweep l from 0 to N-1:
    # At each l:
    # We have a set of active rectangles. Each active rectangle covers r in [v_i, N-1].
    # We can use a segment tree over r (size N) to maintain:
    # 1. The number of covering rectangles at each r.
    # 2. The ID of the covering rectangle if count == 1.
    # 3. The minimum count, count of minimums, etc. (Segment tree with range add and range queries).
    # Specifically, we want to sum up, for each rectangle i, the number of r values for the current l
    # where the count is 1 and the unique rectangle is i.
    # This is equivalent to: query the segment tree for the total length of r-intervals where count == 1 and ID == i.
    # Since we need this for all l, doing this naively per l is too slow ($O(N \cdot N)$), but with a segment tree,
    # updating when a rectangle is removed takes $O(\log N)$, and querying the total exclusive length for ALL rectangles at once... wait.
    # If we want the exclusive length for ALL rectangles at once at a given l,
    # the segment tree can directly store:
    # - `count`: number of rectangles covering r.
    # - `unique_id`: if `count == 1`, the ID of the rectangle; if `count == 0` or `> 1`, some invalid/null ID.
    # - `exclusive_len[id]`: accumulated exclusive length for each rectangle id!
    # Can we maintain `exclusive_len[id]` across the sweep line?
    # Notice that as l increases by 1, the set of active rectangles changes by removing those with u_i == l - 1.
    # When we remove a rectangle, we can update the segment tree.
    # But wait, how do we accumulate the exclusive length efficiently?
    # At each step l, the segment tree has some intervals where count == 1 and has a specific `unique_id`.
    # The sum of lengths of these intervals for a given `id` is the contribution at this specific l for that `id`!
    # If we can query the sum of lengths for each `id` at each step, or accumulate it... wait,
    # the total exclusive length for rectangle `id` is the sum over all l of (length of r where count==1 and id is active).
    # Since rectangle `id` is active for l = 0..u_i, its exclusive length is simply:
    # Sum_{l=0}^{u_i} (length of r where it's the ONLY active rectangle covering r).
    # This means for a fixed rectangle `id`, its exclusive area is the integral over l in [0, u_i] of (exclusive length of `id` at sweep-line step l).
    # Can we maintain this in a segment tree?
    # When we do range add on the segment tree (when a rectangle is added/removed),
    # the segment tree nodes can maintain the sum of lengths where count == 1 for EACH rectangle? No, too many rectangles.
    # But wait! Is M and N small enough, or is there an easier way?
    # Let's check standard constraints. If this is a typical problem, M, N might be up to 200,000,
    # but maybe we can use coordinate compression or the total number of pairs is small?
    # Wait, if M <= 200,000 and N <= 200,000, let's check if we can do something simpler,
    # or if we can use a randomized algorithm, or if M is actually small (e.g., M <= 500)?
    # Since I don't know the exact problem statement source (likely a recent Codeforces or AtCoder problem),
    # let's consider if M is small or if there's a simpler interpretation.
    # "Remove at most one conflicting pair so the total number of valid subarrays is maximized."
    # Wait! Could "conflicting pair" mean elements of the array, and M is the number of pairs?
    # If M is small (e.g. M <= 300 or M <= 2000), an $O(M^2)$ or $O(M \log M)$ approach works.
    # Let's write a solution that handles general M and N efficiently if possible, or uses an optimal approach.
    # Wait, let's re-read: "Remove at most one conflicting pair so the total number of valid subarrays is maximized."
    # If M is up to 200,000, $O(M \log M)$ is required.
    # Let's think: what if we just compute the answer using an interval sweep-line?
    # Let's implement a sweep-line algorithm that works for moderate N, M.
    # Python's speed might be an issue for 200,000, so we should keep it concise and fast.

    # Let's structure the sweep-line:
    # Events at each l:
    # Since l goes from 0 to N-1, and u_i can be up to N-1,
    # we can collect events:
    # Add events at l = 0 for all rectangles (since they all start at l=0? No, u_i is the upper bound for l, so l can be 0 up to u_i).
    # Wait! A pair (u, v) forbids L <= u and R >= v.
    # So for a fixed pair, L ranges from 0 to u (u + 1 choices), and R ranges from v to n-1 (n - v choices).
    # So the rectangle of forbidden (L, R) for pair i is [0, u_i] x [v_i, n-1].
    # ALL rectangles start at L = 0 and end at L = u_i!
    # This is a set of rectangles all starting at x = 0!
    # Rectangle i covers L in [0, u_i] and R in [v_i, n-1].
    # This means as L goes from 0 to N-1:
    # At L = 0, ALL rectangles whose u_i >= 0 are active.
    # As L increases, rectangles whose u_i < L become INACTIVE.
    # This is even simpler! Rectangles only DEPART as L increases!
    # Initially (at L = 0), all rectangles with u_i >= 0 are active.
    # As L goes from 0 to N-1, at each L, some rectangles expire (u_i == L - 1).
    # We want to find, for each rectangle, its exclusive area.
    # The exclusive area of rectangle i is the sum over L from 0 to u_i of the length of R-interval where IT IS THE ONLY ACTIVE RECTANGLE.

    # Let's use a Segment Tree over R (from 0 to N-1).
    # Initially at L = 0, all rectangles are active.
    # We insert all rectangles into the segment tree. Each rectangle i covers R in [v_i, n-1].
    # So we do range add (+1) on [v_i, n-1] for all i.
    # After setting up the segment tree at L = 0:
    # We can query the total exclusive length for all rectangles currently active!
    # Wait, how to query exclusive length for each rectangle efficiently?
    # A segment tree node can maintain:
    # - `min_count`: minimum cover count in the subtree.
    # - `count_of_min`: how many leaves have the minimum count.
    # - `exclusive_len`: sum of lengths of leaves where `count == 1`.
    # Wait! If we want the exclusive length FOR EACH RECTANGLE individually, maintaining `exclusive_len[id]` for all M rectangles in the segment tree nodes is too large if M is large.
    # BUT wait! Do we need the exclusive length for *each* rectangle, or can we compute the change when a rectangle is removed?
    # Wait! The total union area is the integral over L of the length of the union of active R-intervals.
    # When we remove rectangle i, the union area changes.
    # Specifically, the decrease in the union area when we remove rectangle i is EXACTLY the exclusive area of rectangle i!
    # Can we compute the union area of all rectangles? Yes.
    # Can we compute the union area of all rectangles EXCEPT i, for all i?
    # That would give us the exact valid subarrays if we remove i.
    # Valid subarrays with removal of i = Total - (Union Area without i).
    # To maximize valid subarrays, we want to MINIMIZE (Union Area without i).
    # Union Area without i = Total Union Area - Exclusive Area of i.
    # Minimizing Union Area without i <=> Maximizing Exclusive Area of i!
    # So it all comes down to finding the Exclusive Area of each rectangle i.

    # If M is up to 200,000, can we compute exclusive area efficiently?
    # Notice that a point (l, r) is exclusively covered by i if it's covered by i and nobody else.
    # This means for a fixed l, the r-intervals where rectangle i is the *only* active rectangle
    # can be found by looking at the active intervals of R.
    # Since active R-intervals are all of the form [v_i, n-1] (they all extend to the right endpoint n-1!),
    # this is a very special set of intervals: they ALL share the right endpoint n-1!
    # Let's order the active rectangles by v_i!
    # Since all active rectangles cover up to n-1, their R-intervals are nested or overlap in a suffix!
    # Specifically, an active rectangle i covers [v_i, n-1].
    # If we sort active rectangles by v_i ascending:
    # v_1 <= v_2 <= ... <= v_k.
    # Then their R-intervals are:
    # Rect 1: [v_1, n-1]
    # Rect 2: [v_2, n-1]
    # ...
    # Rect k: [v_k, n-1]
    # Look at this structure!
    # The points covered by ONLY Rect 1 are r in [v_1, v_2 - 1] (if v_1 < v_2).
    # The points covered by ONLY Rect 2? Wait, Rect 2 covers [v_2, n-1]. But Rect 1 also covers [v_1, n-1], which includes [v_2, n-1] since v_1 <= v_2!
    # Therefore, Rect 2 is ALWAYS covered by Rect 1 (because v_1 <= v_2 => [v_2, n-1] is a subset of [v_1, n-1])!
    # THAT IS AN AMAZING PROPERTY!
    # Let's re-verify:
    # Every active rectangle has R-interval [v_i, n-1].
    # If we sort active rectangles by v_i ascending:
    # v_1 <= v_2 <= ... <= v_k.
    # Then [v_i, n-1] contains [v_{i+1}, n-1] for all i < k!
    # This means rectangle i + 1 is FULLY contained within rectangle i in terms of its R-interval!
    # Thus, rectangle i + 1 is covered by rectangle i (and all rectangles 1..i-1 that also cover it).
    # Therefore, for ANY rectangle i > 1 (in sorted order of v), it is covered by rectangle 1!
    # In fact, rectangle 1 covers [v_1, n-1], which is the LARGEST R-interval among all active rectangles!
    # Thus, ANY point covered by rectangle i > 1 is ALSO covered by rectangle 1!
    # Therefore, NO rectangle i > 1 can EVER have any exclusively covered points!
    # BECAUSE rectangle 1 covers everything that rectangle i covers, plus more (since v_1 <= v_i)!
    # WOW. Let's double check this:
    # Does rectangle 1 cover everything that rectangle i covers?
    # For a fixed l:
    # Active rectangles have ranges [v_j, n-1] for l <= u_j.
    # Sort active rectangles by v ascending: v_1 <= v_2 <= ... <= v_k.
    # Then R-interval of 1 is [v_1, n-1].
    # R-interval of 2 is [v_2, n-1]. Since v_1 <= v_2, [v_2, n-1] is inside [v_1, n-1].
    # Thus, 2 is a subset of 1.
    # Therefore, any point (l, r) covered by 2 is ALSO covered by 1.
    # Thus, 2 has ZERO exclusively covered points!
    # In fact, the ONLY rectangle that can possibly have exclusively covered points is the one with the SMALLEST v_i among all active rectangles!
    # Wait! Is that true for a fixed l?
    # At a fixed l, among all active rectangles, let the one with the minimum v be $min\_v$.
    # Its interval is [$min\_v$, n-1].
    # The points in [$min\_v$, second\_min\_v - 1] are covered ONLY by the rectangle with $min\_v$!
    # All points >= second_min_v are covered by at least two rectangles (the one with $min\_v$ and the one with $second\_min\_v$).
    # Hence, at any fixed l, the ONLY points that have coverage count == 1 are in the range [$min\_v$, $second\_min\_v - 1$] (exclusive of second_min_v),
    # and they are exclusively covered by the rectangle with the minimum v!
    # That means at any step l, at most ONE rectangle has any exclusive points, and it's the one with the smallest v among active rectangles!
    # Its exclusive length at this l is simply:
    # (second_min_v - min_v) (if there is a second min v, else (n - min_v)).
    # This is incredible! The structure is immensely simplified!

    # Let's summarize for a fixed l:
    # Active rectangles are those with u_i >= l.
    # Let their v values be $V_{active}$.
    # If $V_{active}$ is empty, exclusive lengths are 0.
    # If $V_{active}$ has elements, sort them: $v_{(1)} \le v_{(2)} \le \dots \le v_{(k)}$.
    # The rectangle corresponding to $v_{(1)}$ gets exclusive length:
    # - $v_{(2)} - v_{(1)}$ if $k \ge 2$
    # - $n - v_{(1)}$ if $k = 1$.
    # All other rectangles get 0 exclusive length at this l.

    # Since l goes from 0 to N-1, we can maintain the multiset of active v values as l increases!
    # Initially, at l = 0, all rectangles are active.
    # As l increases from 0 to N-1:
    # Rectangles with u_i == l - 1 are REMOVED from the active set.
    # We can use a data structure that supports:
    # - Adding/Removing elements (v values)
    # - Finding the smallest and second smallest elements efficiently.
    # Python's `sortedcontainers` is standard, but since we might not have external libraries installed beyond standard library,
    # can we use a min-heap or balanced BST?
    # Wait, in standard Python, `heapq` only allows efficient removal of the smallest element.
    # But here, rectangles expire at specific l values (when l = u_i + 1).
    # Since M up to 200,000, we can use a hash map or lazy deletion heap, or a Fenwick tree / Segment tree over v (since v ranges from 0 to N-1)!
    # Since v ranges from 0 to N-1, we can use a Segment Tree over v (size N) that maintains:
    # - presence of v (count of active rectangles having this v)
    # - to find the 1st and 2nd smallest active v, a segment tree over v can easily find the 1st and 2nd non-zero indices!
    # A segment tree over v of size N:
    # Each leaf at index v stores the count of active rectangles with this v.
    # Segment tree nodes can store the number of active rectangles in their subtree.
    # Finding the 1st and 2nd non-zero indices takes $O(\log N)$ time!
    # And when a rectangle expires at l, we decrement the count at its v in the segment tree ($O(\log N)$).

    # Let's trace the algorithm:
    # 1. Group rectangles by u_i.
    #    `rects_ending_at[u]` = list of v's for rectangles with `u_i = u`.
    #    Wait, rectangles are active for `l <= u_i`. So they expire when `l` becomes `u_i + 1`.
    #    Let's collect all v's for rectangles with `u_i >= l` at l = 0.
    #    So at l = 0, we insert all v's into the segment tree.
    #    As l goes from 0 to N-1:
    #    - Before processing l, we remove all rectangles that have `u_i == l - 1`. (At l=0, none are removed).
    #    - Then, query the segment tree to find the smallest active v (`v1`) and second smallest active v (`v2`).
    #      - If no active v, exclusive length contribution for this l is 0.
    #      - If 1 distinct v value exists (even if multiple rectangles share it? Wait!
    #        If multiple rectangles share the *same* v, say two rectangles have (u, v),
    #        then at r = v, BOTH cover it, so count is >= 2, so neither is exclusive!
    #        Wait! If two rectangles have the exact same (u, v), or same v while u >= l,
    #        then for r = v, both cover it, so count is 2 (or more), meaning NO rectangle has exclusive coverage at r = v!
    #        Let's check: if there are multiple rectangles with the *minimum* v, then at r = v, count >= 2, so the exclusive length starting at v is 0!
    #        Let's refine:
    #        If the minimum v has a count >= 2 in the active set, then at r = min_v, count >= 2, so exclusive length starting at min_v is 0!
    #        In general, the exclusive points exist only if the minimum v has count == 1!
    #        If count of min_v is 1, then the unique rectangle with this min_v gets exclusive length:
    #        - up to the next active v (whether it has count 1 or more).
    #        Let's check: if min_v has count 1, its R-range is [min_v, n-1].
    #        The next active v is `next_v` (which could be larger than min_v, with any count).
    #        For r in [min_v, next_v - 1], the only active rectangle covering these r is the one with min_v!
    #        Why? Because any other active rectangle has v' >= next_v > r, so they do NOT cover r!
    #        Thus, all points r in [min_v, next_v - 1] are covered ONLY by the rectangle with min_v!
    #        So the exclusive length is indeed `next_v - min_v` (if next_v exists) or `n - min_v` (if no next_v, i.e., only one active v with count 1).
    #        What if min_v has count >= 2? Then at r = min_v, at least 2 rectangles cover it, so exclusive length starting at min_v is 0!
    #        This is so clean!
    #        So for each l:
    #        - Find the smallest active v, let's call it `v1`, and its multiplicity (count of rectangles with `v1`).
    #        - Find the next active v (strictly greater than `v1`), let's call it `v2` (if exists).
    #        - If count of `v1` == 1:
    #          - The unique rectangle with this `v1` and current `l` gets an exclusive length increment of:
    #            (`v2` - `v1`) if `v2` exists else (`n` - `v1`).
    #          - Which specific rectangle is this? We need to know its original index `id`!
    #          - Ah, we need to map v to its original rectangle ID(s).
    #            Since multiple rectangles can have the same (u, v), we can store a list of IDs for each (u, v) or keep track of them.
    #            Wait, if multiple rectangles have the *exact same* (u, v), can one be exclusive?
    #            If two rectangles have the exact same u and v, they have the exact same forbidden region.
    #            Then neither can ever be exclusive because any point covered by one is covered by the other!
    #            So any rectangle that shares its (u, v) with another rectangle will have 0 exclusive area.
    #            We can easily pre-group or identify unique pairs.

    # Let's double check if we can implement a Segment Tree over v (0 to N-1) supporting:
    # - point add/subtract of count
    # - finding 1st non-zero and 2nd non-zero with their counts and which rectangle ID they correspond to.
    # Since N <= 200,000, a Segment tree of size N is very efficient.

    # Let's write out the Segment Tree operations:
    # Leaf at index v stores:
    # - `count`: number of active rectangles with this v.
    # - `ids`: list of rectangle IDs that have this v (and are currently active).
    # Since we need to know the ID when count == 1, storing the list of IDs at each leaf is sufficient.
    # When count == 1, `ids[0]` is the unique rectangle ID.
    # When count > 1, we don't even need the ID because exclusive length will be 0 (since count >= 2).
    # Wait, what if count == 1, we need the ID. If count > 1, we don't.
    # So each leaf can maintain:
    # - `count`
    # - `id` (the single ID if count == 1, or -1 if count != 1).

    # Let's structure the Segment Tree:
    # Size: N.
    # Node attributes:
    # - `left_active_v`: the smallest active v in this subtree (or -1).
    # - `left_active_count`: count at that smallest active v.
    # - `left_active_id`: id at that smallest active v.
    # - `second_active_v`: the second smallest active v in this subtree (or -1).
    # Wait, merging two children (left and right):
    # - The smallest active v of the parent is min(left.min_v, right.min_v).
    # - If left.min_v < right.min_v:
    #   - parent.min_v = left.min_v
    #   - parent.count = left.count
    #   - parent.id = left.id
    #   - parent.second_v = min(left.second_v, right.min_v)
    # - If left.min_v > right.min_v:
    #   - parent.min_v = right.min_v
    #   - parent.count = right.count
    #   - parent.id = right.id
    #   - parent.second_v = min(right.second_v, left.min_v)
    # - If left.min_v == right.min_v (can only happen if they are the same leaf, which doesn't happen between left/right children since ranges are disjoint):
    # Wait, left and right children cover disjoint ranges of v, so their min_v are from disjoint intervals!
    # Thus left.min_v and right.min_v are ALWAYS distinct (unless one is -1).
    # So merging is extremely clean:
    # Let `get_min(node)` return `(min_v, count, id, second_v)` for the subtree.
    # When combining `L` and `R`:
    # v1_L, c1_L, id_L, v2_L = L.min_info
    # v1_R, c1_R, id_R, v2_R = R.min_info
    # We want to find the top 2 minimum active v's between the two children.
    # Candidates for 1st min: `v1_L` (if valid) and `v1_R` (if valid).
    # The absolute minimum is `min(v1_L, v1_R)` (ignoring -1).
    # Suppose `v1_L < v1_R`:
    #   - 1st min is `v1_L`, count `c1_L`, id `id_L`.
    #   - 2nd min is `min(v2_L, v1_R)`.
    # Suppose `v1_R < v1_L`:
    #   - 1st min is `v1_R`, count `c1_R`, id `id_R`.
    #   - 2nd min is `min(v2_R, v1_L)`.
    # This segment tree is super simple and powerful! It allows us to query the 1st and 2nd smallest active v's in O(1) from the root!

    class SegTree:

        def __init__(self, size):
            self.n = size
            # Each node stores: (v1, count1, id1, v2)
            # v1: smallest active v, count1: its count, id1: its id (if count1==1 else -1), v2: second smallest active v
            self.tree = [(-1, 0, -1, -1)] * (4 * size)

        def _merge(self, left, right):
            v1_l, c1_l, id_l, v2_l = left
            v1_r, c1_r, id_r, v2_r = right

            if v1_l == -1:
                return right
            if v1_r == -1:
                return left

            if v1_l < v1_r:
                # 1st is v1_l
                cand_v2 = v2_l if v2_l != -1 else v1_r
                if v1_r < cand_v2:
                    cand_v2 = v1_r
                return (v1_l, c1_l, id_l, cand_v2)
            else:
                # 1st is v1_r
                cand_v2 = v2_r if v2_r != -1 else v1_l
                if v1_l < cand_v2:
                    cand_v2 = v1_l
                return (v1_r, c1_r, id_r, cand_v2)

        def update(self, node, l, r, idx, delta, rect_id):
            if l == r:
                v1, c1, id1, v2 = self.tree[node]
                new_c = c1 + delta
                if new_c == 0:
                    self.tree[node] = (-1, 0, -1, -1)
                elif new_c == 1:
                    if delta > 0:
                        self.tree[node] = (l, 1, rect_id, -1)
                    else:
                        # If delta < 1 and new_c == 1, but we didn't track other IDs... wait!
                        # Can a leaf have multiple distinct rectangle IDs?
                        # YES! Multiple rectangles can have the SAME (u, v).
                        # If multiple rectangles have the same v, when one is removed, count drops from 2 to 1.
                        # Which rectangle ID is left? We need to maintain a list/set of active IDs at each leaf!
                        pass
                else:
                    self.tree[node] = (l, new_c, -1, -1)
                return

            mid = (l + r) // 2
            if idx <= mid:
                self.update(2 * node, l, mid, idx, delta, rect_id)
            else:
                self.update(2 * node + 1, mid + 1, r, idx, delta, rect_id)
            self.tree[node] = self._merge(
                self.tree[2 * node], self.tree[2 * node + 1]
            )

    # To handle multiple rectangle IDs at the same leaf v, instead of simple count,
    # at each leaf we can store a Python list of active `rect_id`s that have this `v`.
    # Since total number of rectangles M <= 200,000, total updates is 2 * M.
    # Let's implement leaf storage as a list of IDs at each leaf in an array `leaf_ids[v] = list()`.
    leaf_ids = [[] for _ in range(n)]
    tree_v1 = [-1] * (4 * n)
    tree_c1 = [0] * (4 * n)
    tree_id1 = [-1] * (4 * n)
    tree_v2 = [-1] * (4 * n)

    def merge_info(
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

    def update_leaf(node, l, r, idx, rect_id, is_add):
        if l == r:
            if is_add:
                leaf_ids[idx].append(rect_id)
            else:
                leaf_ids[idx].remove(rect_id)

            c = len(leaf_ids[idx])
            if c == 0:
                tree_v1[node] = -1
                tree_c1[node] = 0
                tree_id1[node] = -1
                tree_v2[node] = -1
            elif c == 1:
                tree_v1[node] = l
                tree_c1[node] = 1
                tree_id1[node] = leaf_ids[idx][0]
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

    # Group rectangles by u_i
    # Rectangles start being active at l = 0 and expire when l = u_i + 1.
    events_add = [[] for _ in range(n)]
    events_remove = [[] for _ in range(n)]

    for i, (u, v) in enumerate(pairs):
        # active for l in [0, u]
        # so added at l = 0, removed at l = u + 1
        events_add[0].append((v, i))
        if u + 1 < n:
            events_remove[u + 1].append((v, i))

    # Initialize at l = 0: add all rectangles that start at l = 0
    # Wait, all pairs have u >= 0 (since 0-indexed, u in [0, n-1]).
    # So all rectangles are active at l = 0.
    for i, (u, v) in enumerate(pairs):
        update_leaf(1, 0, n - 1, v, i, True)

    exclusive_area = [0] * m

    # Sweep l from 0 to n-1
    for l in range(n):
        # Remove rectangles expiring at this l
        if l > 0:
            for v, i in events_remove[l]:
                update_leaf(1, 0, n - 1, v, i, False)

        # Query the segment tree root (node 1)
        v1 = tree_v1[1]
        c1 = tree_c1[1]
        id1 = tree_id1[1]
        v2 = tree_v2[1]

        if v1 != -1 and c1 == 1 and id1 != -1:
            # The unique rectangle id1 has exclusive coverage at this l
            length = (v2 - v1) if v2 != -1 else (n - v1)
            exclusive_area[id1] += length

    # Base valid subarrays = Total - Union Area
    # Total Union Area can be computed or we can use the fact that:
    # Total Union Area = Total Subarrays - Base Valid.
    # Wait, what is Total Union Area?
    # Each point (l, r) is in the union if it's covered by at least one rectangle.
    # The number of points in the union equals Total Subarrays - Base Valid Subarrays.
    # Also, Total Union Area = Sum over all l of (length of union of R-intervals at l).
    # For a fixed l, the union of R-intervals of active rectangles:
    # Since active rectangles have R-intervals [v_i, n-1], their union is simply [min_active_v, n-1]!
    # WOW! Because every active rectangle extends to n-1, their union is just from the MINIMUM active v up to n-1!
    # So for a given l, the number of invalid subarrays (union length) is (n - min_active_v) (if there are active rectangles).
    # This means the total invalid subarrays (Union Area) is simply the sum over l of (n - min_active_v) for all l where active rectangles exist!
    # Let's verify this:
    # Union of [v_i, n-1] for all active i is [min(v_i), n-1].
    # The number of such pairs (l, r) for this l is n - min(v_i).
    # So Total Invalid Subarrays = sum over l=0..n-1 of (n - min_active_v_at_l) (when active set is non-empty).
    # We can get min_active_v at each l directly from `tree_v1[1]`!
    # So Base Invalid Subarrays = sum over l of (n - tree_v1[1]) when tree_v1[1] != -1.
    # Base Valid Subarrays = total_subarrays - Base Invalid Subarrays.

    # Let's re-run or calculate Base Invalid Subarrays during the sweep-line!
    # We can do the sweep line and sum up invalid subarrays, AND compute exclusive areas at the same time!

    # Let's re-initialize tree and events for the sweep-line:
    leaf_ids = [[] for _ in range(n)]
    tree_v1 = [-1] * (4 * n)
    tree_c1 = [0] * (4 * n)
    tree_id1 = [-1] * (4 * n)
    tree_v2 = [-1] * (4 * n)

    for i, (u, v) in enumerate(pairs):
        update_leaf(1, 0, n - 1, v, i, True)

    base_invalid = 0
    exclusive_area = [0] * m

    for l in range(n):
        if l > 0:
            for v, i in events_remove[l]:
                update_leaf(1, 0, n - 1, v, i, False)

        v1 = tree_v1[1]
        if v1 != -1:
            # Union length at this l
            base_invalid += n - v1

            c1 = tree_c1[1]
            id1 = tree_id1[1]
            v2 = tree_v2[1]
            if c1 == 1 and id1 != -1:
                length = (v2 - v1) if v2 != -1 else (n - v1)
                exclusive_area[id1] += length

    base_valid = total_subarrays - base_invalid

    # If we remove the best pair i, the valid subarrays become base_valid + exclusive_area[i].
    # If we remove nothing, it's base_valid + 0.
    max_exclusive = max(exclusive_area) if exclusive_area else 0
    ans = base_valid + max_exclusive

    print(ans)


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
