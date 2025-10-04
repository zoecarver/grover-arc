```python
from typing import List, Tuple

def get_five_bbox(g: List[List[int]]) -> Tuple[int, int, int, int]:
    positions = [(i, j) for i in range(len(g)) for j in range(len(g[i])) if g[i][j] == 5]
    if not positions:
        return -1, -1, -1, -1
    min_r = min(r for r, _ in positions)
    max_r = max(r for r, _ in positions)
    min_c = min(c for _, c in positions)
    max_c = max(c for _, c in positions)
    return min_r, max_r, min_c, max_c

def get_leftmost_color(g: List[List[int]]) -> int:
    min_col = float('inf')
    c = 0
    for i in range(len(g)):
        for j in range(len(g[i])):
            val = g[i][j]
            if val > 1 and val != 5 and j < min_col:
                min_col = j
                c = val
    return c

def get_left_right_colors(row: List[int]) -> List[int]:
    n = len(row)
    groups = []
    i = 0
    while i < n:
        if row[i] == 0 or row[i] == 5:
            i += 1
            continue
        start = i
        left_c = row[i]
        i += 1
        while i < n and row[i] != 0 and row[i] != 5:
            i += 1
        right_c = row[i - 1]
        size = i - start
        if size >= 2:
            groups.append((left_c, right_c))
    if groups:
        return [groups[0][0], groups[-1][1]]
    # fallback single
    single_c = 0
    for val in row:
        if val != 0 and val != 5:
            single_c = val
            break
    return [single_c, single_c]

def program(g: List[List[int]]) -> List[List[int]]:
    min_r, max_r, min_c, max_c = get_five_bbox(g)
    if min_r < 0:
        return []
    h = max_r - min_r + 1
    w = max_c - min_c + 1
    c = get_leftmost_color(g)
    if w != 2:
        # general frame
        grid = [[0] * w for _ in range(h)]
        # top and bottom full
        for j in range(w):
            grid[0][j] = c
            if h > 1:
                grid[h - 1][j] = c
        # left stem for middle rows
        for i in range(1, h - 1):
            grid[i][0] = c
        if h > w:
            # vertical: right stem full
            for i in range(h):
                grid[i][w - 1] = c
            # inner columns alternating full/sparse rows
            for i in range(h):
                is_full = (i % 2 == 0)
                for j in range(1, w - 1):
                    if is_full:
                        grid[i][j] = c
        return grid
    else:
        # special case for w == 2: extract pairs from upper, mirror swap reverse for lower, adjust last
        half = h // 2
        upper_pairs = []
        for k in range(half):
            row_idx = min_r + k
            row_data = g[row_idx]
            pair = get_left_right_colors(row_data)
            upper_pairs.append(pair)
        # lower: reverse upper, swapped
        lower_pairs = []
        for k in range(half - 1, -1, -1):
            pair = upper_pairs[k]
            swapped = [pair[1], pair[0]]
            lower_pairs.append(swapped)
        all_pairs = upper_pairs + lower_pairs
        # adjust last row left to 0
        if all_pairs:
            all_pairs[-1][0] = 0
        # if odd h, insert middle (last upper no swap) before lower
        if h % 2 == 1:
            middle = upper_pairs[-1][:]
            all_pairs = upper_pairs[:-1] + [middle] + lower_pairs
            # adjust last again
            all_pairs[-1][0] = 0
        return [[p[0], p[1]] for p in all_pairs]
```