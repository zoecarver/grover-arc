```python
from collections import Counter
from typing import List, Tuple

def get_background(g: List[List[int]]) -> int:
    flat = [c for row in g for c in row]
    return Counter(flat).most_common(1)[0][0]

def get_consecutive_lengths(row: List[int], color: int) -> List[Tuple[int, int]]:
    lengths = []
    i = 0
    n = len(row)
    while i < n:
        if row[i] == color:
            start = i
            while i < n and row[i] == color:
                i += 1
            lengths.append((start, i - start))
        else:
            i += 1
    return lengths

def get_fill_colors(g: List[List[int]], skeleton: int, bg: int) -> Tuple[int, int]:
    upper = None
    lower = None
    for row in g:
        for cell in row:
            if cell != bg and cell != skeleton:
                if upper is None:
                    upper = cell
                elif lower is None and cell != upper:
                    lower = cell
                if upper is not None and lower is not None:
                    return upper, lower
    return upper, lower

def program(g: List[List[int]]) -> List[List[int]]:
    if not g or not g[0]:
        return []
    h = len(g)
    w_len = len(g[0])
    bg = get_background(g)
    colors = {c for row in g for c in row}
    if 3 not in colors:
        return [[bg for _ in range(w_len)] for _ in range(h)]
    skeleton = 3
    upper_fill, lower_fill = get_fill_colors(g, skeleton, bg)
    if upper_fill is None or lower_fill is None:
        return [[bg for _ in range(w_len)] for _ in range(h)]
    max_w = 0
    for row in g:
        cons = get_consecutive_lengths(row, skeleton)
        for _, le in cons:
            max_w = max(max_w, le)
    if max_w < 3:
        return [[bg for _ in range(w_len)] for _ in range(h)]
    w = max_w
    full_rows = []
    start_col_dict = {}
    partials = []
    for r in range(h):
        cons = get_consecutive_lengths(g[r], skeleton)
        for sc, le in cons:
            if le == w:
                full_rows.append(r)
                start_col_dict[r] = sc
            if le == 2:
                partials.append((r, sc))
    if len(full_rows) != 2 or len(partials) != 1:
        return [[bg for _ in range(w_len)] for _ in range(h)]
    top_full = min(full_rows)
    bottom_full = max(full_rows)
    partial_row, partial_sc = partials[0]
    if not (top_full < partial_row < bottom_full):
        return [[bg for _ in range(w_len)] for _ in range(h)]
    start_col = start_col_dict[top_full]
    if start_col_dict.get(bottom_full) != start_col:
        return [[bg for _ in range(w_len)] for _ in range(h)]
    if partial_row == top_full + 1:
        partial_upper = True
        gap_row = top_full + 2
    else:
        partial_upper = False
        gap_row = top_full + 1
    if gap_row >= h or bottom_full != max(top_full, partial_row) + 2:
        return [[bg for _ in range(w_len)] for _ in range(h)]
    if partial_sc == start_col:
        direction = 1
        bulge_right = True
    elif partial_sc == start_col + w - 2:
        direction = -1
        bulge_right = False
    else:
        return [[bg for _ in range(w_len)] for _ in range(h)]
    bulge_width = 5
    if bulge_right:
        bulge_start = start_col + w
        bulge_cols = list(range(bulge_start, bulge_start + bulge_width))
    else:
        bulge_start = start_col - bulge_width
        bulge_cols = list(range(bulge_start, start_col))
    far_col = bulge_cols[-1] if direction == 1 else bulge_cols[0]
    inner_color = lower_fill if partial_upper else upper_fill
    outer_color = upper_fill if partial_upper else lower_fill
    out = [[bg for _ in range(w_len)] for _ in range(h)]
    for r in range(h):
        for c in range(w_len):
            if g[r][c] == skeleton:
                out[r][c] = skeleton
    for c in range(start_col, start_col + w):
        if out[partial_row][c] == bg:
            out[partial_row][c] = inner_color
    for c in range(start_col, start_col + w):
        out[gap_row][c] = inner_color
    for c in bulge_cols:
        if 0 <= c < w_len:
            out[partial_row][c] = outer_color
    if 0 <= far_col < w_len:
        out[gap_row][far_col] = outer_color
    next_far = far_col + direction
    if 0 <= far_col < w_len and 0 <= next_far < w_len:
        if partial_upper:
            out[bottom_full][far_col] = outer_color
            out[bottom_full][next_far] = outer_color
        else:
            out[top_full][far_col] = outer_color
            out[top_full][next_far] = outer_color
    return out
```