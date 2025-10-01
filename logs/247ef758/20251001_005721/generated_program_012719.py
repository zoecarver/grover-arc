```python
from typing import List
from collections import defaultdict

def find_spine(grid: List[List[int]], middle_rows: List[int], m: int) -> int:
    spine = -1
    max_count = 0
    for j in range(m):
        colors = [grid[i][j] for i in middle_rows]
        non_zero_colors = [col for col in colors if col != 0]
        if non_zero_colors and len(set(non_zero_colors)) == 1:
            count = len(non_zero_colors)
            if count > max_count:
                max_count = count
                spine = j
    if spine == -1:
        for j in range(m):
            colors = [grid[i][j] for i in middle_rows]
            if all(c == colors[0] for c in colors) and colors[0] != 0:
                spine = j
                break
    return spine

def find_specials(grid: List[List[int]], row_color_col: int, m: int) -> List[int]:
    special = []
    for j in range(row_color_col + 1, m - 1):
        c = grid[0][j]
        if c != 0 and c != grid[0][j - 1] and c != grid[0][j + 1]:
            special.append(j)
    return special

def program(g: List[List[int]]) -> List[List[int]]:
    n = len(g)
    if n < 3:
        return [row[:] for row in g]
    m = len(g[0])
    middle_rows = list(range(1, n - 1))
    spine = find_spine(g, middle_rows, m)
    if spine == -1:
        return [row[:] for row in g]
    s = g[middle_rows[0]][spine] if middle_rows else 0
    out = [row[:] for row in g]
    for i in range(n):
        for k in range(spine):
            out[i][k] = 0
        out[i][spine] = s
    known_colors = {c for c in out[0] if c != 0}
    for i in middle_rows:
        for k in range(spine):
            if out[i][k] != 0 and out[i][k] in known_colors:
                out[i][k] = 0
    row_color_col = spine + 1
    if row_color_col < m:
        for i in range(n):
            out[i][m - 1] = out[i][row_color_col]
    specials = find_specials(out, row_color_col, m)
    r_cs = defaultdict(list)
    for i in middle_rows:
        r = out[i][row_color_col]
        if r != 0:
            r_cs[r].append(i)
    half = m // 2
    for p in specials:
        if p < half:
            continue
        c = out[0][p]
        if c not in r_cs:
            continue
        homes = sorted(r_cs[c])
        skip_center = (p + 1 == m - 2)
        for h in homes:
            for dk in [-1, 0, 1]:
                kk = p + dk
                if 0 <= kk < m - 1 and out[h][kk] == 0:
                    if not (dk == 0 and skip_center):
                        out[h][kk] = c
            for drow in [-1, 1]:
                nr = h + drow
                if 1 <= nr <= n - 2 and out[nr][p] == 0:
                    out[nr][p] = c
    return out
```