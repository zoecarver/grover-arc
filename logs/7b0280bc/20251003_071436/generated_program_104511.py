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

def get_bbox(comp: List[Tuple[int, int]]) -> Tuple[int, int, int, int]:
    if not comp:
        return 0, 0, 0, 0
    min_i = min(i for i, j in comp)
    max_i = max(i for i, j in comp)
    min_j = min(j for i, j in comp)
    max_j = max(j for i, j in comp)
    return min_i, max_i, min_j, max_j

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

def touches_bottom(comp: List[Tuple[int, int]], n: int) -> bool:
    return max((i for i, j in comp), default=-1) >= n - 4

def fill_vertical_down(out: List[List[int]], seeds: set, target: int):
    n = len(out)
    m = len(out[0])
    for j in range(m):
        i = 0
        while i < n:
            if out[i][j] in seeds:
                i += 1
                while i < n and out[i][j] == 0:
                    out[i][j] = target
                    i += 1
            i += 1

def flood_from_seeds(out: List[List[int]], seeds: set, target: int):
    n = len(out)
    m = len(out[0])
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
    visited = [[False] * m for _ in range(n)]
    queue = collections.deque()
    for i in range(n):
        for j in range(m):
            if out[i][j] in seeds:
                for di, dj in directions:
                    ni, nj = i + di, j + dj
                    if 0 <= ni < n and 0 <= nj < m and out[ni][nj] == 0 and not visited[ni][nj]:
                        out[ni][nj] = target
                        visited[ni][nj] = True
                        queue.append((ni, nj))
    while queue:
        i, j = queue.popleft()
        for di, dj in directions:
            ni, nj = i + di, j + dj
            if 0 <= ni < n and 0 <= nj < m and out[ni][nj] == 0 and not visited[ni][nj]:
                out[ni][nj] = target
                visited[ni][nj] = True
                queue.append((ni, nj))

def program(g: List[List[int]]) -> List[List[int]]:
    out = copy_grid(g)
    bg = get_background(g)
    n = get_size(g)
    m = len(g[0])
    present = set()
    for row in g:
        for cell in row:
            if cell != bg and cell != 0:
                present.add(cell)
    if bg == 8:
        green_src = set()
    else:
        odds = [c for c in present if c % 2 == 1 and c != bg and c != 5]
        green_src = set(odds) if odds else set()
    evens_non2 = [c for c in present if c % 2 == 0 and c != bg and c != 2]
    orange_src = set(evens_non2) if evens_non2 else set()
    # Recolor green to 3
    for c in green_src:
        comps = extract_components(g, c)
        for comp in comps:
            if not comp:
                continue
            min_i, _, min_j, max_j = get_bbox(comp)
            w = max_j - min_j + 1
            if (has_left_visible(comp, g, bg) or
                (has_top_visible(comp, g, bg) and min_i <= 1 and w == 1) or
                (has_top_visible(comp, g, bg) and min_i == 2 and w > 1)):
                for i, j in comp:
                    out[i][j] = 3
    # Recolor orange to 5
    for c in orange_src:
        comps = extract_components(g, c)
        for comp in comps:
            if not comp:
                continue
            min_i, _, min_j, max_j = get_bbox(comp)
            w = max_j - min_j + 1
            if (has_left_visible(comp, g, bg) or
                (has_top_visible(comp, g, bg) and min_i <= 1 and w == 1) or
                (has_top_visible(comp, g, bg) and min_i == 2 and w > 1)):
                for i, j in comp:
                    out[i][j] = 5
    # Special for bg==8, change bottom 2 to 3
    if bg == 8:
        comps = extract_components(g, 2)
        for comp in comps:
            if touches_bottom(comp, n):
                for i, j in comp:
                    out[i][j] = 3
    # Vertical down fill from 1,3,5
    seeds_vertical = {1, 3, 5}
    fill_vertical_down(out, seeds_vertical, 5)
    # Flood connected from 3,5
    seeds_flood = {3, 5}
    flood_from_seeds(out, seeds_flood, 5)
    return out
```