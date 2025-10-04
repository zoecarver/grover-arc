```python
import collections
from typing import List, Tuple

def copy_grid(g: List[List[int]]) -> List[List[int]]:
    return [row[:] for row in g]

def get_background(g: List[List[int]]) -> int:
    return g[0][0]

def extract_components(g: List[List[int]], target_color: int, bg: int) -> List[List[Tuple[int, int]]]:
    n, m = len(g), len(g[0])
    visited = [[False] * m for _ in range(n)]
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
    components = []
    for i in range(n):
        for j in range(m):
            if not visited[i][j] and g[i][j] == target_color:
                component = []
                queue = collections.deque([(i, j)])
                visited[i][j] = True
                component.append((i, j))
                while queue:
                    x, y = queue.popleft()
                    for dx, dy in directions:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < n and 0 <= ny < m and not visited[nx][ny] and g[nx][ny] == target_color:
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
            if cell != bg and cell != 0 and cell != 1:
                visible = False
                break
        if visible:
            return True
    return False

def touches_bottom(component: List[Tuple[int, int]], n: int, g: List[List[int]], bg: int) -> bool:
    m = len(g[0])
    for i, j in component:
        if i == n - 1 or (i == n - 2 and 0 <= j < m and g[i + 1][j] == bg):
            return True
    return False

def touches_left(component: List[Tuple[int, int]], g: List[List[int]], bg: int, m: int) -> bool:
    n = len(g)
    for i, j in component:
        if j == 0 or (j == 1 and 0 <= i < n and g[i][0] == bg):
            return True
    return False

def flood_fill_from_seeds(out: List[List[int]]) -> None:
    n = len(out)
    m = len(out[0])
    queue = collections.deque()
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
    seeds = {1, 3, 5}
    # Enqueue initial adjacent 0s from seeds
    for i in range(n):
        for j in range(m):
            if out[i][j] in seeds:
                for di, dj in directions:
                    ni = i + di
                    nj = j + dj
                    if 0 <= ni < n and 0 <= nj < m and out[ni][nj] == 0:
                        out[ni][nj] = 5
                        queue.append((ni, nj))
    # Propagate
    while queue:
        i, j = queue.popleft()
        for di, dj in directions:
            ni = i + di
            nj = j + dj
            if 0 <= ni < n and 0 <= nj < m and out[ni][nj] == 0:
                out[ni][nj] = 5
                queue.append((ni, nj))

def program(g: List[List[int]]) -> List[List[int]]:
    out = copy_grid(g)
    bg = get_background(g)
    n = len(g)
    m = len(g[0])
    green_colors = [1, 7, 9]
    orange_colors = [4, 6]
    colors_to_process = set(green_colors + orange_colors)
    for color in colors_to_process:
        components = extract_components(g, color, bg)
        for comp in components:
            if not comp:
                continue
            min_i_comp = min(ii for ii, _ in comp)
            h_t = has_top_visible(comp, g, bg)
            h_l = has_left_visible(comp, g, bg)
            h_r = has_right_visible(comp, g, bg)
            change = False
            target = 3 if color in green_colors else 5
            if color in green_colors:
                if h_t and (not h_r or min_i_comp == 0):
                    change = True
            else:
                if (h_t or h_l) and (not h_r or min_i_comp == 0):
                    change = True
            if change:
                for i, j in comp:
                    out[i][j] = target
    # Special case for background 8 and color 2 touching bottom without touching left
    if bg == 8:
        components = extract_components(g, 2, bg)
        for comp in components:
            if touches_bottom(comp, n, g, bg) and not touches_left(comp, g, bg, m):
                for i, j in comp:
                    out[i][j] = 3
    # Flood fill 0s adjacent to seeds {1,3,5} using 8-connect
    flood_fill_from_seeds(out)
    return out
```