```python
from typing import List, Tuple

def replace_ones(grid: List[List[int]]) -> List[List[int]]:
    return [[2 if cell == 1 else cell for cell in row] for row in grid]

def find_seed(grid: List[List[int]]) -> Tuple[int, int]:
    rows_n = len(grid)
    for i in range(rows_n):
        cols_n = len(grid[i])
        for j in range(cols_n):
            if grid[i][j] == 3:
                return i, j
    return -1, -1

def is_vertical_mode(grid: List[List[int]], s: int, c: int) -> bool:
    cols_n = len(grid[0]) if grid else 0
    return any(grid[s][j] == 2 for j in range(c + 1, cols_n))

def has_left_guide(grid: List[List[int]], s: int, c: int) -> bool:
    return any(grid[s][j] == 2 for j in range(c))

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

def find_right_guides(grid: List[List[int]], s: int, c: int) -> List[Tuple[int, int, int, int]]:
    guides = []
    rows_n = len(grid)
    cols_n = len(grid[0])
    for j in range(c + 1, cols_n):
        start_r = rows_n
        b_start = rows_n
        b_end = -1
        has_guide = False
        for i in range(rows_n):
            if grid[i][j] == 2:
                start_r = min(start_r, i)
                if i >= s:
                    has_guide = True
                    b_start = min(b_start, i)
                    b_end = max(b_end, i)
        if has_guide:
            guides.append((j, start_r, b_start, b_end))
    return sorted(guides, key=lambda x: x[0])

def propagate_right(grid: List[List[int]], s: int, c: int, guides: List[Tuple[int, int, int, int]], rows_n: int, cols_n: int) -> List[List[int]]:
    if not guides:
        return grid
    current_col = c
    connect_row = s
    for idx, (j, start_r, b_start, b_end) in enumerate(guides):
        has_at_s = (grid[s][j] == 2)
        if idx == 0 and has_at_s:
            above_len = s - start_r
            below_len = b_end - s
            gap_num = 1 if above_len == below_len else 2
            fill_end = j - gap_num - 1
            fill_end = max(fill_end, current_col)
            fill_line_horizontal(grid, s, current_col, fill_end)
            attach_col = fill_end
            v_start = s + 1
            v_end = min(b_end + gap_num + 1, rows_n - 1)
            fill_line_vertical(grid, attach_col, v_start, v_end)
            connect_row = v_end
            current_col = attach_col
        else:
            row_dist = b_start - s
            new_attach = j - row_dist
            new_attach = max(new_attach, 0)
            new_attach = min(new_attach, j - 1)
            fill_line_horizontal(grid, connect_row, current_col, new_attach)
            attach_col = new_attach
            fill_line_vertical(grid, attach_col, s, connect_row)
            fill_line_horizontal(grid, s, attach_col, cols_n - 1)
            current_col = attach_col
    return grid

def find_left_guides(grid: List[List[int]], s: int, c: int) -> List[Tuple[int, int, int, int]]:
    guides = []
    rows_n = len(grid)
    cols_n = len(grid[0])
    for j in range(c - 1, -1, -1):
        start_r = rows_n
        b_start = rows_n
        b_end = -1
        has_guide = False
        for i in range(rows_n):
            if grid[i][j] == 2:
                start_r = min(start_r, i)
                if i >= s:
                    has_guide = True
                    b_start = min(b_start, i)
                    b_end = max(b_end, i)
        if has_guide:
            guides.append((j, start_r, b_start, b_end))
    return sorted(guides, key=lambda x: -x[0])

def propagate_left(grid: List[List[int]], s: int, c: int, guides: List[Tuple[int, int, int, int]], rows_n: int, cols_n: int) -> List[List[int]]:
    if not guides:
        return grid
    current_col = c
    connect_row = s
    for idx, (j, start_r, b_start, b_end) in enumerate(guides):
        has_at_s = (grid[s][j] == 2)
        if idx == 0 and has_at_s:
            above_len = s - start_r
            below_len = b_end - s
            gap_num = 1 if above_len == below_len else 2
            fill_start = j + gap_num + 1
            fill_start = min(fill_start, current_col)
            fill_line_horizontal(grid, s, fill_start, current_col)
            attach_col = fill_start
            v_start = s + 1
            v_end = min(b_end + gap_num + 1, rows_n - 1)
            fill_line_vertical(grid, attach_col, v_start, v_end)
            connect_row = v_end
            current_col = attach_col
        else:
            row_dist = b_start - s
            new_attach = j + row_dist
            new_attach = min(new_attach, current_col - 1)
            new_attach = max(new_attach, j + 1)
            fill_line_horizontal(grid, connect_row, new_attach, current_col)
            attach_col = new_attach
            fill_line_vertical(grid, attach_col, s, connect_row)
            fill_line_horizontal(grid, s, 0, attach_col)
            current_col = attach_col
    return grid

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

def propagate_down(grid: List[List[int]], s: int, c: int, segments: List[Tuple[int, int, int]], rows_n: int, cols_n: int) -> List[List[int]]:
    if s + 1 < rows_n:
        fill_line_vertical(grid, c, s + 1, s + 1)
    if not segments:
        fill_line_vertical(grid, c, s + 1, rows_n - 1)
        return grid
    current_row = s + 2
    current_col = c
    prev_direction_right = None
    left_target = 1
    right_target = min(2 * c, cols_n - 1)
    last_v_start = -1
    last_attach_col = -1
    for idx, (seg_r, seg_start, seg_end) in enumerate(segments):
        if idx == 0:
            l_dist = c - seg_start
            r_dist = seg_end - c
            direction_right = r_dist < l_dist
            target_col = right_target if direction_right else left_target
        else:
            direction_right = not prev_direction_right
            target_col = right_target if direction_right else left_target
        prev_direction_right = direction_right
        if direction_right:
            h_start = current_col
            h_end = target_col
        else:
            h_start = target_col
            h_end = current_col
        fill_line_horizontal(grid, current_row, min(h_start, h_end), max(h_start, h_end))
        attach_col = target_col
        current_col = target_col
        v_start = current_row + 1
        v_end = seg_r + 2
        v_end = min(v_end, rows_n - 1)
        fill_line_vertical(grid, attach_col, v_start, v_end)
        last_v_start = v_start
        last_attach_col = attach_col
        current_row = v_end + 1
        if idx == len(segments) - 1:
            fill_line_vertical(grid, attach_col, v_start, rows_n - 1)
    return grid

def program(g: List[List[int]]) -> List[List[int]]:
    grid = replace_ones(g)
    s, c = find_seed(grid)
    if s == -1:
        return grid
    rows_n = len(grid)
    cols_n = len(grid[0])
    grid[s][c] = 3
    if is_vertical_mode(grid, s, c):
        right_guides = find_right_guides(grid, s, c)
        grid = propagate_right(grid, s, c, right_guides, rows_n, cols_n)
    elif has_left_guide(grid, s, c):
        left_guides = find_left_guides(grid, s, c)
        grid = propagate_left(grid, s, c, left_guides, rows_n, cols_n)
    else:
        segments = find_horizontal_segments(grid, s)
        grid = propagate_down(grid, s, c, segments, rows_n, cols_n)
    return grid
```