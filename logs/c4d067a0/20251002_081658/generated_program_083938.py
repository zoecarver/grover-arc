```python
from typing import List
from collections import Counter

def get_background(g: List[List[int]]) -> int:
    flat = [cell for row in g for cell in row]
    c = Counter(flat)
    return c.most_common(1)[0][0]

def get_levels(n: int) -> List[int]:
    L = (n - 1) // 6
    return [2 * i + 1 for i in range(L)]

def get_upper_cols(g: List[List[int]], levels: List[int], bg: int, n: int) -> List[int]:
    cols = set()
    for r in levels:
        for c in range(n):
            if g[r][c] != bg:
                cols.add(c)
    return sorted(cols)

def get_upper_colors(g: List[List[int]], levels: List[int], upper_cols: List[int], n: int) -> List[List[int]]:
    S = len(upper_cols)
    L = len(levels)
    colors = [[0] * S for _ in range(L)]
    for i in range(L):
        for jj in range(S):
            c = upper_cols[jj]
            if c < n:
                colors[i][jj] = g[levels[i]][c]
    return colors

def find_seed_block(g: List[List[int]], n: int, bg: int) -> tuple:
    max_h = 0
    best_start = -1
    best_pat = set()
    for r_start in range(n // 2, n):
        pat = {c for c in range(n) if g[r_start][c] != bg}
        if not pat:
            continue
        h = 1
        r = r_start + 1
        while r < n:
            pat_r = {c for c in range(n) if g[r][c] != bg}
            if pat_r == pat:
                h += 1
                r += 1
            else:
                break
        if h > max_h:
            max_h = h
            best_start = r_start
            best_pat = pat
    return best_start, max_h, best_pat

def get_lower_groups(pat_set: set, n: int) -> List[List[int]]:
    if not pat_set:
        return []
    cl = sorted(pat_set)
    groups = []
    if not cl:
        return groups
    curr_start = cl[0]
    prev = cl[0]
    for i in range(1, len(cl)):
        if cl[i] == prev + 1:
            prev = cl[i]
        else:
            group = list(range(curr_start, prev + 1))
            if all(0 <= c < n for c in group):
                groups.append(group)
            curr_start = cl[i]
            prev = cl[i]
    group = list(range(curr_start, prev + 1))
    if all(0 <= c < n for c in group):
        groups.append(group)
    return groups

def find_k_seed(g: List[List[int]], upper_colors: List[List[int]], lower_pos: List[List[int]], start: int, B: int, S: int, n: int) -> int:
    L = len(upper_colors)
    for k in range(L - 1, -1, -1):
        match = True
        for b in range(B):
            if B == 2 and S == 3:
                s = 0 if b == 0 else 2
            else:
                s = b
            if s >= S:
                match = False
                break
            pos = lower_pos[b]
            if not pos:
                continue
            col_lower = g[start][pos[0]]
            uniform = all(g[start][c] == col_lower and 0 <= c < n for c in pos)
            if not uniform:
                match = False
                break
            col_upper = upper_colors[k][s]
            if col_upper != col_lower:
                match = False
                break
        if match:
            return k
    return -1

def is_position_empty(g: List[List[int]], s_j: int, h: int, n: int, lower_pos: List[List[int]], bg: int) -> bool:
    all_pos = [c for pos in lower_pos for c in pos if 0 <= c < n]
    for rr in range(s_j, s_j + h):
        if rr >= n:
            return False
        for c in all_pos:
            if g[rr][c] != bg:
                return False
    return True

def set_level(g_out: List[List[int]], s_j: int, h: int, n: int, lower_pos: List[List[int]], col_list: List[int], bg: int):
    for b in range(len(lower_pos)):
        col = col_list[b]
        if col == bg:
            continue
        pos = lower_pos[b]
        for rr in range(s_j, s_j + h):
            if rr >= n:
                break
            for c in pos:
                if c < n:
                    g_out[rr][c] = col

def program(g: List[List[int]]) -> List[List[int]]:
    n = len(g)
    bg = get_background(g)
    levels = get_levels(n)
    L = len(levels)
    upper_cols = get_upper_cols(g, levels, bg, n)
    S = len(upper_cols)
    upper_colors = get_upper_colors(g, levels, upper_cols, n)
    start, h, pat = find_seed_block(g, n, bg)
    if start == -1 or h == 0:
        return [row[:] for row in g]
    lower_pos = get_lower_groups(pat, n)
    B = len(lower_pos)
    k_seed = find_k_seed(g, upper_colors, lower_pos, start, B, S, n)
    if k_seed == -1:
        return [row[:] for row in g]
    g_out = [row[:] for row in g]
    interval = 5
    for j in range(L):
        if j == k_seed:
            continue
        delta = j - k_seed
        s_j = start + delta * interval
        if s_j < 0 or s_j + h > n:
            continue
        if not is_position_empty(g, s_j, h, n, lower_pos, bg):
            continue
        col_list = []
        for b in range(B):
            if B == 2 and S == 3:
                s = 0 if b == 0 else 2
            else:
                s = b
            if s < S:
                col = upper_colors[j][s]
                col_list.append(col)
            else:
                col_list.append(bg)
        set_level(g_out, s_j, h, n, lower_pos, col_list, bg)
    return g_out
```