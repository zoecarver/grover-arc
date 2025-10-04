```python
from typing import List, Tuple

def find_red_component(i: int, j: int, g: List[List[int]], visited: List[List[bool]]) -> List[Tuple[int, int]]:
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
            # Check horizontal run in row nx, starting from ny
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

def find_enclosed_zeros(g: List[List[int]]) -> List[List[Tuple[int, int]]]:
    n = len(g)
    visited = [[False] * n for _ in range(n)]
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    components = []
    for i in range(n):
        for j in range(n):
            if g[i][j] == 0 and not visited[i][j]:
                component = []
                touches_boundary = (i == 0 or i == n-1 or j == 0 or j == n-1)
                stack = [(i, j)]
                visited[i][j] = True
                while stack:
                    x, y = stack.pop()
                    component.append((x, y))
                    if x == 0 or x == n-1 or y == 0 or y == n-1:
                        touches_boundary = True
                    for dx, dy in directions:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < n and 0 <= ny < n and g[nx][ny] == 0 and not visited[nx][ny]:
                            visited[nx][ny] = True
                            stack.append((nx, ny))
                if not touches_boundary:
                    components.append(component)
    return components

def program(g: List[List[int]]) -> List[List[int]]:
    n = len(g)
    new_g = [row[:] for row in g]
    # Erase unsupported reds
    visited = [[False] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if new_g[i][j] == 2 and not visited[i][j]:
                component = find_red_component(i, j, new_g, visited)
                supported = any(has_qualifying_blue_run(new_g, x, y, n) for x, y in component)
                if not supported:
                    for x, y in component:
                        new_g[x][y] = 0
    # Fill enclosed zeros
    zero_components = find_enclosed_zeros(new_g)
    for component in zero_components:
        for x, y in component:
            new_g[x][y] = 1
    return new_g
```