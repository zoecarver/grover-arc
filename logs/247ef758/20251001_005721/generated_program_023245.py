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

def find_specials(g: List[List[int]], row_color_col: int, m: int, border: int = 0) -> List[int]:
    special = []
    for j in range(row_color_col + 1, m - 1):
        c = g[border][j]
        left = g[border][j - 1]
        right = g[border][j + 1]
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

def do_single(g: List[List[int]], j: int, row_color_col: int, m: int, n: int, r_cs: defaultdict, half: int, count_c: Counter, border: int = 0):
    c = g[border][j]
    qual = [i for i in r_cs.get(c, []) if 1 <= i < n - 1 and (i <= j if border == 0 else i >= n - 1 - j)]
    do_skip = (j > half) and (count_c[c] == 1)
    l = max(row_color_col + 1, j - 1)
    r = min(m - 2, j + 1)
    for i in qual:
        for k in range(l, r + 1):
            if g[i][k] == 0 and not (do_skip and k == j):
                g[i][k] = c
        for dr in [-1, 1]:
            ii = i + dr
            if 1 <= ii < n - 1 and g[ii][j] == 0:
                g[ii][j] = c

def do_pair(g: List[List[int]], j1: int, j2: int, row_color_col: int, m: int, n: int, r_cs: defaultdict, half: int, count_c: Counter, border: int = 0):
    # First special
    c1 = g[border][j1]
    qual1 = [i for i in r_cs.get(c1, []) if 1 <= i < n - 1 and (i <= j1 if border == 0 else i >= n - 1 - j1)]
    l1 = max(row_color_col + 1, j1 - 1)
    r1 = min(m - 2, j1 + 1)
    for i in qual1:
        for k in range(l1, r1 + 1):
            if g[i][k] == 0:
                g[i][k] = c1
        for dr in [-1, 1]:
            ii = i + dr
            if 1 <= ii < n - 1 and g[ii][j1] == 0:
                g[ii][j1] = c1
    # Second special
    c2 = g[border][j2]
    qual2 = [i for i in r_cs.get(c2, []) if 1 <= i < n - 1 and (i <= j2 if border == 0 else i >= n - 1 - j2)]
    l2 = max(row_color_col + 1, j2 - 1)
    r2 = min(m - 2, j2 + 1)
    for i in qual2:
        for k in range(l2, r2 + 1):
            if g[i][k] == 0:
                g[i][k] = c2
        for dr in [-1, 1]:
            ii = i + dr
            if 1 <= ii < n - 1 and g[ii][j2] == 0:
                g[ii][j2] = c2
        # Extra full horizontal in adjacent rows for second special
        for dr in [-1, 1]:
            ii = i + dr
            if 1 <= ii < n - 1:
                for k in range(l2, r2 + 1):
                    if g[ii][k] == 0:
                        g[ii][k] = c2

def program(g: List[List[int]]) -> List[List[int]]:
    n = len(g)
    if n == 0:
        return g
    m = len(g[0])
    g_out = [row[:] for row in g]
    if n < 3:
        return g_out
    middle_rows = list(range(1, n - 1))
    spine = find_spine(g_out, middle_rows, m)
    if spine == -1:
        return g_out
    row_color_col = spine + 1
    if row_color_col >= m:
        return g_out
    # Set last column for middle rows
    for i in middle_rows:
        c = g_out[i][row_color_col]
        g_out[i][m - 1] = c
    # Forbidden colors from top and bottom starting from spine
    forbidden = set()
    for jj in range(spine, m):
        if g_out[0][jj] != 0:
            forbidden.add(g_out[0][jj])
        if g_out[n - 1][jj] != 0:
            forbidden.add(g_out[n - 1][jj])
    # Clear forbidden colors left of spine in all rows
    for i in range(n):
        for j in range(spine):
            if g_out[i][j] != 0 and g_out[i][j] in forbidden:
                g_out[i][j] = 0
    # Row colors
    r_cs = defaultdict(list)
    for i in middle_rows:
        c = g_out[i][row_color_col]
        if c != 0:
            r_cs[c].append(i)
    half = m // 2
    # Propagate from top
    specials_top = find_specials(g_out, row_color_col, m, border=0)
    groups_top = group_specials(specials_top)
    count_c_top = Counter(g_out[0][jj] for jj in range(row_color_col, m) if g_out[0][jj] != 0)
    for group in groups_top:
        glen = len(group)
        if glen == 1:
            do_single(g_out, group[0], row_color_col, m, n, r_cs, half, count_c_top, border=0)
        elif glen == 2:
            do_pair(g_out, group[0], group[1], row_color_col, m, n, r_cs, half, count_c_top, border=0)
        elif glen == 3:
            do_single(g_out, group[0], row_color_col, m, n, r_cs, half, count_c_top, border=0)
            do_single(g_out, group[2], row_color_col, m, n, r_cs, half, count_c_top, border=0)
        else:
            for js in group:
                do_single(g_out, js, row_color_col, m, n, r_cs, half, count_c_top, border=0)
    # Propagate from bottom
    specials_bottom = find_specials(g_out, row_color_col, m, border=n-1)
    groups_bottom = group_specials(specials_bottom)
    count_c_bottom = Counter(g_out[n-1][jj] for jj in range(row_color_col, m) if g_out[n-1][jj] != 0)
    for group in groups_bottom:
        glen = len(group)
        if glen == 1:
            do_single(g_out, group[0], row_color_col, m, n, r_cs, half, count_c_bottom, border=n-1)
        elif glen == 2:
            do_pair(g_out, group[0], group[1], row_color_col, m, n, r_cs, half, count_c_bottom, border=n-1)
        elif glen == 3:
            do_single(g_out, group[0], row_color_col, m, n, r_cs, half, count_c_bottom, border=n-1)
            do_single(g_out, group[2], row_color_col, m, n, r_cs, half, count_c_bottom, border=n-1)
        else:
            for js in group:
                do_single(g_out, js, row_color_col, m, n, r_cs, half, count_c_bottom, border=n-1)
    return g_out
```