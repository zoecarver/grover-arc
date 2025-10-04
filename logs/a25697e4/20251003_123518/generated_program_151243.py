```python
from typing import List, Tuple
from collections import Counter

def detect_background(g: List[List[int]]) -> int:
    flat = [cell for row in g for cell in row]
    if not flat:
        return 0
    return Counter(flat).most_common(1)[0][0]

def detect_anchoring(g: List[List[int]], bg: int) -> bool:
    return any(row and row[0] != bg for row in g)

def extract_components(g: List[List[int]], bg: int) -> List[Tuple[int, List[Tuple[int, int]]]]:
    h = len(g)
    if h == 0:
        return []
    w = len(g[0])
    if w == 0:
        return []
    visited = [[False] * w for _ in range(h)]
    components = []
    directions: List[Tuple[int, int]] = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for i in range(h):
        for j in range(w):
            if not visited[i][j] and g[i][j] != bg:
                color = g[i][j]
                component: List[Tuple[int, int]] = []
                stack: List[Tuple[int, int]] = [(i, j)]
                visited[i][j] = True
                while stack:
                    x, y = stack.pop()
                    component.append((x, y))
                    for dx, dy in directions:
                        nx = x + dx
                        ny = y + dy
                        if 0 <= nx < h and 0 <= ny < w and not visited[nx][ny] and g[nx][ny] == color:
                            visited[nx][ny] = True
                            stack.append((nx, ny))
                components.append((color, component))
    return components

def touches_left(positions: List[Tuple[int, int]]) -> bool:
    return any(c == 0 for _, c in positions)

def touches_bottom(positions: List[Tuple[int, int]], h: int) -> bool:
    return any(r == h - 1 for r, _ in positions)

def compute_min_row(positions: List[Tuple[int, int]]) -> int:
    return min(r for r, _ in positions)

def build_background_grid(h: int, w: int, bg: int) -> List[List[int]]:
    return [[bg] * w for _ in range(h)]

def place_component(grid: List[List[int]], color: int, positions: List[Tuple[int, int]]) -> None:
    h = len(grid)
    if h == 0:
        return
    w = len(grid[0])
    for r, c in positions:
        if 0 <= r < h and 0 <= c < w:
            grid[r][c] = color

def get_min_row_for_color(g: List[List[int]], color: int, h: int, w: int) -> int:
    for r in range(h):
        for c in range(w):
            if g[r][c] == color:
                return r
    return float('inf')

def compute_left_counts(g: List[List[int]], main_color: int, h: int, w: int) -> List[int]:
    ls = min(4, w)
    counts = []
    for r in range(h):
        count = 0
        for j in range(ls):
            if g[r][j] == main_color:
                count += 1
        counts.append(count)
    return counts

def identify_structural_rows(counts: List[int], h: int) -> Tuple[int, int, int, int]:
    full = [r for r in range(h) if counts[r] == 4]
    partial = [r for r in range(h) if counts[r] == 2]
    if len(full) != 2 or len(partial) != 1:
        return -1, -1, -1, -1
    top = min(full)
    bottom = max(full)
    if bottom - top != 3:
        return -1, -1, -1, -1
    middle = partial[0]
    if not (top < middle < bottom):
        return -1, -1, -1, -1
    possible_gaps = [r for r in range(top + 1, bottom) if counts[r] == 0 and r != middle]
    if len(possible_gaps) != 1:
        return -1, -1, -1, -1
    return top, middle, possible_gaps[0], bottom

def identify_noise_colors(g: List[List[int]], comps: List[Tuple[int, List[Tuple[int, int]]]], bg: int, main_color: int, h: int, w: int) -> Tuple[int, int]:
    noise_clrs = {clr for clr, pos in comps if clr != bg and clr != main_color and not touches_left(pos)}
    if len(noise_clrs) != 2:
        return None, None
    min_rows = {clr: get_min_row_for_color(g, clr, h, w) for clr in noise_clrs}
    sorted_clrs = sorted(noise_clrs, key=lambda clr: min_rows[clr])
    return sorted_clrs[0], sorted_clrs[1]

def handle_unanchored(g: List[List[int]], bg: int, h: int, w: int) -> List[List[int]]:
    comps = extract_components(g, bg)
    stayers = [(color, positions) for color, positions in comps if touches_bottom(positions, h)]
    movables = [(color, positions, compute_min_row(positions)) for color, positions in comps if not touches_bottom(positions, h)]
    movables.sort(key=lambda x: -x[2])
    out = build_background_grid(h, w, bg)
    for color, positions in stayers:
        place_component(out, color, positions)
    for color, positions, _ in movables:
        target_positions = [(r + 1, c + 6) for r, c in positions]
        if all(0 <= tr < h and 0 <= tc < w for tr, tc in target_positions) and all(out[tr][tc] == bg for tr, tc in target_positions):
            place_component(out, color, target_positions)
        else:
            place_component(out, color, positions)
    return out

def handle_anchored(g: List[List[int]], bg: int, h: int, w: int) -> List[List[int]]:
    comps = extract_components(g, bg)
    anchored_comps = [(color, positions) for color, positions in comps if touches_left(positions)]
    main_candidates = {color for color, _ in anchored_comps}
    if len(main_candidates) != 1:
        out = build_background_grid(h, w, bg)
        for color, positions in anchored_comps:
            place_component(out, color, positions)
        return out
    main_color = next(iter(main_candidates))
    anchored_subs = [positions for color, positions in anchored_comps]
    if len(anchored_subs) != 2:
        out = build_background_grid(h, w, bg)
        for positions in anchored_subs:
            place_component(out, main_color, positions)
        return out
    upper_noise, lower_noise = identify_noise_colors(g, comps, bg, main_color, h, w)
    if upper_noise is None:
        out = build_background_grid(h, w, bg)
        for positions in anchored_subs:
            place_component(out, main_color, positions)
        return out
    left_counts = compute_left_counts(g, main_color, h, w)
    top, middle, gap, bottom = identify_structural_rows(left_counts, h)
    if top == -1:
        out = build_background_grid(h, w, bg)
        for positions in anchored_subs:
            place_component(out, main_color, positions)
        return out
    inner = upper_noise if gap < middle else lower_noise
    outer = lower_noise if gap < middle else upper_noise
    out = build_background_grid(h, w, bg)
    ls = min(4, w)
    for r in (top, bottom):
        for j in range(ls):
            out[r][j] = main_color
    for j in range(ls):
        if g[middle][j] == main_color:
            out[middle][j] = main_color
    for r in (middle, gap):
        for j in range(ls):
            if out[r][j] == bg:
                out[r][j] = inner
    for j in range(4, min(9, w)):
        out[middle][j] = outer
    if w > 8:
        out[gap][8] = outer
    adj_r = top if gap == top + 1 else (bottom if gap == bottom - 1 else -1)
    if adj_r != -1 and w > 8:
        for j in range(8, min(10, w)):
            out[adj_r][j] = outer
    return out

def program(g: List[List[int]]) -> List[List[int]]:
    if not g:
        return []
    h = len(g)
    w = len(g[0])
    bg = detect_background(g)
    if not detect_anchoring(g, bg):
        return handle_unanchored(g, bg, h, w)
    return handle_anchored(g, bg, h, w)
```