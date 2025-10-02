```python
from typing import List

def get_background(grid: List[List[int]]) -> int:
    return grid[0][0] if grid else 0

def find_indicator_column(grid: List[List[int]], bg: int, rows: int, cols: int) -> int:
    max_count = 0
    best_c = -1
    for c in range(cols):
        ind_rs: List[int] = []
        for r in range(rows):
            val = grid[r][c]
            if val != 0 and val != bg:
                ind_rs.append(r)
        isolated = True
        for i in range(1, len(ind_rs)):
            if ind_rs[i] == ind_rs[i - 1] + 1:
                isolated = False
                break
        if isolated and len(ind_rs) > max_count:
            max_count = len(ind_rs)
            best_c = c
    return best_c

def get_indicator_rows(grid: List[List[int]], c_ind: int, bg: int, rows: int) -> List[int]:
    ind_rows: List[int] = []
    for r in range(rows):
        if grid[r][c_ind] != 0 and grid[r][c_ind] != bg:
            ind_rows.append(r)
    return ind_rows

def get_strip_bounds(ind_rows: List[int], rows: int) -> tuple:
    min_r = min(ind_rows)
    max_r = max(ind_rows)
    s = max(0, min_r - 1)
    e = min(rows - 1, max_r + 1)
    return s, e

def get_strip_l_r(grid: List[List[int]], c_ind: int, s: int, e: int, bg: int, cols: int) -> tuple:
    l = c_ind
    strip_r = c_ind
    # expand left
    while l > 0:
        candidate = l - 1
        all_empty = True
        has_zero = False
        for rr in range(s, e + 1):
            val = grid[rr][candidate]
            if val != 0 and val != bg:
                all_empty = False
                break
            if val == 0:
                has_zero = True
        if all_empty and has_zero:
            l = candidate
        else:
            break
    # expand right
    while strip_r < cols - 1:
        candidate = strip_r + 1
        all_empty = True
        has_zero = False
        for rr in range(s, e + 1):
            val = grid[rr][candidate]
            if val != 0 and val != bg:
                all_empty = False
                break
            if val == 0:
                has_zero = True
        if all_empty and has_zero:
            strip_r = candidate
        else:
            break
    return l, strip_r

def count_components(grid: List[List[int]], color: int, s: int, e: int, l: int, strip_r: int, rows: int, cols: int) -> int:
    visited = [[False] * cols for _ in range(rows)]
    count = 0
    dirs = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    def dfs(start_r: int, start_c: int):
        stack: List[tuple] = [(start_r, start_c)]
        while stack:
            cr, cc = stack.pop()
            if not (0 <= cr < rows and 0 <= cc < cols) or visited[cr][cc]:
                continue
            if grid[cr][cc] != color:
                continue
            if s <= cr <= e and l <= cc <= strip_r:
                continue
            visited[cr][cc] = True
            for dr, dc in dirs:
                nr, nc = cr + dr, cc + dc
                stack.append((nr, nc))
    for r in range(rows):
        for c in range(cols):
            if not visited[r][c] and grid[r][c] == color and not (s <= r <= e and l <= c <= strip_r):
                dfs(r, c)
                count += 1
    return count

def program(g: List[List[int]]) -> List[List[int]]:
    if not g:
        return []
    rows = len(g)
    cols = len(g[0])
    bg = get_background(g)
    c_ind = find_indicator_column(g, bg, rows, cols)
    if c_ind == -1:
        return [[0] * cols for _ in range(rows)]
    ind_rows_list = get_indicator_rows(g, c_ind, bg, rows)
    num_ind = len(ind_rows_list)
    if num_ind == 0:
        return []
    s, e = get_strip_bounds(ind_rows_list, rows)
    l, strip_r = get_strip_l_r(g, c_ind, s, e, bg, cols)
    width = strip_r - l + 1
    height = 2 * num_ind + 1
    output = [[0] * width for _ in range(height)]
    for k in range(num_ind):
        out_row = 2 * k + 1
        color = g[ind_rows_list[k]][c_ind]
        num_reps = count_components(g, color, s, e, l, strip_r, rows, cols)
        for i in range(num_reps):
            out_col = 2 * i + 1
            if out_col < width:
                output[out_row][out_col] = color
    return output
```