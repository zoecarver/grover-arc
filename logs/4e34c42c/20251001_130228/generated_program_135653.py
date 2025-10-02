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
                if len(comp) >= 5:
                    components.append(comp)
    return components

def get_bounding_subgrid(g: List[List[int]], comp: List[Tuple[int, int]], bg: int) -> List[List[int]]:
    if not comp:
        return []
    minr = min(r for r, c in comp)
    maxr = max(r for r, c in comp)
    minc = min(c for r, c in comp)
    maxc = max(c for r, c in comp)
    h = maxr - minr + 1
    w = maxc - minc + 1
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
    if not sub or not sub[0]:
        return sub
    h = len(sub)
    w = len(sub[0])
    while w > 0:
        col = [row[0] for row in sub]
        non_bg_col = [c for c in col if c != bg]
        unique_non = set(non_bg_col)
        num_non = len(non_bg_col)
        condition = (unique_non.issubset({1, 4}) or unique_non == {8}) and (num_non == h or num_non <= 1)
        if condition:
            sub = [row[1:] for row in sub]
            w -= 1
        else:
            break
    return sub

def trim_right_protrusions(sub: List[List[int]], bg: int) -> List[List[int]]:
    if not sub or not sub[0]:
        return sub
    h = len(sub)
    w = len(sub[0])
    while w > 0:
        col = [row[w - 1] for row in sub]
        non_bg_col = [c for c in col if c != bg]
        unique_non = set(non_bg_col)
        num_non = len(non_bg_col)
        condition = 5 in unique_non and len(unique_non) <= 2 and (num_non == h or num_non <= 1)
        if condition:
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
        bg = 0
        return [[bg] * 0 for _ in range(5)]
    bg = g[0][0]
    components = find_large_components(g)
    processed = []
    for comp in components:
        sub = get_bounding_subgrid(g, comp, bg)
        if not sub or not sub[0]:
            continue
        sub = trim_outer_bg(sub, bg)
        sub = trim_left_protrusions(sub, bg)
        sub = trim_right_protrusions(sub, bg)
        # duplication rule
        if sub and len(sub[0]) >= 2:
            right_col = [row[-1] for row in sub]
            non_bg_right = set(c for c in right_col if c != bg)
            if 4 in non_bg_right or 9 in non_bg_right:
                penultimate_col = [row[-2] for row in sub]
                for _ in range(2):
                    for j in range(len(sub)):
                        sub[j].append(penultimate_col[j])
        sub = pad_to_5_rows(sub, bg)
        if not sub or not sub[0]:
            continue
        minr = min(r for r, c in comp)
        minc = min(c for r, c in comp)
        processed.append((minr, minc, sub))
    if not processed:
        return [[bg] * 0 for _ in range(5)]
    processed.sort(key=lambda x: (x[0], x[1]))
    out = [[] for _ in range(5)]
    for _, _, sub in processed:
        for i in range(5):
            out[i].extend(sub[i])
    return out
```