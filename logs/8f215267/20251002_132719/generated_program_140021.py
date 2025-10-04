```python
from typing import List
import copy

def get_background(grid: List[List[int]]) -> int:
    return grid[0][0]

def get_pattern(color: int, background: int) -> List[int]:
    if color == 8:
        return [0, 2, 4, 6, 8, 10]
    if color == 6:
        return [0, 4, 6, 8, 10]
    if color == 4:
        return [0, 6, 8, 10]
    if color == 3:
        return [0, 4, 6, 8, 10]
    if color == 1 or color == 2:
        if background == 3:
            if color == 1:
                return [0, 6, 8, 10]
            return []
        return [0, 8, 10]
    return []

def remove_small_components(grid: List[List[int]], background: int, threshold: int = 10) -> List[List[int]]:
    rows = len(grid)
    cols = len(grid[0])
    visited = [[False] * cols for _ in range(rows)]
    output = copy.deepcopy(grid)
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] != background and not visited[i][j]:
                stack = [(i, j)]
                component = []
                size = 0
                component_color = grid[i][j]
                visited[i][j] = True
                while stack:
                    x, y = stack.pop()
                    size += 1
                    component.append((x, y))
                    for dx, dy in directions:
                        nx = x + dx
                        ny = y + dy
                        if 0 <= nx < rows and 0 <= ny < cols and not visited[nx][ny] and grid[nx][ny] == component_color:
                            visited[nx][ny] = True
                            stack.append((nx, ny))
                if size <= threshold:
                    for x, y in component:
                        output[x][y] = background
    return output

def is_solid_run(grid: List[List[int]], row: int, start_col: int, width: int, color: int) -> bool:
    return all(grid[row][start_col + k] == color for k in range(width))

def is_isolated(grid: List[List[int]], row: int, start_col: int, width: int, color: int, cols: int) -> bool:
    left_ok = start_col == 0 or grid[row][start_col - 1] != color
    right_ok = start_col + width == cols or grid[row][start_col + width] != color
    return left_ok and right_ok

def find_bottom_row(grid: List[List[int]], start_row: int, start_col: int, color: int, rows: int, cols: int, width: int = 11) -> int:
    bottom_row = -1
    for r in range(start_row + 1, rows):
        if is_solid_run(grid, r, start_col, width, color) and is_isolated(grid, r, start_col, width, color, cols):
            bottom_row = r
    return bottom_row

def set_thin_rows(grid: List[List[int]], top_row: int, bottom_row: int, start_col: int, color: int, background: int, width: int = 11):
    for r in range(top_row + 1, bottom_row):
        grid[r][start_col] = color
        grid[r][start_col + width - 1] = color
        for k in range(1, width - 1):
            grid[r][start_col + k] = background

def apply_pattern_fill(grid: List[List[int]], top_row: int, start_col: int, color: int, background: int, cols: int):
    pattern_row = top_row + 2
    if pattern_row >= len(grid):
        return
    pattern = get_pattern(color, background)
    for pos in pattern:
        col = start_col + pos
        if 0 <= col < cols:
            grid[pattern_row][col] = color

def detect_and_complete_us(grid: List[List[int]], background: int) -> List[List[int]]:
    rows = len(grid)
    cols = len(grid[0])
    r = 0
    width = 11
    while r < rows:
        found = False
        for s in range(cols - width + 1):
            c = grid[r][s]
            if c == background:
                continue
            if is_solid_run(grid, r, s, width, c) and is_isolated(grid, r, s, width, c, cols):
                bottom_r = find_bottom_row(grid, r, s, c, rows, cols)
                if bottom_r != -1:
                    n_thin = bottom_r - r - 1
                    if n_thin >= 3:
                        set_thin_rows(grid, r, bottom_r, s, c, background)
                        apply_pattern_fill(grid, r, s, c, background, cols)
                        r = bottom_r + 1
                        found = True
                        break
        if not found:
            r += 1
    return grid

def program(g: List[List[int]]) -> List[List[int]]:
    grid = copy.deepcopy(g)
    background = get_background(grid)
    grid = remove_small_components(grid, background)
    grid = detect_and_complete_us(grid, background)
    return grid
```