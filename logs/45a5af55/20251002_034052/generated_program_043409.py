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
    # top t rows full
    for rr in range(t):
        r = current_start + rr
        if 0 <= r < s:
            grid[r][current_start : end + 1] = [col] * current_size
    # bottom t rows full
    for rr in range(t):
        r = end - rr
        if 0 <= r < s:
            grid[r][current_start : end + 1] = [col] * current_size
    # left t columns full height
    for jj in range(t):
        j = current_start + jj
        set_column(grid, j, current_start, end, col)
    # right t columns full height
    for jj in range(t):
        j = end - jj
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
        rr = min(s - 1, bar_right)
        for j in range(l, rr + 1):
            grid[r][j] = col

def program(g: List[List[int]]) -> List[List[int]]:
    seq = extract_colors(g)
    n = len(seq)
    s = 2 * n - 2
    grid = [[0] * s for _ in range(s)]
    current_start = 0
    current_size = s
    i = 0
    while i < n:
        col = seq[i]
        t = 0
        j = i
        while j < n and seq[j] == col:
            t += 1
            j += 1
        if current_size <= 0:
            break
        set_perimeter(grid, current_start, current_size, t, col)
        current_start += t
        current_size -= 2 * t
        if current_size < 0:
            current_size = 0
        i = j
    # add center bar for innermost
    if n > 0:
        set_center_bar(grid, 0, s, seq[-1])
    return grid
```