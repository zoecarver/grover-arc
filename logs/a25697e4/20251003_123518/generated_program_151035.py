```python
from typing import List, Tuple
from collections import Counter

def get_background(g: List[List[int]]) -> int:
    if not g or not g[0]:
        return 0
    flat = [cell for row in g for cell in row]
    if not flat:
        return 0
    return Counter(flat).most_common(1)[0][0]

def find_components(g: List[List[int]], background: int) -> List[Tuple[int, List[Tuple[int, int]]]]:
    rows = len(g)
    if rows == 0:
        return []
    cols = len(g[0])
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

def count_main_left(g: List[List[int]], r: int, main_color: int, w: int) -> int:
    left_size = min(4, w)
    return sum(1 for j in range(left_size) if g[r][j] == main_color)

def get_min_row_for_color(g: List[List[int]], color: int, bg: int, h: int, w: int) -> int:
    min_r = float('inf')
    for r in range(h):
        for c in range(w):
            if g[r][c] == color and g[r][c] != bg:
                min_r = min(min_r, r)
                break
        if min_r < float('inf'):
            return min_r
    return float('inf')

def build_bg_grid(h: int, w: int, bg: int) -> List[List[int]]:
    return [[bg for _ in range(w)] for _ in range(h)]

def place_component(out: List[List[int]], color: int, positions: List[Tuple[int, int]]) -> None:
    for r, c in positions:
        if 0 <= r < len(out) and 0 <= c < len(out[0]):
            out[r][c] = color

def program(g: List[List[int]]) -> List[List[int]]:
    h = len(g)
    if h == 0:
        return []
    w = len(g[0])
    bg = get_background(g)
    comps = find_components(g, bg)
    anchored_comps = [c for c in comps if touches_left(c[1])]
    if anchored_comps:
        main_color = anchored_comps[0][0]
        if any(c[0] != main_color for c in anchored_comps):
            out = build_bg_grid(h, w, bg)
            main_subs = [c for c in comps if c[0] == main_color and touches_left(c[1])]
            for color, pos in main_subs:
                place_component(out, color, pos)
            return out
        main_subs = [c for c in comps if c[0] == main_color and touches_left(c[1])]
        if len(main_subs) != 2:
            out = build_bg_grid(h, w, bg)
            for color, pos in main_subs:
                place_component(out, color, pos)
            return out
        floating_non_main = [c for c in comps if not touches_left(c[1]) and c[0] != main_color and c[0] != bg]
        noise_colors_set = set(c[0] for c in floating_non_main)
        if len(noise_colors_set) != 2:
            out = build_bg_grid(h, w, bg)
            for color, pos in main_subs:
                place_component(out, color, pos)
            return out
        noise_colors = list(noise_colors_set)
        min_rows = {col: get_min_row_for_color(g, col, bg, h, w) for col in noise_colors}
        sorted_noises = sorted(noise_colors, key=lambda col: min_rows[col])
        upper_noise, lower_noise = sorted_noises
        left_size = min(4, w)
        full_rows = [r for r in range(h) if count_main_left(g, r, main_color, w) == left_size]
        partial_rows = [r for r in range(h) if count_main_left(g, r, main_color, w) == 2]
        if len(full_rows) != 2 or len(partial_rows) != 1 or max(full_rows) != min(full_rows) + 3:
            out = build_bg_grid(h, w, bg)
            for color, pos in main_subs:
                place_component(out, color, pos)
            return out
        top = min(full_rows)
        bottom = max(full_rows)
        middle = partial_rows[0]
        if not (top < middle < bottom):
            out = build_bg_grid(h, w, bg)
            for color, pos in main_subs:
                place_component(out, color, pos)
            return out
        potential_gaps = [r for r in range(top + 1, bottom) if r != middle and count_main_left(g, r, main_color, w) == 0]
        if len(potential_gaps) != 1:
            out = build_bg_grid(h, w, bg)
            for color, pos in main_subs:
                place_component(out, color, pos)
            return out
        gap = potential_gaps[0]
        if gap > middle:
            inner = lower_noise
            outer = upper_noise
        else:
            inner = upper_noise
            outer = lower_noise
        out = build_bg_grid(h, w, bg)
        for rr in [top, bottom]:
            for j in range(left_size):
                out[rr][j] = main_color
        for j in range(2):
            out[middle][j] = main_color
        for j in range(2, left_size):
            out[middle][j] = inner
        for j in range(4, min(9, w)):
            out[middle][j] = outer
        for j in range(left_size):
            out[gap][j] = inner
        if w > 8:
            out[gap][8] = outer
        if gap == top + 1:
            for j in range(8, min(10, w)):
                out[top][j] = outer
        if gap == bottom - 1:
            for j in range(8, min(10, w)):
                out[bottom][j] = outer
        for color, pos in main_subs:
            for r, c in pos:
                if c >= left_size or (r not in [top, bottom, middle] and r != gap):
                    out[r][c] = color
        return out
    else:
        def get_max_row(comp: Tuple[int, List[Tuple[int, int]]]) -> int:
            pos = comp[1]
            return max((r for r, _ in pos), default=-1)
        sorted_comps = sorted(comps, key=get_max_row, reverse=True)
        out = build_bg_grid(h, w, bg)
        for color, pos_list in sorted_comps:
            targets = [(r + 1, c + 6) for r, c in pos_list]
            can_shift = all(0 <= nr < h and 0 <= nc < w for nr, nc in targets) and all(out[nr][nc] == bg for nr, nc in targets)
            if can_shift:
                place_component(out, color, targets)
            else:
                place_component(out, color, pos_list)
        return out
```