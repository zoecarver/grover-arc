```python
from typing import List, Tuple

def get_bg(g: List[List[int]]) -> int:
    return g[0][0] if g else 0

def get_same_color_components(g: List[List[int]], bg: int) -> List[Tuple[int, int, int, int]]:
    rows = len(g)
    if rows == 0:
        return []
    cols = len(g[0])
    visited = [[False] * cols for _ in range(rows)]
    components = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for i in range(rows):
        for j in range(cols):
            if not visited[i][j] and g[i][j] != bg:
                current_color = g[i][j]
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
                        if 0 <= nx < rows and 0 <= ny < cols and not visited[nx][ny] and g[nx][ny] == current_color:
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

def contains_9(sub: List[List[int]]) -> bool:
    return any(9 in row for row in sub)

def contains_four(sub: List[List[int]]) -> bool:
    return any(4 in row for row in sub)

def pad_vertical(sub: List[List[int]], orig_h: int, w: int, bg: int) -> List[List[int]]:
    pad_top = (5 - orig_h) // 2
    pad_bottom = 5 - orig_h - pad_top
    padded = [[bg for _ in range(w)] for _ in range(pad_top)] + sub + [[bg for _ in range(w)] for _ in range(pad_bottom)]
    return padded

def trim_full_bg_columns(sub: List[List[int]], bg: int) -> List[List[int]]:
    if not sub or not sub[0]:
        return []
    h = len(sub)
    w = len(sub[0])
    left = 0
    while left < w and all(sub[r][left] == bg for r in range(h)):
        left += 1
    right = w - 1
    while right > left and all(sub[r][right] == bg for r in range(h)):
        right -= 1
    if left > right:
        return []
    return [row[left : right + 1] for row in sub]

def trim_gap_columns(sub: List[List[int]], bg: int) -> List[List[int]]:
    h = len(sub)
    if h != 5:
        return sub
    w = len(sub[0]) if sub else 0
    while w > 0 and sub[2][0] == bg:
        sub = [row[1:] for row in sub]
        w -= 1
    while w > 0 and sub[2][-1] == bg:
        sub = [row[:-1] for row in sub]
        w -= 1
    return sub

def process_normal(g: List[List[int]], comp: Tuple[int, int, int, int], bg: int, global_max_r: int) -> List[List[int]]:
    min_r, max_r, min_c, max_c, size = comp
    if min_r > global_max_r - 3:
        return []
    h = max_r - min_r + 1
    sub = extract_subgrid(g, min_r, max_r, min_c, max_c, bg)
    # Set 4 to bg and adjacent cells to bg
    four_positions = []
    for r in range(h):
        for c in range(len(sub[r])):
            if g[min_r + r][min_c + c] == 4:
                sub[r][c] = bg
                four_positions.append((r, c))
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for fr, fc in four_positions:
        for dx, dy in directions:
            nr = fr + dx
            nc = fc + dy
            if 0 <= nr < h and 0 <= nc < len(sub[0]):
                sub[nr][nc] = bg
    # Skip if contains 9 and h < 5
    if contains_9(sub) and h < 5:
        return []
    if h < 5:
        sub = pad_vertical(sub, h, len(sub[0]), bg)
    sub = trim_full_bg_columns(sub, bg)
    sub = trim_gap_columns(sub, bg)
    if not sub or not sub[0]:
        return []
    return sub

def process_special(g: List[List[int]], comp: Tuple[int, int, int, int], bg: int) -> List[List[int]]:
    min_r, max_r, min_c, max_c = comp
    h = max_r - min_r + 1
    if h != 5:
        return []
    temp_sub = extract_subgrid(g, min_r, max_r, min_c, max_c, bg)
    if not contains_9(temp_sub):
        return []
    w_temp = len(temp_sub[0])
    if not all(temp_sub[r][0] != bg and temp_sub[r][0] == temp_sub[0][0] for r in range(5)):
        return []
    if not (temp_sub[0][-1] == 9 and temp_sub[4][-1] == 9):
        return []
    # Special right frame
    new_max_c = min_c + 3
    sub = extract_subgrid(g, min_r, max_r, min_c, new_max_c, bg)
    fill_color = g[min_r + 1][min_c + 1]
    for r in range(1, 4):
        for c in range(1, 4):
            if sub[r][c] == bg:
                sub[r][c] = fill_color
    sub = trim_full_bg_columns(sub, bg)
    sub = trim_gap_columns(sub, bg)
    if not sub or not sub[0]:
        return []
    return sub

def program(g: List[List[int]]) -> List[List[int]]:
    bg = get_bg(g)
    rows = len(g)
    if rows == 0:
        return [[bg]]
    # Find global max_r
    global_max_r = max((i for i in range(rows) if any(cell != bg for cell in g[i])), default=0)
    components = get_same_color_components(g, bg)
    special_processed = []
    normal_pos = []
    for comp in components:
        min_r, max_r, min_c, max_c, size = comp
        temp_sub = extract_subgrid(g, min_r, max_r, min_c, max_c, bg)
        has9 = contains_9(temp_sub)
        h = max_r - min_r + 1
        if has9 and h == 5:
            sub = process_special(g, comp, bg)
            if sub:
                special_processed.append((min_c, min_r, sub))
        else:
            sub = process_normal(g, comp, bg, global_max_r)
            if sub:
                normal_pos.append((min_c, min_r, sub))
    # Sort special and normal
    special_processed.sort(key=lambda x: (x[0], x[1]))
    normal_pos.sort(key=lambda x: (x[0], x[1]))
    all_subs = [p[2] for p in special_processed] + [p[2] for p in normal_pos]
    if not all_subs:
        return [[bg]]
    w_total = sum(len(s[0]) for s in all_subs)
    result = [[bg for _ in range(w_total)] for _ in range(5)]
    current = 0
    for s in all_subs:
        w = len(s[0])
        for r in range(5):
            for c in range(w):
                result[r][current + c] = s[r][c]
        current += w
    return result
```