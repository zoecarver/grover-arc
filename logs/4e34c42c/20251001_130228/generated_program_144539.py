```python
from typing import List, Tuple

def find_large_components(g: List[List[int]]) -> List[List[Tuple[int, int]]]:
    if not g or not g[0]:
        return []
    bg = g[0][0]
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
    if not sub:
        return []
    h = len(sub)
    if h == 0:
        return []
    pending = False
    while len(sub[0]) > 0:
        col = [sub[r][0] for r in range(h)]
        non_bg = [v for v in col if v != bg]
        if not non_bg:
            sub = [row[1:] for row in sub]
            continue
        s = set(non_bg)
        ls = len(s)
        num_non = len(non_bg)
        trim_it = False
        if num_non == h and 4 in s and ls <= 3:
            trim_it = True
            pending = True
        elif pending and num_non == h and s == {1}:
            trim_it = True
            pending = True
        elif pending and num_non <= 1 and s == {1}:
            trim_it = True
            pending = False
        if not trim_it:
            break
        sub = [row[1:] for row in sub]
    return sub

def trim_right_protrusions(sub: List[List[int]], bg: int) -> List[List[int]]:
    if not sub:
        return []
    h = len(sub)
    if h == 0:
        return []
    pending = False
    while len(sub[0]) > 0:
        col = [sub[r][-1] for r in range(h)]
        non_bg = [v for v in col if v != bg]
        if not non_bg:
            sub = [row[:-1] for row in sub]
            continue
        s = set(non_bg)
        ls = len(s)
        num_non = len(non_bg)
        trim_it = False
        if num_non == h and 5 in s and ls <= 3:
            trim_it = True
            pending = True
        elif pending and num_non == h and s == {1}:
            trim_it = True
            pending = True
        elif pending and num_non <= 1 and s == {1}:
            trim_it = True
            pending = False
        if not trim_it:
            break
        sub = [row[:-1] for row in sub]
    return sub

def special_complete_shape(sub: List[List[int]], bg: int) -> List[List[int]]:
    h = len(sub)
    if h != 5:
        return sub
    w = len(sub[0]) if h > 0 else 0
    if w < 2:
        return sub
    left_col = [sub[r][0] for r in range(h)]
    right_col = [sub[r][w - 1] for r in range(h)]
    left_set = set(left_col)
    if len(left_set) != 1 or list(left_set)[0] == bg:
        return sub
    C = list(left_set)[0]
    if right_col[0] != right_col[4] or right_col[0] == C or right_col[0] == bg:
        return sub
    D = right_col[0]
    four_positions = [r for r in range(1, 4) if right_col[r] == 4]
    if len(four_positions) != 1:
        return sub
    four_row = four_positions[0]
    col1 = [sub[r][1] for r in range(h)]
    new_col3 = col1[:]
    new_col4 = [bg] * h
    new_col4[four_row] = 1
    for r in range(h):
        sub[r].append(new_col3[r])
        sub[r].append(new_col4[r])
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
        sub = special_complete_shape(sub, bg)
        h = len(sub)
        w = len(sub[0]) if h > 0 else 0
        if w == 0:
            continue
        padded = pad_to_5_rows(sub, bg)
        minr = min(r for r, c in comp)
        processed.append((minr, padded))
    if not processed:
        return [[] for _ in range(5)]
    processed.sort(key=lambda x: -x[0])
    output = [[] for _ in range(5)]
    for _, padded in processed:
        for i in range(5):
            output[i].extend(padded[i])
    return output
```