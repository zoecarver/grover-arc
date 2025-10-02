```python
from collections import Counter, defaultdict
import copy

def find_background(g):
    if not g or not g[0]:
        return 0
    flat = [num for row in g for num in row]
    return Counter(flat).most_common(1)[0][0]

def fill_group(g, C, bg, rows, cols, pos):
    if len(pos) < 2:
        return
    ps = sorted(pos, key=lambda p: p[0])
    r1, c1 = ps[0]
    r2, c2 = ps[-1]
    dr = r2 - r1
    dc = c2 - c1
    if dr <= 0 or abs(dc) != dr:
        return
    slope = 1 if dc > 0 else -1
    if slope == 1:
        k = c1 - r1
        for rr in range(r1, r2 + 1):
            cc = rr + k
            if 0 <= cc < cols and g[rr][cc] == bg:
                g[rr][cc] = C
    else:
        m = r1 + c1
        for rr in range(r1, r2 + 1):
            cc = m - rr
            if 0 <= cc < cols and g[rr][cc] == bg:
                g[rr][cc] = C

def collect_skipped(g, C, bg, rows, cols, pos):
    skipped = {}
    if len(pos) < 2:
        return skipped
    ps = sorted(pos, key=lambda p: p[0])
    r1, c1 = ps[0]
    r2, c2 = ps[-1]
    dr = r2 - r1
    dc = c2 - c1
    if dr <= 0 or abs(dc) != dr:
        return skipped
    slope = 1 if dc > 0 else -1
    other = 6 if C == 1 else 1
    if slope == 1:
        k = c1 - r1
        for rr in range(r1, r2 + 1):
            cc = rr + k
            if 0 <= cc < cols and g[rr][cc] == other:
                skipped[(rr, cc)] = slope
    else:
        m = r1 + c1
        for rr in range(r1, r2 + 1):
            cc = m - rr
            if 0 <= cc < cols and g[rr][cc] == other:
                skipped[(rr, cc)] = slope
    return skipped

def fill_full_perp(g, sr, sc, slope, D, bg, rows, cols):
    if slope == 1:  # perp anti
        m = sr + sc
        for rr in range(rows):
            cc = m - rr
            if 0 <= cc < cols and g[rr][cc] == bg:
                g[rr][cc] = D
    else:  # perp main
        k = sc - sr
        for rr in range(rows):
            cc = rr + k
            if 0 <= cc < cols and g[rr][cc] == bg:
                g[rr][cc] = D

def program(g: List[List[int]]) -> List[List[int]]:
    if not g or not g[0]:
        return g
    rows = len(g)
    cols = len(g[0])
    grid = copy.deepcopy(g)
    bg = find_background(grid)
    pos = defaultdict(list)
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] != bg:
                pos[grid[i][j]].append((i, j))
    skipped = {}
    for C in [1, 6]:
        if C in pos:
            this_skipped = collect_skipped(grid, C, bg, rows, cols, pos[C])
            for key, val in this_skipped.items():
                skipped[key] = val
    for C in [1, 6]:
        if C in pos:
            fill_group(grid, C, bg, rows, cols, pos[C])
    for (sr, sc), slope in skipped.items():
        D = grid[sr][sc]
        fill_full_perp(grid, sr, sc, slope, D, bg, rows, cols)
    return grid
```