```python
from typing import List, Tuple, Set

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
                touches_top = False
                stack = [(i, j)]
                visited[i][j] = True
                while stack:
                    x, y = stack.pop()
                    component.append((x, y))
                    if x == 0:
                        touches_top = True
                    for dx, dy in directions:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < n and 0 <= ny < n and not visited[nx][ny] and g[nx][ny] == 2:
                            visited[nx][ny] = True
                            stack.append((nx, ny))
                if len(component) == 1 or touches_top:
                    for x, y in component:
                        new_g[x][y] = 0
    return new_g

def label_blue_components(g: List[List[int]]) -> List[List[int]]:
    n = len(g)
    if n == 0:
        return []
    label_grid = [[0] * n for _ in range(n)]
    visited = [[False] * n for _ in range(n)]
    label = 1
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
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

def find_zero_component(g: List[List[int]], label_grid: List[List[int]], start_i: int, start_j: int, n: int) -> Tuple[List[Tuple[int, int]], bool, Set[int], bool]:
    visited = [[False] * n for _ in range(n)]
    component = []
    stack = [(start_i, start_j)]
    visited[start_i][start_j] = True
    touches_border_flag = touches_border(start_i, start_j, n)
    adj_labels = set()
    touches_red = False
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    while stack:
        x, y = stack.pop()
        component.append((x, y))
        touches_border_flag = touches_border_flag or touches_border(x, y, n)
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < n and 0 <= ny < n and not visited[nx][ny]:
                if g[nx][ny] == 0:
                    visited[nx][ny] = True
                    stack.append((nx, ny))
                elif g[nx][ny] == 1:
                    if label_grid[nx][ny] > 0:
                        adj_labels.add(label_grid[nx][ny])
                elif g[nx][ny] == 2:
                    touches_red = True
    return component, touches_border_flag, adj_labels, touches_red

def fill_internal_blue_holes(g: List[List[int]]) -> List[List[int]]:
    n = len(g)
    if n == 0:
        return []
    label_grid = label_blue_components(g)
    visited = [[False] * n for _ in range(n)]
    new_g = [row[:] for row in g]
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # not used directly but for completeness
    for i in range(n):
        for j in range(n):
            if g[i][j] == 0 and not visited[i][j]:
                component, touches_b, adj_labels, touches_r = find_zero_component(g, label_grid, i, j, n)
                if not touches_b and len(adj_labels) == 1 and not touches_r:
                    for x, y in component:
                        new_g[x][y] = 1
                for x, y in component:  # mark visited regardless
                    visited[x][y] = True
    return new_g

def program(g: List[List[int]]) -> List[List[int]]:
    g = handle_red(g)
    g = fill_internal_blue_holes(g)
    return g
```