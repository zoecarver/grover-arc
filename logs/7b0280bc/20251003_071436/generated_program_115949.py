```python
from typing import List, Tuple, Set
import collections

def copy_grid(g: List[List[int]]) -> List[List[int]]:
    return [row[:] for row in g]

def get_used_colors(g: List[List[int]], b: int) -> Set[int]:
    s: Set[int] = set()
    for row in g:
        for cell in row:
            if cell != b and cell != 0:
                s.add(cell)
    return s

def extract_components(g: List[List[int]], target: int) -> List[List[Tuple[int, int]]]:
    n = len(g)
    m = len(g[0])
    visited = [[False] * m for _ in range(n)]
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
    components = []
    for i in range(n):
        for j in range(m):
            if not visited[i][j] and g[i][j] == target:
                component = []
                queue = collections.deque([(i, j)])
                visited[i][j] = True
                component.append((i, j))
                while queue:
                    x, y = queue.popleft()
                    for dx, dy in directions:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < n and 0 <= ny < m and not visited[nx][ny] and g[nx][ny] == target:
                            visited[nx][ny] = True
                            queue.append((nx, ny))
                            component.append((nx, ny))
                if component:
                    components.append(component)
    return components

def has_top_visible(comp: List[Tuple[int, int]], g: List[List[int]], b: int) -> bool:
    n = len(g)
    for i, j in comp:
        visible = True
        for k in range(i):
            if g[k][j] != b and g[k][j] != 0:
                visible = False
                break
        if visible:
            return True
    return False

def has_left_visible(comp: List[Tuple[int, int]], g: List[List[int]], b: int) -> bool:
    m = len(g[0])
    for i, j in comp:
        visible = True
        for l in range(j):
            if g[i][l] != b and g[i][l] != 0:
                visible = False
                break
        if visible:
            return True
    return False

def touches_bottom(comp: List[Tuple[int, int]], n: int) -> bool:
    return max(i for i, _ in comp) >= n - 3

def touches_right(comp: List[Tuple[int, int]], m: int) -> bool:
    return any(j == m - 1 for _, j in comp)

def is_valid(x: int, y: int, n: int, m: int) -> bool:
    return 0 <= x < n and 0 <= y < m

def get_adjacent_seed(out: List[List[int]], i: int, j: int, n: int, m: int, seeds: Set[int]) -> bool:
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
    for di, dj in directions:
        ni, nj = i + di, j + dj
        if is_valid(ni, nj, n, m) and out[ni][nj] in seeds:
            return True
    return False

def program(g: List[List[int]]) -> List[List[int]]:
    out = copy_grid(g)
    n = len(g)
    m = len(g[0])
    b = g[0][0]
    used = get_used_colors(g, b)
    seeds_set = {1, 3, 5}
    directions8 = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]

    # Special rule for color 2 when background is 8
    if b == 8:
        comps_2 = extract_components(g, 2)
        for comp in comps_2:
            if touches_bottom(comp, n):
                for i, j in comp:
                    out[i][j] = 3

    # First pass: change qualifying components based on color and background
    stem_cs: Set[int] = set()
    if b == 9:
        stem_cs.add(4)
    elif b == 7:
        stem_cs.add(6)
    # For b == 4 or 8, stem_cs empty

    for c in used:
        if c == 2 or c == b:
            continue
        comps = extract_components(g, c)
        for comp in comps:
            min_row = min(i for i, _ in comp)
            if min_row > 4:
                continue
            top_vis = has_top_visible(comp, g, b)
            left_vis = has_left_visible(comp, g, b)
            change_to = 0
            if c == 1:
                if min_row <= 2 and top_vis and left_vis:
                    change_to = 3
            elif c % 2 == 1:  # Other odds: 7, 9
                if min_row <= 2 and top_vis and (min_row == 0 or left_vis):
                    change_to = 3
            elif c in stem_cs:
                right_touch = touches_right(comp, m)
                if min_row <= 4 and top_vis and not right_touch:
                    change_to = 5
            if change_to > 0:
                for i, j in comp:
                    out[i][j] = change_to

    # Second pass: change remaining stem components adjacent to seeds
    for c in stem_cs:
        comps = extract_components(out, c)
        for comp in comps:
            adj_to_seed = False
            for i, j in comp:
                if get_adjacent_seed(out, i, j, n, m, seeds_set):
                    adj_to_seed = True
                    break
            if adj_to_seed:
                for i, j in comp:
                    out[i][j] = 5

    # Flood fill 0s connected to seeds {1,3,5} using 8-way
    visited = [[False] * m for _ in range(n)]
    queue = collections.deque()
    for i in range(n):
        for j in range(m):
            if out[i][j] == 0 and not visited[i][j]:
                if get_adjacent_seed(out, i, j, n, m, seeds_set):
                    out[i][j] = 5
                    visited[i][j] = True
                    queue.append((i, j))
    while queue:
        i, j = queue.popleft()
        for di, dj in directions8:
            ni, nj = i + di, j + dj
            if is_valid(ni, nj, n, m) and out[ni][nj] == 0 and not visited[ni][nj]:
                out[ni][nj] = 5
                visited[ni][nj] = True
                queue.append((ni, nj))

    return out
```