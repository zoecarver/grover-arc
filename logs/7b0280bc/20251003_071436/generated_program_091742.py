```python
from typing import List, Tuple
import collections

def copy_grid(g: List[List[int]]) -> List[List[int]]:
    return [row[:] for row in g]

def get_background(g: List[List[int]]) -> int:
    return g[0][0]

def get_size(g: List[List[int]]) -> int:
    return len(g)

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

def has_bottom_visible(component: List[Tuple[int, int]], g: List[List[int]], bg: int) -> bool:
    n = len(g)
    for i, j in component:
        visible = True
        for k in range(i + 1, n):
            if g[k][j] != bg and g[k][j] != 0:
                visible = False
                break
        if visible:
            return True
    return False

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
    n = get_size(g)
    m = len(g[0])
    changes = {}
    greens = [c for c in [1, 7, 9] if c != bg]
    oranges = [c for c in [4, 6] if c != bg]
    for c in greens:
        components = extract_components(g, c)
        for positions in components:
            if not positions:
                continue
            min_i_val = min(i for i, _ in positions)
            max_i_val = max(i for i, _ in positions)
            min_j_val = min(j for _, j in positions)
            max_j_val = max(j for _, j in positions)
            h = max_i_val - min_i_val + 1
            w = max_j_val - min_j_val + 1
            top_vis = has_top_visible(positions, g, bg)
            if not top_vis:
                continue
            do_change = False
            if w > h:
                do_change = True
            else:
                right_vis = has_right_visible(positions, g, bg)
                if not right_vis or min_i_val == 0:
                    do_change = True
            if do_change:
                for i, j in positions:
                    changes[(i, j)] = 3
    for c in oranges:
        components = extract_components(g, c)
        for positions in components:
            if not positions:
                continue
            min_i_val = min(i for i, _ in positions)
            max_i_val = max(i for i, _ in positions)
            min_j_val = min(j for _, j in positions)
            max_j_val = max(j for _, j in positions)
            h = max_i_val - min_i_val + 1
            w = max_j_val - min_j_val + 1
            top_vis = has_top_visible(positions, g, bg)
            left_vis = has_left_visible(positions, g, bg)
            if not (top_vis or left_vis):
                continue
            do_change = False
            if w > h:
                do_change = True
            else:
                right_vis = has_right_visible(positions, g, bg)
                if not right_vis or min_i_val == 0:
                    do_change = True
            if do_change:
                for i, j in positions:
                    changes[(i, j)] = 5
    if bg == 8:
        c = 2
        components = extract_components(g, c)
        for positions in components:
            if has_bottom_visible(positions, g, bg):
                for i, j in positions:
                    changes[(i, j)] = 3
    for (i, j), new_val in changes.items():
        out[i][j] = new_val
    flood_fill_from_seeds(out)
    return out
```