class Solution:
    def maxFreeTime(self, eventTime: int, k: int, startTime: list[int], endTime: list[int]) -> int:
        meetings = list(zip(startTime, endTime))
        n = len(meetings)
        
        # We want to find a window of size (n - k) meetings that we KEEP fixed.
        # Wait, if we keep a window of size `m = n - k` meetings fixed, the free intervals
        # between them are also fixed. But wait, can we move the kept meetings?
        # The problem states: "reschedule at most k meetings while preserving their durations and order".
        # This means we choose any $n - k$ meetings to keep in their original relative positions 
        # (or rather, their exact original positions as a block), and the other $k$ meetings can be 
        # removed and placed anywhere else.
        # Actually, a simpler way to view the free intervals between meetings:
        # We have `n + 1` free intervals between the `n` meetings (including the start and end of the day).
        # If we keep any block of `n - k` meetings fixed, we can merge all the free intervals 
        # surrounding the removed $k$ meetings plus the boundaries into one large free interval.
        #
        # Let's list the free intervals:
        # f_0 = meetings[0][0] - 0
        # f_1 = meetings[1][0] - meetings[0][1]
        # ...
        # f_n = eventTime - meetings[n-1][1]
        #
        # There are n + 1 free intervals in total: index 0 to n.
        # If we keep a contiguous block of meetings from index `i` to `j` (where length is `m = n - k`),
        # the meetings kept are `meetings[i ... j]`.
        # The free intervals that are swallowed/combined by moving the meetings outside `[i, j]` 
        # are all the free intervals that were adjacent to the moved meetings.
        # Specifically, if we keep meetings `i` through `j` (inclusive), the meetings before `i` (0 to i-1) 
        # and after `j` (j+1 to n-1) are rescheduled.
        # When we reschedule them, we can pack them together, effectively combining the free intervals 
        # that were spanned by them.
        # 
        # More precisely, the free intervals involved when keeping block `i` to `j`:
        # The kept block spans from `meetings[i][0]` to `meetings[j][1]`.
        # The free intervals strictly *inside* the kept block (between meetings `i` and `j`) are preserved.
        # The free interval *before* the kept block can be merged with the free intervals of all the 
        # rescheduled meetings before `i`, AND we can also push the kept block all the way to the left 
        # (or right) to combine everything into one massive free interval!
        #
        # Let's formalize using free intervals:
        # Free intervals:
        gaps = [0] * (n + 1)
        gaps[0] = meetings[0][0]
        for idx in range(1, n):
            gaps[idx] = meetings[idx][0] - meetings[idx-1][1]
        gaps[n] = eventTime - meetings[n-1][1]

        # If we can reschedule k meetings, we can choose any window of k+1 consecutive free intervals 
        # and merge them together along with the durations of the k meetings between them!
        # Wait! Is it always choosing a window of length `k + 1` in the `gaps` array?
        # Let's check: if we fix a block of meetings, say we keep meetings `i` to `j`. 
        # The number of kept meetings is `m = j - i + 1`. The number of rescheduled meetings is `n - m = n - (j - i + 1)`.
        # We need this to be at most `k`, so `n - j + i - 1 <= k` => `j - i + 1 >= n - k`.
        # The free intervals that get combined are all the gaps surrounding the rescheduled meetings.
        # Actually, if we keep meetings `i` through `j`, the gaps *inside* the kept block are `gaps[i+1 ... j]`.
        # The gaps outside are `gaps[0 ... i]` and `gaps[j+1 ... n]`.
        # Can we combine all gaps outside `[i+1, j]`? 
        # Plus, we can add the durations of all the meetings that were removed!
        # Wait, the sum of gaps and meeting durations in the removed section:
        # If we remove meetings from 0 to `i-1` and `j+1` to `n-1`, 
        # the total free space we can create by packing them is:
        # (sum of gaps 0 to i) + (sum of durations of meetings 0 to i-1) + ... wait, 
        # simpler: the total available time in those regions minus the meeting durations.
        # But even simpler: 
        # Any contiguous group of $k$ meetings can be removed. Removing a meeting of duration $d$ 
        # adds $d$ to the adjacent free space.
        # If we choose to keep a block of meetings from index `i` to `j`, the number of removed meetings is `k' = n - (j - i + 1)`.
        # Since we can choose any $j - i + 1 \ge n - k$, the maximum number of meetings we can remove is $k$.
        # Thus, we can choose any window of $k$ consecutive meetings to remove, OR more generally, 
        # any block of kept meetings of size $m = n - k$ (or larger, up to $n$).
        # Wait, if we keep meetings `i` to `j`, the free space we get on the left (if we push the kept block to the right) 
        # or on the right (if we push the kept block to the left) is simply:
        # Total free space = (Sum of gaps from 0 to i) + (sum of durations of meetings 0 to i-1) ... wait no.
        
        # Let's use the standard prefix sum approach on gaps and meeting durations.
        # A well-known property for this specific problem (LeetCode 3439 / similar):
        # We can keep any block of `m` meetings where `m = n - k`. 
        # Wait, can `m` be larger than `n - k`? Yes, keeping more meetings is a subset of cases, 
        # but to maximize free space, keeping fewer meetings (i.e. removing $k$ meetings) gives more freedom. 
        # Actually, we can remove *any* $k$ meetings, but since order is preserved, removing $k$ meetings 
        # is equivalent to keeping a contiguous block of $n - k$ meetings (say from index `i` to `i + n - k - 1`), 
        # and shifting the kept block either all the way to the left or all the way to the right!
        
        # Let's re-verify the two shifts for a fixed kept block `i` to `j` (where `j - i + 1 = n - k`):
        # 1. Shift kept block to the left: 
        #    The kept block starts at time `0` (plus any gaps before? No, if we shift it to the left, 
        #    all $k$ rescheduled meetings are packed to the right of the kept block, 
        #    meaning the free interval is at the very end of the day).
        #    Wait! If all rescheduled meetings are packed to the right, then the kept block starts at 0? 
        #    No, the kept block keeps its internal structure (its own meetings and internal gaps), 
        #    so it starts at... wait, if we push everything to the left, the kept block starts at 
        #    the sum of durations of the rescheduled meetings? No! 
        #    If we push the kept block to the *left*, the rescheduled meetings are placed at the *end* of the day 
        #    (or before/after). 
        #    Let's check the two canonical ways to place a kept block `[i, j]` while rescheduling the rest:
        #    - Option A (Pusher left): The kept block starts at `sum of gaps before i`? 
        #      Wait, if we push the kept block as far left as possible, it starts at `0` (if we ignore gaps before i, 
        #      by combining gap 0 through i into the free space). 
        #      Specifically, the free space before the kept block becomes:
        #      `sum of gaps from 0 to i` + `sum of durations of meetings 0 to i-1`? 
        #      No! The space before the kept block is simply all time from 0 up to `meetings[i][0]`, 
        #      minus the durations of meetings that are kept... wait.
        
        # Let's use the interval-gap formulation which is foolproof:
        # Gaps array has length `n + 1`: `gaps[0], gaps[1], ..., gaps[n]`.
        # When we keep a block of meetings from `i` to `j` (inclusive), the meetings kept are `i..j`.
        # The gaps strictly inside the kept block are `gaps[i+1 ... j]`. These CANNOT be touched (they are between kept meetings).
        # The gaps outside are `gaps[0 ... i]` and `gaps[j+1 ... n]`.
        # Since we removed all meetings outside `[i, j]` (which are meetings `0..i-1` and `j+1..n-1`), 
        # all the gaps in `0..i` and all the gaps in `j+1..n` can be merged together!
        # Plus, the durations of all the removed meetings can also be added to this free space!
        # Wait, what is the sum of gaps and meeting durations in the removed sections?
        # Notice that:
        # Sum of gaps `0` to `i` + sum of durations `0` to `i-1` = `meetings[i][0]` ? 
        # Let's check: 
        # gaps[0] = meetings[0][0]
        # gaps[1] = meetings[1][0] - meetings[0][1]
        # ...
        # gaps[i] = meetings[i][0] - meetings[i-1][1]
        # Sum of gaps `0` to `i` = `meetings[i][0] - (durations of 0..i-1)`.
        # Therefore, (Sum of gaps `0` to `i`) + (Sum of durations `0` to `i-1`) = `meetings[i][0]`!
        # That's just the start time of meeting `i`!
        # Similarly, for the right side:
        # Sum of gaps `j+1` to `n` + Sum of durations `j+1` to `n-1` = `eventTime - meetings[j][1]`!
        # 
        # This means if we isolate the left side (everything before meeting `i`), its total available time span is `meetings[i][0]`.
        # If we isolate the right side (everything after meeting `j`), its total available time span is `eventTime - meetings[j][1]`.
        # 
        # Since we can move the rescheduled meetings, we can either:
        # 1. Push all rescheduled meetings to the right side, so the entire left side (`0` to `meetings[i][0]`) becomes ONE massive free interval!
        #    Its size is simply `meetings[i][0]`.
        # 2. Push all rescheduled meetings to the left side, so the entire right side (`meetings[j][1]` to `eventTime`) becomes ONE massive free interval!
        #    Its size is simply `eventTime - meetings[j][1]`.
        # 3. What about combining across the kept block? We can't combine across the kept block into a single interval *unless* 
        #    we also consider the internal gaps of the kept block if we can move them, but the kept block is fixed.
        #    Wait, what about the gaps *inside* the kept block? `gaps[i+1 ... j]`. 
        #    Any gap inside the kept block, i.e., `gaps[x]` for `x` in `i+1 ... j`, is also a valid free interval!
        #    So we should consider:
        #    - `meetings[i][0]` (left side free space if all left-side meetings are rescheduled)
        #    - `eventTime - meetings[j][1]` (right side free space if all right-side meetings are rescheduled)
        #    - Every internal gap `gaps[x]` for `x` from `i+1` to `j`.
        # 
        # Wait, is that it?! 
        # Let's check if we can combine gaps adjacent to the kept block or if `meetings[i][0]` and `eventTime - meetings[j][1]` 
        # already account for the maximum possible free interval by pushing all $k$ meetings to one side.
        # Yes! If we push all $k$ rescheduled meetings to the right, the entire space from `0` to `meetings[i][0]` 
        # is unoccupied by any meeting, hence it's a single continuous free interval of size `meetings[i][0]`.
        # If we push all $k$ rescheduled meetings to the left, the entire space from `meetings[j][1]` to `eventTime` 
        # is unoccupied, hence a single continuous free interval of size `eventTime - meetings[j][1]`.
        # And what if the kept block size is smaller, or we just consider all valid windows of kept meetings 
        # of size `m = n - k`?
        
        m = n - k
        max_free = 0
        
        # Also, don't forget we can just keep zero meetings if k >= n, handled separately:
        if k >= n:
            return eventTime

        # Prefix sums of gaps for internal gaps check
        # gaps has length n + 1
        
        for i in range(n - m + 1):
            j = i + m - 1
            # 1. Left side free interval
            max_free = max(max_free, meetings[i][0])
            
            # 2. Right side free interval
            max_free = max(max_free, eventTime - meetings[j][1])
            
            # 3. Internal gaps within the kept block [i, j]
            # The gaps inside are gaps[i+1 ... j]
            for g_idx in range(i + 1, j + 1):
                max_free = max(max_free, gaps[g_idx])
                
        # Wait, what if k = 0? Then m = n, i = 0, j = n - 1.
        # Then max_free will check meetings[0][0], eventTime - meetings[n-1][1], and all internal gaps gaps[1...n-1].
        # Which correctly covers all original free intervals when k = 0!
        
        return max_free

