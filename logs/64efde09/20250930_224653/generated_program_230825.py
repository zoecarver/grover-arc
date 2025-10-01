```python
from typing import List, Dict, Tuple
from collections import defaultdict

def count_non_blanks(g: List[List[int]]) -> Dict[int, int]:
    h = len(g)
    if h == 0:
        return {}
    w = len(g[0])
    counts = defaultdict(int)
    for i in range(h):
        for j in range(w):
            c = g[i][j]
            if c != 8:
                counts[c] += 1
    return counts

def find_singleton_positions(g: List[List[int]], singletons: List[int]) -> Dict[int, Tuple[int, int]]:
    h = len(g)
    w = len(g[0]) if h > 0 else 0
    pos_dict: Dict[int, Tuple[int, int]] = {}
    for i in range(h):
        for j in range(w):
            cc = g[i][j]
            if cc in singletons:
                pos_dict[cc] = (i, j)
    return pos_dict

def place_top_pattern(grid: List[List[int]], h: int, w: int, sk: int, r: int, c: int, s1: int, s2: int, s3: int):
    if r != 0:
        return
    if sk == s1:
        off = 4
    elif sk == s2:
        off = 2
    else:
        off = 0
    start_col = c - off
    if start_col < 0:
        return
    pat_cols = [start_col + 0, start_col + 2, start_col + 4]
    pat_cols = [pc for pc in pat_cols if 0 <= pc < w]
    if len(pat_cols) != 3:
        return
    pat_colors = [s3, s2, s1]
    # place in row 0
    for j in range(3):
        pc = pat_cols[j]
        if grid[0][pc] == 8:
            grid[0][pc] = pat_colors[j]
    # propagate downward
    for i in range(1, h):
        if not all(grid[i][pc] == 8 for pc in pat_cols):
            break
        for j in range(3):
            grid[i][pat_cols[j]] = pat_colors[j]

def place_bottom_pattern(grid: List[List[int]], h: int, w: int, sk: int, r: int, c: int, s1: int, s2: int, s3: int):
    if r != h - 1:
        return
    if sk == s1:
        pat_cols = [c, c + 1, c + 3]
        pat_colors = [s1, s2, s3]
    elif sk == s2:
        pat_cols = [c - 1, c, c + 3]
        pat_colors = [s1, s2, s3]
    else:  # s3
        pat_cols = [c - 3, c - 1, c]
        pat_colors = [s1, s2, s3]
    pat_cols = [pc for pc in pat_cols if 0 <= pc < w]
    if len(pat_cols) != 3:
        return
    # place in row r
    for j in range(3):
        pc = pat_cols[j]
        if grid[r][pc] == 8:
            grid[r][pc] = pat_colors[j]
    # propagate upward
    for i in range(r - 1, -1, -1):
        if not all(grid[i][pc] == 8 for pc in pat_cols):
            break
        for j in range(3):
            grid[i][pat_cols[j]] = pat_colors[j]

def extend_middle_horizontal(grid: List[List[int]], r: int, c: int, color: int, w: int):
    # left
    j = c - 1
    while j >= 0 and grid[r][j] == 8:
        grid[r][j] = color
        j -= 1
    # right
    j = c + 1
    while j < w and grid[r][j] == 8:
        grid[r][j] = color
        j += 1

def find_stems(g: List[List[int]], h: int, w: int) -> List[Tuple[int, int, int, int]]:
    runs = []
    for col in range(w):
        i = 0
        while i < h:
            val = g[i][col]
            if val == 1 or val == 2:
                start_i = i
                cl = val
                while i < h and g[i][col] == cl:
                    i += 1
                ln = i - start_i
                if ln >= 4:
                    runs.append((start_i, i, col, cl))
            else:
                i += 1
    return runs

def process_stems(grid: List[List[int]], runs: List[Tuple[int, int, int, int]], s1: int, s2: int, s3: int, h: int, w: int):
    if not runs:
        return
    type1_cols = {col for _, _, col, cl in runs if cl == 1}
    type2_cols = {col for _, _, col, cl in runs if cl == 2}
    for st_row, end_row, c, cl in runs:
        other_cl = 3 - cl
        other_cols = type1_cols if cl == 2 else type2_cols
        if (c - 1 in other_cols) or (c + 1 in other_cols):
            continue
        l = end_row - st_row
        if cl == 1:
            row_offs = [1, 3, 5]
            fill_colors = [s1, s2, s3]
        else:
            row_offs = [0, 3, l - 2]
            fill_colors = [s3, s2, s1]
        for k in range(3):
            tr = st_row + row_offs[k]
            if 0 <= tr < h:
                color = fill_colors[k]
                # left adjacent blank run
                if c > 0 and grid[tr][c - 1] == 8:
                    j = c - 1
                    while j >= 0 and grid[tr][j] == 8:
                        grid[tr][j] = color
                        j -= 1
                # right adjacent blank run
                if c < w - 1 and grid[tr][c + 1] == 8:
                    j = c + 1
                    while j < w and grid[tr][j] == 8:
                        grid[tr][j] = color
                        j += 1

def program(g: List[List[int]]) -> List[List[int]]:
    h = len(g)
    if h == 0:
        return []
    w = len(g[0])
    counts = count_non_blanks(g)
    singletons = [col for col, cnt in counts.items() if cnt == 1]
    if len(singletons) != 3:
        return [row[:] for row in g]
    s1, s2, s3 = sorted(singletons)
    pos = find_singleton_positions(g, [s1, s2, s3])
    grid = [row[:] for row in g]
    for sk in [s1, s2, s3]:
        if sk not in pos:
            continue
        r, c = pos[sk]
        place_top_pattern(grid, h, w, sk, r, c, s1, s2, s3)
        place_bottom_pattern(grid, h, w, sk, r, c, s1, s2, s3)
        if 0 < r < h - 1:
            extend_middle_horizontal(grid, r, c, sk, w)
    runs = find_stems(grid, h, w)
    process_stems(grid, runs, s1, s2, s3, h, w)
    return grid
```