```python
from typing import List

def find_wall_cols(g: List[List[int]]) -> List[int]:
    if not g or not g[0]:
        return []
    n_cols = len(g[0])
    return [j for j in range(n_cols) if g[0][j] == 5]

def find_panel_starts(wall_cols: List[int], n_cols: int) -> List[int]:
    starts = [0]
    for wall in wall_cols:
        if wall + 1 < n_cols:
            starts.append(wall + 1)
    return starts

def get_w(starts: List[int], wall_cols: List[int], n_cols: int) -> int:
    if not starts:
        return n_cols
    first_end = wall_cols[0] if wall_cols else n_cols
    return first_end - starts[0]

def find_seed_row(g: List[List[int]]) -> int:
    n_rows = len(g)
    for i in range(n_rows - 1, -1, -1):
        if any(cell != 0 and cell != 5 for cell in g[i]):
            return i
    return 0

def get_colors(g: List[List[int]], seed_row: int, starts: List[int], w: int, m: int) -> List[int]:
    colors = []
    n_cols = len(g[0]) if g else 0
    for k in range(m):
        center = starts[k] + w // 2
        color = g[seed_row][center] if seed_row < len(g) and center < n_cols else 0
        colors.append(color)
    return colors

def get_patterns(g: List[List[int]], starts: List[int], w: int, m: int) -> List[List[List[int]]]:
    patterns = []
    n_rows = len(g)
    n_cols = len(g[0]) if g else 0
    for k in range(m):
        pat = []
        for r in range(min(w, n_rows)):
            start_col = starts[k]
            end_col = min(start_col + w, n_cols)
            slice_ = g[r][start_col:end_col]
            five_count = sum(1 for x in slice_ if x == 5)
            is_wall = five_count > w // 2
            if is_wall:
                row = [1 if jj != w // 2 else 0 for jj in range(w)]
            else:
                row = [1 if x != 0 and x != 5 else 0 for x in slice_]
            if len(row) < w:
                row += [0] * (w - len(row))
            row = row[:w]
            pat.append(row)
        while len(pat) < w:
            pat.append([0] * w)
        patterns.append(pat)
    return patterns

def is_block(pat: List[List[int]]) -> bool:
    if not pat:
        return False
    w = len(pat[0])
    if w == 0:
        return False
    return all(sum(row) == w for row in pat)

def is_swap(p0: List[List[int]]) -> bool:
    if not p0 or not p0[0]:
        return False
    top = p0[0]
    w = len(top)
    return top[0] == 0 or top[w - 1] == 0

def place(out: List[List[int]], r_start: int, c_start: int, pat: List[List[int]], col: int, w: int):
    for rr in range(w):
        for cc in range(w):
            if pat[rr][cc] == 1:
                if r_start + rr < len(out) and c_start + cc < len(out[0]):
                    out[r_start + rr][c_start + cc] = col

def program(g: List[List[int]]) -> List[List[int]]:
    if not g:
        return []
    n_rows = len(g)
    n_cols = len(g[0]) if n_rows > 0 else 0
    if n_cols == 0:
        return []
    wall_cols = find_wall_cols(g)
    starts = find_panel_starts(wall_cols, n_cols)
    w = get_w(starts, wall_cols, n_cols)
    if w == 0:
        return [[0]]
    m = min(3, len(starts))
    seed_row = find_seed_row(g)
    colors = get_colors(g, seed_row, starts, w, m)
    patterns = get_patterns(g, starts, w, m)
    while len(colors) < 3:
        colors.append(0)
    while len(patterns) < 3:
        patterns.append([[0] * w for _ in range(w)])
    p0, p1, p2 = patterns
    c0, c1, c2 = colors
    s = w * w
    out = [[0] * s for _ in range(s)]
    if is_block(p0):
        # block mode
        for k in range(w - 1):
            r_start = k * w
            # p1 at super col k
            place(out, r_start, k * w, p1, c1, w)
            # p2 at super cols k+1 to w-1
            for j in range(k + 1, w):
                place(out, r_start, j * w, p2, c2, w)
        # lower
        r_start = (w - 1) * w
        place(out, r_start, 0, p0, c0, w)
        place(out, r_start, (w - 1) * w, p1, c1, w)
    else:
        # pointy mode
        swap = is_swap(p0)
        for k in range(w - 1):
            r_start = k * w
            # left p2 c2
            place(out, r_start, 0, p2, c2, w)
            # right
            if swap:
                right_pat = p0
                right_col = c0
            else:
                right_pat = p1
                right_col = c1
            right_start = (w - 1) * w
            place(out, r_start, right_start, right_pat, right_col, w)
        # lower
        r_start = (w - 1) * w
        if swap:
            left_pat = p1
            left_col = c1
        else:
            left_pat = p0
            left_col = c0
        for j in range(w - 1):
            place(out, r_start, j * w, left_pat, left_col, w)
        if not swap:
            # add right p2 in lower for non-swap
            place(out, r_start, (w - 1) * w, p2, c2, w)
    return out
```