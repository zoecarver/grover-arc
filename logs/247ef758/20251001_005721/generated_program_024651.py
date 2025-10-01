```python
from typing import List
from collections import defaultdict, Counter

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

def find_specials(grid: List[List[int]], row_color_col: int, m: int, border: int) -> List[int]:
    special = []
    for j in range(row_color_col + 1, m - 1):
        c = grid[border][j]
        left = grid[border][j - 1]
        right = grid[border][j + 1]
        if c != 0 and c != left and c != right:
            special.append(j)
    return special

def group_specials(special: List[int]) -> List[List[int]]:
    groups = []
    if special:
        current = [special[0]]
        for j in special[1:]:
            if j == current[-1] + 1:
                current.append(j)
            else:
                groups.append(current)
                current = [j]
        groups.append(current)
    return groups

def fill_horizontal(g_out: List[List[int]], i: int, l: int, r: int, c: int, skip_center: bool = False, center_j: int = -1):
    for k in range(l, r + 1):
        if g_out[i][k] == 0 and not (skip_center and k == center_j):
            g_out[i][k] = c

def fill_vertical(g_out: List[List[int]], i: int, j: int, c: int, n: int):
    for dr in [-1, 1]:
        ii = i + dr
        if 1 <= ii < n - 1 and g_out[ii][j] == 0:
            g_out[ii][j] = c

def do_single(g_out: List[List[int]], j: int, grid: List[List[int]], row_color_col: int, m: int, n: int, r_cs: defaultdict, half: int, num_specials: Counter, border: int):
    c = grid[border][j]
    if border == 0:
        qual = [ii for ii in r_cs.get(c, []) if ii <= j]
    else:
        qual = [ii for ii in r_cs.get(c, []) if ii >= n - 1 - j]
    if not qual:
        return
    do_skip = (j > half) and (num_specials[c] == 1)
    l = max(row_color_col + 1, j - 1)
    r = min(m - 2, j + 1)
    for i in qual:
        fill_horizontal(g_out, i, l, r, c, do_skip, j)
        fill_vertical(g_out, i, j, c, n)

def do_pair(g_out: List[List[int]], j1: int, j2: int, grid: List[List[int]], row_color_col: int, m: int, n: int, r_cs: defaultdict, half: int, num_specials: Counter, border: int):
    # Single for j1 with possible skip
    do_single(g_out, j1, grid, row_color_col, m, n, r_cs, half, num_specials, border)
    # For j2, horizontal in qual without skip, vertical
    c2 = grid[border][j2]
    if border == 0:
        qual2 = [ii for ii in r_cs.get(c2, []) if ii <= j2]
    else:
        qual2 = [ii for ii in r_cs.get(c2, []) if ii >= n - 1 - j2]
    if not qual2:
        return
    l2 = max(row_color_col + 1, j2 - 1)
    r2 = min(m - 2, j2 + 1)
    for i in qual2:
        fill_horizontal(g_out, i, l2, r2, c2, skip_center=False)
        fill_vertical(g_out, i, j2, c2, n)
    # Extra horizontal in adj of qual2 without skip
    for i in qual2:
        for dr in [-1, 1]:
            ii = i + dr
            if 1 <= ii < n - 1:
                fill_horizontal(g_out, ii, l2, r2, c2, skip_center=False)

def program(g: List[List[int]]) -> List[List[int]]:
    n = len(g)
    if n < 3:
        return [row[:] for row in g]
    m = len(g[0])
    middle_rows = list(range(1, n - 1))
    spine = find_spine(g, middle_rows, m)
    if spine == -1 or spine >= m - 1:
        return [row[:] for row in g]
    row_color_col = spine + 1
    g_out = [row[:] for row in g]
    # Set last column for middle rows
    for i in middle_rows:
        c = g_out[i][row_color_col]
        if c != 0:
            g_out[i][m - 1] = c
    # Forbidden colors from top and bottom >= spine
    forbidden = set()
    for br in [0, n - 1]:
        for j in range(spine, m):
            cj = g[br][j]
            if cj != 0:
                forbidden.add(cj)
    # Clear forbidden in columns < spine, all rows
    for i in range(n):
        for j in range(spine):
            if g_out[i][j] in forbidden:
                g_out[i][j] = 0
    # r_cs from row_color_col in middle rows
    r_cs = defaultdict(list)
    for i in middle_rows:
        c = g_out[i][row_color_col]
        if c != 0:
            r_cs[c].append(i)
    half = m // 2
    # Process top (border 0)
    top_specials = find_specials(g, row_color_col, m, 0)
    num_specials_top = Counter(g[0][j] for j in top_specials)
    valid_top = [j for j in top_specials if len(r_cs.get(g[0][j], [])) == num_specials_top[g[0][j]]]
    groups_top = group_specials(valid_top)
    for group in groups_top:
        glen = len(group)
        if glen == 1:
            do_single(g_out, group[0], g, row_color_col, m, n, r_cs, half, num_specials_top, 0)
        elif glen == 2:
            do_pair(g_out, group[0], group[1], g, row_color_col, m, n, r_cs, half, num_specials_top, 0)
        else:
            for jj in group:
                do_single(g_out, jj, g, row_color_col, m, n, r_cs, half, num_specials_top, 0)
    # Process bottom (border n-1)
    bottom_specials = find_specials(g, row_color_col, m, n - 1)
    num_specials_bottom = Counter(g[n - 1][j] for j in bottom_specials)
    valid_bottom = [j for j in bottom_specials if len(r_cs.get(g[n - 1][j], [])) == num_specials_bottom[g[n - 1][j]]]
    groups_bottom = group_specials(valid_bottom)
    for group in groups_bottom:
        glen = len(group)
        if glen == 1:
            do_single(g_out, group[0], g, row_color_col, m, n, r_cs, half, num_specials_bottom, n - 1)
        elif glen == 2:
            do_pair(g_out, group[0], group[1], g, row_color_col, m, n, r_cs, half, num_specials_bottom, n - 1)
        else:
            for jj in group:
                do_single(g_out, jj, g, row_color_col, m, n, r_cs, half, num_specials_bottom, n - 1)
    return g_out
```