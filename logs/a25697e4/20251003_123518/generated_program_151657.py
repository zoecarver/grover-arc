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

def copy_grid(g: List[List[int]]) -> List[List[int]]:
    return [row[:] for row in g]

def build_bg_grid(h: int, w: int, bg: int) -> List[List[int]]:
    return [[bg] * w for _ in range(h)]

def get_main_color(g: List[List[int]], bg: int) -> int:
    left_colors = {row[0] for row in g if row[0] != bg}
    if len(left_colors) != 1:
        return -1
    return next(iter(left_colors))

def get_min_row_for_color(g: List[List[int]], color: int, h: int, w: int) -> int:
    for r in range(h):
        for c in range(w):
            if g[r][c] == color:
                return r
    return float('inf')

def get_noise_colors(g: List[List[int]], bg: int, main: int, h: int, w: int) -> Tuple[int, int]:
    comps = find_components(g, bg)
    noise_colors = set()
    for colr, pos in comps:
        if colr != bg and colr != main and not touches_left(pos):
            noise_colors.add(colr)
    if len(noise_colors) != 2:
        return -1, -1
    noises = list(noise_colors)
    noises.sort(key=lambda c: get_min_row_for_color(g, c, h, w))
    return noises[0], noises[1]

def detect_structural_rows(g: List[List[int]], main: int, h: int, w: int) -> Tuple[int, int, int, int]:
    left_size = min(4, w)
    counts = [0] * h
    for r in range(h):
        for j in range(left_size):
            if g[r][j] == main:
                counts[r] += 1
    full_rows = [r for r, cnt in enumerate(counts) if cnt == left_size]
    partial_rows = [r for r, cnt in enumerate(counts) if cnt == 2]
    if len(full_rows) != 2 or len(partial_rows) != 1:
        return -1, -1, -1, -1
    top, bottom = sorted(full_rows)
    if bottom != top + 3:
        return -1, -1, -1, -1
    middle = partial_rows[0]
    if not (top < middle < bottom):
        return -1, -1, -1, -1
    gap_candidates = [r for r in range(top + 1, bottom) if r != middle and counts[r] == 0]
    if len(gap_candidates) != 1:
        return -1, -1, -1, -1
    gap = gap_candidates[0]
    return top, middle, bottom, gap

def apply_anchored(g: List[List[int]], bg: int, h: int, w: int) -> List[List[int]]:
    main = get_main_color(g, bg)
    if main == -1:
        return copy_grid(g)
    upper_n, lower_n = get_noise_colors(g, bg, main, h, w)
    if upper_n == -1:
        out = build_bg_grid(h, w, bg)
        top, middle, bottom, _ = detect_structural_rows(g, main, h, w)
        ls = min(4, w)
        if top != -1:
            out[top][:ls] = [main] * ls
            out[bottom][:ls] = [main] * ls
            out[middle][:2] = [main] * 2
        return out
    top, middle, bottom, gap = detect_structural_rows(g, main, h, w)
    if top == -1:
        return copy_grid(g)
    if gap < middle:
        inner = upper_n
        outer = lower_n
    else:
        inner = lower_n
        outer = upper_n
    out = build_bg_grid(h, w, bg)
    ls = min(4, w)
    out[top][:ls] = [main] * ls
    out[bottom][:ls] = [main] * ls
    out[middle][:2] = [main] * 2
    out[middle][2:4] = [inner] * 2
    start_outer_m = 4
    end_outer_m = min(9, w)
    if start_outer_m < w:
        out[middle][start_outer_m:end_outer_m] = [outer] * (end_outer_m - start_outer_m)
    out[gap][:ls] = [inner] * ls
    if 8 < w:
        out[gap][8] = outer
    if top + 1 == gap:
        if 8 < w:
            out[top][8] = outer
        if 9 < w:
            out[top][9] = outer
    if bottom - 1 == gap:
        if 8 < w:
            out[bottom][8] = outer
        if 9 < w:
            out[bottom][9] = outer
    return out

def apply_unanchored(g: List[List[int]], bg: int, h: int, w: int) -> List[List[int]]:
    out = copy_grid(g)
    comps = find_components(g, bg)
    movables = [(color, pos) for color, pos in comps if not touches_bottom(pos, h)]
    def get_min_row(pos: List[Tuple[int, int]]) -> int:
        return min(r for r, _ in pos)
    movables.sort(key=lambda x: -get_min_row(x[1]))
    for color, pos in movables:
        target_pos = [(r + 1, c + 6) for r, c in pos]
        if any(tr >= h or tc >= w or tr < 0 or tc < 0 for tr, tc in target_pos):
            continue
        if any(out[tr][tc] != bg for tr, tc in target_pos):
            continue
        for r, c in pos:
            out[r][c] = bg
        for tr, tc in target_pos:
            out[tr][tc] = color
    return out

def program(g: List[List[int]]) -> List[List[int]]:
    if not g:
        return []
    bg = get_background(g)
    h = len(g)
    w = len(g[0]) if h > 0 else 0
    if h == 0 or w == 0:
        return g
    is_anchored = any(row[0] != bg for row in g)
    if is_anchored:
        return apply_anchored(g, bg, h, w)
    else:
        return apply_unanchored(g, bg, h, w)
```