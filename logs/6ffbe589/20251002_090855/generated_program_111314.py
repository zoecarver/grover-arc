```python
from typing import List
from collections import deque

def omit_peripheral_small_components(g: List[List[int]]) -> List[List[int]]:
    """Omit small components (size <=2, no holes assumed, high y >=15) by setting to 0."""
    rows, cols = len(g), len(g[0])
    grid = [row[:] for row in g]
    visited = [[False] * cols for _ in range(rows)]
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] != 0 and not visited[i][j]:
                color = grid[i][j]
                component_size = 0
                min_r_comp = rows
                stack = [(i, j)]
                visited[i][j] = True
                while stack:
                    x, y = stack.pop()
                    component_size += 1
                    min_r_comp = min(min_r_comp, x)
                    for dx, dy in directions:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < rows and 0 <= ny < cols and not visited[nx][ny] and grid[nx][ny] == color:
                            visited[nx][ny] = True
                            stack.append((nx, ny))
                if component_size <= 2 and min_r_comp >= 15:
                    # Reset component to 0 (simplified, reflood to set)
                    visited_reset = [[False] * cols for _ in range(rows)]
                    reset_stack = [(i, j)]
                    visited_reset[i][j] = True
                    while reset_stack:
                        x, y = reset_stack.pop()
                        grid[x][y] = 0
                        for dx, dy in directions:
                            nx, ny = x + dx, y + dy
                            if 0 <= nx < rows and 0 <= ny < cols and not visited_reset[nx][ny] and g[nx][ny] == color:
                                visited_reset[nx][ny] = True
                                reset_stack.append((nx, ny))
    return grid

def trim_empty_borders(g: List[List[int]]) -> List[List[int]]:
    """Trim empty borders by extracting minimal bounding box subgrid."""
    rows, cols = len(g), len(g[0])
    min_r, max_r, min_c, max_c = rows, -1, cols, -1
    for i in range(rows):
        for j in range(cols):
            if g[i][j] != 0:
                min_r = min(min_r, i)
                max_r = max(max_r, i)
                min_c = min(min_c, j)
                max_c = max(max_c, j)
    if max_r < 0:
        return [[]]
    subgrid = [g[i][min_c:max_c + 1] for i in range(min_r, max_r + 1)]
    return subgrid

def pad_to_square(grid: List[List[int]]) -> List[List[int]]:
    """Pad the grid to a square by adding zero columns/rows on right/bottom."""
    if not grid:
        return [[]]
    h = len(grid)
    w = len(grid[0]) if h > 0 else 0
    side = max(h, w)
    new_grid = [[0] * side for _ in range(side)]
    for i in range(h):
        for j in range(w):
            new_grid[i][j] = grid[i][j]
    return new_grid

def program(g: List[List[int]]) -> List[List[int]]:
    """Compose rules: omit small peripheral, trim borders, pad to square."""
    g = omit_peripheral_small_components(g)
    g = trim_empty_borders(g)
    g = pad_to_square(g)
    return g
```