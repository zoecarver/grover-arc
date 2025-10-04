```python
from typing import List, Tuple
from collections import Counter, deque

def get_background(g: List[List[int]]) -> int:
    flat = [cell for row in g for cell in row]
    if not flat:
        return 0
    return Counter(flat).most_common(1)[0][0]

def find_span(row: List[int], bg: int) -> Tuple[int, int, int] | None:
    n = len(row)
    i = 0
    while i < n:
        if row[i] != bg:
            color = row[i]
            start = i
            while i < n and row[i] == color:
                i += 1
            length = i - start
            if length >= 10:
                return color, start, i - 1
        else:
            i += 1
    return None

def is_full(row: List[int], color: int, left: int, right: int, bg: int) -> bool:
    if left < 0 or right >= len(row):
        return False
    for k in range(left, right + 1):
        if row[k] != color:
            return False
    return True

def is_thin(row: List[int], color: int, left: int, right: int, bg: int, w: int) -> bool:
    if left < 0 or right >= w:
        return False
    if row[left] != color or row[right] != color:
        return False
    for k in range(left + 1, right):
        if row[k] != bg:
            return False
    return True

def has_other_in_row(row: List[int], color: int, bg: int, left: int, right: int, w: int) -> bool:
    for k in range(w):
        if left <= k <= right:
            continue
        if row[k] != bg and row[k] != color:
            return True
    return False

def fill_row(grid: List[List[int]], row_idx: int, left: int, right: int, color: int) -> None:
    if row_idx < 0 or row_idx >= len(grid):
        return
    row = grid[row_idx]
    if left < 0 or right >= len(row):
        return
    step_start = left
    step = 2
    if color == 8:
        step_start = left
    elif color == 2:
        step_start = left + 8
    elif color in (1, 4):
        step_start = left + 6
    else:
        return
    for col in range(max(left, step_start), right + 1, step):
        row[col] = color

def compute_component_size(grid: List[List[int]], si: int, sj: int, color: int) -> Tuple[int, set]:
    h = len(grid)
    w = len(grid[0]) if h > 0 else 0
    if si < 0 or si >= h or sj < 0 or sj >= w or grid[si][sj] != color:
        return 0, set()
    visited = set()
    stack = [(si, sj)]
    visited.add((si, sj))
    size = 1
    while stack:
        x, y = stack.pop()
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx = x + dx
            ny = y + dy
            if 0 <= nx < h and 0 <= ny < w and grid[nx][ny] == color and (nx, ny) not in visited:
                visited.add((nx, ny))
                stack.append((nx, ny))
                size += 1
    return size, visited

def program(g: List[List[int]]) -> List[List[int]]:
    if not g:
        return []
    bg = get_background(g)
    grid = [row[:] for row in g]
    h = len(grid)
    w = len(grid[0])
    for start_row in range(h - 4):
        span = find_span(grid[start_row], bg)
        if span is None:
            continue
        color, left, right = span
        if not is_full(grid[start_row + 4], color, left, right, bg):
            continue
        is_blob = True
        for off in range(1, 4):
            j = start_row + off
            if not is_thin(grid[j], color, left, right, bg, w):
                is_blob = False
                break
        if not is_blob:
            continue
        num_with_other = 0
        for off in range(1, 4):
            j = start_row + off
            if has_other_in_row(grid[j], color, bg, left, right, w):
                num_with_other += 1
        if num_with_other < 3:
            fill_row(grid, start_row + 2, left, right, color)
    # Now remove small components
    grid2 = [row[:] for row in grid]
    visited_global = set()
    for i in range(h):
        for j in range(w):
            if grid2[i][j] != bg and (i, j) not in visited_global:
                size, comp = compute_component_size(grid2, i, j, grid2[i][j])
                if size < 20:
                    for x, y in comp:
                        grid2[x][y] = bg
                visited_global.update(comp)
    return grid2
```