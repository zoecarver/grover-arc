```python
from typing import List

def extract_colors(g: List[List[int]]) -> List[int]:
    return [row[0] for row in g]

def set_column(grid: List[List[int]], j: int, start_r: int, end_r: int, col: int) -> None:
    s = len(grid)
    for r in range(max(0, start_r), min(s, end_r + 1)):
        if 0 <= j < s:
            grid[r][j] = col

def set_perimeter(grid: List[List[int]], current_start: int, current_size: int, t: int, col: int) -> None:
    if current_size <= 0 or t <= 0:
        return
    s = len(grid)
    end = current_start + current_size - 1
    set_left = max(0, current_start + 1)
    set_right = min(s - 1, end - 1)
    set_width = max(0, set_right - set_left + 1)
    # top t rows
    for rr in range(t):
        r = current_start + rr
        if 0 <= r < s and set_width > 0:
            grid[r][set_left : set_right + 1] = [col] * set_width
    # bottom t rows
    for rr in range(t):
        r = end - rr
        if 0 <= r < s and set_width > 0:
            grid[r][set_left : set_right + 1] = [col] * set_width
    # left sides
    left_start_j = max(0, current_start + 1)
    left_end_j = min(s - 1, current_start + t)
    for j in range(left_start_j, left_end_j + 1):
        set_column(grid, j, current_start, end, col)
    # right sides
    right_start_j = max(0, end - t)
    right_end_j = min(s - 1, end - 1)
    for j in range(right_start_j, right_end_j + 1):
        set_column(grid, j, current_start, end, col)

def set_center_bar(grid: List[List[int]], current_start: int, current_size: int, col: int) -> None:
    if current_size <= 0:
        return
    s = len(grid)
    end = current_start + current_size - 1
    cross_width = 2 if current_size >= 2 else current_size
    bar_left = current_start + (current_size - cross_width) // 2
    bar_right = bar_left + cross_width - 1
    for r in range(max(0, current_start), min(s, end + 1)):
        l = max(0, bar_left)
        rr = min(s, bar_right + 1)
        w = max(0, rr - l)
        if w > 0:
            grid[r][l : rr] = [col] * w

def program(g: List[List[int]]) -> List[List[int]]:
    c = extract_colors(g)
    h = len(c)
    if h == 0:
        return []
    s = 2 * h - 2
    grid: List[List[int]] = [[0] * s for _ in range(s)]
    i = 0
    current_start = 0
    current_size = s
    first_t = 0
    while i < h:
        col = c[i]
        group_start = i
        count = 0
        while i < h and c[i] == col:
            count += 1
            i += 1
        t = count
        if current_size <= 0:
            continue
        end = current_start + current_size - 1
        is_last = (i == h)
        if is_last:
            set_center_bar(grid, current_start, current_size, col)
        else:
            set_perimeter(grid, current_start, current_size, t, col)
        # fill after first group
        if group_start == 0 and i < h:
            next_col = c[i]
            fill_start = current_start + t
            fill_size = current_size - 2 * t
            if fill_size > 0:
                fill_end = fill_start + fill_size - 1
                fill_left = fill_start
                fill_right = fill_left + fill_size - 1
                for r in range(max(0, fill_start), min(s, fill_end + 1)):
                    l = max(0, fill_left)
                    rr = min(s, fill_right + 1)
                    w = max(0, rr - l)
                    if w > 0:
                        grid[r][l : rr] = [next_col] * w
            first_t = t
        current_start += t
        current_size -= 2 * t
    # if any 0 left, fill with first inner color if possible
    bg_col = c[first_t] if first_t < h else c[0]
    for r in range(s):
        for j in range(s):
            if grid[r][j] == 0:
                grid[r][j] = bg_col
    return grid
```