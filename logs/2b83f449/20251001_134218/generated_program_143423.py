```python
from typing import List
import math

def process_odd_row_pattern_replacement(row: List[int]) -> List[int]:
    """
    Handles the rule for odd rows: Replaces non-overlapping sequences of three 7s with [8, 6, 8].
    This implements the observed pattern transformation in odd-indexed rows from training examples.
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

def initialize_even_row_with_nonzero_to_eight(g_row: List[int], n: int) -> List[int]:
    """
    For even rows: Sets positions to 8 where input is non-zero, 0 otherwise.
    This is the base layer for even rows before overlays, observed in training outputs.
    """
    return [0 if g_row[k] == 0 else 8 for k in range(n)]

def overlay_six_from_adjacent_rows(g: List[List[int]], out: List[List[int]], j: int, n: int, base_row: List[int]) -> List[int]:
    """
    Overlays 6 in even row positions where the upper or lower adjacent row (if exists) has a 6.
    This propagates vertical connections observed in training examples where 6s align across rows.
    """
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

def add_three_at_zero_adjacent_segment_edges(temp: List[int], out: List[List[int]], j: int, n: int, is_bottom: bool) -> List[int]:
    """
    For even rows: Identifies non-zero segments and sets edge positions to 3 if adjacent to 0 and the segment has a 6 in the upper row.
    Skips right edge for bottom row. This handles gap capping observed in training where 3s appear next to 0s under upper 6 conditions.
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

def set_border_threes_based_on_upper_six_proximity_and_input(temp: List[int], g: List[List[int]], out: List[List[int]], j: int, n: int, num_rows: int) -> List[int]:
    """
    For even rows: Sets left/right border to 3 if upper row has a 6 nearby within segment (left: min_k <=5, right: dist <=4), or input is 3; top row forces 8.
    Bottom row sets 3 if condition or input. This implements asymmetric border rules observed in training for edge capping.
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
        left_has_such = False
        left_min_k = float('inf')
        if has_upper:
            for k in range(left_end + 1):
                if out[j - 1][k] == 6:
                    left_has_such = True
                    left_min_k = min(left_min_k, k)
        input_left_3 = (g[j][0] == 3)
        if not is_top:
            if left_has_such:
                if is_bottom or left_min_k <= 5:
                    new_row[0] = 3
                else:
                    new_row[0] = 8
            else:
                new_row[0] = 3 if input_left_3 else 8
        else:
            new_row[0] = 8
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
        input_right_3 = (g[j][n - 1] == 3)
        if not is_top:
            if right_has_such:
                dist = n - 1 - right_max_k
                if is_bottom or dist <= 4:
                    new_row[n - 1] = 3
                else:
                    new_row[n - 1] = 8
            else:
                new_row[n - 1] = 3 if input_right_3 else 8
        else:
            new_row[n - 1] = 8
    return new_row

def extend_three_inward_at_edges_if_no_zeros(temp: List[int], n: int, is_bottom: bool) -> List[int]:
    """
    For even non-bottom rows without zeros and n>=2: Extends 3 inward if edge is 3 followed by 8 (left: pos1=3, right: pos n-2=3).
    This handles border thickening observed in training for continuous segments.
    """
    if is_bottom or n < 2:
        return temp[:]
    new_row = temp[:]
    has_zero = 0 in new_row
    if has_zero:
        return new_row
    if new_row[0] == 3 and new_row[1] == 8:
        new_row[1] = 3
    if new_row[n - 1] == 3 and new_row[n - 2] == 8:
        new_row[n - 2] = 3
    return new_row

def program(g: List[List[int]]) -> List[List[int]]:
    """
    Main function: Copies input to output, processes all odd rows with pattern replacement,
    then processes even rows sequentially: base 8s, overlay 6s, add 3s at zero-adjacent edges,
    set borders, and extend if applicable. This composes all rules to match training transformations.
    """
    if not g:
        return []
    num_rows = len(g)
    if num_rows == 0:
        return [row[:] for row in g]
    n = len(g[0])
    out = [row[:] for row in g]
    # Process all odd rows first
    for jj in range(1, num_rows, 2):
        out[jj] = process_odd_row_pattern_replacement(out[jj])
    # Process even rows top to bottom
    for j in range(0, num_rows, 2):
        is_bottom = (j == num_rows - 1)
        base = initialize_even_row_with_nonzero_to_eight(g[j], n)
        temp = overlay_six_from_adjacent_rows(g, out, j, n, base)
        temp = add_three_at_zero_adjacent_segment_edges(temp, out, j, n, is_bottom)
        temp = set_border_threes_based_on_upper_six_proximity_and_input(temp, g, out, j, n, num_rows)
        temp = extend_three_inward_at_edges_if_no_zeros(temp, n, is_bottom)
        out[j] = temp
    return out
```