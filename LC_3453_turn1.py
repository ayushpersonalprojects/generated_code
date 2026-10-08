from typing import List, Tuple

def find_equal_area_horizontal_line(squares: List[Tuple[float, float, float]]) -> float:
    """
    Given a list of axis-aligned squares, represented as (x, y, s) where (x, y) 
    is the bottom-left corner and s is the side length, find the y-coordinate 
    of a horizontal line that divides the total area of the squares into two equal halves.
    """
    if not squares:
        return 0.0

    # Calculate total area
    total_area = sum(s * s for x, y, s in squares)
    target_area = total_area / 2.0

    # Collect all unique y-coordinates (bottoms and tops of squares)
    events = set()
    for x, y, s in squares:
        events.add(y)
        events.add(y + s)
    
    y_coords = sorted(list(events))

    # If there's only one unique y-coordinate (e.g., degenerate case)
    if len(y_coords) <= 1:
        return y_coords[0] if y_coords else 0.0

    # We will sweep from bottom to top and track the accumulated area
    current_area = 0.0
    
    for i in range(len(y_coords) - 1):
        y_low = y_coords[i]
        y_high = y_coords[i+1]
        height = y_high - y_low
        
        if height == 0:
            continue

        # Calculate the total width of all squares active in this interval [y_low, y_high]
        # A square is active in this interval if its bottom <= y_low and its top >= y_high
        active_width = 0.0
        for x, y, s in squares:
            if y <= y_low and (y + s) >= y_high:
                active_width += s

        interval_area = active_width * height

        # Check if the target area is reached within this strip
        if current_area + interval_area >= target_area:
            # It falls within this strip, interpolate to find exact y
            needed_area = target_area - current_area
            if active_width == 0:
                return y_low
            return y_low + (needed_area / active_width)

        current_area += interval_area

    return y_coords[-1]

if __name__ == "__main__":
    # Example usage:
    # Two squares:
    # 1. bottom-left (0, 0), side 2 -> Area = 4 (covers y: 0 to 2)
    # 2. bottom-left (2, 0), side 2 -> Area = 4 (covers y: 0 to 2)
    # Total Area = 8, Target Area = 4.
    # For y from 0 to 2, total width = 2 + 2 = 4. Area per unit height = 4.
    # To get area 4, height = 4 / 4 = 1. So y = 1.
    squares = [(0, 0, 2), (2, 0, 2)]
    print(f"Dividing line y = {find_equal_area_horizontal_line(squares)}")

# --- DYNAMIC AUTOMATED TEST HARNESS ---
if __name__ == '__main__':
    import inspect
    sol = Solution()
    # Find the user's defined method on Solution (skipping dunder methods)
    methods = [m for m in dir(sol) if not m.startswith('_') and callable(getattr(sol, m))]
    if not methods:
        raise AttributeError("No solution method found in class Solution")
    target_method = getattr(sol, methods[0])

    assert target_method(squares=[[0, 0, 2], [1, 1, 2]]) == 1.5
    assert target_method(squares=[[0, 0, 1]]) == 0.5
