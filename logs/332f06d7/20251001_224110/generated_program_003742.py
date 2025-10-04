```python
from typing import List, Tuple

def find_positions(g: List[List[int]], color: int) -> List[Tuple[int, int]]:
    n = len(g)
    pos = []
    for i in range(n):
        for j in range(n):
            if g[i][j] == color:
                pos.append((i, j))
    return pos

def get_bbox(pos: List[Tuple[int, int]]) -> Tuple[int, int, int, int]:
    if not pos:
        return 0, 0, 0, 0
    rows = [p[0] for p in pos]
    cols = [p[1] for p in pos]
    return min(rows), max(rows), min(cols), max(cols)

def zero_rightmost_w(row: List[int], w: int, n: int) -> None:
    best_end = -1
    current_length = 0
    for j in range(n):
        if row[j] == 1:
            current_length += 1
        else:
            if current_length >= w:
                this_end = j - 1
                if this_end > best_end:
                    best_end = this_end
            current_length = 0
    if current_length >= w:
        this_end = n - 1
        if this_end > best_end:
            best_end = this_end
    if best_end != -1:
        zero_start = best_end - w + 1
        for k in range(w):
            col = zero_start + k
            if 0 <= col < n:
                row[col] = 0

def program(g: List[List[int]]) -> List[List[int]]:
    n = len(g)
    zero_pos = find_positions(g, 0)
    red_pos = find_positions(g, 2)
    if not zero_pos:
        return [row[:] for row in g]
    min_row0, max_row0, min_col0, max_col0 = get_bbox(zero_pos)
    red_min_row = min((p[0] for p in red_pos), default=0)
    red_max_row = max((p[0] for p in red_pos), default=0)
    red_size = len(red_pos)
    is_transfer = (red_min_row == 0) or (red_max_row == n - 1 and red_size == 1)
    new_g = [row[:] for row in g]
    # Fill the hole rectangle
    for i in range(min_row0, max_row0 + 1):
        for j in range(min_col0, max_col0 + 1):
            new_g[i][j] = 1
    if is_transfer:
        for i, j in red_pos:
            new_g[i][j] = 0
    else:
        h = max_row0 - min_row0 + 1
        w = max_col0 - min_col0 + 1
        new_row_min = (min_row0 + red_min_row) // 2
        for rr in range(new_row_min, new_row_min + h):
            if 0 <= rr < n:
                zero_rightmost_w(new_g[rr], w, n)
    return new_g
```