def max_free_interval(meetings, k, eventTime=None):
    if not meetings:
        return eventTime if eventTime is not None else 0
    if eventTime is None:
        eventTime = meetings[-1][1]
    
    n = len(meetings)
    if k >= n:
        return eventTime
        
    gaps = [0] * (n + 1)
    gaps[0] = meetings[0][0]
    for idx in range(1, n):
        gaps[idx] = meetings[idx][0] - meetings[idx-1][1]
    gaps[n] = eventTime - meetings[n-1][1]
    
    m = n - k
    max_free = 0
    
    for i in range(n - m + 1):
        j = i + m - 1
        max_free = max(max_free, meetings[i][0])
        max_free = max(max_free, eventTime - meetings[j][1])
        for g_idx in range(i + 1, j + 1):
            max_free = max(max_free, gaps[g_idx])
            
    return max_free

# --- DYNAMIC AUTOMATED TEST HARNESS ---
if __name__ == '__main__':
    import inspect
    sol = Solution()
    # Find the user's defined method on Solution (skipping dunder methods)
    methods = [m for m in dir(sol) if not m.startswith('_') and callable(getattr(sol, m))]
    if not methods:
        raise AttributeError("No solution method found in class Solution")
    target_method = getattr(sol, methods[0])

    assert target_method(eventTime=5, k=1, startTime=[1, 3], endTime=[2, 4]) == 2
    assert target_method(eventTime=10, k=1, startTime=[0, 2, 5], endTime=[1, 3, 6]) == 4
