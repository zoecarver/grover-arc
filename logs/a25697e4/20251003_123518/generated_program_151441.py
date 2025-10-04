```python
from typing import List, Tuple
from collections import Counter

def program(g: List[List[int]]) -> List[List[int]]:
    h = len(g)
    if h == 0:
        return []
    w = len(g[0])
    bg = get_background(g)
    if not has_anchored(g, bg):
        return apply_unanchored(g, bg, h, w)
    else:
        return apply_anchored(g, bg, h, w)

def get_background(g: List[List[int]]) -> int:
    if not g or not g[0]:
        return 0
    flat = [cell for row in g for cell in row]
    if not flat:
        return 0
    return Counter(flat).most_common(1)[0][0]

def copy_grid(g: List[List[int]]) -> List[List[int]]:
    return [row[:] for row in g]

def build_bg_grid(h: int, w: int, bg: int) -> List[List[int]]:
    return [[bg] * w for _ in range(h)]

def place_component(out: List[List[int]], color: int, positions: List[Tuple[int, int]]) -> None:
    for r, c in positions:
        if 0 <= r < len(out) and 0 <= c < len(out[0]):
            out[r][c] = color

def has_anchored(g: List[List[int]], bg: int) -> bool:
    return any(row and row[0] != bg for row in g)

def find_components(g: List[List[int]], background: int) -> List[Tuple[int, List[Tuple[int, int]]]]:
    rows = len(g)
    if rows == 0:
        return []
    cols = len(g[0])
    if cols == 0:
        return []
    visited = [[False] * cols for _ in range(rows)]
    components = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for i in range(rows):
        for j in range(cols):
            if not visited[i][j] and g[i][j] != background:
                color = g[i][j]
                component = []
                stack = [(i, j)]
                visited[i][j] = True
                while stack:
                    x, y = stack.pop()
                    component.append((x, y))
                    for dx, dy in directions:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < rows and 0 <= ny < cols and not visited[nx][ny] and g[nx][ny] == color:
                            visited[nx][ny] = True
                            stack.append((nx, ny))
                components.append((color, component))
    return components

def touches_left(component: List[Tuple[int, int]]) -> bool:
    return any(c == 0 for _, c in component)

def touches_bottom(component: List[Tuple[int, int]], h: int) -> bool:
    return any(r == h - 1 for r, _ in component)

def get_min_row(g: List[List[int]], color: int, h: int, w: int) -> int:
    for r in range(h):
        for c in range(w):
            if g[r][c] == color:
                return r
    return h

def count_left_main(g: List[List[int]], r: int, main_color: int, w: int) -> int:
    left_size = min(4, w)
    return sum(1 for j in range(left_size) if g[r][j] == main_color)

def apply_unanchored(g: List[List[int]], bg: int, h: int, w: int) -> List[List[int]]:
    out = copy_grid(g)
    components = find_components(g, bg)
    movables = [c for c in components if not touches_bottom(c[1], h)]
    movables.sort(key=lambda c: -max(r for r, _ in c[1]))
    for color, pos in movables:
        target = [(r + 1, c + 6) for r, c in pos]
        if all(0 <= tr < h and 0 <= tc < w and out[tr][tc] == bg for tr, tc in target):
            for r, c in pos:
                out[r][c] = bg
            for tr, tc in target:
                out[tr][tc] = color
    return out

def apply_anchored(g: List[List[int]], bg: int, h: int, w: int) -> List[List[int]]:
    out = build_bg_grid(h, w, bg)
    left_colors = {g[r][0] for r in range(h) if g[r][0] != bg}
    if len(left_colors) != 1:
        return copy_grid(g)
    main_color = next(iter(left_colors))
    components = find_components(g, bg)
    anchored_comps = [c for c in components if c[0] == main_color and touches_left(c[1])]
    for color, pos in anchored_comps:
        place_component(out, color, pos)
    floating_comps = [c for c in components if c[0] != bg and c[0] != main_color and not touches_left(c[1])]
    noise_colors_set = set(c[0] for c in floating_comps)
    min_rows = {col: get_min_row(g, col, h, w) for col in noise_colors_set}
    noise_list = [col for col in noise_colors_set if min_rows[col] < h]
    noise_list.sort(key=lambda col: min_rows[col])
    if len(noise_list) != 2:
        return out
    upper_noise = noise_list[0]
    lower_noise = noise_list[1]
    left_size = min(4, w)
    full_rows = [r for r in range(h) if count_left_main(g, r, main_color, w) == left_size]
    partial_rows = [r for r in range(h) if count_left_main(g, r, main_color, w) == 2]
    if len(full_rows) != 2 or len(partial_rows) != 1:
        return out
    top, bottom = sorted(full_rows)
    if bottom != top + 3:
        return out
    middle = partial_rows[0]
    if not (top < middle < bottom):
        return out
    gap_cands = [r for r in range(top + 1, bottom) if r != middle and count_left_main(g, r, main_color, w) == 0]
    if len(gap_cands) != 1:
        return out
    gap = gap_cands[0]
    if gap < middle:
        inner = upper_noise
        outer = lower_noise
    else:
        inner = lower_noise
        outer = upper_noise
    for r in [top, bottom]:
        for j in range(left_size):
            if out[r][j] == bg:
                out[r][j] = main_color
    for j in range(2):
        if out[middle][j] == bg:
            out[middle][j] = main_color
    for j in range(2, left_size):
        if out[middle][j] == bg:
            out[middle][j] = inner
    for j in range(4, min(9, w)):
        if out[middle][j] == bg:
            out[middle][j] = outer
    for j in range(left_size):
        if out[gap][j] == bg:
            out[gap][j] = inner
    if w > 8 and out[gap][8] == bg:
        out[gap][8] = outer
    adj = None
    if gap == top + 1:
        adj = top
    elif gap == bottom - 1:
        adj = bottom
    if adj is not None:
        start_j = 8
        end_j = min(10, w)
        for j in range(start_j, end_j):
            if out[adj][j] == bg:
                out[adj][j] = outer
    return out
```