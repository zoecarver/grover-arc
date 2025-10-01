```python
from typing import List, Tuple

def get_bg(g: List[List[int]]) -> int:
    return g[0][0] if g and g[0] else 0

def extract_subgrid(g: List[List[int]], min_r: int, max_r: int, min_c: int, max_c: int, bg: int) -> List[List[int]]:
    h = max_r - min_r + 1
    w = max_c - min_c + 1
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

def pad_vertical(sub: List[List[int]], orig_h: int, w: int, bg: int) -> List[List[int]]:
    if not sub:
        return []
    pad_top = (5 - orig_h) // 2
    pad_bottom = 5 - orig_h - pad_top
    padded = [[bg] * w for _ in range(pad_top)] + sub + [[bg] * w for _ in range(pad_bottom)]
    return padded

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
    return [row[left : right + 1] for row in sub]

def contains_value(sub: List[List[int]], val: int) -> bool:
    return any(val in row for row in sub)

def program(g: List[List[int]]) -> List[List[int]]:
    if not g or not g[0]:
        return [[get_bg(g)]]
    bg = get_bg(g)
    rows = len(g)
    if rows == 0:
        return [[bg]]
    cols = len(g[0])
    global_max_r = max((i for i in range(rows) if any(c != bg for c in g[i])), default = -1)
    visited = [[False] * cols for _ in range(rows)]
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    components: List[Tuple[int, int, int, List[List[int]], bool, int]] = []
    # Detect special frames
    for start_r in range(rows - 4):
        for start_c in range(cols):
            bar_color = g[start_r][start_c]
            if bar_color == bg:
                continue
            is_bar = all(g[start_r + i][start_c] == bar_color for i in range(5))
            if not is_bar:
                continue
            for d in range(start_c + 1, cols):
                if g[start_r][d] == 9 and g[start_r + 4][d] == 9:
                    min_r = start_r
                    max_r = start_r + 4
                    min_c_comp = start_c
                    max_c_comp = d + 1
                    sub = extract_subgrid(g, min_r, max_r, min_c_comp, max_c_comp, bg)
                    inside_color = g[start_r + 1][start_c + 1]
                    for rr in range(1, 4):
                        for cc in range(1, len(sub[rr])):
                            if sub[rr][cc] == bg:
                                sub[rr][cc] = inside_color
                    # Mark visited the frame area
                    for ii in range(5):
                        for jj in range(len(sub[0])):
                            nr = min_r + ii
                            nc = min_c_comp + jj
                            if 0 <= nc < cols:
                                visited[nr][nc] = True
                    components.append((min_r, min_c_comp, max_c_comp, sub, True, inside_color))
                    break  # Assume one frame per bar
    # Normal components
    for i in range(rows):
        for j in range(cols):
            if visited[i][j] or g[i][j] == bg:
                continue
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
            if size < 2 or h > 5 or min_r > global_max_r - 3:
                continue
            sub = extract_subgrid(g, min_r, max_r, min_c, max_c, bg)
            has_9 = contains_value(sub, 9)
            has_4 = contains_value(sub, 4)
            if has_9 and h < 5 or has_4:
                continue
            orig_h = h
            if h < 5:
                sub = pad_vertical(sub, orig_h, len(sub[0]), bg)
            sub = trim_subgrid(sub, bg)
            if not sub or not sub[0]:
                continue
            components.append((min_r, min_c, max_c, sub, False, 0))
    if not components:
        return [[bg]]
    # Sort by descending min_r (ascending -min_r), then ascending min_c
    components.sort(key=lambda x: (-x[0], x[1]))
    # Build result
    result = [[] for _ in range(5)]
    previous_is_special = False
    previous_inside = 0
    for comp in components:
        min_r, min_c, max_c, sub, is_special, inside = comp
        if previous_is_special:
            gap_w = 2
            for r in range(5):
                fill_val = previous_inside if r == 2 else bg
                result[r].extend([fill_val] * gap_w)
        # Add the sub
        for r in range(5):
            result[r].extend(sub[r])
        previous_is_special = is_special
        previous_inside = inside
    return result
```