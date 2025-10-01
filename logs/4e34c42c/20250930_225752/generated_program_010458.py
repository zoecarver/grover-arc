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
    return any(val in row for row in sub)

def get_global_max_r(g: List[List[int]], bg: int) -> int:
    rows = len(g)
    max_r = -1
    for r in range(rows):
        if any(cell != bg for cell in g[r]):
            max_r = r
    return max_r

def find_special_frames(g: List[List[int]], bg: int) -> List[Tuple[int, int, int, List[List[int]], int]]:
    rows = len(g)
    cols = len(g[0]) if rows > 0 else 0
    specials = []
    directions = []  # not used
    for start_r in range(rows - 4):
        for bar_c in range(cols):
            bar_color = g[start_r][bar_c]
            if bar_color == bg:
                continue
            uniform = all(g[start_r + i][bar_c] == bar_color for i in range(5))
            if not uniform:
                continue
            top_9 = -1
            for cc in range(bar_c + 1, cols):
                if g[start_r][cc] == 9:
                    top_9 = cc
                    break
            if top_9 == -1:
                continue
            bottom_9 = -1
            for cc in range(bar_c + 1, cols):
                if g[start_r + 4][cc] == 9:
                    bottom_9 = cc
                    break
            if bottom_9 != top_9:
                continue
            right_c = top_9
            orig_max_c = right_c
            inner_color = g[start_r + 1][bar_c + 1]
            new_max_c = bar_c + 3
            sub = extract_subgrid(g, start_r, start_r + 4, bar_c, new_max_c, bg)
            for rel_r in range(1, 4):
                if 3 < len(sub[rel_r]):
                    sub[rel_r][3] = inner_color
            specials.append((bar_c, orig_max_c, start_r, sub, inner_color))
    return specials

def get_regular_components(g: List[List[int]], bg: int, visited: List[List[bool]]) -> List[Tuple[int, int, int, int]]:
    rows = len(g)
    cols = len(g[0]) if rows > 0 else 0
    comps = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for i in range(rows):
        for j in range(cols):
            if not visited[i][j] and g[i][j] != bg:
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
                if h <= 5 and size >= 2:
                    comps.append((min_r, max_r, min_c, max_c))
    return comps

def build_groups(items: List[Tuple[int, int, int, List[List[int]]]], bg: int) -> List[Tuple[int, List[List[int]]]]:
    if not items:
        return []
    sorted_items = sorted(items, key=lambda t: (t[0], t[2]))
    groups = []
    curr_subs = [sorted_items[0][3]]
    curr_min_c = sorted_items[0][0]
    curr_max_c = sorted_items[0][1]
    for it in sorted_items[1:]:
        if it[0] == curr_max_c + 1:
            curr_subs.append(it[3])
            curr_max_c = it[1]
        else:
            group = concat_subgrids(curr_subs)
            groups.append((curr_min_c, group))
            curr_subs = [it[3]]
            curr_min_c = it[0]
            curr_max_c = it[1]
    group = concat_subgrids(curr_subs)
    groups.append((curr_min_c, group))
    return groups

def concat_subgrids(subs: List[List[List[int]]]) -> List[List[int]]:
    if not subs:
        return []
    h = 5
    total_w = sum(len(s[0]) for s in subs)
    res = [[0] * total_w for _ in range(h)]
    cur = 0
    for s in subs:
        sw = len(s[0])
        for r in range(h):
            for c in range(sw):
                res[r][cur + c] = s[r][c]
        cur += sw
    return res

def program(g: List[List[int]]) -> List[List[int]]:
    if not g or not g[0]:
        return [[0]]
    bg = get_bg(g)
    rows = len(g)
    cols = len(g[0])
    specials = find_special_frames(g, bg)
    visited = [[False] * cols for _ in range(rows)]
    for min_c, orig_max_c, min_r, _, _ in specials:
        max_r = min_r + 4
        for rr in range(min_r, max_r + 1):
            for cc in range(min_c, orig_max_c + 1):
                if cc < cols:
                    visited[rr][cc] = True
    regular_comps = get_regular_components(g, bg, visited)
    global_max_r = get_global_max_r(g, bg)
    normal_items = []
    for min_r, max_r, min_c, max_c in regular_comps:
        if global_max_r >= 0 and min_r > global_max_r - 3:
            continue
        sub = extract_subgrid(g, min_r, max_r, min_c, max_c, bg)
        h_orig = max_r - min_r + 1
        if contains_value(sub, 9) and h_orig < 5:
            continue
        if bg != 4 and contains_value(sub, 4):
            continue
        w = max_c - min_c + 1
        padded = pad_vertical(sub, h_orig, w, bg)
        trimmed = trim_subgrid(padded, bg)
        if not trimmed or not trimmed[0]:
            continue
        normal_items.append((min_c, max_c, min_r, trimmed))
    normal_groups = build_groups(normal_items, bg)
    sorted_normal_groups = sorted(normal_groups, key=lambda t: t[0])
    special_items = sorted(specials, key=lambda t: (t[0], t[2]))
    special_groups = []
    for min_c, orig_max_c, min_r, sub, inner_color in special_items:
        special_groups.append((min_c, sub, inner_color))
    result_rows = [[] for _ in range(5)]
    for min_c, sub, inner_color in special_groups:
        for r in range(5):
            result_rows[r].extend(sub[r])
        gap = [[bg] * 2 for _ in range(5)]
        gap[2] = [inner_color] * 2
        for r in range(5):
            result_rows[r].extend(gap[r])
    for min_c, group in sorted_normal_groups:
        for r in range(5):
            result_rows[r].extend(group[r])
    if all(len(row) == 0 for row in result_rows):
        return [[bg]]
    return result_rows
```