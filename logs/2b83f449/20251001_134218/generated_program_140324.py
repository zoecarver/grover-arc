```python
from typing import List

def process_pattern(row: List[int]) -> List[int]:
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

def get_6_overlay(g: List[List[int]], out: List[List[int]], j: int, n: int) -> List[int]:
    new_row = [0 if g[j][k] == 0 else 8 for k in range(n)]
    has_upper = j > 0
    has_lower = j < len(g) - 1
    for k in range(n):
        from_upper = has_upper and out[j - 1][k] == 6
        from_lower = has_lower and out[j + 1][k] == 6
        if from_upper or from_lower:
            new_row[k] = 6
    return new_row

def add_0_adjacent(temp: List[int], out: List[List[int]], j: int, n: int, is_bottom: bool) -> List[int]:
    new_row = temp[:]
    has_upper = j > 0
    segments = []
    i = 0
    while i < n:
        if new_row[i] == 0:
            i += 1
            continue
        start = i
        while i < n and new_row[i] != 0:
            i += 1
        end = i - 1
        segments.append((start, end))
    for start, end in segments:
        segment_has_upper6 = False
        if has_upper:
            for k in range(start, end + 1):
                if out[j - 1][k] == 6:
                    segment_has_upper6 = True
                    break
        if start > 0 and new_row[start - 1] == 0:
            if segment_has_upper6:
                new_row[start] = 3
        if not is_bottom and end < n - 1 and new_row[end + 1] == 0:
            if segment_has_upper6:
                new_row[end] = 3
    return new_row

def add_border_3s(temp: List[int], g: List[List[int]], out: List[List[int]], j: int, n: int, num_rows: int) -> List[int]:
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

def add_extension(temp: List[int], n: int) -> List[int]:
    new_row = temp[:]
    if n >= 2 and new_row[0] == 3 and new_row[1] == 8:
        new_row[1] = 3
    if n >= 2 and new_row[n - 1] == 3 and new_row[n - 2] == 8:
        new_row[n - 2] = 3
    return new_row

def program(g: List[List[int]]) -> List[List[int]]:
    if not g:
        return []
    out = [row[:] for row in g]
    num_rows = len(g)
    if num_rows == 0:
        return out
    n = len(g[0])
    for jj in range(1, num_rows, 2):
        out[jj] = process_pattern(out[jj])
    for j in range(0, num_rows, 2):
        temp = get_6_overlay(g, out, j, n)
        temp = add_0_adjacent(temp, out, j, n, is_bottom=(j == num_rows - 1))
        temp = add_border_3s(temp, g, out, j, n, num_rows)
        is_bottom = (j == num_rows - 1)
        has_zero = 0 in temp
        if not is_bottom and not has_zero and n >= 2:
            temp = add_extension(temp, n)
        out[j] = temp
    return out
```