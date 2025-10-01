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

def find_specials(grid: List[List[int]], row_color_col: int, m: int, border: int = 0) -> List[int]:
    special = []
    for j in range(row_color_col + 1, m - 1):
        c = grid[border][j]
        if c != 0 and c != grid[border][j - 1] and c != grid[border][j + 1]:
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

def program(g: List[List[int]]) -> List[List[int]]:
    n = len(g)
    if n == 0:
        return g
    m = len(g[0])
    if n < 3:
        return [row[:] for row in g]
    middle_rows = list(range(1, n - 1))
    spine = find_spine(g, middle_rows, m)
    if spine == -1:
        return [row[:] for row in g]
    row_color_col = min(spine + 1, m - 1)
    forbidden = set()
    for i in (0, n - 1):
        for j in range(spine, m):
            c = g[i][j]
            if c != 0:
                forbidden.add(c)
    g_out = [row[:] for row in g]
    for i in range(n):
        for j in range(spine):
            if g_out[i][j] in forbidden:
                g_out[i][j] = 0
    for i in middle_rows:
        c = g_out[i][row_color_col]
        if c != 0:
            g_out[i][m - 1] = c
    r_cs = defaultdict(list)
    for i in middle_rows:
        c = g_out[i][row_color_col]
        if c != 0:
            r_cs[c].append(i)

    def propagate_from_border(border_row: int, is_top: bool):
        if not is_top and max(find_specials(g_out, row_color_col, m, border_row) or [0]) <= m // 2:
            return
        special = find_specials(g_out, row_color_col, m, border_row)
        groups = group_specials(special)
        count_c = Counter(g_out[border_row][row_color_col + 1 :])
        half = m // 2
        for group in groups:
            glen = len(group)
            if glen == 2:
                j1 = group[0]
                c1 = g_out[border_row][j1]
                min_i = 0 if not is_top else -float('inf')
                max_i = n - 1 if not is_top else float('inf')
                qual1 = [ii for ii in r_cs[c1] if (min_i <= ii <= j1 if is_top else n - 1 - j1 <= ii <= max_i)]
                l1 = max(row_color_col + 1, j1 - 1)
                r1 = min(m - 2, j1 + 1)
                do_skip1 = (j1 > half + 1) and (count_c[c1] == 1)
                for i in qual1:
                    for k in range(l1, r1 + 1):
                        if g_out[i][k] == 0 and not (do_skip1 and k == j1):
                            g_out[i][k] = c1
                    for dr in [-1, 1]:
                        ii = i + dr
                        if 1 <= ii < n - 1 and g_out[ii][j1] == 0:
                            g_out[ii][j1] = c1
                j2 = group[1]
                c2 = g_out[border_row][j2]
                qual2 = [ii for ii in r_cs[c2] if (min_i <= ii <= j2 if is_top else n - 1 - j2 <= ii <= max_i)]
                l2 = max(row_color_col + 1, j2 - 1)
                r2 = min(m - 2, j2 + 1)
                do_skip2 = (j2 > half + 1) and (count_c[c2] == 1)
                for i in qual2:
                    for k in range(l2, r2 + 1):
                        if g_out[i][k] == 0 and not (do_skip2 and k == j2):
                            g_out[i][k] = c2
                    for dr in [-1, 1]:
                        ii = i + dr
                        if 1 <= ii < n - 1 and g_out[ii][j2] == 0:
                            g_out[ii][j2] = c2
                for i in qual2:
                    for dr in [-1, 1]:
                        ii = i + dr
                        if 1 <= ii < n - 1:
                            for dk in [-1, 1]:
                                k = j2 + dk
                                if l2 <= k <= r2 and g_out[ii][k] == 0:
                                    g_out[ii][k] = c2
            else:
                local_js = []
                for jj in group:
                    cc = g_out[border_row][jj]
                    num_in_group = sum(1 for kkk in group if g_out[border_row][kkk] == cc)
                    if count_c[cc] == num_in_group:
                        local_js.append(jj)
                for j in local_js:
                    c = g_out[border_row][j]
                    min_i = 0 if not is_top else -float('inf')
                    max_i = n - 1 if not is_top else float('inf')
                    qual = [ii for ii in r_cs[c] if (min_i <= ii <= j if is_top else n - 1 - j <= ii <= max_i)]
                    if not qual:
                        continue
                    is_left_end = (j == min(group) and glen > 2)
                    is_right_end = (j == max(group) and glen > 2)
                    l = max(row_color_col + 1, j - 1)
                    r = min(m - 2, j + 1)
                    if is_left_end:
                        r = min(m - 2, j + 2)
                    if is_right_end:
                        l = j
                    do_skip = (j > half + 1) and (count_c[c] == 1)
                    only_center = (glen == 1 and j > half + 3)
                    if only_center:
                        l = r = j
                    for i in qual:
                        for k in range(l, r + 1):
                            if g_out[i][k] == 0 and not (do_skip and k == j):
                                g_out[i][k] = c
                    is_small_single = (glen == 1)
                    for i in qual:
                        # upper
                        ii = i - 1
                        if 1 <= ii < n - 1:
                            if not (is_small_single and j > half + 3):
                                if is_small_single and j <= half + 1:
                                    k_fill = j - 1
                                    if row_color_col + 1 <= k_fill <= m - 2 and g_out[ii][k_fill] == 0:
                                        g_out[ii][k_fill] = c
                                elif j > half:
                                    if g_out[ii][j] == 0:
                                        g_out[ii][j] = c
                        # lower
                        ii = i + 1
                        if 1 <= ii < n - 1:
                            if is_small_single and j <= half + 1:
                                k_fill = j - 1
                                if row_color_col + 1 <= k_fill <= m - 2 and g_out[ii][k_fill] == 0:
                                    g_out[ii][k_fill] = c
                            else:
                                if g_out[ii][j] == 0:
                                    g_out[ii][j] = c

    propagate_from_border(0, True)
    propagate_from_border(n - 1, False)
    return g_out
```