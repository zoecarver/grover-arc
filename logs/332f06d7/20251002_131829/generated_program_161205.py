```python
from typing import List
from collections import deque

def fill_blacks_with_blue(grid: List[List[int]]) -> List[List[int]]:
    n = len(grid)
    current = [row[:] for row in grid]
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for _ in range(n):
        new_g = [row[:] for row in current]
        changed = False
        for i in range(n):
            for j in range(n):
                if current[i][j] == 2:
                    has_blue = any(
                        0 <= i + di < n and 0 <= j + dj < n and current[i + di][j + dj] == 1
                        for di, dj in directions
                    )
                    if has_blue:
                        new_g[i][j] = 1
                        changed = True
        current = new_g
        if not changed:
            break
    return current

def erase_anomalous_red(grid: List[List[int]]) -> List[List[int]]:
    n = len(grid)
    new_grid = [row[:] for row in grid]
    visited = [[False] * n for _ in range(n)]
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for i in range(n):
        for j in range(n):
            if new_grid[i][j] == 3 and not visited[i][j]:
                queue = deque([(i, j)])
                visited[i][j] = True
                component = [(i, j)]
                touches_left = (j == 0)
                touches_right = (j == n - 1)
                touches_bottom = (i == n - 1)
                size_comp = 1
                while queue:
                    x, y = queue.popleft()
                    for dx, dy in directions:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < n and 0 <= ny < n and new_grid[nx][ny] == 3 and not visited[nx][ny]:
                            visited[nx][ny] = True
                            queue.append((nx, ny))
                            component.append((nx, ny))
                            size_comp += 1
                            touches_left = touches_left or (ny == 0)
                            touches_right = touches_right or (ny == n - 1)
                            touches_bottom = touches_bottom or (nx == n - 1)
                keep = size_comp > 1 and (touches_left or touches_right or touches_bottom)
                if not keep:
                    for cx, cy in component:
                        new_grid[cx][cy] = 2
    return new_grid

def program(g: List[List[int]]) -> List[List[int]]:
    temp = fill_blacks_with_blue(g)
    result = erase_anomalous_red(temp)
    return result
```