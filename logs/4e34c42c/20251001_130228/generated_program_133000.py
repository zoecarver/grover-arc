```python
from typing import List, Tuple

def find_large_components(g: List[List[int]]) -> List[List[Tuple[int, int]]]:
    if not g or not g[0]:
        return []
    bg = g[0][0]
    rows, cols = len(g), len(g[0])
    visited = [[False] * cols for _ in range(rows)]
    components = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for i in range(rows):
        for j in range(cols):
            if g[i][j] != bg and not visited[i][j]:
                comp = []
                stack = [(i, j)]
                visited[i][j] = True
                while stack:
                    x, y = stack.pop()
                    comp.append((x, y))
                    for dx, dy in directions:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < rows and 0 <= ny < cols and not visited[nx][ny] and g[nx][ny] != bg:
                            visited[nx][ny] = True
                            stack.append((nx, ny))
                if len(comp) >= 10:
                    components.append(comp)
    return components

def get_bounding_subgrid(g: List[List[int]], comp: List[Tuple[int, int]], bg: int) -> List[List[int]]:
    if not comp:
        return []
    minr = min(r for r, c in comp)
    maxr = max(r for r, c in comp)
    minc = min(c for r, c in comp)
    maxc = max(c for r, c in comp)
    h, w = maxr - minr + 1, maxc - minc + 1
    sub = [[g[minr + ii][minc + jj] for jj in range(w)] for ii in range(h)]
    return sub

def trim_outer_bg(sub: List[List[int]], bg: int) -> List[List[int]]:
    if not sub:
        return []
    h = len(sub)
    if h == 0:
        return []
    w = len(sub[0])
    if w == 0:
        return sub
    # trim left
    while w > 0 and all(sub[r][0] == bg for r in range(h)):
        sub = [row[1:] for row in sub]
        w -= 1
    # trim right
    while w > 0 and all(sub[r][w - 1] == bg for r in range(h)):
        sub = [row[:-1] for row in sub]
        w -= 1
    return sub

def trim_left_protrusions(sub: List[List[int]], bg: int) -> List[List[int]]:
    if not sub:
        return []
    h = len(sub)
    if h == 0:
        return sub
    w = len(sub[0])
    if w == 0:
        return sub
    while w > 0:
        col_set = {sub[r][0] for r in range(h) if sub[r][0] != bg}
        ls = len(col_set)
        if (ls <= 3 and 4 in col_set) or (ls == 1 and 8 in col_set):
            sub = [row[1:] for row in sub]
            w -= 1
        else:
            break
    return sub

def trim_right_protrusions(sub: List[List[int]], bg: int) -> List[List[int]]:
    if not sub:
        return []
    h = len(sub)
    if h == 0:
        return sub
    w = len(sub[0])
    if w == 0:
        return sub
    while w > 0:
        col_set = {sub[r][w - 1] for r in range(h) if sub[r][w - 1] != bg}
        ls = len(col_set)
        if ls <= 2 and 5 in col_set:
            sub = [row[:-1] for row in sub]
            w -= 1
        else:
            break
    return sub

def pad_to_5_rows(sub: List[List[int]], bg: int) -> List[List[int]]:
    if not sub:
        return [[bg] * 0 for _ in range(5)]
    h = len(sub)
    w = len(sub[0]) if h > 0 else 0
    if h > 5:
        start = (h - 5) // 2
        sub = sub[start:start + 5]
        h = 5
    if h < 5:
        pad_top = (5 - h) // 2
        pad_bottom = 5 - h - pad_top
        padded = [[bg] * w for _ in range(pad_top)] + sub + [[bg] * w for _ in range(pad_bottom)]
        return padded
    return sub

def program(g: List[List[int]]) -> List[List[int]]:
    if not g or not g[0]:
        return [[] for _ in range(5)]
    bg = g[0][0]
    components = find_large_components(g)
    if not components:
        return [[] for _ in range(5)]
    processed = []
    for comp in components:
        if not comp:
            continue
        minr = min(r for r, c in comp)
        sub = get_bounding_subgrid(g, comp, bg)
        sub = trim_outer_bg(sub, bg)
        if not sub or len(sub[0]) == 0:
            continue
        sub = trim_left_protrusions(sub, bg)
        if not sub or len(sub[0]) == 0:
            continue
        sub = trim_right_protrusions(sub, bg)
        if not sub or len(sub[0]) == 0:
            continue
        padded = pad_to_5_rows(sub, bg)
        processed.append((minr, padded))
    if not processed:
        return [[] for _ in range(5)]
    # Order by descending minr (larger minr first)
    processed.sort(key=lambda x: -x[0])
    # Concatenate horizontally
    out = [[] for _ in range(5)]
    for _, pad in processed:
        for i in range(5):
            out[i].extend(pad[i])
    return out
```