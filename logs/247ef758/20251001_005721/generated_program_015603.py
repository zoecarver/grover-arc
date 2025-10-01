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
    g_out = [row[:] for row in g]
    n = len(g)
    m = len(g[0]) if n > 0 else 0
    if n < 3:
        return g_out
    middle_rows = list(range(1, n - 1))
    spine = find_spine(g, middle_rows, m)
    if spine == -1:
        return g_out
    row_color_col = spine + 1
    if row_color_col >= m:
        return g_out
    # Set last column to row color
    for i in middle_rows:
        c = g_out[i][row_color_col]
        if g_out[i][m - 1] == 0 or g_out[i][m - 1] != c:
            g_out[i][m - 1] = c
    # Collect forbidden colors from top and bottom right of spine
    forbidden = set()
    for row in [0, n - 1]:
        for j in range(spine, m):
            if g_out[row][j] != 0:
                forbidden.add(g_out[row][j])
    # Clear forbidden colors left of spine in middle rows
    for i in middle_rows:
        for j in range(spine):
            if g_out[i][j] != 0 and g_out[i][j] in forbidden:
                g_out[i][j] = 0
    # Collect homes per color
    r_cs = defaultdict(list)
    for i in middle_rows:
        c = g_out[i][row_color_col]
        if c != 0:
            r_cs[c].append(i)
    # Find specials
    specials = find_specials(g_out, row_color_col, m)
    # Process each special as single
    for j in specials:
        c = g_out[0][j]
        homes = [ii for ii in r_cs[c] if ii <= j]
        for ii in homes:
            l = max(row_color_col + 1, j - 1)
            r = min(m - 2, j + 1)
            if j >= m - 3:
                l = max(l, j + 1)
            for k in range(l, r + 1):
                if g_out[ii][k] == 0:
                    g_out[ii][k] = c
        # Vertical propagation to adjacent rows
        for ii in homes:
            for dr in [-1, 1]:
                ni = ii + dr
                if 1 <= ni <= n - 2 and g_out[ni][j] == 0:
                    g_out[ni][j] = c
    return g_out
```