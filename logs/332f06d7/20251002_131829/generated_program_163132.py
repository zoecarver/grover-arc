```python
import typing as tp
from collections import deque

def program(g: tp.List[tp.List[int]]) -> tp.List[tp.List[int]]:
    n = len(g)
    grid = [row[:] for row in g]
    # Handle red components (2's): turn to 0 if size == 1 or touches top row
    grid = handle_red_components(grid, n)
    # Fill 0's adjacent to 1's with 1's
    grid = fill_adjacent_blacks(grid, n)
    return grid

def handle_red_components(grid: tp.List[tp.List[int]], n: int) -> tp.List[tp.List[int]]:
    visited = [[False] * n for _ in range(n)]
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for i in range(n):
        for j in range(n):
            if grid[i][j] == 2 and not visited[i][j]:
                component = []
                min_row = n
                q = deque([(i, j)])
                visited[i][j] = True
                component.append((i, j))
                min_row = min(min_row, i)
                while q:
                    x, y = q.popleft()
                    for dx, dy in dirs:
                        nx = x + dx
                        ny = y + dy
                        if 0 <= nx < n and 0 <= ny < n and grid[nx][ny] == 2 and not visited[nx][ny]:
                            visited[nx][ny] = True
                            q.append((nx, ny))
                            component.append((nx, ny))
                            min_row = min(min_row, nx)
                size = len(component)
                if size == 1 or min_row == 0:
                    for cx, cy in component:
                        grid[cx][cy] = 0
    return grid

def fill_adjacent_blacks(grid: tp.List[tp.List[int]], n: int) -> tp.List[tp.List[int]]:
    new_grid = [row[:] for row in grid]
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for i in range(n):
        for j in range(n):
            if grid[i][j] == 0:
                should_fill = any(
                    0 <= i + dx < n and 0 <= j + dy < n and grid[i + dx][j + dy] == 1
                    for dx, dy in dirs
                )
                if should_fill:
                    new_grid[i][j] = 1
            # Copy other cells
            else:
                new_grid[i][j] = grid[i][j]
    return new_grid
```