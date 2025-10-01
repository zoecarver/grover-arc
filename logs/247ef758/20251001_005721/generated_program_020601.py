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

def process_group(g_out: List[List[int]], group: List[int], row_color_col: int, m: int, r_cs: dict, n: int, is_pair: bool) -> List[List[int]]:
    color_specials = defaultdict(list)
    for j in group:
        color_specials[g_out[0][j]].append(j)
    half = m // 2
    for c, specs in color_specials.items():
        max_j = max(specs) if specs else 0
        qual_homes = [h for h in r_cs.get(c, []) if h <= max_j]
        num_specs = len(specs)
        if len(qual_homes) != num_specs:
            continue
        for h in qual_homes:
            for j in specs:
                if h > j:
                    continue
                l = max(row_color_col + 1, j - 1)
                r = min(m - 2, j + 1)
                count_top = sum(1 for jj in range(m) if g_out[0][jj] == c)
                fill_center = (count_top >= 2) or (j == half)
                if is_pair:
                    fill_center = True
                center_was_zero = (g_out[h][j] == 0)
                skipped_center = False
                for jj in range(l, r + 1):
                    if g_out[h][jj] == 0:
                        if jj == j and not fill_center:
                            skipped_center = True
                            continue
                        g_out[h][jj] = c
                if skipped_center and center_was_zero:
                    near_end = (j + 1 == m - 2)
                    if not near_end:
                        for dr in [-1, 1]:
                            nh = h + dr
                            if 1 <= nh <= n - 2 and g_out[nh][j] == 0:
                                g_out[nh][j] = c
    return g_out

def program(g: List[List[int]]) -> List[List[int]]:
    n = len(g)
    if n == 0:
        return g
    m = len(g[0])
    g_out = [row[:] for row in g]
    middle_rows = list(range(1, n - 1)) if n > 2 else []
    if not middle_rows:
        return g_out
    spine = find_spine(g_out, middle_rows, m)
    if spine == -1 or spine + 1 >= m:
        return g_out
    row_color_col = spine + 1
    for i in middle_rows:
        c = g_out[i][row_color_col]
        if c != 0:
            g_out[i][m - 1] = c
    forbidden = set()
    for i in [0, n - 1]:
        for j in range(spine, m):
            if g_out[i][j] != 0:
                forbidden.add(g_out[i][j])
    for i in middle_rows:
        for j in range(spine):
            if g_out[i][j] != 0 and g_out[i][j] in forbidden:
                g_out[i][j] = 0
    r_cs = defaultdict(list)
    for i in middle_rows:
        c = g_out[i][row_color_col]
        if c != 0:
            r_cs[c].append(i)
    specials = find_specials(g_out, row_color_col, m)
    groups = group_specials(specials)
    r_cs_dict = dict(r_cs)
    for group in groups:
        glen = len(group)
        if glen == 2:
            j1 = group[0]
            j2 = group[1]
            c1 = g_out[0][j1]
            c2 = g_out[0][j2]
            g_out = process_group(g_out, group, row_color_col, m, r_cs_dict, n, True)
            qual_h1 = [h for h in r_cs_dict.get(c1, []) if h <= j1]
            qual_h2 = [h for h in r_cs_dict.get(c2, []) if h <= j2]
            if len(qual_h1) == 1 and len(qual_h2) == 1 and qual_h2[0] == qual_h1[0] + 2:
                h1 = qual_h1[0]
                h2 = qual_h2[0]
                if h1 > 1:
                    uu = h1 - 1
                    if g_out[uu][j1] == 0:
                        g_out[uu][j1] = c1
                gap = h1 + 1
                if 1 <= gap <= n - 2:
                    if g_out[gap][j1] == 0:
                        g_out[gap][j1] = c1
                    if g_out[gap][j2] == 0:
                        g_out[gap][j2] = c2
                    if j2 + 1 < m and g_out[gap][j2 + 1] == 0:
                        g_out[gap][j2 + 1] = c2
                ll = h2 + 1
                if 1 <= ll <= n - 2:
                    for jj in range(j1, j1 + 3):
                        if jj < m and g_out[ll][jj] == 0:
                            g_out[ll][jj] = c2
        else:
            g_out = process_group(g_out, group, row_color_col, m, r_cs_dict, n, False)
    return g_out
```