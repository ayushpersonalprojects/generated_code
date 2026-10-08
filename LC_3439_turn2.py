class Solution:
    def maxFreeTime(self, eventTime: int, k: int, startTime: list[int], endTime: list[int]) -> int:
        return max_free_interval(list(zip(startTime, endTime)), k, eventTime)

def max_free_interval(meetings, k, eventTime=None):
    """
    Given a list of meetings (each as [start, end]) representing intervals within a day,
    reschedule at most k meetings while preserving their durations and order to maximize 
    one continuous free interval.
    """
    if not meetings:
        return eventTime if eventTime is not None else 0

    if eventTime is None:
        eventTime = meetings[-1][1]

    n = len(meetings)
    durations = [m[1] - m[0] for m in meetings]

    if k >= n:
        return eventTime - sum(durations)

    pref = [0] * (n + 1)
    for idx in range(n):
        pref[idx + 1] = pref[idx] + durations[idx]

    def get_sum(l, r):
        if l > r:
            return 0
        return pref[r + 1] - pref[l]

    m = n - k  # size of the kept block
    max_free = 0

    for i in range(n - m + 1):
        j = i + m - 1
        orig_span = meetings[j][1] - meetings[i][0]
        total_resched = get_sum(0, i - 1) + get_sum(j + 1, n - 1)

        # Case 1: Pack all k rescheduled meetings at the beginning of the day (day_start = 0).
        # Free interval is after the shifted kept block.
        free_after = eventTime - (total_resched + orig_span)
        max_free = max(max_free, free_after)

        # Case 2: Pack all k rescheduled meetings at the end of the day (up to eventTime).
        # Free interval is before the shifted kept block.
        free_before = (eventTime - total_resched - orig_span)
        max_free = max(max_free, free_before)

    return max(0, max_free)

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
