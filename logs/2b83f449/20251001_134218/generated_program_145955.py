```python
from typing import List

def replace_triple_sevens(row: List[int]) -> List[int]:
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

def initialize_even_base(g_row: List[int]) -> List[int]:
    return [8 if val != 0 else 0 for val in g_row]

def overlay_sixes(g: List[List[int]], out: List[List[int]], j: int, num_rows: int, n: int, base: List[int]) -> List[int]:
    new_row = base[:]
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

def cap_segment_edges(temp: List[int], upper: List[int], j: int, n: int, is_bottom: bool) -> List[int]:
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
        segment_has_6 = False
        if has_upper:
            for k in range(start, end + 1):
                if upper[k] == 6:
                    segment_has_6 = True
                    break
        if start > 0 and new_row[start - 1] == 0 and segment_has_6:
            new_row[start] = 3
        if not is_bottom and end < n - 1 and new_row[end + 1] == 0 and segment_has_6:
            new_row[end] = 3
    return new_row

def set_left_border(temp: List[int], g_row: List[int], upper: List[int], j: int, n: int, num_rows: int) -> List[int]:
    new_row = temp[:]
    if new_row[0] == 0:
        return new_row
    is_top = j == 0
    is_bottom = j == num_rows - 1
    has_upper_local = j > 0
    if is_top:
        new_row[0] = 8
        return new_row
    left_end = 0
    while left_end < n - 1 and new_row[left_end + 1] != 0:
        left_end += 1
    left_has_6 = False
    left_min_k = float('inf')
    if has_upper_local:
        for k in range(left_end + 1):
            if upper[k] == 6:
                left_has_6 = True
                left_min_k = min(left_min_k, k)
    if left_has_6:
        if is_bottom or left_min_k <= 5:
            new_row[0] = 3
        else:
            new_row[0] = 8
    else:
        new_row[0] = 3 if g_row[0] == 3 else 8
    return new_row

def set_right_border(temp: List[int], g_row: List[int], upper: List[int], j: int, n: int, num_rows: int) -> List[int]:
    new_row = temp[:]
    if new_row[n - 1] == 0:
        return new_row
    is_top = j == 0
    is_bottom = j == num_rows - 1
    has_upper_local = j > 0
    if is_top:
        new_row[n - 1] = 8
        return new_row
    right_start = n - 1
    while right_start > 0 and new_row[right_start - 1] != 0:
        right_start -= 1
    right_has_6 = False
    right_max_k = -1
    if has_upper_local:
        for k in range(right_start, n):
            if upper[k] == 6:
                right_has_6 = True
                right_max_k = max(right_max_k, k)
    if right_has_6:
        dist = (n - 1) - right_max_k
        if is_bottom or dist <= 4:
            new_row[n - 1] = 3
        else:
            new_row[n - 1] = 8
    else:
        new_row[n - 1] = 3 if g_row[n - 1] == 3 else 8
    return new_row

def extend_border_threes(temp: List[int], n: int, is_bottom: bool) -> List[int]:
    new_row = temp[:]
    if is_bottom or 0 in new_row or n < 2:
        return new_row
    if new_row[0] == 3 and new_row[1] == 8:
        new_row[1] = 3
    if new_row[n - 1] == 3 and new_row[n - 2] == 8:
        new_row[n - 2] = 3
    return new_row

def program(g: List[List[int]]) -> List[List[int]]:
    if not g or not g[0]:
        return []
    num_rows = len(g)
    n = len(g[0])
    out = [row[:] for row in g]
    for j in range(1, num_rows, 2):
        out[j] = replace_triple_sevens(out[j])
    for j in range(0, num_rows, 2):
        is_bottom = (j == num_rows - 1)
        base = initialize_even_base(g[j])
        temp = overlay_sixes(g, out, j, num_rows, n, base)
        upper = out[j - 1] if j > 0 else [0] * n
        temp = cap_segment_edges(temp, upper, j, n, is_bottom)
        temp = set_left_border(temp, g[j], upper, j, n, num_rows)
        temp = set_right_border(temp, g[j], upper, j, n, num_rows)
        temp = extend_border_threes(temp, n, is_bottom)
        out[j] = temp
    return out
```