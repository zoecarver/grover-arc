```python
from typing import List, Tuple
import collections

def copy_grid(g: List[List[int]]) -> List[List[int]]:
    return [row[:] for row in g]

def get_background(g: List[List[int]]) -> int:
    return g[0][0]

def extract_components(g: List[List[int]], target_val: int) -> List[List[Tuple[int, int]]]:
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
                if component:
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

def has_right_visible(component: List[Tuple[int, int]], g: List[List[int]], bg: int) -> bool:
    m = len(g[0])
    for i, j in component:
        visible = True
        for l in range(j + 1, m):
            cell = g[i][l]
            if cell != bg and cell != 0:
                visible = False
                break
        if visible:
            return True
    return False

def touches_bottom(component: List[Tuple[int, int]], n: int) -> bool:
    return any(i >= n - 5 for i, _ in component)

def flood_fill_from_seeds(out: List[List[int]]) -> None:
    n = len(out)
    m = len(out[0])
    queue = collections.deque()
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
    seeds = {1, 3, 5, 7, 9}
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

def program(g: List[List[int]]) -> List[List[int]]:
    out = copy_grid(g)
    bg = get_background(g)
    n = len(g)
    m = len(g[0])
    # Special for bg == 8, change bottom 2's to 3
    if bg == 8:
        components = extract_components(g, 2)
        for component in components:
            if touches_bottom(component, n):
                for i, j in component:
                    out[i][j] = 3
    # General for green colors {1,7,9} excluding bg
    green_colors = {1, 7, 9} - {bg}
    for c in green_colors:
        components = extract_components(g, c)
        for component in components:
            if len(component) > 4:
                continue
            min_i = min(i for i, _ in component)
            max_i = max(i for i, _ in component)
            min_j = min(j for _, j in component)
            max_j = max(j for _, j in component)
            h = max_i - min_i + 1
            w = max_j - min_j + 1
            if has_top_visible(component, g, bg) and (w > h or (h == w and min_i <= 2 and not has_right_visible(component, g, bg))):
                for i, j in component:
                    out[i][j] = 3
    # General for orange colors {4,6} excluding bg, with size <=6 and min_i <=3
    orange_colors = {4, 6} - {bg}
    for c in orange_colors:
        components = extract_components(g, c)
        for component in components:
            if len(component) > 6:
                continue
            min_i = min(i for i, _ in component)
            if min_i > 3:
                continue
            if has_top_visible(component, g, bg) or has_left_visible(component, g, bg):
                for i, j in component:
                    out[i][j] = 5
    # Flood fill from seeds
    flood_fill_from_seeds(out)
    return out
```