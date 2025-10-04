```python
from typing import List
import copy

def get_background(grid: List[List[int]]) -> int:
    return grid[0][0] if grid and grid[0] else 0

def get_pattern(color: int, background: int) -> List[int]:
    if color == 8:
        return [0, 2, 4, 6, 8, 10]
    if color == 6:
        return [0, 4, 6, 8, 10]
    if color == 4:
        return [0, 6, 8, 10]
    if color == 3:
        return [0, 4, 6, 8, 10]
    if color == 1:
        return [0, 6, 8, 10] if background == 3 else [0, 8, 10]
    if color == 2:
        return [] if background == 3 else [0, 8, 10]
    return []

def is_solid_run(grid: List[List[int]], row: int, start: int, width: int, color: int) -> bool:
    if row >= len(grid) or start + width > len(grid[row]):
        return False
    return all(grid[row][start + k] == color for k in range(width))

def remove_small_components(grid: List[List[int]], background: int, threshold: int = 5) -> List[List[int]]:
    g = copy.deepcopy(grid)
    rows = len(g)
    cols = len(g[0]) if rows > 0 else 0
    if rows == 0 or cols == 0:
        return g
    visited = [[False] * cols for _ in range(rows)]
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for i in range(rows):
        for j in range(cols):
            if g[i][j] != background and not visited[i][j]:
                component = []
                stack = [(i, j)]
                color = g[i][j]
                while stack:
                    x, y = stack.pop()
                    if visited[x][y]:
                        continue
                    visited[x][y] = True
                    component.append((x, y))
                    for dx, dy in directions:
                        nx = x + dx
                        ny = y + dy
                        if 0 <= nx < rows and 0 <= ny < cols and not visited[nx][ny] and g[nx][ny] == color:
                            stack.append((nx, ny))
                if len(component) <= threshold:
                    for x, y in component:
                        g[x][y] = background
    return g

def program(g: List[List[int]]) -> List[List[int]]:
    rows = len(g)
    if rows == 0:
        return g
    cols = len(g[0])
    bg = get_background(g)
    grid = remove_small_components(g, bg, 5)
    r = 0
    while r < rows - 4:
        found = False
        for s in range(cols - 10):
            c = grid[r][s]
            if c == bg:
                continue
            if not is_solid_run(grid, r, s, 11, c):
                continue
            if s > 0 and grid[r][s - 1] == c:
                continue
            b = r + 4
            if b >= rows:
                continue
            is_bottom_solid = is_solid_run(grid, b, s, 11, c)
            is_bottom_thin = (grid[b][s] == c and grid[b][s + 10] == c and
                              all(grid[b][j] == bg for j in range(s + 1, s + 10)))
            if is_bottom_solid or is_bottom_thin:
                for k in range(r + 1, b):
                    grid[k][s] = c
                    grid[k][s + 10] = c
                    for j in range(s + 1, s + 10):
                        grid[k][j] = bg
                pat_row = r + 2
                if pat_row < rows:
                    pat = get_pattern(c, bg)
                    for off in pat:
                        j = s + off
                        if 0 <= j < cols:
                            grid[pat_row][j] = c
                found = True
                break
        if found:
            r = b + 1
        else:
            r += 1
    return grid
```