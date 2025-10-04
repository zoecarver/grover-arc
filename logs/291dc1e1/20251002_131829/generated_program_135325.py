```python
from typing import List, Tuple

def find_label_col(header: List[int]) -> int:
    return header.index(0)

def remove_col(grid: List[List[int]], col: int) -> List[List[int]]:
    return [[row[j] for j in range(len(row)) if j != col] for row in grid]

def is_all8(row: List[int]) -> bool:
    return all(x == 8 for x in row)

def get_max_horizontal_run(groups: List[Tuple[int, List[int]]]) -> int:
    max_r = 0
    for _, row in groups:
        j = 0
        w = len(row)
        while j < w:
            if row[j] == 8:
                j += 1
                continue
            c = row[j]
            start = j
            j += 1
            while j < w and row[j] == c:
                j += 1
            max_r = max(max_r, j - start)
    return max_r

def extract_runs(row: List[int], reverse_dir: bool = False, min_len: int = 2) -> List[Tuple[int, int]]:
    if reverse_dir:
        row = row[::-1]
    runs = []
    j = 0
    w = len(row)
    while j < w:
        if row[j] == 8:
            j += 1
            continue
        c = row[j]
        l = 1
        j += 1
        while j < w and row[j] == c:
            l += 1
            j += 1
        if l >= min_len:
            runs.append((c, l))
    if reverse_dir:
        runs = runs[::-1]
    return runs

def render_bar(c: int, length: int, max_w: int) -> List[int]:
    pad_l = (max_w - length) // 2
    pad_r = max_w - length - pad_l
    return [8] * pad_l + [c] * length + [8] * pad_r

def find_groups(grid: List[List[int]]) -> List[Tuple[int, List[int]]]:
    groups = []
    i = 0
    h = len(grid)
    while i < h:
        if is_all8(grid[i]):
            i += 1
            continue
        start = i
        row = grid[i]
        i += 1
        while i < h and grid[i] == row:
            i += 1
        groups.append((i - start, row))
    return groups

def get_max_vertical_run(grid: List[List[int]], content_cols: List[int]) -> int:
    max_r = 0
    h = len(grid)
    for col in content_cols:
        i = 0
        while i < h:
            if grid[i][col] == 8:
                i += 1
                continue
            c = grid[i][col]
            start = i
            i += 1
            while i < h and grid[i][col] == c:
                i += 1
            max_r = max(max_r, i - start)
    return max_r if max_r > 0 else 1

def get_band_groups(grid: List[List[int]], band_cols: List[int]) -> List[Tuple[int, int]]:
    groups = []
    h = len(grid)
    i = 0
    while i < h:
        active = any(grid[i][c] != 8 for c in band_cols)
        if not active:
            i += 1
            continue
        start = i
        i += 1
        while i < h:
            active = any(grid[i][c] != 8 for c in band_cols)
            if not active:
                break
            i += 1
        h_g = i - start
        groups.append((start, h_g))
    return groups

def render_seq(seq: List[int], max_w: int) -> List[int]:
    ln = len(seq)
    if ln == max_w:
        return seq[:]
    pad_l = (max_w - ln) // 2
    pad_r = max_w - ln - pad_l
    return [8] * pad_l + seq + [8] * pad_r

def process_wide(grid: List[List[int]], original_w: int, label_col: int) -> List[List[int]]:
    reverse_dir = label_col > (original_w - 1) / 2
    groups = find_groups(grid)
    if not groups:
        return []
    max_w = get_max_horizontal_run(groups)
    output = []
    for h_g, row in groups:
        runs = extract_runs(row, reverse_dir)
        for c, ln in runs:
            bar = render_bar(c, ln, max_w)
            output.extend([bar] * h_g)
    return output

def process_tall(grid: List[List[int]], original_w: int, label_col: int) -> List[List[int]]:
    reverse_dir = label_col > (original_w - 1) / 2
    content_cols = [1, 2, 4, 5]
    max_v = get_max_vertical_run(grid, content_cols)
    left_band = [1, 2]
    right_band = [4, 5]
    if reverse_dir:
        left_band = [4, 5]
        right_band = [1, 2]
    bands = [left_band, right_band]
    output = []
    for band_cols in bands:
        col_right = band_cols[1]
        col_left = band_cols[0]
        groups = get_band_groups(grid, band_cols)
        for start, h_g in groups:
            seq_r = [grid[start + k][col_right] for k in range(h_g)]
            seq_l = [grid[start + k][col_left] for k in range(h_g)]
            rendered_r = render_seq(seq_r, max_v)
            rendered_l = render_seq(seq_l, max_v)
            output.append(rendered_r)
            output.append(rendered_l)
    return output

def program(g: List[List[int]]) -> List[List[int]]:
    original_w = len(g[0])
    label_col = find_label_col(g[0])
    grid = remove_col(g, label_col)[1:]
    if not grid:
        return []
    w_after = len(grid[0])
    if w_after > 7:
        return process_wide(grid, original_w, label_col)
    else:
        return process_tall(grid, original_w, label_col)
```