```python
from typing import List, Tuple, Set
import collections

def copy_grid(g: List[List[int]]) -> List[List[int]]:
    return [row[:] for row in g]

def get_background(g: List[List[int]]) -> int:
    return g[0][0]

def get_used_colors(grid: List[List[int]], b: int) -> Set[int]:
    s: Set[int] = set()
    for row in grid:
        for cell in row:
            if cell != b and cell > 0:
                s.add(cell)
    return s

def extract_components(g: List[List[int]], target_val: int) -> List[List[Tuple[int, int]]]:
    n = len(g)
    m = len(g[0])
    visited = [[False] * m for _ in range(n)]
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
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

def has_top_visible(component: List[Tuple[int, int]], g: List[List[int]], b: int) -> bool:
    n = len(g)
    for i, j in component:
        visible = True
        for k in range(i):
            if g[k][j] != b and g[k][j] != 0:
                visible = False
                break
        if visible:
            return True
    return False

def has_left_visible(component: List[Tuple[int, int]], g: List[List[int]], b: int) -> bool:
    m = len(g[0])
    for i, j in component:
        visible = True
        for l in range(j):
            if g[i][l] != b and g[i][l] != 0:
                visible = False
                break
        if visible:
            return True
    return False

def touches_bottom(component: List[Tuple[int, int]], n: int) -> bool:
    if not component:
        return False
    return max(i for i, _ in component) >= n - 3

def flood_fill_from_seeds(out: List[List[int]]) -> None:
    n = len(out)
    m = len(out[0])
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
    seeds = {1, 3, 5}
    visited = [[False] * m for _ in range(n)]
    queue = collections.deque()
    for i in range(n):
        for j in range(m):
            if out[i][j] in seeds:
                for di, dj in directions:
                    ni, nj = i + di, j + dj
                    if 0 <= ni < n and 0 <= nj < m and out[ni][nj] == 0 and not visited[ni][nj]:
                        out[ni][nj] = 5
                        visited[ni][nj] = True
                        queue.append((ni, nj))
    while queue:
        i, j = queue.popleft()
        for di, dj in directions:
            ni, nj = i + di, j + dj
            if 0 <= ni < n and 0 <= nj < m and out[ni][nj] == 0 and not visited[ni][nj]:
                out[ni][nj] = 5
                visited[ni][nj] = True
                queue.append((ni, nj))

def program(g: List[List[int]]) -> List[List[int]]:
    out = copy_grid(g)
    n = len(g)
    b = get_background(g)
    used = get_used_colors(g, b)
    # Special rule for color 2 when background is 8
    if b == 8:
        comps = extract_components(g, 2)
        for comp in comps:
            if touches_bottom(comp, n):
                for i, j in comp:
                    out[i][j] = 3
    # Rule for odd colors
    for c in used:
        if c % 2 == 1 and c != b and not (c == 1 and b == 8):
            comps = extract_components(g, c)
            for comp in comps:
                min_i = min(i for i, _ in comp)
                if min_i <= 3 and has_top_visible(comp, g, b):
                    for i, j in comp:
                        out[i][j] = 3
    # Rule for even colors
    for c in used:
        if c % 2 == 0 and c != b and c != 2 and not (c == 6 and b == 9):
            comps = extract_components(g, c)
            for comp in comps:
                min_i = min(i for i, _ in comp)
                if min_i <= 3 and (has_top_visible(comp, g, b) or has_left_visible(comp, g, b)):
                    for i, j in comp:
                        out[i][j] = 5
    # Flood fill empty spaces from seeds
    flood_fill_from_seeds(out)
    return out
```