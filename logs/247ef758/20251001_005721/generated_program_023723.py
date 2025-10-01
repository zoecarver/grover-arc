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

def find_specials(grid: List[List[int]], row_color_col: int, m: int) -> List[int]:
    special = []
    for j in range(row_color_col + 1, m - 1):
        c = grid[0][j]
        if c != 0 and c != grid[0][j - 1] and c != grid[0][j + 1]:
            special.append(j)
    return special

def program(g: List[List[int]]) -> List[List[int]]:
    n = len(g)
    if n == 0:
        return g
    m = len(g[0])
    if n < 3:
        return [row[:] for row in g]
    g_out = [row[:] for row in g]
    middle_rows = list(range(1, n - 1))
    spine = find_spine(g, middle_rows, m)
    if spine == -1 or spine + 1 >= m:
        return g_out
    row_color_col = spine + 1
    for i in middle_rows:
        c = g_out[i][row_color_col]
        if c != 0:
            g_out[i][m - 1] = c
    forbidden = set()
    for row in (0, n - 1):
        for j in range(spine, m):
            cj = g[row][j]
            if cj != 0:
                forbidden.add(cj)
    for i in range(n):
        for j in range(spine):
            if g_out[i][j] != 0 and g_out[i][j] in forbidden:
                g_out[i][j] = 0
    r_cs = defaultdict(list)
    for i in middle_rows:
        c = g_out[i][row_color_col]
        if c != 0:
            r_cs[c].append(i)
    special = find_specials(g_out, row_color_col, m)
    if not special:
        return g_out
    count_c = Counter()
    for j in range(row_color_col + 1, m):
        cj = g_out[0][j]
        if cj != 0:
            count_c[cj] += 1
    num_specials_c = Counter(g_out[0][j] for j in special)
    half = m // 2
    for j in special:
        c = g_out[0][j]
        if len(r_cs[c]) != num_specials_c[c]:
            continue
        qual = [ii for ii in r_cs[c] if ii <= j]
        if not qual:
            continue
        do_skip = (j > half) and (count_c[c] == 1)
        l = max(row_color_col + 1, j - 1)
        r = min(m - 2, j + 1)
        for ii in qual:
            for k in range(l, r + 1):
                if g_out[ii][k] == 0 and not (do_skip and k == j):
                    g_out[ii][k] = c
            for drr in [-1, 1]:
                iii = ii + drr
                if 1 <= iii < n - 1 and g_out[iii][j] == 0:
                    g_out[iii][j] = c
    for idx in range(len(special) - 1):
        j1 = special[idx]
        j2 = special[idx + 1]
        if j2 != j1 + 1:
            continue
        c1 = g_out[0][j1]
        c2 = g_out[0][j2]
        if len(r_cs[c1]) == num_specials_c[c1] and len(r_cs[c2]) == num_specials_c[c2]:
            qual2 = [ii for ii in r_cs[c2] if ii <= j2]
            l2 = max(row_color_col + 1, j2 - 1)
            r2 = min(m - 2, j2 + 1)
            for ii in qual2:
                for drr in [-1, 1]:
                    iii = ii + drr
                    if 1 <= iii < n - 1:
                        for k in range(l2, r2 + 1):
                            if g_out[iii][k] == 0:
                                g_out[iii][k] = c2
    return g_out
```