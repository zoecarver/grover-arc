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

def vertical_fill(grid: List[List[int]], s: int, c: int) -> List[List[int]]:
    rows_n = len(grid)
    cols_n = len(grid[0])
    BACKGROUND = 8
    new_grid = [row[:] for row in grid]

    # Find left_red_col
    left_red_col = None
    for j in range(c + 1, cols_n):
        if grid[s][j] == 2:
            left_red_col = j
            break
    if left_red_col is None:
        return new_grid

    # Find end_left
    end_left = s
    col = left_red_col
    while end_left + 1 < rows_n and grid[end_left + 1][col] == 2:
        end_left += 1
    num_8s = end_left - s + 1
    left_v = c + num_8s
    if left_v >= cols_n:
        left_v = cols_n - 1

    # Find right_red_col: first col > left_red_col with 2 below s
    right_red_col = None
    for j in range(left_red_col + 1, cols_n):
        found = False
        for k in range(s + 1, rows_n):
            if grid[k][j] == 2:
                found = True
                break
        if found:
            right_red_col = j
            break
    if right_red_col is None:
        return new_grid

    right_start = right_red_col - num_8s
    if right_start < 0:
        right_start = 0
    right_v = right_start

    b = BACKGROUND
    if b >= rows_n:
        b = rows_n - 1

    # Fill left horizontal
    for j in range(c, left_v + 1):
        if new_grid[s][j] == 8:
            new_grid[s][j] = 3

    # Fill right horizontal
    for j in range(right_start, cols_n):
        if new_grid[s][j] == 8:
            new_grid[s][j] = 3

    # Fill vertical left_v
    for i in range(s, b + 1):
        if new_grid[i][left_v] == 8:
            new_grid[i][left_v] = 3

    # Fill vertical right_v
    for i in range(s, b + 1):
        if new_grid[i][right_v] == 8:
            new_grid[i][right_v] = 3

    # Fill connecting horizontal at b
    connect_end = right_red_col - left_v
    if connect_end > cols_n - 1:
        connect_end = cols_n - 1
    for j in range(left_v, connect_end + 1):
        if new_grid[b][j] == 8:
            new_grid[b][j] = 3

    return new_grid

def horizontal_fill(grid: List[List[int]], s: int, c: int) -> List[List[int]]:
    rows_n = len(grid)
    cols_n = len(grid[0])
    BACKGROUND = 8
    new_grid = [row[:] for row in grid]

    # Find segments
    segments: List[Tuple[int, int, int]] = []
    for r in range(s + 1, rows_n):
        row = grid[r]
        j = 0
        while j < cols_n:
            if row[j] == 2:
                st = j
                while j < cols_n and row[j] == 2:
                    j += 1
                en = j - 1
                if en - st + 1 >= 2:
                    segments.append((r, st, en))
            else:
                j += 1

    previous_h = s - 1
    current_c = c
    is_first = True
    for r, start, en in segments:
        l = en - start + 1
        if not (start <= current_c <= en):
            continue
        p = current_c - start
        dist_left = p
        dist_right = en - current_c
        closer_dist = min(dist_left, dist_right)
        is_left_closer = dist_left <= dist_right
        length_v = closer_dist + 1
        edge_case = False
        if is_left_closer:
            test_start = current_c - (BACKGROUND - 1)
            if test_start < 0:
                edge_case = True
        else:
            test_end = BACKGROUND
            if test_end >= cols_n:
                edge_case = True
        if edge_case:
            length_v = l
        if is_first:
            start_v = s
            is_first = False
        else:
            start_v = previous_h + 1
        h = start_v + length_v - 1
        # Cap to before r
        if h >= r:
            h = r - 1
            length_v = max(1, h - start_v + 1)
        # Fill vertical
        for ii in range(start_v, h + 1):
            jj = current_c
            if 0 <= jj < cols_n and new_grid[ii][jj] == 8:
                new_grid[ii][jj] = 3
        # Horizontal at h
        if edge_case or not is_left_closer:
            hor_start = current_c
            hor_end = BACKGROUND
        else:
            hor_start = BACKGROUND - (BACKGROUND - 1)
            hor_end = BACKGROUND
        hor_start = max(0, hor_start)
        hor_end = min(cols_n - 1, hor_end)
        min_j = min(hor_start, hor_end)
        max_j = max(hor_start, hor_end)
        for jj in range(min_j, max_j + 1):
            if 0 <= jj < cols_n and new_grid[h][jj] == 8:
                new_grid[h][jj] = 3
        # New c
        if (edge_case or not is_left_closer):
            new_c = hor_end
        else:
            new_c = hor_start
        current_c = new_c
        previous_h = h

    # Final vertical
    start_v = previous_h + 1
    for ii in range(start_v, rows_n):
        jj = current_c
        if 0 <= jj < cols_n and new_grid[ii][jj] == 8:
            new_grid[ii][jj] = 3

    return new_grid

def program(g: List[List[int]]) -> List[List[int]]:
    grid = replace_ones(g)
    seed = find_seed(grid)
    if seed is None:
        return grid
    s, c = seed
    if is_vertical_mode(grid, s, c):
        return vertical_fill(grid, s, c)
    else:
        return horizontal_fill(grid, s, c)
```