```python
from collections import Counter
from typing import List, Tuple

def find_background(g: List[List[int]]) -> int:
    flat = [cell for row in g for cell in row]
    return Counter(flat).most_common(1)[0][0]

def dfs(g: List[List[int]], i: int, j: int, bg: int, visited: List[List[bool]]) -> List[Tuple[int, int]]:
    h = len(g)
    w = len(g[0])
    c = g[i][j]
    stack = [(i, j)]
    comp = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    while stack:
        x, y = stack.pop()
        if visited[x][y]:
            continue
        visited[x][y] = True
        comp.append((x, y))
        for dx, dy in directions:
            nx = x + dx
            ny = y + dy
            if 0 <= nx < h and 0 <= ny < w and not visited[nx][ny] and g[nx][ny] == c:
                stack.append((nx, ny))
    return comp

def get_components(g: List[List[int]], bg: int) -> List[Tuple[int, List[Tuple[int, int]]]]:
    h = len(g)
    w = len(g[0])
    visited = [[False] * w for _ in range(h)]
    components = []
    for i in range(h):
        for j in range(w):
            if not visited[i][j] and g[i][j] != bg:
                comp = dfs(g, i, j, bg, visited)
                components.append((g[i][j], comp))
    return components

def decide_group(c: int, has7: bool, has9: bool) -> str:
    if c == 3:
        return 'top'
    if c == 4:
        return 'bottom'
    if c == 1:
        return 'bottom' if has9 else 'top'
    if c == 2:
        return 'top' if has7 else 'bottom'
    if c in (7, 9):
        return 'top'
    return 'top'

def program(g: List[List[int]]) -> List[List[int]]:
    if not g or not g[0]:
        return g
    bg = find_background(g)
    components = get_components(g, bg)
    has7 = any(cc == 7 for cc, _ in components)
    has9 = any(cc == 9 for cc, _ in components)
    top_places = []
    bottom_places = []
    h = len(g)
    w = len(g[0])
    for c, pos in components:
        group = decide_group(c, has7, has9)
        if not pos:
            continue
        rs = [r for r, _ in pos]
        minr = min(rs)
        maxr = max(rs)
        if group == 'top':
            for r, cc in pos:
                nr = r - minr
                top_places.append((nr, cc, c))
        else:
            shift = h - 1 - maxr
            for r, cc in pos:
                nr = r + shift
                bottom_places.append((nr, cc, c))
    out = [[bg] * w for _ in range(h)]
    for nr, cc, val in top_places + bottom_places:
        if 0 <= nr < h and 0 <= cc < w:
            out[nr][cc] = val
    return out
```