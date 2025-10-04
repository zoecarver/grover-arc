```python
from typing import List

def find_wall_cols(g: List[List[int]]) -> List[int]:
    if not g:
        return []
    cols = len(g[0])
    return [j for j in range(cols) if g[0][j] == 5]

def find_panel_starts(wall_cols: List[int], cols: int) -> List[int]:
    starts = [0]
    for wall in wall_cols:
        if wall + 1 < cols:
            starts.append(wall + 1)
    return starts

def get_w(starts: List[int], wall_cols: List[int], cols: int) -> int:
    if not starts:
        return 0
    next_wall = wall_cols[0] if wall_cols else cols
    return next_wall - starts[0]

def find_seed_row(g: List[List[int]]) -> int:
    rows = len(g)
    for i in range(rows - 1, -1, -1):
        if any(cell != 0 and cell != 5 for cell in g[i]):
            return i
    return 0

def get_colors(g: List[List[int]], seed_row: int, starts: List[int], w: int, m: int) -> List[int]:
    colors = []
    for k in range(m):
        center = starts[k] + w // 2
        colors.append(g[seed_row][center])
    return colors

def get_patterns(g: List[List[int]], starts: List[int], w: int, m: int, colors: List[int]) -> List[List[List[int]]]:
    patterns = []
    for k in range(m):
        pat = []
        for r in range(w):
            row = []
            five_count = sum(1 for jj in range(w) if g[r][starts[k] + jj] == 5)
            is_wall_row = five_count > w // 2
            for jj in range(w):
                cell = g[r][starts[k] + jj]
                if is_wall_row:
                    if jj == w // 2:
                        row.append(0)
                    else:
                        row.append(colors[k])
                elif cell != 0 and cell != 5:
                    row.append(colors[k])
                else:
                    row.append(0)
            pat.append(row)
        patterns.append(pat)
    return patterns

def is_block(pattern: List[List[int]], w: int) -> bool:
    return all(sum(1 for x in row if x != 0) == w for row in pattern)

def fill_upper_block(out: List[List[int]], patterns: List[List[List[int]]], w: int):
    s = w * w
    upper_h = w * (w - 1)
    # left second pattern
    for rep in range(w - 1):
        for rr in range(w):
            orow = rep * w + rr
            for jj in range(w):
                out[orow][jj] = patterns[1][rr][jj]
    # right third pattern horz (w-1) copies
    for rep in range(w - 1):
        for rr in range(w):
            orow = rep * w + rr
            for rep_h in range(w - 1):
                for jj in range(w):
                    out[orow][w + rep_h * w + jj] = patterns[2][rr][jj]

def fill_lower_block(out: List[List[int]], patterns: List[List[List[int]]], w: int):
    s = w * w
    lower_start = w * (w - 1)
    # left first
    for rr in range(w):
        for jj in range(w):
            out[lower_start + rr][jj] = patterns[0][rr][jj]
    # right second
    for rr in range(w):
        for jj in range(w):
            out[lower_start + rr][s - w + jj] = patterns[1][rr][jj]

def fill_upper_pointy(out: List[List[int]], patterns: List[List[int]], w: int):
    s = w * w
    upper_h = w * (w - 1)
    # left third
    for rep in range(w - 1):
        for rr in range(w):
            orow = rep * w + rr
            for jj in range(w):
                out[orow][jj] = patterns[2][rr][jj]
    # right first
    for rep in range(w - 1):
        for rr in range(w):
            orow = rep * w + rr
            for jj in range(w):
                out[orow][s - w + jj] = patterns[0][rr][jj]

def fill_lower_pointy(out: List[List[int]], patterns: List[List[int]], w: int):
    s = w * w
    lower_start = w * (w - 1)
    # left second horz (w - 1) copies
    for rr in range(w):
        for rep_h in range(w - 1):
            for jj in range(w):
                out[lower_start + rr][rep_h * w + jj] = patterns[1][rr][jj]

def program(g: List[List[int]]) -> List[List[int]]:
    if not g:
        return []
    rows = len(g)
    cols = len(g[0])
    wall_cols = find_wall_cols(g)
    starts = find_panel_starts(wall_cols, cols)
    m = len(starts)
    if m == 0:
        return [[0]]
    w = get_w(starts, wall_cols, cols)
    seed_row = find_seed_row(g)
    colors = get_colors(g, seed_row, starts, w, m)
    patterns = get_patterns(g, starts, w, m, colors)
    s = w * w
    out = [[0] * s for _ in range(s)]
    if m < 3:
        return out  # or handle, but assume m>=3
    # take first 3
    p0 = patterns[0]
    p1 = patterns[1]
    p2 = patterns[2]
    c0 = colors[0]
    # but patterns already have colors
    is_block0 = is_block(p0, w)
    if is_block0:
        fill_upper_block(out, [p0, p1, p2], w)
        fill_lower_block(out, [p0, p1, p2], w)
    else:
        fill_upper_pointy(out, [p0, p1, p2], w)
        fill_lower_pointy(out, [p0, p1, p2], w)
    return out
```