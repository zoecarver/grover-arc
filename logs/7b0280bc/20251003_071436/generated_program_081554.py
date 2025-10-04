```python
from typing import List, Tuple
import collections

def copy_grid(g: List[List[int]]) -> List[List[int]]:
    return [row[:] for row in g]

def get_background(g: List[List[int]]) -> int:
    return g[0][0]

def get_size(g: List[List[int]]) -> int:
    return len(g)

def extract_components(g: List[List[int]], target_val: int, bg: int) -> List[List[Tuple[int, int]]]:
    n, m = len(g), len(g[0])
    visited = [[False] * m for _ in range(n)]
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
    components = []
    for i in range(n):
        for j in range(m):
            if not visited[i][j] and g[i][j] == target_val:
                component = []
                queue = collections.deque([(i, j)])
                visited[i][j] = True
                component.append((i, j))
                while queue:
                    x, y = queue.popleft()
                    for dx, dy in directions:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < n and 0 <= ny < m and not visited[nx][ny] and g[nx][ny] == target_val:
                            visited[nx][ny] = True
                            queue.append((nx, ny))
                            component.append((nx, ny))
                components.append(component)
    return components

def has_top_visible(component: List[Tuple[int, int]], g: List[List[int]], bg: int) -> bool:
    n = len(g)
    for i, j in component:
        visible = True
        for k in range(i):
            if g[k][j] != bg and g[k][j] != 0:
                visible = False
                break
        if visible:
            return True
    return False

def has_left_visible(component: List[Tuple[int, int]], g: List[List[int]], bg: int) -> bool:
    m = len(g[0])
    for i, j in component:
        visible = True
        for l in range(j):
            if g[i][l] != bg and g[i][l] != 0:
                visible = False
                break
        if visible:
            return True
    return False

def touches_bottom(component: List[Tuple[int, int]], n: int, g: List[List[int]], bg: int) -> bool:
    for i, j in component:
        if i >= n - 3:
            return True
    return False

def flood_fill_from_seeds(out: List[List[int]]) -> None:
    n = len(out)
    m = len(out[0])
    queue = collections.deque()
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
    seeds = {1, 3, 5}
    visited = [[False] * m for _ in range(n)]
    for i in range(n):
        for j in range(m):
            if out[i][j] in seeds:
                for di, dj in directions:
                    ni = i + di
                    nj = j + dj
                    if 0 <= ni < n and 0 <= nj < m and out[ni][nj] == 0 and not visited[ni][nj]:
                        out[ni][nj] = 5
                        visited[ni][nj] = True
                        queue.append((ni, nj))
    while queue:
        i, j = queue.popleft()
        for di, dj in directions:
            ni = i + di
            nj = j + dj
            if 0 <= ni < n and 0 <= nj < m and out[ni][nj] == 0 and not visited[ni][nj]:
                out[ni][nj] = 5
                visited[ni][nj] = True
                queue.append((ni, nj))

def fill_enclosed_zeros(g: List[List[int]], new_color: int = 5) -> List[List[int]]:
    n, m = len(g), len(g[0])
    out = copy_grid(g)
    visited = [[False] * m for _ in range(n)]
    queue = collections.deque()
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
    for j in range(m):
        if g[0][j] == 0:
            queue.append((0, j))
            visited[0][j] = True
        if g[n - 1][j] == 0:
            queue.append((n - 1, j))
            visited[n - 1][j] = True
    for i in range(n):
        if g[i][0] == 0:
            queue.append((i, 0))
            visited[i][0] = True
        if g[i][m - 1] == 0:
            queue.append((i, m - 1))
            visited[i][m - 1] = True
    while queue:
        i, j = queue.popleft()
        for di, dj in directions:
            ni, nj = i + di, j + dj
            if 0 <= ni < n and 0 <= nj < m and not visited[ni][nj] and g[ni][nj] == 0:
                visited[ni][nj] = True
                queue.append((ni, nj))
    for i in range(n):
        for j in range(m):
            if g[i][j] == 0 and not visited[i][j]:
                out[i][j] = new_color
    return out

def program(g: List[List[int]]) -> List[List[int]]:
    out = copy_grid(g)
    bg = get_background(g)
    n = get_size(g)
    if bg == 8:
        components = extract_components(g, 2, bg)
        for component in components:
            if touches_bottom(component, n, g, bg):
                for i, j in component:
                    out[i][j] = 3
        flood_fill_from_seeds(out)
        return out
    green = [1, 7, 9]
    for c in green:
        components = extract_components(g, c, bg)
        for component in components:
            if has_top_visible(component, g, bg):
                for i, j in component:
                    out[i][j] = 3
    orange = [4, 6]
    for c in orange:
        components = extract_components(g, c, bg)
        for component in components:
            if has_top_visible(component, g, bg) or has_left_visible(component, g, bg):
                for i, j in component:
                    out[i][j] = 5
    flood_fill_from_seeds(out)
    out = fill_enclosed_zeros(out)
    return out
```