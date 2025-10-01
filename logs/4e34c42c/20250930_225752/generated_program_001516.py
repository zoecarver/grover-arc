```python
from typing import List, Tuple

def get_bg(g: List[List[int]]) -> int:
    return g[0][0] if g else 0

def find_components(g: List[List[int]], bg: int) -> List[Tuple[int, int, int, int, int]]:
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
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < rows and 0 <= ny < cols and not visited[nx][ny] and g[nx][ny] == color:
                            visited[nx][ny] = True
                            stack.append((nx, ny))
                            size += 1
                h = max_r - min_r + 1
                if h <= 5 and size >= 2:
                    components.append((min_r, max_r, min_c, max_c, color))
    return components

def extract_subgrid(g: List[List[int]], min_r: int, max_r: int, min_c: int, max_c: int, bg: int) -> List[List[int]]:
    h = max_r - min_r + 1
    w = max_c - min_c + 1
    sub = []
    for r in range(min_r, max_r + 1):
        row = [g[r][c] if 0 <= c < len(g[0]) else bg for c in range(min_c, max_c + 1)]
        sub.append(row)
    return sub

def contains_value(sub: List[List[int]], val: int) -> bool:
    return any(val in row for row in sub)

def pad_vertical(sub: List[List[int]], bg: int) -> List[List[int]]:
    h = len(sub)
    if h == 0:
        return []
    w = len(sub[0])
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

def process_component(g: List[List[int]], comp: Tuple[int, int, int, int, int], bg: int) -> List[List[int]] or None:
    min_r, max_r, min_c, max_c, color = comp
    sub = extract_subgrid(g, min_r, max_r, min_c, max_c, bg)
    h = len(sub)
    has9 = contains_value(sub, 9)
    has4 = contains_value(sub, 4)
    if has4 and not has9:
        return None
    if h < 5:
        sub = pad_vertical(sub, bg)
    elif has9:
        new_max_c = max_c + 1
        sub = extract_subgrid(g, min_r, max_r, min_c, new_max_c, bg)
        w = len(sub[0])
        for r in range(1, 4):
            sub[r][w - 1] = 1
    sub = trim_subgrid(sub, bg)
    if not sub or len(sub[0]) == 0:
        return None
    return sub

def concat_subgrids(subs: List[List[List[int]]]) -> List[List[int]]:
    if not subs:
        return []
    h = 5
    w_total = sum(len(s[0]) for s in subs)
    result = [[0] * w_total for _ in range(h)]
    current = 0
    for s in subs:
        w = len(s[0])
        for r in range(h):
            for c in range(w):
                result[r][current + c] = s[r][c]
        current += w
    return result

def group_and_concat(items: List[Tuple[List[List[int]], int, int]]) -> List[List[List[int]]]:
    if not items:
        return []
    groups = []
    current_group = [items[0][0]]
    current_max_c = items[0][2]
    for item in items[1:]:
        sub, min_c, max_c = item
        if min_c == current_max_c + 1:
            current_group.append(sub)
            current_max_c = max_c
        else:
            group_grid = concat_subgrids(current_group)
            groups.append(group_grid)
            current_group = [sub]
            current_max_c = max_c
    group_grid = concat_subgrids(current_group)
    groups.append(group_grid)
    return groups

def concatenate_with_gaps(grids: List[List[List[int]]], bg: int, gap_width: int) -> List[List[int]]:
    if not grids:
        return [[bg]]
    result = [row[:] for row in grids[0]]
    for grid in grids[1:]:
        for r in range(5):
            result[r] += [bg] * gap_width
            result[r] += grid[r]
    return result

def program(g: List[List[int]]) -> List[List[int]]:
    bg = get_bg(g)
    comps = find_components(g, bg)
    processed = []
    for comp in comps:
        sub = process_component(g, comp, bg)
        if sub is not None:
            min_r, _, min_c, max_c, _ = comp
            processed.append((sub, min_c, max_c, min_r))
    special = [p for p in processed if contains_value(p[0], 9)]
    normal = [p for p in processed if not contains_value(p[0], 9)]
    if special:
        max_special_min_r = max(p[3] for p in special)
        normal = [p for p in normal if p[3] <= max_special_min_r]
    special.sort(key=lambda p: p[1])
    normal.sort(key=lambda p: p[1])
    special_groups = group_and_concat([(p[0], p[1], p[2]) for p in special])
    normal_groups = group_and_concat([(p[0], p[1], p[2]) for p in normal])
    all_groups = special_groups + normal_groups
    if not all_groups:
        return [[bg]]
    return concatenate_with_gaps(all_groups, bg, 2)
```