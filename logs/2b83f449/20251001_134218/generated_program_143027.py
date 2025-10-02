```python
from typing import List
import math

def replace_777_to_868(row: List[int]) -> List[int]:
    """
    Rule: In odd rows, replace every non-overlapping sequence of three consecutive 7s with [8, 6, 8].
    This handles the pattern transformation observed in odd rows of training examples.
    """
    if len(row) < 3:
        return row[:]
    new_row = row[:]
    i = 0
    while i < len(new_row) - 2:
        if new_row[i] == 7 and new_row[i + 1] == 7 and new_row[i + 2] == 7:
            new_row[i] = 8
            new_row[i + 1] = 6
            new_row[i + 2] = 8
            i += 3
        else:
            i += 1
    return new_row

def overlay_6_from_adjacent(g: List[List[int]], out: List[List[int]], j: int, n: int) -> List[int]:
    """
    Rule: For even rows, initialize with 8 where input is non-zero, 0 elsewhere; then overlay 6 where
    the upper row (if exists) or lower row (if exists) has a 6 in the same column. This propagates
    vertical connections observed in training outputs.
    """
    new_row = [0 if g[j][k] == 0 else 8 for k in range(n)]
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

def add_3_at_zero_adjacent_edges(temp: List[int], out: List[List[int]], j: int, n: int, is_bottom: bool) -> List[int]:
    """
    Rule: In even rows, for each contiguous non-zero segment, if the segment has a 6 in the upper row
    (if exists) within its columns, set the left edge to 3 if adjacent to 0 on left, and set the right
    edge to 3 if adjacent to 0 on right and not bottom row. This handles edge capping observed in
    training examples with gaps.
    """
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
        # Check if segment has upper 6
        segment_has_upper_6 = False
        if has_upper:
            for k in range(start, end + 1):
                if out[j - 1][k] == 6:
                    segment_has_upper_6 = True
                    break
        # Left edge adjacent to 0
        if start > 0 and new_row[start - 1] == 0 and segment_has_upper_6:
            new_row[start] = 3
        # Right edge adjacent to 0, if not bottom
        if not is_bottom and end < n - 1 and new_row[end + 1] == 0 and segment_has_upper_6:
            new_row[end] = 3
    return new_row

def set_border_3_based_on_upper_6_proximity(temp: List[int], g: List[List[int]], out: List[List[int]], j: int, n: int, num_rows: int) -> List[int]:
    """
    Rule: For even rows, handle left and right borders of the grid. For left border (if non-zero):
    if top row, set to 8; else if upper has 6 in leftmost segment with min_k <=5 or bottom row,
    set to 3, else if input was 3 set to 3 else 8. For right border (if non-zero): similar but
    use max_k with dist = n-1 - max_k <=4 or bottom row to set 3 vs 8, fallback to input 3.
    This captures asymmetric border conditions in training examples.
    """
    new_row = temp[:]
    is_top = (j == 0)
    is_bottom = (j == num_rows - 1)
    has_upper = (j > 0)
    # Left border
    if new_row[0] != 0:
        left_end = 0
        while left_end < n - 1 and new_row[left_end + 1] != 0:
            left_end += 1
        left_has_6 = False
        left_min_k = math.inf
        if has_upper:
            for k in range(left_end + 1):
                if out[j - 1][k] == 6:
                    left_has_6 = True
                    left_min_k = min(left_min_k, k)
        input_left_3 = (g[j][0] == 3)
        if is_top:
            new_row[0] = 8
        elif left_has_6:
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
        right_has_6 = False
        right_max_k = -1
        if has_upper:
            for kk in range(n - 1, right_start - 1, -1):
                if out[j - 1][kk] == 6:
                    right_max_k = kk
                    right_has_6 = True
                    break
        input_right_3 = (g[j][n - 1] == 3)
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

def extend_inward_3_at_edges(temp: List[int], n: int, is_bottom: bool, has_zero: bool) -> List[int]:
    """
    Rule: For non-bottom even rows without any 0s and n >= 2, if left edge is 3 followed by 8,
    set the next to 3; similarly if right edge is 8 followed by 3, set the previous to 3.
    This handles single-step border thickening observed in full-span training rows.
    """
    if is_bottom or has_zero or n < 2:
        return temp[:]
    new_row = temp[:]
    if new_row[0] == 3 and new_row[1] == 8:
        new_row[1] = 3
    if new_row[n - 2] == 8 and new_row[n - 1] == 3:
        new_row[n - 2] = 3
    return new_row

def program(g: List[List[int]]) -> List[List[int]]:
    """
    Main composition: Copy input to output. Process all odd rows with 777 replacement.
    Then process even rows top-to-bottom: overlay 6s, add 3s at zero-adjacent edges,
    set borders based on upper 6 proximity, and conditionally extend edge 3s.
    """
    if not g:
        return []
    num_rows = len(g)
    if num_rows == 0:
        return []
    n = len(g[0])
    out = [row[:] for row in g]
    # Process odd rows
    for jj in range(1, num_rows, 2):
        out[jj] = replace_777_to_868(out[jj])
    # Process even rows
    for j in range(0, num_rows, 2):
        temp = overlay_6_from_adjacent(g, out, j, n)
        is_bottom = (j == num_rows - 1)
        temp = add_3_at_zero_adjacent_edges(temp, out, j, n, is_bottom)
        temp = set_border_3_based_on_upper_6_proximity(temp, g, out, j, n, num_rows)
        has_zero = 0 in temp
        temp = extend_inward_3_at_edges(temp, n, is_bottom, has_zero)
        out[j] = temp
    return out
```