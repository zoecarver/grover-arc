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

def do_single(g: List[List[int]], j: int, c: int, row_color_col: int, m: int, n: int, r_cs: defaultdict, thresh: int, middle_start: int, middle_end: int):
    qual = [i for i in r_cs[c] if i <= j]
    if not qual:
        return
    l = max(row_color_col + 1, j - 1)
    r = min(m - 2, j + 1)
    do_skip = (j >= thresh) and (len(r_cs[c]) == 1)
    for i in qual:
        for k in range(l, r + 1):
            if g[i][k] == 0 and not (do_skip and k == j):
                g[i][k] = c
        for dr in [-1, 1]:
            ii = i + dr
            if middle_start <= ii < middle_end and g[ii][j] == 0:
                g[ii][j] = c

def do_pair(g: List[List[int]], j1: int, j2: int, row_color_col: int, m: int, n: int, r_cs: defaultdict, middle_start: int, middle_end: int):
    c1 = g[0][j1]
    c2 = g[0][j2]
    qual1 = [i for i in r_cs[c1] if i <= j1]
    qual2 = [i for i in r_cs[c2] if i <= j2]
    # First special
    l1 = max(row_color_col + 1, j1 - 1)
    r1 = min(m - 2, j1 + 1)
    for i in qual1:
        for k in range(l1, r1 + 1):
            if g[i][k] == 0:
                g[i][k] = c1
        for dr in [-1, 1]:
            ii = i + dr
            if middle_start <= ii < middle_end and g[ii][j1] == 0:
                g[ii][j1] = c1
    # Second special
    l2 = max(row_color_col + 1, j2 - 1)
    r2 = min(m - 2, j2 + 1)
    for i in qual2:
        for k in range(l2, r2 + 1):
            if g[i][k] == 0:
                g[i][k] = c2
        for dr in [-1, 1]:
            ii = i + dr
            if middle_start <= ii < middle_end:
                for k in range(l2, r2 + 1):
                    if g[ii][k] == 0:
                        g[ii][k] = c2

def program(g: List[List[int]]) -> List[List[int]]:
    if not g:
        return []
    n = len(g)
    if n == 0:
        return []
    m = len(g[0])
    out = [row[:] for row in g]
    if n < 3:
        return out
    middle_rows = list(range(1, n - 1))
    spine = find_spine(out, middle_rows, m)
    if spine == -1 or spine >= m - 1:
        return out
    row_color_col = spine + 1
    # Propagate to last column
    for i in middle_rows:
        c = out[i][row_color_col]
        if c != 0:
            out[i][m - 1] = c
    # Forbidden colors
    forbidden = set()
    for i in (0, n - 1):
        for j in range(spine, m):
            if out[i][j] != 0:
                forbidden.add(out[i][j])
    # Clear left of spine
    for i in range(n):
        for j in range(spine):
            if out[i][j] in forbidden:
                out[i][j] = 0
    # Row colors
    r_cs = defaultdict(list)
    for i in middle_rows:
        c = out[i][row_color_col]
        if c != 0:
            r_cs[c].append(i)
    # Specials from top
    specials = []
    for j in range(row_color_col + 1, m - 1):
        c = out[0][j]
        if c != 0 and c != out[0][j - 1] and c != out[0][j + 1]:
            specials.append(j)
    # Num specials per color
    num_specials_dict = Counter(out[0][j] for j in specials)
    # Propagatable specials
    prop_specials = [j for j in specials if len(r_cs[out[0][j]]) == num_specials_dict[out[0][j]]]
    # Groups
    groups = group_specials(prop_specials)
    # Threshold for skip
    half = m // 2
    thresh = half + 2
    middle_start = 1
    middle_end = n - 1
    # Process groups
    for group in groups:
        if len(group) == 2:
            j1 = group[0]
            j2 = group[1]
            do_pair(out, j1, j2, row_color_col, m, n, r_cs, middle_start, middle_end)
        else:
            for j in group:
                c = out[0][j]
                do_single(out, j, c, row_color_col, m, n, r_cs, thresh, middle_start, middle_end)
    return out
```