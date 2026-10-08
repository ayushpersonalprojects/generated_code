from typing import List, Tuple


class Solution:

    def maxFreePeriod(
        self, event_interval: Tuple[int, int], meetings: List[Tuple[int, int]]
    ) -> int:
        E_start, E_end = event_interval

        # If there are no meetings, the entire interval is free
        if not meetings:
            return E_end - E_start

        # Filter and clip meetings to the event interval
        valid_meetings = []
        for m_start, m_end in meetings:
            s = max(E_start, m_start)
            e = min(E_end, m_end)
            if s < e:
                valid_meetings.append((s, e))

        if not valid_meetings:
            return E_end - E_start

        # Sort meetings by start time, then end time
        valid_meetings.sort(key=lambda x: (x[0], x[1]))

        # Merge overlapping meetings for baseline free period calculation
        merged = []
        for m in valid_meetings:
            if not merged or merged[-1][1] < m[0]:
                merged.append(list(m))
            else:
                merged[-1][1] = max(merged[-1][1], m[1])

        # Find the maximum free period without moving any meeting
        def get_max_gap(m_list, start, end):
            max_g = 0
            curr = start
            for m_s, m_e in m_list:
                if m_s > curr:
                    max_g = max(max_g, m_s - curr)
                curr = max(curr, m_e)
            if end > curr:
                max_g = max(max_g, end - curr)
            return max_g

        best_free = get_max_gap(merged, E_start, E_end)

        # Now consider removing each meeting and placing its duration elsewhere.
        n = len(valid_meetings)
        for i in range(n):
            # Remove meeting i
            sub_meetings = valid_meetings[:i] + valid_meetings[i + 1 :]

            # If sub_meetings is empty, the whole interval is free
            if not sub_meetings:
                best_free = max(best_free, E_end - E_start)
                continue

            # Merge sub_meetings to find gaps
            sub_merged = []
            for m in sub_meetings:
                if not sub_merged or sub_merged[-1][1] < m[0]:
                    sub_merged.append(list(m))
                else:
                    sub_merged[-1][1] = max(sub_merged[-1][1], m[1])

            g = get_max_gap(sub_merged, E_start, E_end)
            best_free = max(best_free, g)

        return best_free


def max_free_period(
    event_interval: Tuple[int, int], meetings: List[Tuple[int, int]]
) -> int:
    sol = Solution()
    return sol.maxFreePeriod(event_interval, meetings)

# --- DYNAMIC AUTOMATED TEST HARNESS ---
if __name__ == '__main__':
    import inspect
    sol = Solution()
    # Find the user's defined method on Solution (skipping dunder methods)
    methods = [m for m in dir(sol) if not m.startswith('_') and callable(getattr(sol, m))]
    if not methods:
        raise AttributeError("No solution method found in class Solution")
    target_method = getattr(sol, methods[0])

    assert target_method(eventTime=10, startTime=[1, 3, 7], endTime=[2, 4, 8]) == 3
    assert target_method(eventTime=5, startTime=[1], endTime=[2]) == 4
