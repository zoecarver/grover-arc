```python
from typing import List, Tuple

def get_bg(g: List[List[int]]) -> int:
    return g[0][0]

def get_non_bg_components(g: List[List[int]], bg: int) -> List[Tuple[int, int, int, int, int]]:
    rows = len(g)
    cols = len(g[0])
    visited = [[False] * cols for _ in range(rows)]
    components = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for i in range(rows):
        for j in range(cols):
            if not visited[i][j] and g[i][j] != bg:
                min_r, max_r = i, i
                min_c, max_c = j, j
                size = 0
                stack = [(i, j)]
                visited[i][j] = True
                size += 1
                while stack:
                    x, y = stack.pop()
                    min_r = min(min_r, x)
                    max_r = max(max_r, x)
                    min_c = min(min_c, y)
                    max_c = max(max_c, y)
                    for dx, dy in directions:
                        nx = x + dx
                        ny = y + dy
                        if 0 <= nx < rows and 0 <= ny < cols and not visited[nx][ny] and g[nx][ny] != bg:
                            visited[nx][ny] = True
                            stack.append((nx, ny))
                            size += 1
                h = max_r - min_r + 1
                if h <= 5 and size >= 2:
                    components.append((min_r, max_r, min_c, max_c, size))
    return components

def extract_subgrid(g: List[List[int]], min_r: int, max_r: int, min_c: int, max_c: int, bg: int) -> List[List[int]]:
    h = max_r - min_r + 1
    w = max_c - min_c + 1
    sub = []
    for r in range(min_r, max_r + 1):
        row = []
        for c in range(min_c, max_c + 1):
            if 0 <= c < len(g[0]):
                row.append(g[r][c])
            else:
                row.append(bg)
        sub.append(row)
    return sub

def pad_vertical(sub: List[List[int]], h: int, w: int, bg: int) -> List[List[int]]:
    pad_top = (5 - h) // 2
    pad_bottom = 5 - h - pad_top
    padded = [[bg for _ in range(w)] for _ in range(pad_top)] + sub + [[bg for _ in range(w)] for _ in range(pad_bottom)]
    return padded

def get_min_r_non9(g: List[List[int]], min_r: int, max_r: int, min_c: int, max_c: int, bg: int) -> int:
    min_r_non9 = None
    for r in range(min_r, max_r + 1):
        for c in range(min_c, max_c + 1):
            if g[r][c] != bg and g[r][c] != 9:
                if min_r_non9 is None or r < min_r_non9:
                    min_r_non9 = r
    return min_r_non9 if min_r_non9 is not None else min_r

def contains_9(sub: List[List[int]]) -> bool:
    return any(9 in row for row in sub)

def process_component(g: List[List[int]], comp: Tuple[int, int, int, int, int], bg: int) -> List[List[int]]:
    min_r, max_r, min_c, max_c, size = comp
    h = max_r - min_r + 1
    sub = extract_subgrid(g, min_r, max_r, min_c, max_c, bg)
    contains_9_flag = contains_9(sub)
    if h < 5:
        if contains_9_flag:
            return None
        padded = pad_vertical(sub, h, len(sub[0]), bg)
    else:
        if contains_9_flag:
            sub0 = sub[0]
            sub4 = sub[4]
            w = len(sub0)
            if sub0[w - 1] == 9 and sub4[w - 1] == 9:
                # right frame
                new_max_c = max_c + 1
                sub = extract_subgrid(g, min_r, max_r, min_c, new_max_c, bg)
                for r in range(1, 4):
                    sub[r][-1] = 1
                padded = sub
            elif sub0[0] == 9 and sub4[0] == 9:
                # left frame
                inner = sub[1:4]
                center_row = inner[1][:]
                w_inner = len(center_row)
                for k in range(w_inner):
                    center_row[k] = 1
                center_row = center_row[0:2]  # width 2
                w = len(center_row)
                padded = [[bg for _ in range(w)] for _ in range(5)]
                padded[2] = center_row[:]
            else:
                padded = sub
        else:
            padded = sub
    # trim left and right all bg columns
    w = len(padded[0])
    left = 0
    while left < w and all(padded[r][left] == bg for r in range(5)):
        left += 1
    right = w - 1
    while right > left and all(padded[r][right] == bg for r in range(5)):
        right -= 1
    if left > right:
        return None
    for r in range(5):
        padded[r] = padded[r][left : right + 1]
    return padded

def program(g: List[List[int]]) -> List[List[int]]:
    bg = get_bg(g)
    components = get_non_bg_components(g, bg)
    comp_with_key = []
    for comp in components:
        min_r, max_r, min_c, max_c, size = comp
        min_r_non9 = get_min_r_non9(g, min_r, max_r, min_c, max_c, bg)
        key = (-min_r_non9, min_c)
        comp_with_key.append((comp, key))
    comp_with_key.sort(key=lambda x: x[1])
    processed = []
    for comp, key in comp_with_key:
        p = process_component(g, comp, bg)
        if p is not None:
            processed.append(p)
    if not processed:
        return [[bg]]
    total_w = sum(len(p[0]) for p in processed)
    output = [[bg for _ in range(total_w)] for _ in range(5)]
    current_col = 0
    for p in processed:
        pw = len(p[0])
        for r in range(5):
            for c in range(pw):
                output[r][current_col + c] = p[r][c]
        current_col += pw
    return output
```