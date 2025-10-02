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
    h = len(sub)
    if h == 0:
        return sub
    pending = False
    while True:
        w = len(sub[0]) if sub and sub[0] else 0
        if w == 0:
            return sub
        col = [row[0] for row in sub]
        non_bg = [c for c in col if c != bg]
        if not non_bg:
            sub = [row[1:] for row in sub]
            continue
        u = set(non_bg)
        ls = len(u)
        trim_it = False
        if ls <= 3 and 4 in u:
            trim_it = True
            pending = True
        elif pending and ls == 1 and 1 in u:
            trim_it = True
        elif ls == 1 and 8 in u:
            trim_it = True
            pending = False
        if not trim_it:
            pending = False
            break
        sub = [row[1:] for row in sub]
    return sub

def trim_right_protrusions(sub: List[List[int]], bg: int) -> List[List[int]]:
    h = len(sub)
    if h == 0:
        return sub
    pending = False
    while True:
        w = len(sub[0]) if sub and sub[0] else 0
        if w == 0:
            return sub
        col = [row[w-1] for row in sub]
        non_bg = [c for c in col if c != bg]
        if not non_bg:
            sub = [row[:-1] for row in sub]
            continue
        u = set(non_bg)
        ls = len(u)
        trim_it = False
        if ls <= 2 and 5 in u:
            trim_it = True
            pending = True
        elif pending and ls == 1 and 3 in u:
            trim_it = True
        elif ls == 1 and 8 in u:
            trim_it = True
            pending = False
        if not trim_it:
            pending = False
            break
        sub = [row[:-1] for row in sub]
    return sub

def special_complete_frame(sub: List[List[int]], bg: int) -> List[List[int]]:
    h = len(sub)
    if h != 5:
        return sub
    w = len(sub[0]) if sub else 0
    if w < 2:
        return sub
    left_col_val = sub[0][0]
    if left_col_val == bg:
        return sub
    if not all(sub[r][0] == left_col_val for r in range(h)):
        return sub
    right_top = sub[0][w-1]
    right_bot = sub[4][w-1]
    if right_top != right_bot or right_top == bg or right_top == left_col_val:
        return sub
    k = -1
    for r in range(1, 4):
        if sub[r][w-1] == 4:
            k = r
            break
    if k == -1:
        return sub
    added = 3
    for r in range(5):
        for _ in range(added):
            sub[r].append(bg)
    for m in range(added):
        sub[k][w + m] = 1
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
    processed = []
    for comp in components:
        sub = get_bounding_subgrid(g, comp, bg)
        sub = trim_outer_bg(sub, bg)
        sub = trim_left_protrusions(sub, bg)
        sub = trim_right_protrusions(sub, bg)
        sub = special_complete_frame(sub, bg)
        if sub and sub[0]:
            sub = pad_to_5_rows(sub, bg)
            if sub[0]:  # non empty
                min_r = min(r for r, c in comp)
                processed.append((min_r, sub))
    if not processed:
        return [[] for _ in range(5)]
    processed.sort(key=lambda x: x[0], reverse=True)
    out = [[] for _ in range(5)]
    for _, sub in processed:
        for r in range(5):
            out[r].extend(sub[r])
    return out
```