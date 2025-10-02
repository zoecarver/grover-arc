```python
from typing import List, Tuple

def program(g: List[List[int]]) -> List[List[int]]:
    if not g or not g[0]:
        return [[] for _ in range(5)]
    bg = g[0][0]
    components = find_large_components(g)
    processed = []
    for comp in components:
        if len(comp) <= 10:
            continue
        minr = min(r for r, _ in comp)
        sub = get_bounding_subgrid(g, comp, bg)
        sub = trim_outer_bg(sub, bg)
        sub = trim_left_protrusions(sub, bg)
        sub = trim_right_protrusions(sub, bg)
        sub = apply_special_completion(sub, bg)
        sub = pad_to_5_rows(sub, bg)
        if sub and sub[0]:  # skip if empty after processing
            processed.append((minr, sub))
    if not processed:
        return [[] for _ in range(5)]
    processed.sort(key=lambda x: -x[0])  # descending minr, bottom first
    out = [[] for _ in range(5)]
    for _, sub in processed:
        for i in range(5):
            out[i].extend(sub[i])
    return out

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
                        if 0 <= nx < rows and 0 <= ny < cols and g[nx][ny] != bg and not visited[nx][ny]:
                            visited[nx][ny] = True
                            stack.append((nx, ny))
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
    while True:
        w = len(sub[0])
        if w <= 1:
            break
        col = [sub[r][0] for r in range(h)]
        non_bg = [c for c in col if c != bg]
        if not non_bg:
            sub = [row[1:] for row in sub]
            continue
        s = set(non_bg)
        ls = len(s)
        if (ls <= 3 and 4 in s) or (ls == 1 and 8 in s):
            sub = [row[1:] for row in sub]
            continue
        break
    return sub

def trim_right_protrusions(sub: List[List[int]], bg: int) -> List[List[int]]:
    if not sub or not sub[0]:
        return sub
    h = len(sub)
    while True:
        w = len(sub[0])
        if w <= 1:
            break
        col = [sub[r][w - 1] for r in range(h)]
        non_bg = [c for c in col if c != bg]
        if not non_bg:
            sub = [row[:-1] for row in sub]
            continue
        s = set(non_bg)
        ls = len(s)
        if (ls <= 2 and 5 in s) or (ls == 1 and 8 in s):
            sub = [row[:-1] for row in sub]
            continue
        break
    return sub

def apply_special_completion(sub: List[List[int]], bg: int) -> List[List[int]]:
    h = len(sub)
    if h != 5:
        return sub
    w = len(sub[0]) if sub and sub[0] else 0
    if w < 3:
        return sub
    left_col = [sub[i][0] for i in range(h)]
    right_col = [sub[i][w - 1] for i in range(h)]
    l_non_bg = [c for c in left_col if c != bg]
    l_set = set(l_non_bg)
    if len(l_set) != 1 or bg in l_non_bg:
        return sub
    L = next(iter(l_set))
    if right_col[0] != right_col[4] or right_col[0] == bg or right_col[0] == L:
        return sub
    fours = [i for i in range(1, 4) if right_col[i] == 4]
    if len(fours) != 1:
        return sub
    k = fours[0]
    # duplicate penultimate column
    penult_col = [sub[i][w - 2] for i in range(h)]
    for i in range(h):
        sub[i].append(penult_col[i])
    # append two bg columns
    for _ in range(2):
        for i in range(h):
            sub[i].append(bg)
    # set 1 at row k in the two new columns (after duplication, positions w and w+1 where w is now original w+1)
    orig_w = w
    for j in range(orig_w + 1, orig_w + 3):
        sub[k][j] = 1
    return sub

def pad_to_5_rows(sub: List[List[int]], bg: int) -> List[List[int]]:
    if not sub:
        return [[] for _ in range(5)]
    h = len(sub)
    w = len(sub[0]) if h > 0 else 0
    if h > 5:
        start = (h - 5) // 2
        sub = sub[start : start + 5]
        h = 5
    if h < 5:
        pad_top = (5 - h) // 2
        pad_bottom = 5 - h - pad_top
        padded = [[bg] * w for _ in range(pad_top)] + sub + [[bg] * w for _ in range(pad_bottom)]
        return padded
    return sub
```