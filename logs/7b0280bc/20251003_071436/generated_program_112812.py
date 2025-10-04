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

def get_bbox_and_size(comp: List[Tuple[int, int]]) -> Tuple[int, int, int, int, int]:
    if not comp:
        return 0, 0, 0, 0, 0
    min_i = min(i for i, _ in comp)
    max_i = max(i for i, _ in comp)
    min_j = min(j for _, j in comp)
    max_j = max(j for _, j in comp)
    size = len(comp)
    return min_i, max_i, min_j, max_j, size

def has_top_visible(comp: List[Tuple[int, int]], g: List[List[int]], bg: int) -> bool:
    n = len(g)
    for i, j in comp:
        visible = True
        for k in range(i):
            if g[k][j] != bg and g[k][j] != 0:
                visible = False
                break
        if visible:
            return True
    return False

def has_left_visible(comp: List[Tuple[int, int]], g: List[List[int]], bg: int) -> bool:
    m = len(g[0])
    for i, j in comp:
        visible = True
        for l in range(j):
            if g[i][l] != bg and g[i][l] != 0:
                visible = False
                break
        if visible:
            return True
    return False

def has_right_visible(comp: List[Tuple[int, int]], g: List[List[int]], bg: int) -> bool:
    m = len(g[0])
    for i, j in comp:
        visible = True
        for l in range(j + 1, m):
            if g[i][l] != bg and g[i][l] != 0:
                visible = False
                break
        if visible:
            return True
    return False

def touches_bottom(comp: List[Tuple[int, int]], n: int) -> bool:
    if not comp:
        return False
    return max(i for i, _ in comp) >= n - 4

def change_green_components(out: List[List[int]], g: List[List[int]], bg: int, n: int) -> List[List[int]]:
    green_colors = {1, 7, 9} - {bg}
    for c in green_colors:
        comps = extract_components(g, c)
        for comp in comps:
            size = len(comp)
            if size > 4:
                continue
            min_i, max_i, min_j, max_j, _ = get_bbox_and_size(comp)
            h = max_i - min_i + 1
            w = max_j - min_j + 1
            top_vis = has_top_visible(comp, g, bg)
            if not top_vis:
                continue
            left_vis = has_left_visible(comp, g, bg)
            right_vis = has_right_visible(comp, g, bg)
            shape_ok = (w > h) or left_vis or (w == h and size == 1 and (min_i == 0 or not right_vis))
            if shape_ok:
                for i, j in comp:
                    out[i][j] = 3
    return out

def change_orange_components(out: List[List[int]], g: List[List[int]], bg: int, n: int) -> List[List[int]]:
    orange_colors = {4, 6} - {bg}
    for c in orange_colors:
        comps = extract_components(g, c)
        for comp in comps:
            size = len(comp)
            if size > 6:
                continue
            min_i, max_i, min_j, max_j, _ = get_bbox_and_size(comp)
            h = max_i - min_i + 1
            w = max_j - min_j + 1
            top_vis = has_top_visible(comp, g, bg)
            left_vis = has_left_visible(comp, g, bg)
            if not (top_vis or left_vis):
                continue
            right_vis = has_right_visible(comp, g, bg)
            shape_ok = (w > h) or left_vis or (w == h and size == 1 and (min_i == 0 or not right_vis))
            if shape_ok:
                for i, j in comp:
                    out[i][j] = 5
    return out

def change_special_two_components(out: List[List[int]], g: List[List[int]], bg: int, n: int) -> List[List[int]]:
    if bg != 8:
        return out
    comps = extract_components(g, 2)
    for comp in comps:
        if touches_bottom(comp, n):
            for i, j in comp:
                out[i][j] = 3
    return out

def flood_fill_from_seeds(out: List[List[int]]) -> List[List[int]]:
    n, m = len(out), len(out[0])
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
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
    return out

def program(g: List[List[int]]) -> List[List[int]]:
    out = copy_grid(g)
    n = len(g)
    bg = get_background(g)
    out = change_green_components(out, g, bg, n)
    out = change_orange_components(out, g, bg, n)
    out = change_special_two_components(out, g, bg, n)
    out = flood_fill_from_seeds(out)
    return out
```