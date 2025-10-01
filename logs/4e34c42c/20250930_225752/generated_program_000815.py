```python
from typing import List, Tuple

def get_bg(g: List[List[int]]) -> int:
    return g[0][0]

def extract_subgrid(g: List[List[int]], min_r: int, max_r: int, min_c: int, max_c: int, bg: int) -> List[List[int]]:
    h = max_r - min_r + 1
    w = max_c - min_c + 1
    sub = []
    for r in range(min_r, max_r + 1):
        row = [g[r][c] if 0 <= c < len(g[0]) else bg for c in range(min_c, max_c + 1)]
        sub.append(row)
    return sub

def pad_vertical(sub: List[List[int]], target_h: int, bg: int) -> List[List[int]]:
    h = len(sub)
    if h == 0:
        return []
    w = len(sub[0])
    pad_top = (target_h - h) // 2
    pad_bottom = target_h - h - pad_top
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

def contains_four(sub: List[List[int]]) -> bool:
    return any(4 in row for row in sub)

def get_simple_components(g: List[List[int]], bg: int, visited: List[List[bool]]) -> List[Tuple[int, int, int, int, int]]:
    rows = len(g)
    cols = len(g[0])
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
                    components.append((min_r, max_r, min_c, max_c, size))
    return components

def find_special_frames(g: List[List[int]], bg: int, visited: List[List[bool]]) -> List[Tuple[List[List[int]], int, int]]:
    rows = len(g)
    cols = len(g[0])
    special = []
    for start_r in range(rows - 4):
        for c in range(cols):
            if visited[start_r][c]:
                continue
            color = g[start_r][c]
            if color == bg:
                continue
            is_bar = True
            for ii in range(5):
                rr = start_r + ii
                if g[rr][c] != color:
                    is_bar = False
                    break
            if is_bar:
                k = None
                for possible_k in range(c + 1, cols):
                    if g[start_r][possible_k] == 9 and g[start_r + 4][possible_k] == 9:
                        k = possible_k
                        break
                if k is not None:
                    sub = extract_subgrid(g, start_r, start_r + 4, c, k, bg)
                    orig_w = len(sub[0])
                    if orig_w < 4:
                        add_cols = 4 - orig_w
                        for _ in range(add_cols):
                            for i in range(5):
                                val = 1 if 0 < i < 4 else bg
                                for row_idx in range(5):
                                    sub[row_idx].append(val)
                    # mark original cells
                    orig_w_mark = k - c + 1
                    for ii in range(5):
                        for jj in range(orig_w_mark):
                            visited[start_r + ii][c + jj] = True
                    special.append((sub, start_r, c))
    special.sort(key=lambda x: x[2])
    return [(s[0], s[1], s[2]) for s in special]

def program(g: List[List[int]]) -> List[List[int]]:
    if not g or not g[0]:
        return [[0]]
    bg = get_bg(g)
    rows = len(g)
    cols = len(g[0])
    visited = [[False] * cols for _ in range(rows)]
    special_raw = find_special_frames(g, bg, visited)
    special_subs = [s[0] for s in special_raw]
    max_end = 0
    if special_raw:
        max_end = max(s[1] + 4 for s in special_raw)
    simple_raw = get_simple_components(g, bg, visited)
    simple_subs = []
    simple_info = []
    for minr, maxr, minc, maxc, sz in simple_raw:
        if minr > max_end:
            continue
        sub = extract_subgrid(g, minr, maxr, minc, maxc, bg)
        orig_h = maxr - minr + 1
        if contains_four(sub) and orig_h < 5:
            continue
        padded = pad_vertical(sub, 5, bg)
        trimmed = trim_subgrid(padded, bg)
        if trimmed:
            simple_subs.append(trimmed)
            simple_info.append((minr, minc, maxc))
    # sort simple
    idx = sorted(range(len(simple_info)), key=lambda ii: (simple_info[ii][1], simple_info[ii][0]))
    sorted_simple_subs = [simple_subs[i] for i in idx]
    sorted_simple_info = [simple_info[i] for i in idx]
    # build out_grid temp
    max_w = sum(len(s[0]) for s in special_subs + sorted_simple_subs) + 10  # extra for gaps
    out_grid = [[bg] * max_w for _ in range(5)]
    current_col = 0
    # special
    for sub in special_subs:
        w = len(sub[0])
        for rr in range(5):
            for cc in range(w):
                out_grid[rr][current_col + cc] = sub[rr][cc]
        current_col += w
    # simple
    if sorted_simple_subs:
        if special_subs:
            # add 2 bg
            for rr in range(5):
                out_grid[rr][current_col] = bg
                out_grid[rr][current_col + 1] = bg
            current_col += 2
        prev_max_c = None
        for ii in range(len(sorted_simple_subs)):
            minr, minc, maxc = sorted_simple_info[ii]
            sub = sorted_simple_subs[ii]
            if prev_max_c is not None and minc == prev_max_c + 1:
                # no gap
                pass
            else:
                # add 2 bg
                for rr in range(5):
                    out_grid[rr][current_col] = bg
                    out_grid[rr][current_col + 1] = bg
                current_col += 2
            w = len(sub[0])
            for rr in range(5):
                for cc in range(w):
                    out_grid[rr][current_col + cc] = sub[rr][cc]
            current_col += w
            prev_max_c = maxc
    # trim the out_grid to actual width
    actual_w = current_col
    final_out = [row[:actual_w] for row in out_grid]
    if not final_out[0]:
        return [[bg]]
    return final_out
```