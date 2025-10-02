```python
from typing import List

def replace_triple_sevens(row: List[int]) -> List[int]:
    """Replace non-overlapping sequences of three 7s with [8, 6, 8] in odd rows."""
    if len(row) < 3:
        return row[:]
    new_row = row[:]
    i = 0
    while i < len(new_row) - 2:
        if new_row[i:i+3] == [7, 7, 7]:
            new_row[i:i+3] = [8, 6, 8]
            i += 3
        else:
            i += 1
    return new_row

def initialize_even_row_base(input_row: List[int]) -> List[int]:
    """Set 8 for non-zero positions, 0 for zeros in even rows."""
    return [8 if val != 0 else 0 for val in input_row]

def overlay_sixes_from_adjacents(g: List[List[int]], out: List[List[int]], row_index: int, num_rows: int, n: int, base_row: List[int]) -> List[int]:
    """Overlay 6 in even row positions where upper or lower row has 6."""
    new_row = base_row[:]
    has_upper = row_index > 0
    has_lower = row_index < num_rows - 1
    for col in range(n):
        overlay = False
        if has_upper and out[row_index - 1][col] == 6:
            overlay = True
        if has_lower and out[row_index + 1][col] == 6:
            overlay = True
        if overlay:
            new_row[col] = 6
    return new_row

def cap_segment_edges_with_three_if_upper_has_six(temp_row: List[int], upper_row: List[int], row_index: int, n: int, is_bottom: bool) -> List[int]:
    """Set 3 at non-zero segment edges adjacent to 0 if segment has upper 6, without overriding 6; skip right for bottom."""
    new_row = temp_row[:]
    has_upper = row_index > 0
    i = 0
    while i < n:
        if new_row[i] == 0:
            i += 1
            continue
        start = i
        while i < n and new_row[i] != 0:
            i += 1
        end = i - 1
        segment_has_upper_six = False
        if has_upper:
            for k in range(start, end + 1):
                if upper_row[k] == 6:
                    segment_has_upper_six = True
                    break
        # Left edge cap
        if start > 0 and new_row[start - 1] == 0 and segment_has_upper_six and new_row[start] != 6:
            new_row[start] = 3
        # Right edge cap
        if not is_bottom and end < n - 1 and new_row[end + 1] == 0 and segment_has_upper_six and new_row[end] != 6:
            new_row[end] = 3
    return new_row

def set_left_border_three(g: List[List[int]], out: List[List[int]], temp_row: List[int], row_index: int, n: int, num_rows: int) -> List[int]:
    """Set left border (col 0) to 3 based on upper 6 proximity in left segment or input 3, force 8 for top, avoid overriding 6."""
    new_row = temp_row[:]
    is_top = row_index == 0
    is_bottom = row_index == num_rows - 1
    has_upper = row_index > 0
    if new_row[0] == 0 or (not is_top and new_row[0] == 6):
        return new_row
    # Find left segment end
    left_end = 0
    while left_end < n - 1 and new_row[left_end + 1] != 0:
        left_end += 1
    left_has_such = False
    left_min_k = float('inf')
    if has_upper:
        for k in range(left_end + 1):
            if out[row_index - 1][k] == 6:
                left_has_such = True
                left_min_k = min(left_min_k, k)
    input_left_three = g[row_index][0] == 3
    if is_top:
        if new_row[0] != 6:
            new_row[0] = 8
    elif left_has_such and (is_bottom or left_min_k <= 5) and new_row[0] != 6:
        new_row[0] = 3
    elif not left_has_such and input_left_three and new_row[0] != 6:
        new_row[0] = 3
    elif new_row[0] != 6:
        new_row[0] = 8
    return new_row

def set_right_border_three(g: List[List[int]], out: List[List[int]], temp_row: List[int], row_index: int, n: int, num_rows: int) -> List[int]:
    """Set right border (col n-1) to 3 based on upper 6 proximity in right segment or input 3, force 8 for top, avoid overriding 6."""
    new_row = temp_row[:]
    is_top = row_index == 0
    is_bottom = row_index == num_rows - 1
    has_upper = row_index > 0
    if new_row[n - 1] == 0 or (not is_top and new_row[n - 1] == 6):
        return new_row
    # Find right segment start
    right_start = n - 1
    while right_start > 0 and new_row[right_start - 1] != 0:
        right_start -= 1
    right_has_such = False
    right_max_k = -1
    if has_upper:
        for k in range(n - 1, right_start - 1, -1):
            if out[row_index - 1][k] == 6:
                right_max_k = k
                right_has_such = True
                break
    input_right_three = g[row_index][n - 1] == 3
    dist = n - 1 - right_max_k if right_max_k != -1 else float('inf')
    if is_top:
        if new_row[n - 1] != 6:
            new_row[n - 1] = 8
    elif right_has_such and (is_bottom or dist <= 5) and new_row[n - 1] != 6:
        new_row[n - 1] = 3
    elif not right_has_such and input_right_three and new_row[n - 1] != 6:
        new_row[n - 1] = 3
    elif new_row[n - 1] != 6:
        new_row[n - 1] = 8
    return new_row

def extend_threes_inward_at_edges(temp_row: List[int], n: int) -> List[int]:
    """Extend 3 inward by one position if followed by 8 at edges."""
    new_row = temp_row[:]
    if n >= 2 and new_row[0] == 3 and new_row[1] == 8:
        new_row[1] = 3
    if n >= 2 and new_row[n - 1] == 3 and new_row[n - 2] == 8:
        new_row[n - 2] = 3
    return new_row

def program(g: List[List[int]]) -> List[List[int]]:
    """Main function to process the grid: odd rows get pattern replacement, even rows get base, overlays, caps, borders, extensions."""
    if not g:
        return []
    num_rows = len(g)
    if num_rows == 0:
        return []
    n = len(g[0])
    out = [row[:] for row in g]
    # Process all odd rows first
    for j in range(1, num_rows, 2):
        out[j] = replace_triple_sevens(out[j])
    # Process even rows top to bottom
    for j in range(0, num_rows, 2):
        is_bottom = (j == num_rows - 1)
        base = initialize_even_row_base(g[j])
        temp = overlay_sixes_from_adjacents(g, out, j, num_rows, n, base)
        upper = out[j - 1] if j > 0 else None
        temp = cap_segment_edges_with_three_if_upper_has_six(temp, upper, j, n, is_bottom)
        temp = set_left_border_three(g, out, temp, j, n, num_rows)
        temp = set_right_border_three(g, out, temp, j, n, num_rows)
        has_zero = 0 in temp
        if not is_bottom and not has_zero and n >= 2:
            temp = extend_threes_inward_at_edges(temp, n)
        out[j] = temp
    return out
```