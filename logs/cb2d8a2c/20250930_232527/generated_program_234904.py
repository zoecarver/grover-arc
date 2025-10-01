```python
from typing import List, Tuple, Optional

def replace_ones(grid: List[List[int]]) -> List[List[int]]:
    return [[2 if cell == 1 else cell for cell in row] for row in grid]

def find_seed(grid: List[List[int]]) -> Optional[Tuple[int, int]]:
    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            if cell == 3:
                return i, j
    return None

def is_vertical_mode(grid: List[List[int]], s: int, c: int) -> bool:
    return any(grid[s][j] == 2 for j in range(c + 1, len(grid[0])))

def has_left_guide(grid: List[List[int]], s: int, c: int) -> bool:
    return any(grid[s][j] == 2 for j in range(c))

def fill_line_vertical(grid: List[List[int]], col: int, start_row: int, end_row: int):
    rows_n = len(grid)
    for i in range(max(start_row, 0), min(end_row + 1, rows_n)):
        if grid[i][col] == 8:
            grid[i][col] = 3

def fill_line_horizontal(grid: List[List[int]], row: int, start_col: int, end_col: int):
    cols_n = len(grid[0]) if grid else 0
    for j in range(max(start_col, 0), min(end_col + 1, cols_n)):
        if grid[row][j] == 8:
            grid[row][j] = 3

def propagate_right_in_row(grid: List[List[int]], s: int, c: int, rows_n: int, cols_n: int):
    guide_cols = [j for j in range(c + 1, cols_n) if any(grid[i][j] == 2 for i in range(s, rows_n))]
    if not guide_cols:
        return
    guide_cols.sort()
    inner_cols = []
    max_end_r = s
    previous_right_end = c
    for guide_j in guide_cols:
        below_start = next((i for i in range(s, rows_n) if grid[i][guide_j] == 2), rows_n)
        below_end = s - 1
        for i in range(s, rows_n):
            if grid[i][guide_j] == 2:
                below_end = max(below_end, i)
        below_len = below_end - below_start + 1 if below_start < rows_n else 0
        has_at_s = grid[s][guide_j] == 2
        if has_at_s:
            fill_end = guide_j - 2
            fill_start = max(c, previous_right_end + 1)
            if fill_end >= fill_start:
                fill_line_horizontal(grid, s, fill_start, fill_end)
                inner_col = fill_end
                v_length = below_len
                v_end_r = s + v_length
                fill_line_vertical(grid, inner_col, s + 1, v_end_r)
                max_end_r = max(max_end_r, v_end_r)
                inner_cols.append(inner_col)
            previous_right_end = max(fill_end, previous_right_end)
        else:
            row_dist = below_start - s if below_start < rows_n else 0
            fill_start = guide_j - row_dist
            fill_end = cols_n - 1
            actual_start = max(fill_start, previous_right_end + 1)
            if actual_start <= fill_end:
                fill_line_horizontal(grid, s, actual_start, fill_end)
                inner_col = actual_start
                v_length = row_dist
                v_end_r = s + v_length
                fill_line_vertical(grid, inner_col, s + 1, v_end_r)
                max_end_r = max(max_end_r, v_end_r)
                inner_cols.append(inner_col)
            previous_right_end = fill_end
    connect_r = max_end_r + 1
    if connect_r < rows_n and inner_cols:
        min_inner = min(inner_cols)
        max_inner = max(inner_cols)
        fill_line_horizontal(grid, connect_r, min_inner, max_inner)

def propagate_left_in_row(grid: List[List[int]], s: int, c: int, rows_n: int, cols_n: int):
    guide_cols = [j for j in range(c) if any(grid[i][j] == 2 for i in range(s, rows_n))]
    if not guide_cols:
        return
    guide_cols = sorted(set(guide_cols), reverse=True)
    inner_cols = []
    max_end_r = s
    previous_left_end = c
    for guide_j in guide_cols:
        below_start = next((i for i in range(s, rows_n) if grid[i][guide_j] == 2), rows_n)
        below_end = s - 1
        for i in range(s, rows_n):
            if grid[i][guide_j] == 2:
                below_end = max(below_end, i)
        below_len = below_end - below_start + 1 if below_start < rows_n else 0
        has_at_s = grid[s][guide_j] == 2
        if has_at_s:
            fill_start = guide_j + 2
            fill_end = min(c, previous_left_end - 1)
            if fill_start <= fill_end:
                fill_line_horizontal(grid, s, fill_start, fill_end)
                inner_col = fill_start
                v_length = below_len
                v_end_r = s + v_length
                fill_line_vertical(grid, inner_col, s + 1, v_end_r)
                max_end_r = max(max_end_r, v_end_r)
                inner_cols.append(inner_col)
            previous_left_end = min(fill_start, previous_left_end)
        else:
            row_dist = below_start - s if below_start < rows_n else 0
            fill_end = guide_j + row_dist
            fill_start = 0
            actual_end = min(fill_end, previous_left_end - 1)
            if actual_end >= fill_start:
                fill_line_horizontal(grid, s, fill_start, actual_end)
                inner_col = actual_end
                v_length = row_dist
                v_end_r = s + v_length
                fill_line_vertical(grid, inner_col, s + 1, v_end_r)
                max_end_r = max(max_end_r, v_end_r)
                inner_cols.append(inner_col)
            previous_left_end = actual_end
    connect_r = max_end_r + 1
    if connect_r < rows_n and inner_cols:
        min_inner = min(inner_cols)
        max_inner = max(inner_cols)
        fill_line_horizontal(grid, connect_r, min_inner, max_inner)

def propagate_down(grid: List[List[int]], s: int, c: int, rows_n: int, cols_n: int):
    segments = []
    for r in range(s + 1, rows_n):
        i = 0
        n = cols_n
        while i < n:
            if grid[r][i] == 2:
                start = i
                while i < n and grid[r][i] == 2:
                    i += 1
                end = i - 1
                if end - start + 1 >= 2:
                    segments.append((r, start, end))
            else:
                i += 1
    if not segments:
        fill_line_vertical(grid, c, s, rows_n - 1)
        return
    segments.sort(key=lambda x: x[0])
    current_row = s
    current_col = c
    right_target = min(2 * c, cols_n - 1)
    left_target = 1
    seg_r, seg_s, seg_e = segments[0]
    l_dist = max(0, current_col - seg_s)
    r_dist = max(0, seg_e - current_col)
    closer_dist = min(l_dist, r_dist)
    is_left_closer = l_dist <= r_dist
    first_h = s + closer_dist
    first_h = min(first_h, rows_n - 1)
    fill_line_vertical(grid, current_col, s, first_h - 1)
    if is_left_closer:
        h_start = left_target
        h_end = current_col
        current_col = left_target
    else:
        h_start = current_col
        h_end = right_target
        current_col = right_target
    h_start = max(0, h_start)
    h_end = min(cols_n - 1, h_end)
    if h_start <= h_end:
        fill_line_horizontal(grid, first_h, h_start, h_end)
    current_seg_index = 0
    base_dir = -1 if is_left_closer else 1
    while current_seg_index < len(segments):
        seg_r, seg_s, seg_e = segments[current_seg_index]
        end_v = seg_r + 2
        end_v = min(end_v, rows_n - 1)
        start_v = first_h + 1 if current_seg_index == 0 else previous_end_v + 1
        start_v = max(start_v, s + 1)
        if start_v <= end_v:
            fill_line_vertical(grid, current_col, start_v, end_v)
        previous_end_v = end_v
        if current_seg_index + 1 == len(segments):
            bottom = rows_n - 1
            fill_line_vertical(grid, current_col, end_v + 1, bottom)
            break
        next_h = end_v + 1
        next_h = min(next_h, rows_n - 1)
        h_num = current_seg_index + 1
        this_dir = base_dir * ((-1) ** (h_num - 1))
        if this_dir > 0:
            current_col = right_target
        else:
            current_col = left_target
        h_start = left_target
        h_end = right_target
        h_start = max(0, h_start)
        h_end = min(cols_n - 1, h_end)
        fill_line_horizontal(grid, next_h, h_start, h_end)
        current_seg_index += 1

def program(g: List[List[int]]) -> List[List[int]]:
    grid = replace_ones(g)
    seed = find_seed(grid)
    if seed is None:
        return grid
    s, c = seed
    rows_n = len(grid)
    cols_n = len(grid[0]) if rows_n > 0 else 0
    if grid[s][c] != 3:
        grid[s][c] = 3
    if is_vertical_mode(grid, s, c):
        propagate_right_in_row(grid, s, c, rows_n, cols_n)
    else:
        if has_left_guide(grid, s, c):
            propagate_left_in_row(grid, s, c, rows_n, cols_n)
        else:
            propagate_down(grid, s, c, rows_n, cols_n)
    return grid
```