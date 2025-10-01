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

def program(g: List[List[int]]) -> List[List[int]]:
    n = len(g)
    if n < 3:
        return [row[:] for row in g]
    m = len(g[0])
    middle_rows = list(range(1, n - 1))
    spine = find_spine(g, middle_rows, m)
    if spine == -1 or spine + 1 >= m:
        return [row[:] for row in g]
    row_color_col = spine + 1
    g_out = [row[:] for row in g]
    for i in middle_rows:
        g_out[i][m - 1] = g_out[i][row_color_col]
    forbidden = set()
    for row in (0, n - 1):
        for j in range(spine, m):
            c = g_out[row][j]
            if c != 0:
                forbidden.add(c)
    for i in middle_rows:
        for j in range(spine):
            c = g_out[i][j]
            if c != 0 and c in forbidden:
                g_out[i][j] = 0
    r_cs = defaultdict(list)
    for i in middle_rows:
        c = g_out[i][row_color_col]
        if c != 0:
            r_cs[c].append(i)
    def find_specials(grid_out: List[List[int]], rcc: int, mm: int) -> List[int]:
        special = []
        for j in range(rcc + 1, mm - 1):
            c = grid_out[0][j]
            if c != 0 and c != grid_out[0][j - 1] and c != grid_out[0][j + 1]:
                special.append(j)
        return special
    specials = find_specials(g_out, row_color_col, m)
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
    groups = group_specials(specials)
    half = m // 2
    for group in groups:
        glen = len(group)
        if glen == 0:
            continue
        if glen == 1:
            j = group[0]
            c = g_out[0][j]
            count_c = sum(1 for k in range(row_color_col + 1, m) if g_out[0][k] == c)
            skip_center = (count_c == 1 and j > half)
            homes = [ii for ii in r_cs.get(c, []) if ii <= j]
            for i in homes:
                left = max(row_color_col, j - 1)
                right = min(m - 2, j + 1)
                for k in range(left, right + 1):
                    if g_out[i][k] == 0 and not (skip_center and k == j):
                        g_out[i][k] = c
                for di in [-1, 1]:
                    ii = i + di
                    if 1 <= ii < n - 1 and g_out[ii][j] == 0:
                        g_out[ii][j] = c
        else:
            # For glen >= 2, handle without skip_center
            skip = False
            if glen == 2:
                # First
                j = group[0]
                c = g_out[0][j]
                homes = [ii for ii in r_cs.get(c, []) if ii <= j]
                for i in homes:
                    left = max(row_color_col, j - 1)
                    right = min(m - 2, j + 1)
                    for k in range(left, right + 1):
                        if g_out[i][k] == 0 and not (skip and k == j):
                            g_out[i][k] = c
                    for di in [-1, 1]:
                        ii = i + di
                        if 1 <= ii < n - 1 and g_out[ii][j] == 0:
                            g_out[ii][j] = c
                # Second
                j = group[1]
                c = g_out[0][j]
                homes2 = [ii for ii in r_cs.get(c, []) if ii <= j]
                for i in homes2:
                    left = max(row_color_col, j - 1)
                    right = min(m - 2, j + 1)
                    for k in range(left, right + 1):
                        if g_out[i][k] == 0 and not (skip and k == j):
                            g_out[i][k] = c
                    for di in [-1, 1]:
                        ii = i + di
                        if 1 <= ii < n - 1 and g_out[ii][j] == 0:
                            g_out[ii][j] = c
                # Extra for second: 3-wide in adj rows
                for i in homes2:
                    for di in [-1, 1]:
                        ii = i + di
                        if 1 <= ii < n - 1:
                            left = max(row_color_col, j - 1)
                            right = min(m - 2, j + 1)
                            for k in range(left, right + 1):
                                if g_out[ii][k] == 0:
                                    g_out[ii][k] = c
            else:
                # glen > 2, treat each as non-skipping single
                for jj in group:
                    c = g_out[0][jj]
                    homes = [ii for ii in r_cs.get(c, []) if ii <= jj]
                    for i in homes:
                        left = max(row_color_col, jj - 1)
                        right = min(m - 2, jj + 1)
                        for k in range(left, right + 1):
                            if g_out[i][k] == 0 and not (skip and k == jj):
                                g_out[i][k] = c
                        for di in [-1, 1]:
                            ii = i + di
                            if 1 <= ii < n - 1 and g_out[ii][jj] == 0:
                                g_out[ii][jj] = c
    return g_out
```