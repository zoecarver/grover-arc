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

def propagate_right(grid: List[List[int]], s: int, c: int, rows_n: int, cols_n: int) -> None:
    guides = [j for j in range(c + 1, cols_n) if any(grid[i][j] == 2 for i in range(s, rows_n))]
    guides.sort()
    if not guides:
        return
    first_j = guides[0]
    min_i_all = min(i for i in range(rows_n) if grid[i][first_j] == 2)
    max_i_all = max(i for i in range(rows_n) if grid[i][first_j] == 2)
    first_total = max_i_all - min_i_all + 1
    end_row = min(s + first_total - 2, rows_n - 1)
    drop_cols = []
    for j in guides:
        below_len = sum(1 for i in range(s, rows_n) if grid[i][j] == 2)
        has_at_s = grid[s][j] == 2
        b_start = min((i for i in range(s, rows_n) if grid[i][j] == 2), default=None)
        row_dist = (b_start - s) if b_start is not None and not has_at_s else 0
        if has_at_s:
            h_length = below_len + 1
            drop_col = c + h_length - 1
            h_start = c
            h_end = drop_col
        else:
            drop_col = j - row_dist
            h_start = drop_col
            h_end = cols_n - 1
        actual_start = max(0, min(h_start, h_end))
        actual_end = min(cols_n - 1, max(h_start, h_end))
        if actual_start <= actual_end:
            fill_line_horizontal(grid, s, actual_start, actual_end)
        if 0 <= drop_col < cols_n:
            drop_cols.append(drop_col)
    for dc in drop_cols:
        fill_line_vertical(grid, dc, s, end_row)
    if len(drop_cols) > 1:
        min_c = min(drop_cols)
        max_c = max(drop_cols)
        fill_line_horizontal(grid, end_row, min_c, max_c)

def propagate_left(grid: List[List[int]], s: int, c: int, rows_n: int, cols_n: int) -> None:
    guides = [j for j in range(c) if any(grid[i][j] == 2 for i in range(s, rows_n))]
    guides.sort(reverse=True)
    if not guides:
        return
    first_j = guides[0]
    min_i_all = min(i for i in range(rows_n) if grid[i][first_j] == 2)
    max_i_all = max(i for i in range(rows_n) if grid[i][first_j] == 2)
    first_total = max_i_all - min_i_all + 1
    end_row = min(s + first_total - 2, rows_n - 1)
    drop_cols = []
    for j in guides:
        below_len = sum(1 for i in range(s, rows_n) if grid[i][j] == 2)
        has_at_s = grid[s][j] == 2
        b_start = min((i for i in range(s, rows_n) if grid[i][j] == 2), default=None)
        row_dist = (b_start - s) if b_start is not None and not has_at_s else 0
        if has_at_s:
            h_length = below_len + 1
            drop_col = c - h_length + 1
            h_start = drop_col
            h_end = c
        else:
            drop_col = j + row_dist
            h_start = 0
            h_end = drop_col
        actual_start = max(0, min(h_start, h_end))
        actual_end = min(cols_n - 1, max(h_start, h_end))
        if actual_start <= actual_end:
            fill_line_horizontal(grid, s, actual_start, actual_end)
        if 0 <= drop_col < cols_n:
            drop_cols.append(drop_col)
    for dc in drop_cols:
        fill_line_vertical(grid, dc, s, end_row)
    if len(drop_cols) > 1:
        min_c = min(drop_cols)
        max_c = max(drop_cols)
        fill_line_horizontal(grid, end_row, min_c, max_c)

def propagate_down(grid: List[List[int]], s: int, c: int, rows_n: int, cols_n: int) -> None:
    segments = find_horizontal_segments(grid, s)
    if not segments:
        fill_line_vertical(grid, c, s + 1, rows_n - 1)
        return
    original_c = c
    current_r = s
    current_c = c
    # First segment
    first_seg_r, first_start, first_end = segments[0]
    dist = first_seg_r - current_r
    l_dist = current_c - first_start
    r_dist = first_end - current_c
    first_dir = "left" if l_dist <= r_dist else "right"
    target = 1 if first_dir == "left" else min(2 * original_c, cols_n - 1)
    pre_length = 1
    post_length = max(0, dist - 3)
    h_row = current_r + pre_length + 1
    # Pre vertical
    pre_start = current_r + 1
    pre_end = min(h_row - 1, rows_n - 1)
    if pre_start <= pre_end:
        fill_line_vertical(grid, current_c, pre_start, pre_end)
    # Horizontal
    h_start = min(current_c, target)
    h_end = max(current_c, target)
    fill_line_horizontal(grid, h_row, h_start, h_end)
    # Post vertical
    post_start = h_row + 1
    post_end = min(first_seg_r - 1, rows_n - 1)
    if post_start <= post_end and post_length > 0:
        fill_line_vertical(grid, target, post_start, min(post_start + post_length - 1, post_end))
    # Fill at seg_r
    if grid[first_seg_r][target] == 8:
        grid[first_seg_r][target] = 3
    current_r = first_seg_r
    current_c = target
    # Subsequent segments
    is_left = first_dir == "left"
    for seg_idx in range(1, len(segments)):
        seg_r, seg_start, seg_end = segments[seg_idx]
        dist = seg_r - current_r
        this_is_left = not is_left
        is_left = this_is_left
        target = 1 if this_is_left else min(2 * original_c, cols_n - 1)
        pre_length = (dist - 2) // 2
        post_length = dist - 2 - pre_length
        h_row = current_r + pre_length + 1
        # Pre vertical
        pre_start = current_r + 1
        pre_end = min(h_row - 1, rows_n - 1)
        if pre_start <= pre_end:
            fill_line_vertical(grid, current_c, pre_start, pre_end)
        # Horizontal
        h_start = min(current_c, target)
        h_end = max(current_c, target)
        fill_line_horizontal(grid, h_row, h_start, h_end)
        # Post vertical
        post_start = h_row + 1
        post_end = min(seg_r - 1, rows_n - 1)
        if post_start <= post_end and post_length > 0:
            fill_line_vertical(grid, target, post_start, min(post_start + post_length - 1, post_end))
        # Fill at seg_r
        if grid[seg_r][target] == 8:
            grid[seg_r][target] = 3
        current_r = seg_r
        current_c = target
    # Final vertical
    fill_line_vertical(grid, current_c, current_r + 1, rows_n - 1)

def program(g: List[List[int]]) -> List[List[int]]:
    grid = replace_ones(g)
    seed = find_seed(grid)
    if seed is None:
        return grid
    s, c = seed
    grid[s][c] = 3
    rows_n = len(grid)
    if rows_n == 0:
        return grid
    cols_n = len(grid[0])
    if is_vertical_mode(grid, s, c):
        propagate_right(grid, s, c, rows_n, cols_n)
    elif has_left_guide(grid, s, c):
        propagate_left(grid, s, c, rows_n, cols_n)
    else:
        propagate_down(grid, s, c, rows_n, cols_n)
    return grid
```