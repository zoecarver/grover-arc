```python
from typing import List, Tuple

def get_background(g: List[List[int]]) -> int:
    return g[0][0] if g and g[0] else 0

def find_large_components(g: List[List[int]], bg: int) -> List[List[Tuple[int, int]]]:
    if not g or not g[0]:
        return []
    rows = len(g)
    cols = len(g[0])
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
                        nx = x + dx
                        ny = y + dy
                        if 0 <= nx < rows and 0 <= ny < cols and g[nx][ny] != bg and not visited[nx][ny]:
                            visited[nx][ny] = True
                            stack.append((nx, ny))
                if len(comp) >= 10:
                    components.append(comp)
    return components

def get_bounds(comp: List[Tuple[int, int]]) -> Tuple[int, int, int, int]:
    if not comp:
        return 0, 0, 0, 0
    min_r = min(r for r, c in comp)
    max_r = max(r for r, c in comp)
    min_c = min(c for r, c in comp)
    max_c = max(c for r, c in comp)
    return min_r, max_r, min_c, max_c

def extract_subgrid(g: List[List[int]], min_r: int, max_r: int, min_c: int, max_c: int) -> List[List[int]]:
    h = max_r - min_r + 1
    w = max_c - min_c + 1
    return [[g[min_r + i][min_c + j] for j in range(w)] for i in range(h)]

def trim_outer_columns(sub: List[List[int]], bg: int) -> List[List[int]]:
    if not sub:
        return []
    h = len(sub)
    if h == 0:
        return []
    w = len(sub[0])
    if w == 0:
        return sub
    left = 0
    while left < w and all(sub[r][left] == bg for r in range(h)):
        left += 1
    right = w
    while right > left and all(sub[r][right - 1] == bg for r in range(h)):
        right -= 1
    if left >= right:
        return [[] for _ in range(h)]
    return [row[left:right] for row in sub]

def trim_left_protrusions(sub: List[List[int]], bg: int) -> List[List[int]]:
    if not sub:
        return sub
    h = len(sub)
    while True:
        w = len(sub[0]) if sub and sub[0] else 0
        if w <= 0:
            break
        col = [sub[r][0] for r in range(h)]
        non_bg = [c for c in col if c != bg]
        if not non_bg:
            sub = [row[1:] for row in sub]
            continue
        s = set(non_bg)
        if len(s) <= 3 and 4 in s:
            sub = [row[1:] for row in sub]
            continue
        break
    return sub

def trim_right_protrusions(sub: List[List[int]], bg: int) -> List[List[int]]:
    if not sub:
        return sub
    h = len(sub)
    while True:
        w = len(sub[0]) if sub and sub[0] else 0
        if w <= 0:
            break
        col = [sub[r][w - 1] for r in range(h)]
        non_bg = [c for c in col if c != bg]
        if not non_bg:
            sub = [row[:-1] for row in sub]
            continue
        s = set(non_bg)
        if len(s) <= 3 and 5 in s:
            sub = [row[:-1] for row in sub]
            continue
        break
    return sub

def apply_special_completion(sub: List[List[int]], bg: int) -> List[List[int]]:
    h = len(sub)
    if h != 5:
        return sub
    w = len(sub[0]) if sub and sub[0] else 0
    if w < 2:
        return sub
    left_col = [sub[i][0] for i in range(h)]
    right_col = [sub[i][w - 1] for i in range(h)]
    l_non_bg = [c for c in left_col if c != bg]
    l_set = set(l_non_bg)
    if len(l_set) != 1:
        return sub
    L = next(iter(l_set))
    if right_col[0] != right_col[4] or right_col[0] == bg or right_col[0] == L:
        return sub
    fours = [i for i in range(1, 4) if right_col[i] == 4]
    if len(fours) != 1:
        return sub
    k = fours[0]
    orig_w = w
    penult_col = [sub[i][w - 2] for i in range(h)]
    for i in range(h):
        sub[i].append(penult_col[i])
    for _ in range(2):
        for i in range(h):
            sub[i].append(bg)
    for j in range(orig_w + 1, orig_w + 3):
        sub[k][j] = 1
    return sub

def trim_outer_rows(sub: List[List[int]], bg: int) -> List[List[int]]:
    if not sub:
        return []
    h = len(sub)
    if h == 0:
        return []
    w = len(sub[0])
    if w == 0:
        return sub
    top = 0
    while top < h and all(sub[top][j] == bg for j in range(w)):
        top += 1
    bottom = h
    while bottom > top and all(sub[bottom - 1][j] == bg for j in range(w)):
        bottom -= 1
    if top >= bottom:
        return []
    return sub[top:bottom]

def pad_to_5_rows(sub: List[List[int]], bg: int) -> List[List[int]]:
    if not sub:
        return [[] for _ in range(5)]
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
    bg = get_background(g)
    comps = find_large_components(g, bg)
    if not comps:
        return [[] for _ in range(5)]
    items = []
    for comp in comps:
        min_r, max_r, min_c, max_c = get_bounds(comp)
        sub = extract_subgrid(g, min_r, max_r, min_c, max_c)
        sub = trim_outer_columns(sub, bg)
        sub = trim_left_protrusions(sub, bg)
        sub = trim_right_protrusions(sub, bg)
        sub = trim_outer_columns(sub, bg)
        orig_h = len(sub)
        if orig_h == 5:
            sub = apply_special_completion(sub, bg)
        sub = trim_outer_rows(sub, bg)
        padded = pad_to_5_rows(sub, bg)
        if all(len(row) == 0 for row in padded):
            continue
        items.append((max_r, padded))
    if not items:
        return [[] for _ in range(5)]
    items.sort(key=lambda x: -x[0])
    output = [[] for _ in range(5)]
    for _, padded in items:
        for i in range(5):
            output[i].extend(padded[i])
    return output
```