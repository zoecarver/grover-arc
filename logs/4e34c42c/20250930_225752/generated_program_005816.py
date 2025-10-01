```python
from typing import List, Tuple
from collections import Counter

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

def pad_vertical(sub: List[List[int]], h: int, w: int, bg: int) -> List[List[int]]:
    if h == 0:
        return []
    pad_top = (5 - h) // 2
    pad_bottom = 5 - h - pad_top
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
    return [row[left:right + 1] for row in sub]

def contains_value(sub: List[List[int]], val: int) -> bool:
    return any(any(cell == val for cell in row) for row in sub)

def find_special_frames(g: List[List[int]], bg: int, visited: List[List[bool]]) -> List[Tuple[List[List[int]], Tuple[int, int, int, int], int]]:
    components = []
    rows = len(g)
    cols = len(g[0]) if rows > 0 else 0
    for start_r in range(rows - 4):
        for start_c in range(cols):
            if visited[start_r][start_c]:
                continue
            color = g[start_r][start_c]
            if color == bg or color == 9:
                continue
            is_bar = all(g[start_r + i][start_c] == color for i in range(5))
            if not is_bar:
                continue
            found_c = -1
            for c in range(start_c + 1, cols):
                if g[start_r][c] == 9 and g[start_r + 4][c] == 9:
                    found_c = c
                    break
            if found_c == -1:
                continue
            sub = extract_subgrid(g, start_r, start_r + 4, start_c, found_c, bg)
            inner_cells = [cell for rr in range(1, 4) for cell in sub[rr] if cell != bg and cell != 9]
            fill_color = Counter(inner_cells).most_common(1)[0][0] if inner_cells else 1
            orig_w = len(sub[0])
            w = orig_w
            while w < 4:
                for rr in range(5):
                    sub[rr].append(bg)
                w += 1
            for added in range(orig_w, w):
                for rr in range(1, 4):
                    sub[rr][added] = fill_color
            for rr in range(5):
                for cc in range(start_c, found_c + 1):
                    visited[start_r + rr][cc] = True
            bb = (start_r, start_r + 4, start_c, found_c)
            components.append((sub, bb, fill_color))
    return components

def find_normal_components(g: List[List[int]], bg: int, visited: List[List[bool]], global_max_r: int) -> List[Tuple[List[List[int]], Tuple[int, int, int, int]]]:
    components = []
    rows = len(g)
    cols = len(g[0]) if rows > 0 else 0
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for i in range(rows):
        for j in range(cols):
            if visited[i][j] or g[i][j] == bg:
                continue
            color = g[i][j]
            min_r = max_r = i
            min_c = max_c = j
            size = 1
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
                    if 0 <= nx < rows and 0 <= ny < cols and not visited[nx][ny] and g[nx][ny] == color:
                        visited[nx][ny] = True
                        stack.append((nx, ny))
                        size += 1
            h = max_r - min_r + 1
            if h > 5 or size < 2 or min_r > global_max_r - 3:
                continue
            sub = extract_subgrid(g, min_r, max_r, min_c, max_c, bg)
            has9 = contains_value(sub, 9)
            has4 = contains_value(sub, 4)
            if has9 and h < 5:
                continue
            if has4:
                continue
            if h < 5:
                sub = pad_vertical(sub, h, len(sub[0]), bg)
            sub = trim_subgrid(sub, bg)
            if not sub or not sub[0]:
                continue
            bb = (min_r, max_r, min_c, max_c)
            components.append((sub, bb))
    return components

def program(g: List[List[int]]) -> List[List[int]]:
    bg = get_bg(g)
    rows = len(g)
    if rows == 0:
        return [[bg]]
    cols = len(g[0])
    global_max_r = -1
    for i in range(rows - 1, -1, -1):
        if any(g[i][j] != bg for j in range(cols)):
            global_max_r = i
            break
    visited = [[False] * cols for _ in range(rows)]
    specials = find_special_frames(g, bg, visited)
    normals = find_normal_components(g, bg, visited, global_max_r)
    all_comps = specials + normals
    def sort_key(comp):
        if len(comp) == 3:
            _, bb, _ = comp
        else:
            _, bb = comp
        min_r, max_r, min_c, max_c = bb
        return (-max_r, min_c)
    all_comps.sort(key=sort_key)
    if not all_comps:
        return [[bg]]
    result = [[] for _ in range(5)]
    for idx in range(len(all_comps)):
        comp = all_comps[idx]
        if len(comp) == 3:
            sub, bb, fill_color = comp
        else:
            sub, bb = comp
            fill_color = None
        min_r, max_r, min_c, max_c = bb
        add_gap = False
        prev_fill = None
        if idx > 0:
            prev_comp = all_comps[idx - 1]
            if len(prev_comp) == 3:
                prev_sub, prev_bb, prev_fill = prev_comp
                prev_max_c = prev_bb[3]
                is_prev_special = True
            else:
                prev_sub, prev_bb = prev_comp
                prev_max_c = prev_bb[3]
                is_prev_special = False
            if prev_max_c + 1 < min_c:
                add_gap = True
                prev_fill = prev_fill if is_prev_special else None
        if add_gap:
            for r in range(5):
                for _ in range(2):
                    val = prev_fill if (prev_fill is not None and r == 2) else bg
                    result[r].append(val)
        for r in range(5):
            result[r].extend(sub[r])
    return result
```