```python
from typing import List

def find_label_column(grid: List[List[int]]) -> int:
    return next(i for i, val in enumerate(grid[0]) if val == 0)

def remove_column(grid: List[List[int]], col_idx: int) -> List[List[int]]:
    return [row[:col_idx] + row[col_idx + 1:] for row in grid]

def get_max_horizontal_run(grid: List[List[int]]) -> int:
    h, w = len(grid), len(grid[0]) if grid else 0
    max_r = 0
    for row in grid[1:]:
        j = 0
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

def extract_runs_from_row(row: List[int]) -> List[tuple]:
    w = len(row)
    runs = []
    j = 0
    while j < w:
        if row[j] == 8:
            j += 1
            continue
        c = row[j]
        start = j
        j += 1
        while j < w and row[j] == c:
            j += 1
        length = j - start
        if length >= 2:
            runs.append((c, length))
    return runs

def find_pattern_groups(grid: List[List[int]]) -> List[tuple]:
    h = len(grid)
    groups = []
    i = 1
    while i < h:
        row = grid[i]
        if all(v == 8 for v in row):
            i += 1
            continue
        start = i
        i += 1
        while i < h and grid[i] == row:
            i += 1
        group_h = i - start
        runs = extract_runs_from_row(row)
        groups.append((group_h, runs))
    return groups

def build_wide_output(groups: List[tuple], max_run: int) -> List[List[int]]:
    output = []
    for group_h, runs in groups:
        for c, run_len in runs:
            pad_left = (max_run - run_len) // 2
            pad_right = max_run - run_len - pad_left
            row_out = [8] * pad_left + [c] * run_len + [8] * pad_right
            for _ in range(group_h):
                output.append(row_out)
    return output

def get_max_vertical_run(grid: List[List[int]], content_cols: List[int]) -> int:
    h = len(grid)
    max_r = 0
    for col in content_cols:
        i = 1
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
    return max_r

def get_main_color(grid: List[List[int]], start: int, end: int, band_cols: List[int]) -> int:
    cell_count = {}
    for r in range(start, end):
        for col in band_cols:
            val = grid[r][col]
            if val != 8:
                cell_count[val] = cell_count.get(val, 0) + 1
    if not cell_count:
        return 8
    return max(cell_count, key=cell_count.get)

def render_layer(grid: List[List[int]], start_r: int, band_cols: List[int], max_w: int) -> List[int]:
    row = grid[start_r]
    runs = []
    j = 0
    bw = len(band_cols)
    while j < bw:
        col = band_cols[j]
        c = row[col]
        if c == 8:
            j += 1
            continue
        start_j = j
        while j < bw and row[band_cols[j]] == c:
            j += 1
        w_run = j - start_j
        runs.append((c, w_run))
    runs = runs[::-1]
    h_layer = 2
    content = []
    for c, w_run in runs:
        content += [c] * (h_layer * w_run)
    clen = len(content)
    lp = (max_w - clen) // 2
    rp = max_w - clen - lp
    return [8] * lp + content + [8] * rp

def render_group_h2(grid: List[List[int]], start: int, band_cols: List[int], max_w: int, main_c: int) -> tuple:
    r1 = start
    r2 = start + 1
    pos_r1 = [grid[r1][col] for col in band_cols]
    pos_r2 = [grid[r2][col] for col in band_cols]
    mixed_inds = [k for k in range(2) if pos_r1[k] != pos_r2[k]]
    num_m = len(mixed_inds)
    special_pos = None
    for k in mixed_inds:
        c1 = pos_r1[k]
        c2 = pos_r2[k]
        if c1 != main_c and c2 != main_c and c1 != c2:
            special_pos = k
            break
    if num_m > 0 and special_pos is not None and num_m == 1:
        row1 = [main_c] * max_w
        c1 = pos_r1[special_pos]
        c2 = pos_r2[special_pos]
        row2 = [c1, c2] + [main_c] * (max_w - 2)
        return row1, row2
    elif num_m > 0:
        out_u = [pos_r2[k] for k in mixed_inds]
        out_l = [pos_r1[k] for k in mixed_inds]
        fill_l = max_w - num_m
        out_u += [main_c] * fill_l
        out_l += [main_c] * fill_l
        return out_u, out_l
    else:
        c = pos_r1[0]
        if c == 8:
            return [8] * max_w, [8] * max_w
        content_len = 2
        lp = (max_w - content_len) // 2
        rp = max_w - content_len - lp
        block_r = [8] * lp + [c] * content_len + [8] * rp
        return block_r[:], block_r[:]

def render_group_hgt(grid: List[List[int]], start: int, group_h: int, band_cols: List[int], max_w: int, main_c: int) -> tuple:
    r1 = start
    r2 = start + 1
    pos_r1 = [grid[r1][col] for col in band_cols]
    pos_r2 = [grid[r2][col] for col in band_cols]
    mixed_inds = [k for k in range(2) if pos_r1[k] != pos_r2[k]]
    num_m = len(mixed_inds)
    special_pos = None
    for k in mixed_inds:
        c1 = pos_r1[k]
        c2 = pos_r2[k]
        if c1 != main_c and c2 != main_c and c1 != c2:
            special_pos = k
            break
    if num_m > 0:
        if special_pos is not None and num_m == 1:
            row1 = [main_c] * max_w
            c1 = pos_r1[special_pos]
            c2 = pos_r2[special_pos]
            row2 = [c1, c2] + [main_c] * (max_w - 2)
            return row1, row2
        else:
            out_u = [pos_r2[k] for k in mixed_inds]
            out_l = [pos_r1[k] for k in mixed_inds]
            fill_l = max_w - num_m
            out_u += [main_c] * fill_l
            out_l += [main_c] * fill_l
            return out_u, out_l
    else:
        row1 = render_layer(grid, start, band_cols, max_w)
        bottom_start = start + group_h - 2
        row2 = render_layer(grid, bottom_start, band_cols, max_w)
        return row1, row2

def process_band(grid: List[List[int]], band_cols: List[int], max_w: int) -> List[List[int]]:
    h = len(grid)
    band_output = []
    i = 1
    while i < h:
        has_non8 = any(grid[i][col] != 8 for col in band_cols)
        if not has_non8:
            i += 1
            continue
        start = i
        i += 1
        while i < h and any(grid[i][col] != 8 for col in band_cols):
            i += 1
        group_h = i - start
        main_c = get_main_color(grid, start, i, band_cols)
        if group_h == 2:
            row1, row2 = render_group_h2(grid, start, band_cols, max_w, main_c)
        else:
            row1, row2 = render_group_hgt(grid, start, group_h, band_cols, max_w, main_c)
        band_output.append(row1)
        band_output.append(row2)
    return band_output

def program(g: List[List[int]]) -> List[List[int]]:
    label_col = find_label_column(g)
    grid = remove_column(g, label_col)
    h = len(grid)
    w = len(grid[0]) if h > 0 else 0
    if w > 7:
        # wide mode
        groups = find_pattern_groups(grid)
        max_run = get_max_horizontal_run(grid)
        output = build_wide_output(groups, max_run)
    else:
        # tall mode
        content_cols = [1, 2, 4, 5]
        max_w = get_max_vertical_run(grid, content_cols)
        left_band = process_band(grid, [1, 2], max_w)
        right_band = process_band(grid, [4, 5], max_w)
        output = left_band + right_band
    return output
```