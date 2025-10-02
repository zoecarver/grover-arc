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
    if not sub or not sub[0]:
        return sub
    h = len(sub)
    w = len(sub[0])
    while w > 0 and all(sub[r][0] == bg for r in range(h)):
        sub = [row[1:] for row in sub]
        w -= 1
    while w > 0 and all(sub[r][w - 1] == bg for r in range(h)):
        sub = [row[:-1] for row in sub]
        w -= 1
    return sub

def trim_left_protrusions(sub: List[List[int]], bg: int) -> List[List[int]]:
    if not sub or not sub[0]:
        return sub
    h = len(sub)
    w = len(sub[0])
    pending = False
    while w > 0:
        col = [sub[r][0] for r in range(h)]
        nonbg = [c for c in col if c != bg]
        s = set(nonbg)
        if pending:
            if s.issubset({1, 8}):
                sub = [row[1:] for row in sub]
                w -= 1
                continue
            else:
                break
        else:
            if len(s) <= 3 and (4 in s or 5 in s):
                sub = [row[1:] for row in sub]
                w -= 1
                pending = True
                continue
            elif len(s) == 1 and 8 in s and len(nonbg) == h:
                sub = [row[1:] for row in sub]
                w -= 1
                pending = False
                continue
            else:
                break
    return sub

def trim_right_protrusions(sub: List[List[int]], bg: int) -> List[List[int]]:
    if not sub or not sub[0]:
        return sub
    h = len(sub)
    w = len(sub[0])
    pending = False
    while w > 0:
        col = [sub[r][w - 1] for r in range(h)]
        nonbg = [c for c in col if c != bg]
        s = set(nonbg)
        if pending:
            if s.issubset({1, 8}):
                sub = [row[:-1] for row in sub]
                w -= 1
                continue
            else:
                break
        else:
            if len(s) <= 3 and 5 in s:
                sub = [row[:-1] for row in sub]
                w -= 1
                pending = True
                continue
            elif len(s) == 1 and 8 in s and len(nonbg) == h:
                sub = [row[:-1] for row in sub]
                w -= 1
                pending = False
                continue
            else:
                break
    return sub

def special_complete_frame(sub: List[List[int]], bg: int) -> List[List[int]]:
    if not sub or len(sub) != 5 or not sub[0]:
        return sub
    h = 5
    w = len(sub[0])
    if w < 2:
        return sub
    left_col = [sub[i][0] for i in range(h)]
    right_col = [sub[i][w - 1] for i in range(h)]
    left_set = set(c for c in left_col if c != bg)
    if len(left_set) != 1:
        return sub
    left_color = next(iter(left_set))
    if right_col[0] == bg or right_col[4] == bg or right_col[0] != right_col[4] or right_col[0] == left_color:
        return sub
    four_row = -1
    num_four = 0
    for i in range(1, 4):
        if right_col[i] == 4:
            num_four += 1
            four_row = i
    if num_four != 1:
        return sub
    new_sub = [row[:] + [bg] * 3 for row in sub]
    for j in range(w, w + 3):
        new_sub[four_row][j] = 1
    return new_sub

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
        sub = [[bg] * w for _ in range(pad_top)] + sub + [[bg] * w for _ in range(pad_bottom)]
    return sub

def program(g: List[List[int]]) -> List[List[int]]:
    if not g or not g[0]:
        return [[] for _ in range(5)]
    bg = g[0][0]
    components = find_large_components(g)
    processed = []
    for comp in components:
        min_r = min(r for r, c in comp)
        sub = get_bounding_subgrid(g, comp, bg)
        sub = trim_outer_bg(sub, bg)
        sub = trim_left_protrusions(sub, bg)
        sub = trim_right_protrusions(sub, bg)
        sub = special_complete_frame(sub, bg)
        if sub and sub[0]:
            sub = pad_to_5_rows(sub, bg)
            if sub[0]:
                processed.append((min_r, sub))
    processed.sort(key=lambda x: -x[0])
    out = [[] for _ in range(5)]
    for _, sub in processed:
        for i in range(5):
            out[i].extend(sub[i])
    return out
```