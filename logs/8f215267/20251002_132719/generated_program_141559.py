```python
from typing import List
from copy import deepcopy

def get_background(grid: List[List[int]]) -> int:
    return grid[0][0] if grid else 0

def remove_small_components(grid: List[List[int]], background: int, threshold: int = 10) -> List[List[int]]:
    rows = len(grid)
    if rows == 0:
        return grid
    cols = len(grid[0])
    visited = [[False] * cols for _ in range(rows)]
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] != background and not visited[i][j]:
                stack = [(i, j)]
                visited[i][j] = True
                size = 1
                c = grid[i][j]
                while stack:
                    x, y = stack.pop()
                    for dx, dy in directions:
                        nx = x + dx
                        ny = y + dy
                        if 0 <= nx < rows and 0 <= ny < cols and not visited[nx][ny] and grid[nx][ny] == c:
                            visited[nx][ny] = True
                            stack.append((nx, ny))
                            size += 1
                if size <= threshold:
                    stack = [(i, j)]
                    visited[i][j] = True
                    while stack:
                        x, y = stack.pop()
                        grid[x][y] = background
                        for dx, dy in directions:
                            nx = x + dx
                            ny = y + dy
                            if 0 <= nx < rows and 0 <= ny < cols and not visited[nx][ny] and grid[nx][ny] == c:
                                visited[nx][ny] = True
                                stack.append((nx, ny))
    return grid

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

def is_solid_run(grid: List[List[int]], row: int, start_col: int, width: int, color: int) -> bool:
    if row < 0 or row >= len(grid) or start_col < 0 or start_col + width > len(grid[row]):
        return False
    for k in range(width):
        if grid[row][start_col + k] != color:
            return False
    return True

def is_isolated(grid: List[List[int]], row: int, start_col: int, width: int, color: int, cols: int) -> bool:
    left_ok = start_col == 0 or grid[row][start_col - 1] != color
    return left_ok

def find_bottom_row(grid: List[List[int]], start_row: int, start_col: int, color: int, rows: int, cols: int, width: int = 11) -> int:
    for r in range(start_row + 1, rows):
        if is_solid_run(grid, r, start_col, width, color) and is_isolated(grid, r, start_col, width, color, cols):
            return r
    return -1

def set_thin_rows(grid: List[List[int]], top_row: int, bottom_row: int, start_col: int, color: int, background: int, width: int = 11):
    for r in range(top_row + 1, bottom_row):
        if r >= len(grid):
            continue
        # set sides
        if start_col < len(grid[r]):
            grid[r][start_col] = color
        right = start_col + width - 1
        if right < len(grid[r]):
            grid[r][right] = color
        # set middle to background
        for k in range(1, width - 1):
            col = start_col + k
            if col < len(grid[r]):
                grid[r][col] = background

def apply_pattern_fill(grid: List[List[int]], top_row: int, start_col: int, color: int, background: int, cols: int):
    pattern_row = top_row + 2
    if pattern_row >= len(grid):
        return
    row = grid[pattern_row]
    pattern = get_pattern(color, background)
    # clear span including possible extra column
    for k in range(12):
        col = start_col + k
        if col < cols:
            row[col] = background
    # apply pattern
    for pos in pattern:
        col = start_col + pos
        if 0 <= col < cols:
            row[col] = color

def detect_and_complete_us(grid: List[List[int]], background: int) -> List[List[int]]:
    rows = len(grid)
    if rows == 0:
        return grid
    cols = len(grid[0])
    width = 11
    r = 0
    while r < rows:
        found_u = False
        for s in range(cols - width + 1):
            c = grid[r][s]
            if c == background:
                continue
            if not is_solid_run(grid, r, s, width, c):
                continue
            if not is_isolated(grid, r, s, width, c, cols):
                continue
            bottom_r = find_bottom_row(grid, r, s, c, rows, cols, width)
            if bottom_r == -1:
                # remove isolated solid run
                for k in range(width + 1):
                    col = s + k
                    if col < cols and grid[r][col] == c:
                        grid[r][col] = background
                continue
            n_thin = bottom_r - r - 1
            if n_thin < 2:
                continue
            # complete the U
            set_thin_rows(grid, r, bottom_r, s, c, background, width)
            apply_pattern_fill(grid, r, s, c, background, cols)
            # skip past the bottom
            r = bottom_r + 1
            found_u = True
            break
        if not found_u:
            r += 1
    return grid

def program(g: List[List[int]]) -> List[List[int]]:
    grid = deepcopy(g)
    bg = get_background(grid)
    grid = remove_small_components(grid, bg, 10)
    grid = detect_and_complete_us(grid, bg)
    return grid
```