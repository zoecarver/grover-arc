```python
import collections
from typing import List, Tuple

def copy_grid(g: List[List[int]]) -> List[List[int]]:
    return [row[:] for row in g]

def get_background(g: List[List[int]]) -> int:
    return g[0][0]

def get_size(g: List[List[int]]) -> int:
    return len(g)

def has_top_visible(component: List[Tuple[int, int]], g: List[List[int]], bg: int) -> bool:
    n = len(g)
    for i, j in component:
        visible = True
        for k in range(i):
            if g[k][j] != bg:
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
            if g[i][l] != bg:
                visible = False
                break
        if visible:
            return True
    return False

def change_components(g: List[List[int]], colors_to_change: List[int], mapping: dict[int, int], condition_func) -> List[List[int]]:
    n, m = len(g), len(g[0])
    out = copy_grid(g)
    visited = [[False] * m for _ in range(n)]
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
    queue = collections.deque()
    bg = get_background(g)

    for i in range(n):
        for j in range(m):
            if not visited[i][j] and g[i][j] in colors_to_change:
                component = []
                queue.append((i, j))
                visited[i][j] = True
                component.append((i, j))
                while queue:
                    x, y = queue.popleft()
                    for dx, dy in directions:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < n and 0 <= ny < m and not visited[nx][ny] and g[nx][ny] in colors_to_change:
                            visited[nx][ny] = True
                            queue.append((nx, ny))
                            component.append((nx, ny))
                if condition_func(component, g, bg):
                    for x, y in component:
                        old = g[x][y]
                        if old in mapping:
                            out[x][y] = mapping[old]
    return out

def fill_enclosed_zeros(g: List[List[int]]) -> List[List[int]]:
    n, m = len(g), len(g[0])
    out = copy_grid(g)
    visited = [[False] * m for _ in range(n)]
    queue = collections.deque()
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]

    # Enqueue all 0's adjacent to or on border
    # Top
    for j in range(m):
        if g[0][j] == 0:
            queue.append((0, j))
            visited[0][j] = True
        if 1 < n and g[1][j] == 0 and not visited[1][j]:
            queue.append((1, j))
            visited[1][j] = True
    # Bottom
    for j in range(m):
        if g[n - 1][j] == 0:
            queue.append((n - 1, j))
            visited[n - 1][j] = True
        if n - 2 >= 0 and g[n - 2][j] == 0 and not visited[n - 2][j]:
            queue.append((n - 2, j))
            visited[n - 2][j] = True
    # Left
    for i in range(n):
        if g[i][0] == 0:
            queue.append((i, 0))
            visited[i][0] = True
        if 1 < m and g[i][1] == 0 and not visited[i][1]:
            queue.append((i, 1))
            visited[i][1] = True
    # Right
    for i in range(n):
        if g[i][m - 1] == 0:
            queue.append((i, m - 1))
            visited[i][m - 1] = True
        if m - 2 >= 0 and g[i][m - 2] == 0 and not visited[i][m - 2]:
            queue.append((i, m - 2))
            visited[i][m - 2] = True

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
                out[i][j] = 5
    return out

def program(g: List[List[int]]) -> List[List[int]]:
    out = copy_grid(g)
    bg = get_background(g)
    colors = set()
    for row in g:
        for val in row:
            colors.add(val)
    non_bg = [c for c in colors if c != bg and c != 0]

    # First, change top visible to 3
    if non_bg:
        mapping_top = {c: 3 for c in non_bg}
        out = change_components(g, list(mapping_top.keys()), mapping_top, has_top_visible)

    # Then, change left visible to 5 (on original g for condition, but out for finding)
    if non_bg:
        mapping_left = {c: 5 for c in non_bg}
        out = change_components(g, list(mapping_left.keys()), mapping_left, has_left_visible)

    # Fill enclosed 0's with 5
    out = fill_enclosed_zeros(out)
    return out
```