```python
from typing import List

def process_odd_row(row: List[int]) -> List[int]:
    """Replace non-overlapping sequences of [7, 7, 7] with [8, 6, 8] in odd rows."""
    if len(row) < 3:
        return row[:]
    new_row = row[:]
    i = 0
    while i < len(new_row) - 2:
        if new_row[i:i + 3] == [7, 7, 7]:
            new_row[i:i + 3] = [8, 6, 8]
            i += 3
        else:
            i += 1
    return new_row

def initialize_even_row_base(g_row: List[int]) -> List[int]:
    """Initialize even row base: 8 for non-zero input, 0 for zero."""
    return [8 if val != 0 else 0 for val in g_row]

def overlay_six_from_adjacent_rows(g: List[List[int]], out: List[List[int]], j: int, num_rows: int, n: int, base_row: List[int]) -> List[int]:
    """Overlay 6 in even row positions where upper or lower row has 6 in the same column."""
    new_row = base_row[:]
    has_upper = j > 0
    has_lower = j < num_rows - 1
    for k in range(n):
        overlay = False
        if has_upper and out[j - 1][k] == 6:
            overlay = True
        if has_lower and out[j + 1][k] == 6:
            overlay = True
        if overlay:
            new_row[k] = 6
    return new_row

def cap_zero_adjacent_segment_edges(temp: List[int], out: List[List[int]], j: int, n: int, is_bottom: bool) -> List[int]:
    """Cap edges of non-zero segments adjacent to 0s with 3 if segment has upper 6; skip right cap if bottom."""
    new_row = temp[:]
    has_upper = j > 0
    i = 0
    while i < n:
        if new_row[i] == 0:
            i += 1
            continue
        start = i
        while i < n and new_row[i] != 0:
            i += 1
        end = i - 1
        segment_has_upper_6 = False
        if has_upper:
            for k in range(start, end + 1):
                if out[j - 1][k] == 6:
                    segment_has_upper_6 = True
                    break
        if start > 0 and new_row[start - 1] == 0 and segment_has_upper_6:
            new_row[start] = 3
        if not is_bottom and end < n - 1 and new_row[end + 1] == 0 and segment_has_upper_6:
            new_row[end] = 3
    return new_row

def set_left_border(temp: List[int], g_row: List[int], j: int, n: int, num_rows: int, out: List[List[int]]) -> List[int]:
    """Set left border to 3 or 8 based on upper 6 proximity in left segment, input, top/bottom status."""
    new_row = temp[:]
    is_top = j == 0
    is_bottom = j == num_rows - 1
    has_upper = j > 0
    if new_row[0] == 0:
        return new_row
    left_end = 0
    while left_end < n - 1 and new_row[left_end + 1] != 0:
        left_end += 1
    left_has_6 = False
    left_min_k = float('inf')
    if has_upper:
        for k in range(left_end + 1):
            if out[j - 1][k] == 6:
                left_min_k = k
                left_has_6 = True
                break
    input_left_3 = g_row[0] == 3
    if is_top:
        new_row[0] = 8
    elif left_has_6:
        if is_bottom or left_min_k <= 5:
            new_row[0] = 3
        else:
            new_row[0] = 8
    else:
        new_row[0] = 3 if input_left_3 else 8
    return new_row

def set_right_border(temp: List[int], g_row: List[int], j: int, n: int, num_rows: int, out: List[List[int]]) -> List[int]:
    """Set right border to 3 or 8 based on upper 6 proximity in right segment, input, top/bottom status."""
    new_row = temp[:]
    is_top = j == 0
    is_bottom = j == num_rows - 1
    has_upper = j > 0
    if new_row[n - 1] == 0:
        return new_row
    right_start = n - 1
    while right_start > 0 and new_row[right_start - 1] != 0:
        right_start -= 1
    right_has_6 = False
    right_max_k = -1
    if has_upper:
        for kk in range(n - 1, right_start - 1, -1):
            if out[j - 1][kk] == 6:
                right_max_k = kk
                right_has_6 = True
                break
    input_right_3 = g_row[n - 1] == 3
    if is_top:
        new_row[n - 1] = 8
    elif right_has_6:
        dist = n - 1 - right_max_k
        if is_bottom or dist <= 4:
            new_row[n - 1] = 3
        else:
            new_row[n - 1] = 8
    else:
        new_row[n - 1] = 3 if input_right_3 else 8
    return new_row

def extend_border_threes_inward(temp: List[int], n: int, is_bottom: bool) -> List[int]:
    """Extend border 3s inward by one if followed by 8, for non-bottom rows without zeros."""
    new_row = temp[:]
    has_zero = 0 in new_row
    if is_bottom or has_zero or n < 2:
        return new_row
    if new_row[0] == 3 and new_row[1] == 8:
        new_row[1] = 3
    if new_row[n - 1] == 3 and new_row[n - 2] == 8:
        new_row[n - 2] = 3
    return new_row

def program(g: List[List[int]]) -> List[List[int]]:
    """Main program: process odd rows first, then even rows with base, overlay, cap, borders, extend."""
    if not g:
        return []
    num_rows = len(g)
    if num_rows == 0:
        return g
    n = len(g[0])
    out = [row[:] for row in g]
    # Process all odd rows first
    for j in range(1, num_rows, 2):
        out[j] = process_odd_row(out[j])
    # Process even rows top to bottom
    for j in range(0, num_rows, 2):
        is_bottom = (j == num_rows - 1)
        base = initialize_even_row_base(g[j])
        temp = overlay_six_from_adjacent_rows(g, out, j, num_rows, n, base)
        temp = cap_zero_adjacent_segment_edges(temp, out, j, n, is_bottom)
        upper = out[j - 1] if j > 0 else None
        temp = set_left_border(temp, g[j], j, n, num_rows, out)
        temp = set_right_border(temp, g[j], j, n, num_rows, out)
        temp = extend_border_threes_inward(temp, n, is_bottom)
        out[j] = temp
    return out
```