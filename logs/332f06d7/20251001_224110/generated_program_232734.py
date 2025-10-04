```python
from typing import List, Set, Tuple

def touches_border(i: int, j: int, n: int) -> bool:
    return i == 0 or i == n - 1 or j == 0 or j == n - 1

def handle_red(g: List[List[int]]) -> List[List[int]]:
    n = len(g)
    if n == 0:
        return []
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
                size = 1
                component.append((i, j))
                while stack:
                    x, y = stack.pop()
                    for dx, dy in directions:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < n and 0 <= ny < n and not visited[nx][ny] and g[nx][ny] == 2:
                            visited[nx][ny] = True
                            stack.append((nx, ny))
                            size += 1
                            if nx == 0:
                                touches_top = True
                            component.append((nx, ny))
                if size == 1 or touches_top:
                    for x, y in component:
                        new_g[x][y] = 0
    return new_g

def label_blue_components(g: List[List[int]]) -> List[List[int]]:
    n = len(g)
    if n == 0:
        return []
    label_grid = [[0] * n for _ in range(n)]
    visited = [[False] * n for _ in range(n)]
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    label = 1
    for i in range(n):
        for j in range(n):
            if g[i][j] == 1 and not visited[i][j]:
                stack = [(i, j)]
                visited[i][j] = True
                label_grid[i][j] = label
                while stack:
                    x, y = stack.pop()
                    for dx, dy in directions:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < n and 0 <= ny < n and not visited[nx][ny] and g[nx][ny] == 1:
                            visited[nx][ny] = True
                            label_grid[nx][ny] = label
                            stack.append((nx, ny))
                label += 1
    return label_grid

def find_zero_component(g: List[List[int]], label_grid: List[List[int]], start_i: int, start_j: int, n: int) -> Tuple[List[Tuple[int, int]], bool, Set[int]]:
    visited_local = [[False] * n for _ in range(n)]
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    component: List[Tuple[int, int]] = []
    blue_labels: Set[int] = set()
    stack = [(start_i, start_j)]
    visited_local[start_i][start_j] = True
    touches_b = touches_border(start_i, start_j, n)
    while stack:
        x, y = stack.pop()
        component.append((x, y))
        touches_b = touches_b or touches_border(x, y, n)
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < n and 0 <= ny < n:
                if g[nx][ny] == 0 and not visited_local[nx][ny]:
                    visited_local[nx][ny] = True
                    stack.append((nx, ny))
                elif g[nx][ny] == 1:
                    blue_labels.add(label_grid[nx][ny])
    return component, touches_b, blue_labels

def fill_internal_holes(g: List[List[int]]) -> List[List[int]]:
    n = len(g)
    if n == 0:
        return []
    new_g = [row[:] for row in g]
    label_grid = label_blue_components(g)
    visited = [[False] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if g[i][j] == 0 and not visited[i][j]:
                component, touches_b, blue_labels = find_zero_component(g, label_grid, i, j, n)
                if not touches_b and len(blue_labels) == 1:
                    for x, y in component:
                        new_g[x][y] = 1
                for x, y in component:
                    visited[x][y] = True
    return new_g

def program(g: List[List[int]]) -> List[List[int]]:
    g_after_red = handle_red(g)
    g_final = fill_internal_holes(g_after_red)
    return g_final
```