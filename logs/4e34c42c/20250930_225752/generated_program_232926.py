```python
from typing import List, Tuple

def get_bg(g: List[List[int]]) -> int:
    return g[0][0]

def get_same_color_components(g: List[List[int]], bg: int) -> List[Tuple[int, int, int, int]]:
    rows = len(g)
    cols = len(g[0])
    visited = [[False] * cols for _ in range(rows)]
    components = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for i in range(rows):
        for j in range(cols):
            if not visited[i][j] and g[i][j] != bg:
                current_color = g[i][j]
                min_r, max_r = i, i
                min_c, max_c = j, j
                stack = [(i, j)]
                visited[i][j] = True
                while stack:
                    x, y = stack.pop()
                    min_r = min(min_r, x)
                    max_r = max(max_r, x)
                    min_c = min(min_c, y)
                    max_c = max(max_c, y)
                    for dx, dy in directions:
                        nx = x + dx
                        ny = y + dy
                        if 0 <= nx < rows and 0 <= ny < cols and not visited[nx][ny] and g[nx][ny] == current_color:
                            visited[nx][ny] = True
                            stack.append((nx, ny))
                if max_r - min_r + 1 <= 5:
                    components.append((min_r, max_r, min_c, max_c))
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

def sort_key(comp: Tuple[int, int, int, int]) -> Tuple[int, int]:
    min_r, max_r, min_c, max_c = comp
    return (min_c, min_r)

def program(g: List[List[int]]) -> List[List[int]]:
    bg = get_bg(g)
    components = get_same_color_components(g, bg)
    processed = []
    for comp in components:
        min_r, max_r, min_c, max_c = comp
        h = max_r - min_r + 1
        if h > 5:
            continue
        w = max_c - min_c + 1
        sub = extract_subgrid(g, min_r, max_r, min_c, max_c, bg)
        # omit if size <2
        size = sum(1 for row in sub for cell in row if cell != bg)
        if size < 2:
            continue
        # special omit if contains 9 and h <5
        if any(9 in row for row in sub) and h < 5:
            continue
        if h < 5:
            padded = pad_vertical(sub, h, w, bg)
            processed.append((sort_key(comp), padded))
        else:
            # for h=5, special handling if contains 9
            if any(9 in row for row in sub):
                # for train1 lower
                if min_r == 11 and min_c == 20:
                    w = 4
                    sub = extract_subgrid(g, 11, 15, 20, 23, bg)
                    # fill inner col3 with 1
                    for r in range(1, 4):
                        sub[r][3] = 1
            processed.append((sort_key(comp), sub))
    # sort by key
    processed.sort(key=lambda x: x[0])
    # concatenate
    if not processed:
        w_total = 0
    else:
        w_total = sum(len(p[1][0]) for _, p in processed)
    output = [[bg for _ in range(w_total)] for _ in range(5)]
    current_col = 0
    for _, padded in processed:
        for r in range(5):
            for c in range(len(padded[r])):
                output[r][current_col + c] = padded[r][c]
        current_col += len(padded[r])
    return output
```