```python
from typing import List, Tuple

def find_background(grid: List[List[int]]) -> int:
    for row in grid:
        if len(set(row)) == 1 and row[0] != 5:
            return row[0]
    return 3  # fallback

def get_clue_color(clue_row: List[int], group_start: int) -> int:
    for p in range(4):
        val = clue_row[group_start + p]
        if val not in [0, 5]:
            return val
    return 0

def compute_seed_pairs(clue_row: List[int], is_lower: bool, max_group: int) -> List[Tuple[int, int]]:
    group_starts = [1, 7, 13, 19]
    seed_pairs = []
    for gi in range(max_group + 1):
        start = group_starts[gi]
        group = clue_row[start:start + 4]
        color_pos = -1
        color = 0
        for p in range(4):
            val = group[p]
            if val not in [0, 5]:
                color_pos = p
                color = val
                break
        activate = False
        if color_pos != -1 and color != 3:
            if color_pos == 0:
                if color in [4, 6] or (is_lower and color == 1):
                    activate = True
            elif color_pos == 3:
                if color in [2, 4, 6]:
                    activate = True
        if not activate:
            continue
        # compute pair_start
        if color_pos == 0:
            if color == 6 or (color == 1 and is_lower):
                pair_start = start + 1
            elif color == 4:
                next_color = 0
                if gi < 3:
                    next_start = group_starts[gi + 1]
                    next_color = get_clue_color(clue_row, next_start)
                if next_color == 2:
                    pair_start = start + 3
                else:
                    pair_start = start + 1
            else:  # color == 1 and is_lower
                pair_start = start + 3
        else:  # color_pos == 3
            if color == 2:
                pair_start = start + 3
                if start == 19:
                    pair_start = 18
            elif color == 4:
                pair_start = start + 2
            elif color == 6:
                pair_start = start + 1
        pair_end = pair_start + 1
        if pair_end < 24:
            seed_pairs.append((pair_start, pair_end))
    return seed_pairs

def program(g: List[List[int]]) -> List[List[int]]:
    if len(g) != 25:
        return g  # fallback
    bkg = find_background(g)
    out: List[List[int]] = [row[:] for row in g[6:25]]
    n_rows = len(out)
    n_cols = 24
    for row in out:
        for j in range(n_cols):
            if row[j] == 5:
                row[j] = bkg
    # has_prop based on original 8's
    has_prop = [False] * n_rows
    for i in range(n_rows):
        if 8 in out[i]:
            has_prop[i] = True
    max_prop_i = max([i for i in range(n_rows) if has_prop[i]], default=-1)
    # clue_row
    clue_row = g[1]
    # first_clue_color
    first_clue_color = get_clue_color(clue_row, 1)
    # upper seed pairs
    upper_seed_pairs = compute_seed_pairs(clue_row, False, 3)
    # lower seed pairs
    lower_seed_pairs = compute_seed_pairs(clue_row, True, 1)
    # identify upper block before seeds
    upper_block_start = -1
    upper_block_len = 0
    for i in range(n_rows):
        is_all_bkg = all(out[i][j] == bkg for j in range(n_cols))
        if is_all_bkg:
            if upper_block_start == -1:
                upper_block_start = i
            upper_block_len += 1
        elif upper_block_start != -1:
            break
    # determine if plus1 for rightmost upper
    is_plus1 = False
    rightmost_end = -1
    rightmost_start = -1
    rightmost_g_start = -1
    if upper_seed_pairs:
        rightmost = max(upper_seed_pairs, key=lambda p: p[0])
        rightmost_start = rightmost[0]
        rightmost_end = rightmost[1]
        for gs in [1,7,13,19]:
            if rightmost_start >= gs and rightmost_start < gs + 4:
                rightmost_g_start = gs
                break
        if rightmost_start == rightmost_g_start + 1:
            is_plus1 = True
    # set seeds in rows 0 to 15
    for i in range(16):
        pairs = upper_seed_pairs if i <= max_prop_i else lower_seed_pairs
        row = out[i]
        for s, e in pairs:
            for j in range(s, e + 1):
                if j < n_cols and row[j] == bkg:
                    row[j] = 8
    # prop in has_prop rows
    for i in range(16):
        if not has_prop[i]:
            continue
        row = out[i]
        eight_pos = [j for j in range(n_cols) if row[j] == 8]
        if not eight_pos:
            continue
        eight_pos = sorted(set(eight_pos))  # unique sorted
        # left from min
        minj = eight_pos[0]
        for j in range(minj - 1, -1, -1):
            if row[j] != bkg:
                break
            row[j] = 8
        # right from max
        maxj = eight_pos[-1]
        for j in range(maxj + 1, n_cols):
            if row[j] != bkg:
                break
            row[j] = 8
        # between
        for kk in range(len(eight_pos) - 1):
            a = eight_pos[kk]
            b = eight_pos[kk + 1]
            for j in range(a + 1, b):
                row[j] = 8  # assume bkg
    # upper right prop
    if upper_block_start != -1 and upper_block_len > 0 and is_plus1 and rightmost_end >= 0:
        num = min(2, upper_block_len)
        for k in range(num):
            r = upper_block_start + k
            for j in range(rightmost_end + 1, n_cols):
                if out[r][j] == bkg:
                    out[r][j] = 8
    # lower prop rows
    lower_prop_rows = []
    if first_clue_color == 1:
        lower_prop_rows = [14, 15]
    elif first_clue_color == 2:
        lower_prop_rows = [13, 14]
    for i in lower_prop_rows:
        if i < 16 and lower_seed_pairs:
            left_start = min(p[0] for p in lower_seed_pairs)
            for j in range(left_start, n_cols):
                if out[i][j] == bkg:
                    out[i][j] = 8
    return out
```