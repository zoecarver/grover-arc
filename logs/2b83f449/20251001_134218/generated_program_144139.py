```python
from typing import List

def process_odd_row(row: List[int]) -> List[int]:
    """Replaces non-overlapping sequences of [7, 7, 7] with [8, 6, 8] in odd rows."""
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

def initialize_even_row_base(g_row: List[int]) -> List[int]:
    """Initializes even row base: 8 where input non-zero, 0 elsewhere."""
    return [0 if val == 0 else 8 for val in g_row]

def overlay_six_from_adjacents(g: List[List[int]], out: List[List[int]], j: int, n: int, base_row: List[int]) -> List[int]:
    """Overlays 6 in even row where upper or lower adjacent row has 6 in the same column."""
    new_row = base_row[:]
    has_upper = j > 0
    has_lower = j < len(g) - 1
    for k in range(n):
        overlay = False
        if has_upper and out[j - 1][k] == 6:
            overlay = True
        if has_lower and out[j + 1][k] == 6:
            overlay = True
        if overlay:
            new_row[k] = 6
    return new_row

def cap_internal_edges_with_three(temp: List[int], out: List[List[int]], j: int, n: int, is_bottom: bool) -> List[int]:
    """Caps left and right edges of non-zero segments adjacent to 0s with 3 if segment has upper 6; skips right caps on bottom row."""
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

def set_left_border(temp: List[int], g: List[List[int]], out: List[List[int]], j: int, n: int, num_rows: int) -> List[int]:
    """Sets left border (col 0) for even row based on upper 6 proximity in left segment, input, top/bottom status."""
    new_row = temp[:]
    is_top = (j == 0)
    is_bottom = (j == num_rows - 1)
    has_upper = (j > 0)
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
        if is_top:
            new_row[0] = 8
        else:
            if left_has_such:
                if is_bottom or left_min_k <= 5:
                    new_row[0] = 3
                else:
                    new_row[0] = 8
            else:
                new_row[0] = 3 if g[j][0] == 3 else 8
    return new_row

def set_right_border(temp: List[int], g: List[List[int]], out: List[List[int]], j: int, n: int, num_rows: int) -> List[int]:
    """Sets right border (col n-1) for even row based on upper 6 proximity in right segment, input, top/bottom status."""
    new_row = temp[:]
    is_top = (j == 0)
    is_bottom = (j == num_rows - 1)
    has_upper = (j > 0)
    if new_row[n - 1] != 0:
        right_start = n - 1
        while right_start > 0 and new_row[right_start - 1] != 0:
            right_start -= 1
        right_has_such = False
        right_max_k = -1
        if has_upper:
            for kk in range(n - 1, right_start - 1, -1):
                if out[j - 1][kk] == 6:
                    right_has_such = True
                    right_max_k = kk
                    break
        input_right_3 = (g[j][n - 1] == 3)
        if is_top:
            new_row[n - 1] = 8
        else:
            if right_has_such:
                dist = (n - 1) - right_max_k
                if is_bottom or dist <= 4:
                    new_row[n - 1] = 3
                else:
                    new_row[n - 1] = 8
            else:
                new_row[n - 1] = 3 if input_right_3 else 8
    return new_row

def extend_border_threes(temp: List[int], n: int, is_bottom: bool) -> List[int]:
    """Extends border 3 inward by one position if followed/preceded by 8, for non-bottom full non-zero rows."""
    if is_bottom or n < 2 or 0 in temp:
        return temp[:]
    new_row = temp[:]
    if new_row[0] == 3 and new_row[1] == 8:
        new_row[1] = 3
    if new_row[n - 2] == 8 and new_row[n - 1] == 3:
        new_row[n - 2] = 3
    return new_row

def program(g: List[List[int]]) -> List[List[int]]:
    """Main program: processes odd rows with pattern replacement, even rows with base, overlay, caps, borders, and extensions."""
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
    # Process even rows top-to-bottom
    for j in range(0, num_rows, 2):
        base = initialize_even_row_base(g[j])
        temp = overlay_six_from_adjacents(g, out, j, n, base)
        is_bottom = (j == num_rows - 1)
        temp = cap_internal_edges_with_three(temp, out, j, n, is_bottom)
        temp = set_left_border(temp, g, out, j, n, num_rows)
        temp = set_right_border(temp, g, out, j, n, num_rows)
        temp = extend_border_threes(temp, n, is_bottom)
        out[j] = temp
    return out
```