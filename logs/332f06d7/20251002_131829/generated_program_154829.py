```python
from typing import List

def find_red_component(i: int, j: int, g: List[List[int]], visited: List[List[bool]]) -> List[tuple[int, int]]:
    n = len(g)
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    component = []
    stack = [(i, j)]
    visited[i][j] = True
    while stack:
        x, y = stack.pop()
        component.append((x, y))
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < n and 0 <= ny < n and g[nx][ny] == 2 and not visited[nx][ny]:
                visited[nx][ny] = True
                stack.append((nx, ny))
    return component

def has_qualifying_blue_run(g: List[List[int]], x: int, y: int, n: int) -> bool:
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < n and 0 <= ny < n and g[nx][ny] == 1:
            row = g[nx]
            left = ny
            while left > 0 and row[left - 1] == 1:
                left -= 1
            right = ny
            while right < n - 1 and row[right + 1] == 1:
                right += 1
            if right - left + 1 >= 3:
                return True
    return False

def find_enclosed_zeros(g: List[List[int]]) -> List[List[tuple[int, int]]]:
    n = len(g)
    visited = [[False] * n for _ in range(n)]
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    components = []
    for i in range(n):
        for j in range(n):
            if g[i][j] == 0 and not visited[i][j]:
                component = []
                touches_boundary = (i == 0 or i == n - 1 or j == 0 or j == n - 1)
                stack = [(i, j)]
                visited[i][j] = True
                while stack:
                    px, py = stack.pop()
                    component.append((px, py))
                    if px == 0 or px == n - 1 or py == 0 or py == n - 1:
                        touches_boundary = True
                    for dx, dy in directions:
                        nx, ny = px + dx, py + dy
                        if 0 <= nx < n and 0 <= ny < n and g[nx][ny] == 0 and not visited[nx][ny]:
                            visited[nx][ny] = True
                            stack.append((nx, ny))
                if not touches_boundary:
                    components.append(component)
    return components

def program(g: List[List[int]]) -> List[List[int]]:
    n = len(g)
    out = [row[:] for row in g]
    visited = [[False] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if out[i][j] == 2 and not visited[i][j]:
                component = find_red_component(i, j, out, visited)
                supported = any(has_qualifying_blue_run(out, x, y, n) for x, y in component)
                if not supported:
                    for x, y in component:
                        out[x][y] = 0
    zero_components = find_enclosed_zeros(out)
    for component in zero_components:
        for x, y in component:
            out[x][y] = 1
    return out
```