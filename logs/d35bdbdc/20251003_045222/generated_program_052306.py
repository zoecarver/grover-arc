```python
from typing import List

def program(g: List[List[int]]) -> List[List[int]]:
    n = len(g)
    grid = [row[:] for row in g]
    visited = [[False] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if grid[i][j] != 0 and not visited[i][j]:
                color = grid[i][j]
                component = []
                stack = [(i, j)]
                touch_side = False
                while stack:
                    x, y = stack.pop()
                    if visited[x][y]:
                        continue
                    visited[x][y] = True
                    component.append((x, y))
                    if y == 0 or y == n - 1:
                        touch_side = True
                    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < n and 0 <= ny < n and not visited[nx][ny] and grid[nx][ny] == color:
                            stack.append((nx, ny))
                if not touch_side:
                    for x, y in component:
                        grid[x][y] = 0
    return grid
```