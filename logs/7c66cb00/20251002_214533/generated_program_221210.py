```python
from typing import List, Tuple
from collections import defaultdict

def find_small_shapes(g: List[List[int]], bg: int) -> List[Tuple[int, int, int, int]]:
    shapes = []
    n_rows = len(g)
    n_cols = len(g[0])
    i = 0
    while i < n_rows:
        if all(g[i][j] == bg for j in range(n_cols)):
            i += 1
            continue
        start = i
        while i < n_rows and not all(g[i][j] == bg for j in range(n_cols)):
            i += 1
        end = i - 1
        active_cols = set()
        for r in range(start, end + 1):
            for c in range(n_cols):
                if g[r][c] != bg:
                    active_cols.add(c)
        if not active_cols:
            continue
        cols_list = sorted(active_cols)
        intervals = []
        current_start = cols_list[0]
        current_end = cols_list[0]
        for c in cols_list[1:]:
            if c == current_end + 1:
                current_end = c
            else:
                intervals.append((current_start, current_end))
                current_start = c
                current_end = c
        intervals.append((current_start, current_end))
        for left, right in intervals:
            shape_rows = [r for r in range(start, end + 1) if any(g[r][c] != bg for c in range(left, right + 1))]
            if shape_rows:
                min_r = min(shape_rows)
                max_r = max(shape_rows)
                h = max_r - min_r + 1
                shapes.append((min_r, h, left, right))
    return shapes

def find_large_blocks(g: List[List[int]]) -> List[Tuple[int, int, int, int]]:
    blocks = []
    n_rows = len(g)
    n_cols = len(g[0])
    i = 0
    while i < n_rows:
        row = g[i]
        if (len(set(row)) != 2 or row[0] != row[n_cols - 1] or row[1] != row[n_cols - 2] or
            row[0] == row[1] or not all(row[j] == row[1] for j in range(1, n_cols - 1))):
            i += 1
            continue
        b_start = i
        border = row[0]
        fill = row[1]
        while (i < n_rows and len(set(g[i])) == 2 and g[i][0] == border and g[i][n_cols - 1] == border and
               all(g[i][j] == fill for j in range(1, n_cols - 1))):
            i += 1
        b_h = i - b_start
        blocks.append((b_start, b_h, border, fill))
    return blocks

def program(g: List[List[int]]) -> List[List[int]]:
    n_rows = len(g)
    n_cols = len(g[0])
    bg = g[0][0]
    out = [row[:] for row in g]
    # Set non-large rows to background
    for i in range(n_rows):
        row = out[i]
        is_large_row = (len(set(row)) == 2 and row[0] == row[n_cols - 1] and row[1] == row[n_cols - 2] and
                        row[0] != row[1] and all(row[j] == row[1] for j in range(1, n_cols - 1)))
        if not is_large_row:
            out[i] = [bg] * n_cols
    # Find shapes and blocks from original g
    shapes = find_small_shapes(g, bg)
    blocks = find_large_blocks(g)
    # Apply shapes to subsequent blocks
    for shape in shapes:
        s_start, sh, left, right = shape
        s_end = s_start + sh - 1
        for block in blocks:
            b_start, b_h, border, fill = block
            if s_end >= b_start:
                continue
            if sh > b_h:
                continue
            # Find small colors
            small_colors = set()
            for k in range(sh):
                r = s_start + k
                for c in range(left, right + 1):
                    colr = g[r][c]
                    if colr != bg:
                        small_colors.add(colr)
            if len(small_colors) == 0:
                continue
            if len(small_colors) == 1:
                c = next(iter(small_colors))
                if c != fill:
                    continue
                mapped = {c: border}
            else:
                clist = list(small_colors)
                if len(clist) != 2:
                    continue
                c1, c2 = clist
                if c1 == fill:
                    mapped = {c1: border, c2: fill}
                elif c2 == fill:
                    mapped = {c2: border, c1: fill}
                else:
                    continue
            # Apply
            for k in range(sh):
                small_r = s_start + k
                large_r = b_start + b_h - sh + k
                for c in range(left, right + 1):
                    colr = g[small_r][c]
                    if colr != bg and colr in mapped:
                        out[large_r][c] = mapped[colr]
    return out
```