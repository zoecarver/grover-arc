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

def fill_line_vertical(grid: List[List[int]], col: int, start_row: int, end_row: int) -> None:
    rows_n = len(grid)
    for i in range(max(start_row, 0), min(end_row + 1, rows_n)):
        if grid[i][col] == 8:
            grid[i][col] = 3

def fill_line_horizontal(grid: List[List[int]], row: int, start_col: int, end_col: int) -> None:
    cols_n = len(grid[0]) if grid else 0
    for j in range(max(start_col, 0), min(end_col + 1, cols_n)):
        if grid[row][j] == 8:
            grid[row][j] = 3

def is_vertical_mode(grid: List[List[int]], s: int, c: int) -> bool:
    return any(grid[s][j] == 2 for j in range(c + 1, len(grid[0])))

def has_left_guide(grid: List[List[int]], s: int, c: int) -> bool:
    return any(grid[s][j] == 2 for j in range(c))

def find_horizontal_segments(grid: List[List[int]], start_row: int) -> List[Tuple[int, int, int]]:
    segments = []
    rows_n = len(grid)
    for r in range(start_row + 1, rows_n):
        row = grid[r]
        cols_n = len(row)
        i = 0
        while i < cols_n:
            if row[i] == 2:
                seg_start = i
                while i < cols_n and row[i] == 2:
                    i += 1
                seg_end = i - 1
                if seg_end - seg_start + 1 >= 2:
                    segments.append((r, seg_start, seg_end))
            else:
                i += 1
    return sorted(segments)

def down_propagate(grid: List[List[int]], s: int, c: int, rows_n: int, cols_n: int) -> None:
    segments = find_horizontal_segments(grid, s)
    num_segs = len(segments)
    if num_segs == 0:
        fill_line_vertical(grid, c, s, rows_n - 1)
        return
    fill_line_vertical(grid, c, s, min(s + 1, rows_n - 1))
    h_row = s + 2
    if h_row >= rows_n:
        return
    sr, sstart, send = segments[0]
    l_dist = c - sstart
    r_dist = send - c
    dir_left = l_dist <= r_dist
    left_t = 1
    right_t = min(2 * c, cols_n - 1)
    t = left_t if dir_left else right_t
    fill_line_horizontal(grid, h_row, min(c, t), max(c, t))
    current_col = t
    for i in range(num_segs):
        start_v = h_row + 1
        if i < num_segs - 1:
            end_v = segments[i][0] + 2
        else:
            end_v = rows_n - 1
        end_v = min(end_v, rows_n - 1)
        if start_v <= end_v:
            fill_line_vertical(grid, current_col, start_v, end_v)
        if i == num_segs - 1:
            break
        h_row = end_v + 1
        if h_row >= rows_n:
            break
        dir_left = not dir_left
        t = left_t if dir_left else right_t
        fill_line_horizontal(grid, h_row, min(current_col, t), max(current_col, t))
        current_col = t

def find_right_guides(grid: List[List[int]], s: int, rows_n: int, cols_n: int, c: int) -> List[Tuple[int, int, int]]:
    guides = []
    for j in range(c + 1, cols_n):
        has = any(grid[i][j] == 2 for i in range(s, rows_n))
        if has:
            below_len = sum(1 for i in range(s + 1, rows_n) if grid[i][j] == 2)
            b_start = next((i for i in range(s, rows_n) if grid[i][j] == 2), None)
            guides.append((j, below_len, b_start))
    return guides

def right_propagate(grid: List[List[int]], s: int, c: int, rows_n: int, cols_n: int) -> None:
    guides = find_right_guides(grid, s, rows_n, cols_n, c)
    if not guides:
        fill_line_horizontal(grid, s, c, cols_n - 1)
        return
    j1, below_len1, _ = guides[0]
    gap = 2 if below_len1 == 1 else 1
    fill_end = j1 - gap - 1
    if fill_end >= c:
        fill_line_horizontal(grid, s, c, fill_end)
    drop_col = fill_end
    if len(guides) > 1:
        j2, _, b_start2 = guides[1]
        row_dist = b_start2 - s
        connect_col = j2 - row_dist
        connect_r = b_start2 + gap
        connect_r = min(connect_r, rows_n - 1)
        fill_line_vertical(grid, drop_col, s + 1, connect_r)
        fill_line_horizontal(grid, connect_r, drop_col, connect_col)
        fill_line_vertical(grid, connect_col, s, connect_r)
        fill_line_horizontal(grid, s, connect_col, cols_n - 1)
    else:
        end_v = s + below_len1
        end_v = min(end_v, rows_n - 1)
        fill_line_vertical(grid, drop_col, s + 1, end_v)
        fill_line_horizontal(grid, s, drop_col, cols_n - 1)

def find_left_guides(grid: List[List[int]], s: int, rows_n: int, cols_n: int, c: int) -> List[Tuple[int, int, int]]:
    guides = []
    for j in range(c - 1, -1, -1):
        has = any(grid[i][j] == 2 for i in range(s, rows_n))
        if has:
            below_len = sum(1 for i in range(s + 1, rows_n) if grid[i][j] == 2)
            b_start = next((i for i in range(s, rows_n) if grid[i][j] == 2), None)
            guides.append((j, below_len, b_start))
    return guides

def left_propagate(grid: List[List[int]], s: int, c: int, rows_n: int, cols_n: int) -> None:
    guides = find_left_guides(grid, s, rows_n, cols_n, c)
    if not guides:
        fill_line_horizontal(grid, s, 0, c)
        return
    j1, below_len1, _ = guides[0]
    gap = 2 if below_len1 == 1 else 1
    fill_start = j1 + gap + 1
    if fill_start <= c:
        fill_line_horizontal(grid, s, fill_start, c)
    drop_col = fill_start
    if len(guides) > 1:
        j2, _, b_start2 = guides[1]
        row_dist = b_start2 - s
        connect_col = j2 + row_dist
        connect_r = b_start2 + gap
        connect_r = min(connect_r, rows_n - 1)
        fill_line_vertical(grid, drop_col, s + 1, connect_r)
        fill_line_horizontal(grid, connect_r, connect_col, drop_col)
        fill_line_vertical(grid, connect_col, s, connect_r)
        fill_line_horizontal(grid, s, 0, connect_col)
    else:
        end_v = s + below_len1
        end_v = min(end_v, rows_n - 1)
        fill_line_vertical(grid, drop_col, s + 1, end_v)
        fill_line_horizontal(grid, s, 0, drop_col)

def program(g: List[List[int]]) -> List[List[int]]:
    grid = replace_ones(g)
    seed = find_seed(grid)
    if seed is None:
        return grid
    s, c = seed
    rows_n = len(grid)
    if rows_n == 0:
        return grid
    cols_n = len(grid[0])
    if is_vertical_mode(grid, s, c):
        right_propagate(grid, s, c, rows_n, cols_n)
    elif has_left_guide(grid, s, c):
        left_propagate(grid, s, c, rows_n, cols_n)
    else:
        down_propagate(grid, s, c, rows_n, cols_n)
    return grid
```