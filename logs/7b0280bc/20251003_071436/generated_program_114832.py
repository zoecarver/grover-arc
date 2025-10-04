```python
from typing import List, Tuple, Set
import collections

def copy_grid(g: List[List[int]]) -> List[List[int]]:
    return [row[:] for row in g]

def get_background(g: List[List[int]]) -> int:
    return g[0][0]

def extract_components(g: List[List[int]], target: int) -> List[List[Tuple[int, int]]]:
    n = len(g)
    m = len(g[0])
    visited = [[False] * m for _ in range(n)]
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
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
                    for dx, dy in directions:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < n and 0 <= ny < m and not visited[nx][ny] and g[nx][ny] == target:
                            visited[nx][ny] = True
                            q.append((nx, ny))
                            comp.append((nx, ny))
                if comp:
                    comps.append(comp)
    return comps

def has_top_visible(comp: List[Tuple[int, int]], g: List[List[int]], b: int) -> bool:
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

def has_left_visible(comp: List[Tuple[int, int]], g: List[List[int]], b: int) -> bool:
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

def has_right_visible(comp: List[Tuple[int, int]], g: List[List[int]], b: int) -> bool:
    m = len(g[0])
    for i, j in comp:
        vis = True
        for l in range(j + 1, m):
            if g[i][l] != b and g[i][l] != 0:
                vis = False
                break
        if vis:
            return True
    return False

def flood_fill_from_seeds(out: List[List[int]], seeds: Set[int]) -> None:
    n = len(out)
    m = len(out[0])
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
    visited = [[False] * m for _ in range(n)]
    q = collections.deque()
    for i in range(n):
        for j in range(m):
            if out[i][j] in seeds:
                for dx, dy in directions:
                    ni, nj = i + dx, j + dy
                    if 0 <= ni < n and 0 <= nj < m and out[ni][nj] == 0 and not visited[ni][nj]:
                        out[ni][nj] = 5
                        visited[ni][nj] = True
                        q.append((ni, nj))
    while q:
        i, j = q.popleft()
        for dx, dy in directions:
            ni, nj = i + dx, j + dy
            if 0 <= ni < n and 0 <= nj < m and out[ni][nj] == 0 and not visited[ni][nj]:
                out[ni][nj] = 5
                visited[ni][nj] = True
                q.append((ni, nj))

def program(g: List[List[int]]) -> List[List[int]]:
    out = copy_grid(g)
    b = get_background(g)
    n = len(g)
    # Special rule for color 2 when bg == 8 and touches near bottom
    if b == 8:
        comps = extract_components(g, 2)
        for comp in comps:
            if comp and max(i for i, _ in comp) >= n - 4:
                for i, j in comp:
                    out[i][j] = 3
    # Get used colors
    used: Set[int] = set(cell for row in g for cell in row if cell != b and cell > 0)
    # Recolor components based on visibility rules
    for c in used:
        if c == 2:
            continue
        comps = extract_components(g, c)
        target = 3 if c % 2 == 1 else 5
        for comp in comps:
            if not comp:
                continue
            min_i = min(i for i, _ in comp)
            min_j = min(j for _, j in comp)
            max_j = max(j for _, j in comp)
            w = max_j - min_j + 1
            left_vis = has_left_visible(comp, g, b)
            top_vis = has_top_visible(comp, g, b)
            right_vis = has_right_visible(comp, g, b)
            if left_vis or (top_vis and (w > 2 or not right_vis or min_i == 0)):
                for i, j in comp:
                    out[i][j] = target
    # Flood fill 0s connected to seeds
    seeds_set = {1, 3, 5, 7, 9}
    flood_fill_from_seeds(out, seeds_set)
    return out
```