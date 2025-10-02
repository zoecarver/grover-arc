```python
from typing import List, Tuple
import copy

def program(g: List[List[int]]) -> List[List[int]]:
    if not g or not g[0]:
        return [[ ] for _ in range(5)]
    bg = g[0][0]
    components = find_large_components(g)
    processed = []
    for comp in components:
        sub = get_bounding_subgrid(g, comp, bg)
        sub = trim_outer_bg(sub, bg)
        sub = trim_left_protrusions(sub, bg)
        sub = trim_right_protrusions(sub, bg)
        sub = fill_sparse_ones(sub, bg)
        sub = pad_to_5_rows(sub, bg)
        if sub and sub[0]:  # skip empty
            min_r = min(r for r, c in comp)
            processed.append((min_r, sub))
    if not processed:
        return [[ ] for _ in range(5)]
    # Sort by min_r descending (larger min_r first, bottom first)
    processed.sort(key=lambda x: -x[0])
    # Concat horizontally
    output = [[] for _ in range(5)]
    for _, sub in processed:
        for i in range(5):
            output[i].extend(sub[i])
    return output

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
    if not sub:
        return sub
    h = len(sub)
    w = len(sub[0])
    while w > 0:
        non_bg_set = set()
        num_non = 0
        for r in range(h):
            if sub[r][0] != bg:
                non_bg_set.add(sub[r][0])
                num_non += 1
        if num_non == h and len(non_bg_set) <= 3 and 4 in non_bg_set:
            sub = [row[1:] for row in sub]
            w -= 1
        else:
            break
    return sub

def trim_right_protrusions(sub: List[List[int]], bg: int) -> List[List[int]]:
    if not sub:
        return sub
    h = len(sub)
    w = len(sub[0])
    while w > 0:
        non_bg_set = set()
        num_non = 0
        for r in range(h):
            if sub[r][w - 1] != bg:
                non_bg_set.add(sub[r][w - 1])
                num_non += 1
        if (num_non == h or num_non <= 1) and len(non_bg_set) <= 2 and 5 in non_bg_set:
            sub = [row[:-1] for row in sub]
            w -= 1
        else:
            break
    return sub

def fill_sparse_ones(sub: List[List[int]], bg: int) -> List[List[int]]:
    if not sub:
        return sub
    h = len(sub)
    w = len(sub[0])
    sub = copy.deepcopy(sub)  # to modify
    changed = True
    while changed:
        changed = False
        for j in range(w):
            non_bg_set = set()
            positions = []
            num_non = 0
            for r in range(h):
                if sub[r][j] != bg:
                    non_bg_set.add(sub[r][j])
                    positions.append(r)
                    num_non += 1
            if num_non == 1 and 1 in non_bg_set:
                r0 = positions[0]
                # Check left adjacent
                if j > 0:
                    for dr in [-1, 0, 1]:
                        nr = r0 + dr
                        if 0 <= nr < h and sub[nr][j - 1] == 1:
                            if sub[nr][j] != 1:
                                sub[nr][j] = 1
                                changed = True
                # Check right adjacent
                if j < w - 1:
                    for dr in [-1, 0, 1]:
                        nr = r0 + dr
                        if 0 <= nr < h and sub[nr][j + 1] == 1:
                            if sub[nr][j] != 1:
                                sub[nr][j] = 1
                                changed = True
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
```