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

def handle_single(g: List[List[int]], j: int, row_color_col: int, m: int, n: int, r_cs: defaultdict, half: int, count_c: Counter, skip_center: bool = True):
    c = g[0][j]
    qual = [i for i in r_cs.get(c, []) if i <= j]
    do_skip = skip_center and (j > half) and (count_c[c] == 1)
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

def handle_pair(g: List[List[int]], j1: int, j2: int, row_color_col: int, m: int, n: int, r_cs: defaultdict, half: int, count_c: Counter):
    c1 = g[0][j1]
    c2 = g[0][j2]
    qual1 = [i for i in r_cs.get(c1, []) if i <= j1]
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
    qual2 = [i for i in r_cs.get(c2, []) if i <= j2]
    l2 = max(row_color_col + 1, j2 - 1)
    r2 = min(m - 2, j2 + 1)
    for i in qual2:
        for k in range(l2, r2 + 1):
            if g[i][k] == 0:
                g[i][k] = c2
        for dr in [-1, 1]:
            ii = i + dr
            if 1 <= ii < n - 1:
                for k in range(l2, r2 + 1):
                    if g[ii][k] == 0:
                        g[ii][k] = c2

def program(g: List[List[int]]) -> List[List[int]]:
    g_out = [row[:] for row in g]
    n = len(g_out)
    m = len(g_out[0]) if n > 0 else 0
    if n < 3:
        return g_out
    middle_rows = list(range(1, n - 1))
    spine = find_spine(g_out, middle_rows, m)
    if spine == -1 or spine + 1 >= m:
        return g_out
    row_color_col = spine + 1
    forbidden = set()
    for rr in [0, n - 1]:
        for j in range(spine, m):
            c = g_out[rr][j]
            if c != 0:
                forbidden.add(c)
    for r in range(n):
        for j in range(spine):
            c = g_out[r][j]
            if c != 0 and c in forbidden:
                g_out[r][j] = 0
    for i in middle_rows:
        c = g_out[i][row_color_col]
        if c != 0:
            g_out[i][m - 1] = c
    r_cs = defaultdict(list)
    for i in middle_rows:
        c = g_out[i][row_color_col]
        if c != 0:
            r_cs[c].append(i)
    potential = []
    for j in range(row_color_col + 1, m - 1):
        c = g_out[0][j]
        if c != 0 and c != g_out[0][j - 1] and c != g_out[0][j + 1]:
            potential.append(j)
    top_right = g_out[0][row_color_col + 1 : m]
    count_c = Counter(top_right)
    isol_count = defaultdict(int)
    for j in potential:
        isol_count[g_out[0][j]] += 1
    processed = []
    for j in potential:
        c = g_out[0][j]
        if count_c[c] == isol_count[c]:
            processed.append(j)
    groups = group_specials(processed)
    half = m // 2
    for group in groups:
        glen = len(group)
        if glen == 1:
            handle_single(g_out, group[0], row_color_col, m, n, r_cs, half, count_c)
        elif glen == 2:
            handle_pair(g_out, group[0], group[1], row_color_col, m, n, r_cs, half, count_c)
        else:
            for jj in group:
                handle_single(g_out, jj, row_color_col, m, n, r_cs, half, count_c, skip_center=False)
    return g_out
```