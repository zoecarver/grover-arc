```python
from typing import List
from collections import deque

def copy_grid(g: List[List[int]]) -> List[List[int]]:
    """Copy the input grid to avoid mutating the original."""
    return [row[:] for row in g]

def find_and_color_high_blobs(g: List[List[int]]) -> List[List[int]]:
    """Find connected components of cells >4 (4-connected, any >4 value) and assign colors cycling 4,3,2,1."""
    grid = copy_grid(g)
    rows = len(grid)
    cols = len(grid[0])
    visited = [[False] * cols for _ in range(rows)]
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    color_cycle = [4, 3, 2, 1]
    cycle_index = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] > 4 and not visited[r][c]:
                color = color_cycle[cycle_index % 4]
                cycle_index += 1
                stack = deque([(r, c)])
                while stack:
                    x, y = stack.popleft()
                    if visited[x][y]:
                        continue
                    visited[x][y] = True
                    grid[x][y] = color
                    for dx, dy in directions:
                        nx = x + dx
                        ny = y + dy
                        if 0 <= nx < rows and 0 <= ny < cols and not visited[nx][ny] and grid[nx][ny] > 4:
                            stack.append((nx, ny))
    return grid

def program(g: List[List[int]]) -> List[List[int]]:
    """Main program: copy grid, then color high value blobs."""
    grid = copy_grid(g)
    grid = find_and_color_high_blobs(grid)
    return grid
```