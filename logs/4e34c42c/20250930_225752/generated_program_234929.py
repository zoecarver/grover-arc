```python
from typing import List, Tuple

def get_bg(g: List[List[int]]) -> int:
    return g[0][0]

def get_connected_components(g: List[List[int]], bg: int) -> List[Tuple[int, int, int, int]]:
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

def contains_9(sub: List[List[int]]) -> bool:
    return any(9 in row for row in sub)

def process_subgrid(sub: List[List[int]], bg: int) -> List[List[int]]:
    h = len(sub)
    w = len(sub[0]) if h > 0 else 0
    if contains_9(sub):
        for r in range(1, min(4, h)):
            for c in range(w):
                if sub[r][c] == bg:
                    sub[r][c] = 1
    if h < 5:
        pad_top = (5 - h) // 2
        pad_bottom = 5 - h - pad_top
        padded = [[bg for _ in range(w)] for _ in range(pad_top)] + sub + [[bg for _ in range(w)] for _ in range(pad_bottom)]
        sub = padded
        h = 5
    # trim leading and trailing all bg columns
    left = 0
    while left < w and all(sub[r][left] == bg for r in range(h)):
        left += 1
    right = w - 1
    while right > left and all(sub[r][right] == bg for r in range(h)):
        right -= 1
    if left > right:
        return []
    for r in range(h):
        sub[r] = sub[r][left:right + 1]
    return sub

def sort_key(comp: Tuple[int, int, int, int]) -> Tuple[int, int]:
    min_r, max_r, min_c, max_c = comp
    return (min_c, min_r)

def program(g: List[List[int]]) -> List[List[int]]:
    bg = get_bg(g)
    components = get_connected_components(g, bg)
    processed = []
    for comp in components:
        min_r, max_r, min_c, max_c = comp
        sub = extract_subgrid(g, min_r, max_r, min_c, max_c, bg)
        processed_sub = process_subgrid(sub, bg)
        if processed_sub:
            processed.append((comp, processed_sub))
    processed.sort(key=lambda x: sort_key(x[0]))
    if not processed:
        return [[bg]]
    total_w = sum(len(p[1][0]) for p in processed)
    output = [[bg for _ in range(total_w)] for _ in range(5)]
    current_col = 0
    for _, sub in processed:
        w = len(sub[0])
        for r in range(5):
            for c in range(w):
                output[r][current_col + c] = sub[r][c]
        current_col += w
    return output
```