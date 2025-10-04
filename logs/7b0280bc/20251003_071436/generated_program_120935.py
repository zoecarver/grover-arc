```python
from typing import List
import collections

def copy_grid(g: List[List[int]]) -> List[List[int]]:
    return [row[:] for row in g]

def get_background(g: List[List[int]]) -> int:
    return g[0][0]

def get_used_colors(g: List[List[int]], b: int) -> set[int]:
    s: set[int] = set()
    for row in g:
        for cell in row:
            if cell != b and cell != 0:
                s.add(cell)
    return s

directions8 = [(di, dj) for di in [-1, 0, 1] for dj in [-1, 0, 1] if (di, dj) != (0, 0)]

def extract_components(g: List[List[int]], target: int) -> List[List[tuple[int, int]]]:
    n = len(g)
    m = len(g[0])
    visited = [[False] * m for _ in range(n)]
    comps = []
    for i in range(n):
        for j in range(m):
            if not visited[i][j] and g[i][j] == target:
                comp = []
                q = collections.deque([(i, j)])
                visited[i][j] = True
                comp.append((i, j))
                while q:
                    x, y = q.popleft()
                    for dx, dy in directions8:
                        nx = x + dx
                        ny = y + dy
                        if 0 <= nx < n and 0 <= ny < m and not visited[nx][ny] and g[nx][ny] == target:
                            visited[nx][ny] = True
                            q.append((nx, ny))
                            comp.append((nx, ny))
                comps.append(comp)
    return comps

def has_top_visible(comp: List[tuple[int, int]], g: List[List[int]], b: int) -> bool:
    n = len(g)
    for i, j in comp:
        vis = True
        for k in range(i):
            if g[k][j] != b and g[k][j] != 0:
                vis = False
                break
        if vis:
            return True
    return False

def has_left_visible(comp: List[tuple[int, int]], g: List[List[int]], b: int) -> bool:
    m = len(g[0])
    for i, j in comp:
        vis = True
        for l in range(j):
            if g[i][l] != b and g[i][l] != 0:
                vis = False
                break
        if vis:
            return True
    return False

def special_bottom_two(g: List[List[int]]) -> List[List[int]]:
    b = get_background(g)
    if b != 8:
        return g
    n = len(g)
    comps = extract_components(g, 2)
    for comp in comps:
        if comp and max(i for i, _ in comp) >= n - 4:
            for i, j in comp:
                g[i][j] = 3
    return g

def change_visible_components(g: List[List[int]]) -> List[List[int]]:
    b = get_background(g)
    used = get_used_colors(g, b)
    skip = {2}
    if b == 8:
        skip.add(1)
    for c in sorted(used):
        if c in skip or c == b:
            continue
        comps = extract_components(g, c)
        for comp in comps:
            if not comp:
                continue
            top_vis = has_top_visible(comp, g, b)
            left_vis = has_left_visible(comp, g, b)
            same_row = len(set(i for i, _ in comp)) == 1
            change = False
            new_c = 0
            if c % 2 == 1:
                if top_vis:
                    change = True
                    new_c = 3
            else:
                if left_vis or (top_vis and same_row):
                    change = True
                    new_c = 5
            if change:
                for i, j in comp:
                    g[i][j] = new_c
    return g

def fill_stems(g: List[List[int]]) -> List[List[int]]:
    n = len(g)
    m = len(g[0])
    visited = [[False] * m for _ in range(n)]
    q = collections.deque()
    seeds = {1, 3, 5}
    for i in range(n):
        for j in range(m):
            if g[i][j] == 0 and not visited[i][j]:
                adj_seed = any(
                    0 <= i + di < n and 0 <= j + dj < m and g[i + di][j + dj] in seeds
                    for di, dj in directions8
                )
                if adj_seed:
                    g[i][j] = 5
                    visited[i][j] = True
                    q.append((i, j))
    while q:
        i, j = q.popleft()
        for di, dj in directions8:
            ni = i + di
            nj = j + dj
            if 0 <= ni < n and 0 <= nj < m and g[ni][nj] == 0 and not visited[ni][nj]:
                g[ni][nj] = 5
                visited[ni][nj] = True
                q.append((ni, nj))
    return g

def program(g: List[List[int]]) -> List[List[int]]:
    out = copy_grid(g)
    out = change_visible_components(out)
    out = special_bottom_two(out)
    out = fill_stems(out)
    return out
```