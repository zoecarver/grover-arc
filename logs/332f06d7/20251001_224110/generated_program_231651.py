```python
from typing import List

def touches_border(i: int, j: int, n: int) -> bool:
    return i == 0 or i == n - 1 or j == 0 or j == n - 1

def handle_red(g: List[List[int]]) -> List[List[int]]:
    n = len(g)
    if n == 0:
        return [row[:] for row in g]
    new_g = [row[:] for row in g]
    visited = [[False] * n for _ in range(n)]
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for i in range(n):
        for j in range(n):
            if g[i][j] == 2 and not visited[i][j]:
                component = []
                stack = [(i, j)]
                visited[i][j] = True
                touches_top = (i == 0)
                size = 0
                while stack:
                    x, y = stack.pop()
                    component.append((x, y))
                    size += 1
                    for dx, dy in directions:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < n and 0 <= ny < n and g[nx][ny] == 2 and not visited[nx][ny]:
                            visited[nx][ny] = True
                            stack.append((nx, ny))
                            touches_top = touches_top or (nx == 0)
                if size == 1 or touches_top:
                    for x, y in component:
                        new_g[x][y] = 0
    return new_g

def fill_internal_blue_holes(g: List[List[int]]) -> List[List[int]]:
    n = len(g)
    if n == 0:
        return [row[:] for row in g]
    new_g = [row[:] for row in g]
    visited = [[False] * n for _ in range(n)]
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for i in range(n):
        for j in range(n):
            if g[i][j] == 0 and not visited[i][j]:
                component = []
                stack = [(i, j)]
                visited[i][j] = True
                border_touch = touches_border(i, j, n)
                blue_touch = False
                while stack:
                    x, y = stack.pop()
                    component.append((x, y))
                    border_touch = border_touch or touches_border(x, y, n)
                    for dx, dy in directions:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < n and 0 <= ny < n:
                            if g[nx][ny] == 1:
                                blue_touch = True
                            if g[nx][ny] == 0 and not visited[nx][ny]:
                                visited[nx][ny] = True
                                stack.append((nx, ny))
                if not border_touch and blue_touch:
                    for x, y in component:
                        new_g[x][y] = 1
    return new_g

def program(g: List[List[int]]) -> List[List[int]]:
    g = handle_red(g)
    g = fill_internal_blue_holes(g)
    return g
```