```python
from typing import List, Tuple

def get_bg(g: List[List[int]]) -> int:
    return g[0][0] if g else 0

def extract_subgrid(g: List[List[int]], min_r: int, max_r: int, min_c: int, max_c: int, bg: int) -> List[List[int]]:
    sub = []
    rows = len(g)
    cols = len(g[0]) if rows > 0 else 0
    for r in range(min_r, max_r + 1):
        row = []
        for c in range(min_c, max_c + 1):
            if 0 <= r < rows and 0 <= c < cols:
                row.append(g[r][c])
            else:
                row.append(bg)
        sub.append(row)
    return sub

def pad_vertical(sub: List[List[int]], bg: int) -> List[List[int]]:
    h = len(sub)
    if h == 0:
        return []
    w = len(sub[0])
    pad_top = (5 - h) // 2
    pad_bottom = 5 - h - pad_top
    padded_top = [[bg] * w for _ in range(pad_top)]
    padded_bottom = [[bg] * w for _ in range(pad_bottom)]
    return padded_top + sub + padded_bottom

def trim_subgrid(sub: List[List[int]], bg: int) -> List[List[int]]:
    if not sub:
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
    return [row[left:right + 1] for row in sub]

def contains_val(sub: List[List[int]], val: int) -> bool:
    return any(val in row for row in sub)

def find_special_frames(g: List[List[int]], bg: int, visited: List[List[bool]]) -> List[Tuple[Tuple[int, int], List[List[int]]]]:
    rows = len(g)
    cols = len(g[0]) if rows > 0 else 0
    specials = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # unused here
    for start_r in range(rows - 4):
        for start_c in range(cols):
            if visited[start_r][start_c] or g[start_r][start_c] == bg:
                continue
            C = g[start_r][start_c]
            uniform = True
            for k in range(1, 5):
                if g[start_r + k][start_c] != C:
                    uniform = False
                    break
            if not uniform:
                continue
            top9 = -1
            for cc in range(start_c + 1, cols):
                if g[start_r][cc] == 9:
                    top9 = cc
                    break
            bottom9 = -1
            for cc in range(start_c + 1, cols):
                if g[start_r + 4][cc] == 9:
                    bottom9 = cc
                    break
            if top9 != -1 and bottom9 != -1 and top9 == bottom9:
                right_c = top9
                sub = extract_subgrid(g, start_r, start_r + 4, start_c, right_c, bg)
                w = len(sub[0])
                fill_color = None
                for rr in range(1, 4):
                    for cc in range(1, w):
                        v = sub[rr][cc]
                        if v != bg and v != C and v != 9:
                            fill_color = v
                            break
                    if fill_color:
                        break
                if fill_color is None:
                    fill_color = 1
                added = 4 - w
                for _ in range(max(0, added)):
                    for rr in range(5):
                        if rr == 0 or rr == 4:
                            sub[rr].append(bg)
                        else:
                            sub[rr].append(fill_color)
                sub = trim_subgrid(sub, bg)
                if sub:
                    key = (start_c, start_r)
                    specials.append((key, sub))
                # mark visited up to right_c
                for rr in range(start_r, start_r + 5):
                    for cc in range(start_c, right_c + 1):
                        if 0 <= rr < rows and 0 <= cc < cols:
                            visited[rr][cc] = True
    return specials

def get_components(g: List[List[int]], bg: int, visited: List[List[bool]]) -> List[Tuple[int, int, int, int, Tuple[int, int]]]:
    rows = len(g)
    cols = len(g[0]) if rows > 0 else 0
    components = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for i in range(rows):
        for j in range(cols):
            if not visited[i][j] and g[i][j] != bg:
                color = g[i][j]
                min_r = max_r = i
                min_c = max_c = j
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
                        if 0 <= nx < rows and 0 <= ny < cols and not visited[nx][ny] and g[nx][ny] == color:
                            visited[nx][ny] = True
                            stack.append((nx, ny))
                            size += 1
                h = max_r - min_r + 1
                if h <= 5 and size >= 2:
                    key = (min_c, min_r)
                    components.append((min_r, max_r, min_c, max_c, key))
    return components

def program(g: List[List[int]]) -> List[List[int]]:
    if not g:
        return []
    bg = get_bg(g)
    rows = len(g)
    cols = len(g[0]) if rows > 0 else 0
    visited = [[False] * cols for _ in range(rows)]
    special_list = find_special_frames(g, bg, visited)
    comps = get_components(g, bg, visited)
    processed = []
    for min_r, max_r, min_c, max_c, key in comps:
        sub = extract_subgrid(g, min_r, max_r, min_c, max_c, bg)
        h = len(sub)
        skip = False
        if h < 5:
            if contains_val(sub, 9) or contains_val(sub, 4):
                skip = True
        if not skip:
            if h < 5:
                sub = pad_vertical(sub, bg)
            sub = trim_subgrid(sub, bg)
            if sub:
                processed.append((key, sub))
    processed.extend(special_list)
    if not processed:
        return [[bg]]
    processed.sort(key=lambda x: x[0])
    total_w = sum(len(p[1][0]) for p in processed)
    result = [[bg] * total_w for _ in range(5)]
    curr = 0
    for _, sub in processed:
        w_sub = len(sub[0])
        for r in range(5):
            for c in range(w_sub):
                result[r][curr + c] = sub[r][c]
        curr += w_sub
    return result
```