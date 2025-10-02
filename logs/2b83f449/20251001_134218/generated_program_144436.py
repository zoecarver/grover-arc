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

def initialize_even_base(row: List[int]) -> List[int]:
    """Initialize even row base: 8 where input non-zero, 0 where zero."""
    return [8 if x != 0 else 0 for x in row]

def overlay_6(temp: List[int], out: List[List[int]], j: int, n: int) -> List[int]:
    """Overlay 6 in even row where upper or lower adjacent row has 6 in the same column."""
    new_row = temp[:]
    has_upper = j > 0
    has_lower = j < len(out) - 1
    for k in range(n):
        overlay = False
        if has_upper and out[j - 1][k] == 6:
            overlay = True
        if has_lower and out[j + 1][k] == 6:
            overlay = True
        if overlay:
            new_row[k] = 6
    return new_row

def cap_adjacent_zeros(temp: List[int], out: List[List[int]], j: int, n: int, is_bottom: bool) -> List[int]:
    """Cap edges of non-zero segments adjacent to 0s with 3 if segment has upper 6; skip right cap if bottom row."""
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
        segment_has_upper6 = False
        if has_upper:
            for k in range(start, end + 1):
                if out[j - 1][k] == 6:
                    segment_has_upper6 = True
                    break
        if start > 0 and new_row[start - 1] == 0 and segment_has_upper6:
            new_row[start] = 3
        if not is_bottom and end < n - 1 and new_row[end + 1] == 0 and segment_has_upper6:
            new_row[end] = 3
    return new_row

def handle_borders(temp: List[int], input_row: List[int], out: List[List[int]], j: int, n: int, num_rows: int) -> List[int]:
    """Handle left and right borders for even rows: set to 3 or 8 based on upper 6 proximity, input, and top/bottom status."""
    new_row = temp[:]
    is_top = (j == 0)
    is_bottom = (j == num_rows - 1)
    has_upper = j > 0
    # Left border
    if new_row[0] != 0:
        left_end = 0
        while left_end < n - 1 and new_row[left_end + 1] != 0:
            left_end += 1
        left_has_such = False
        left_min_k = float('inf')
        if has_upper:
            for k in range(left_end + 1):
                if out[j - 1][k] == 6:
                    left_has_such = True
                    left_min_k = min(left_min_k, k)
        input_left_3 = (input_row[0] == 3)
        if is_top:
            new_row[0] = 8
        elif left_has_such:
            if is_bottom or left_min_k <= 5:
                new_row[0] = 3
            else:
                new_row[0] = 8
        else:
            new_row[0] = 3 if input_left_3 else 8
    # Right border
    if new_row[n - 1] != 0:
        right_start = n - 1
        while right_start > 0 and new_row[right_start - 1] != 0:
            right_start -= 1
        right_has_such = False
        right_max_k = -1
        if has_upper:
            for kk in range(n - 1, right_start - 1, -1):
                if out[j - 1][kk] == 6:
                    right_max_k = kk
                    right_has_such = True
                    break
        input_right_3 = (input_row[n - 1] == 3)
        if is_top:
            new_row[n - 1] = 8
        elif right_has_such:
            dist = n - 1 - right_max_k
            if is_bottom or dist <= 4:
                new_row[n - 1] = 3
            else:
                new_row[n - 1] = 8
        else:
            new_row[n - 1] = 3 if input_right_3 else 8
    return new_row

def extend_border_threes(temp: List[int], n: int) -> List[int]:
    """Extend 3 inward by one position at borders if 3 followed/preceded by 8."""
    new_row = temp[:]
    if n >= 2 and new_row[0] == 3 and new_row[1] == 8:
        new_row[1] = 3
    if n >= 2 and new_row[n - 1] == 3 and new_row[n - 2] == 8:
        new_row[n - 2] = 3
    return new_row

def program(g: List[List[int]]) -> List[List[int]]:
    """Main program: process odd rows first, then even rows with base, overlay, caps, borders, and extensions."""
    if not g:
        return []
    num_rows = len(g)
    if num_rows == 0:
        return []
    n = len(g[0])
    out = [row[:] for row in g]
    # Process all odd rows
    for j in range(1, num_rows, 2):
        out[j] = process_odd_row(out[j])
    # Process even rows top-to-bottom
    for j in range(0, num_rows, 2):
        temp = initialize_even_base(g[j])
        temp = overlay_6(temp, out, j, n)
        is_bottom = (j == num_rows - 1)
        temp = cap_adjacent_zeros(temp, out, j, n, is_bottom)
        temp = handle_borders(temp, g[j], out, j, n, num_rows)
        has_zero = 0 in temp
        if not is_bottom and not has_zero and n >= 2:
            temp = extend_border_threes(temp, n)
        out[j] = temp
    return out
```