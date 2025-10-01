```python
from typing import List, Tuple

def get_bg(g: List[List[int]]) -> int:
    return g[0][0]

def get_non_bg_components(g: List[List[int]], bg: int) -> List[Tuple[int, int, int, int]]:
    rows = len(g)
    cols = len(g[0]) if rows > 0 else 0
    visited = [[False] * cols for _ in range(rows)]
    components = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for i in range(rows):
        for j in range(cols):
            if not visited[i][j] and g[i][j] != bg:
                min_r = max_r = i
                min_c = max_c = j
                stack = [(i, j)]
                visited[i][j] = True
                size = 1
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
                    components.append((min_r, max_r, min_c, max_c))
    return components

def extract_subgrid(g: List[List[int]], min_r: int, max_r: int, min_c: int, max_c: int, bg: int) -> List[List[int]]:
    h = max_r - min_r + 1
    w = max_c - min_c + 1
    sub = []
    for r in range(min_r, max_r + 1):
        row = [g[r][c] if 0 <= c < len(g[0]) else bg for c in range(min_c, max_c + 1)]
        sub.append(row)
    return sub

def pad_vertical(sub: List[List[int]], h: int, w: int, bg: int) -> List[List[int]]:
    pad_top = (5 - h) // 2
    pad_bottom = 5 - h - pad_top
    padded = [[bg for _ in range(w)] for _ in range(pad_top)] + sub + [[bg for _ in range(w)] for _ in range(pad_bottom)]
    return padded

def trim_subgrid(sub: List[List[int]], bg: int) -> List[List[int]]:
    h = len(sub)
    if h == 0:
        return []
    w = len(sub[0])
    left = 0
    while left < w and all(sub[r][left] == bg for r in range(h)):
        left += 1
    right = w - 1
    while right > left and all(sub[r][right] == bg for r in range(h)):
        right -= 1
    if left > right:
        return []
    return [row[left:right + 1] for row in sub]

def program(g: List[List[int]]) -> List[List[int]]:
    bg = get_bg(g)
    components = get_non_bg_components(g, bg)
    processed = []
    for comp in components:
        min_r, max_r, min_c, max_c = comp
        h = max_r - min_r + 1
        sub = extract_subgrid(g, min_r, max_r, min_c, max_c, bg)
        contains9 = any(9 in row for row in sub)
        special = False
        four_r = -1
        if h == 5 and contains9:
            w = len(sub[0])
            L = sub[0][0]
            if L != bg and all(sub[r][0] == L for r in range(5)) and all(sub[r][w - 1] == bg for r in range(1, 4)) and sub[0][w - 1] == 9 and sub[4][w - 1] == 9:
                special = True
                for r in range(5):
                    for c in range(w):
                        if sub[r][c] == 4:
                            four_r = r
                            break
                    if four_r != -1:
                        break
        if contains9 and not special:
            continue
        if special:
            original_w = len(sub[0])
            new_w = original_w + 3
            new_sub = [[bg for _ in range(new_w)] for _ in range(5)]
            for r in range(5):
                for c in range(original_w):
                    new_sub[r][c] = sub[r][c]
            for r in range(1, 4):
                for c in range(original_w):
                    if new_sub[r][c] == bg:
                        new_sub[r][c] = 1
                new_sub[r][original_w] = 1
            if four_r != -1:
                new_sub[four_r][original_w + 1] = 1
                new_sub[four_r][original_w + 2] = 1
            sub = new_sub
        else:
            sub = trim_subgrid(sub, bg)
            h = len(sub)
            if h == 0:
                continue
            w = len(sub[0])
            sub = pad_vertical(sub, h, w, bg)
        processed.append((sub, min_c, min_r))
    if not processed:
        return [[bg]]
    processed.sort(key=lambda x: (-x[1], x[2]))
    w_total = sum(len(p[0][0]) for p in processed)
    out = [[bg for _ in range(w_total)] for _ in range(5)]
    current = 0
    for sub, _, _ in processed:
        w = len(sub[0])
        for r in range(5):
            for c in range(w):
                out[r][current + c] = sub[r][c]
        current += w
    return out
```