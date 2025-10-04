```python
from typing import List, Tuple

def find_components(g: List[List[int]], color: int) -> List[List[Tuple[int, int]]]:
    if not g or not g[0]:
        return []
    h = len(g)
    w = len(g[0])
    visited = [[False] * w for _ in range(h)]
    components = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for r in range(h):
        for c in range(w):
            if g[r][c] == color and not visited[r][c]:
                comp = []
                stack = [(r, c)]
                visited[r][c] = True
                while stack:
                    x, y = stack.pop()
                    comp.append((x, y))
                    for dx, dy in directions:
                        nx = x + dx
                        ny = y + dy
                        if 0 <= nx < h and 0 <= ny < w and g[nx][ny] == color and not visited[nx][ny]:
                            visited[nx][ny] = True
                            stack.append((nx, ny))
                components.append(comp)
    return components

def get_bbox(comp: List[Tuple[int, int]]) -> Tuple[int, int, int, int, int]:
    if not comp:
        return 0, 0, 0, 0, 0
    rs = [p[0] for p in comp]
    cs = [p[1] for p in comp]
    return min(rs), max(rs), min(cs), max(cs), len(comp)

def has_hole(g: List[List[int]], comp: List[Tuple[int, int]]) -> int:
    # Simple hole detection: if bbox area > pixel count, assume hole count = bbox area - pixels (approximate)
    minr, maxr, minc, maxc, size = get_bbox(comp)
    bbox_area = (maxr - minr + 1) * (maxc - minc + 1)
    return max(0, bbox_area - size)

def identify_main_yellow(yellow_comps: List[List[Tuple[int, int]]], g: List[List[int]]) -> List[Tuple[int, int]]:
    main = None
    max_size = 0
    min_r = len(g)
    min_c = len(g[0])
    for comp in yellow_comps:
        minr, maxr, minc, maxc, size = get_bbox(comp)
        hole = has_hole(g, comp)
        if minr <= 0 and minc <= 0 and hole > 0 and size > max_size:
            main = comp
            max_size = size
            min_r = minr
            min_c = minc
    if main is None:
        main = max(yellow_comps, key=lambda c: get_bbox(c)[4])
    return main

def merge_small_yellows(g: List[List[int]], main_comp: List[Tuple[int, int]], yellow_comps: List[List[Tuple[int, int]]]) -> Tuple[int, int, int, int, int]:
    # Union bbox and total pixels for main yellow after merging small (holes=0, small size)
    minr, maxr, minc, maxc, size = get_bbox(main_comp)
    total_size = size
    for comp in yellow_comps:
        if comp is main_comp:
            continue
        _, _, _, _, s_size = get_bbox(comp)
        hole = has_hole(g, comp)
        if hole == 0 and 2 <= s_size <= 9:
            s_minr, s_maxr, s_minc, s_maxc, _ = get_bbox(comp)
            minr = min(minr, s_minr)
            maxr = max(maxr, s_maxr)
            minc = min(minc, s_minc)
            maxc = max(maxc, s_maxc)
            total_size += s_size
    return minr, maxr, minc, maxc, total_size

def find_dark_reds(g: List[List[int]]) -> List[List[Tuple[int, int]]]:
    return find_components(g, 7)

def create_small_blues(g: List[List[int]], dark_reds: List[List[Tuple[int, int]]], main_blue_y: int) -> List[Tuple[int, int, int, int]]:
    small_blues = []
    for dr in dark_reds:
        rs = [p[0] for p in dr]
        cs = [p[1] for p in dr]
        y = min(rs)
        width = max(cs) - min(cs) + 1
        # Place small blue at y close to dr y, width similar, x position central to main
        dy = max(0, y - main_blue_y)
        small_y_start = y + (1 if dy <= 2 else 0)
        small_x_start = min(cs)  # or central
        small_h = 2 if width <= 3 else 3  # approximate from evidence
        small = (small_y_start, small_y_start + small_h - 1, small_x_start, small_x_start + width - 1)
        small_blues.append(small)
    return small_blues

def identify_main_blue(blue_comps: List[List[Tuple[int, int]]]) -> List[Tuple[int, int]]:
    if not blue_comps:
        return []
    return max(blue_comps, key=lambda c: get_bbox(c)[4])

def reconstruct_grid(minr: int, maxr: int, minc: int, maxc: int, g: List[List[int]], yellow_positions: List[Tuple[int, int]], blue_positions: List[Tuple[int, int]], small_blues: List[Tuple[int, int, int, int]]) -> List[List[int]]:
    h_out = maxr - minr + 1
    w_out = maxc - minc + 1
    out = [[4 for _ in range(w_out)] for _ in range(h_out)]  # default yellow for bbox
    # Place yellow
    for r, c in yellow_positions:
        out[r - minr][c - minc] = 4
    # Place main blue, minus small
    blue_set = set(blue_positions)
    for r, c in blue_positions:
        if (r, c) in blue_set:
            out[r - minr][c - minc] = 1
            blue_set.remove((r, c))
    # Place small blues from remaining blue pixels or new
    remaining_blue = list(blue_set)
    for sy_min, sy_max, sx_min, sx_max in small_blues:
        for rr in range(sy_min - minr, sy_max - minr + 1):
            for cc in range(sx_min - minc, sx_max - minc + 1):
                if 0 <= rr < h_out and 0 <= cc < w_out:
                    out[rr][cc] = 1
    # Fill remaining with yellow if needed for total size
    return out

def handle_dark_red_influence(g: List[List[int]], dark_reds: List[List[Tuple[int, int]]]) -> List[List[int]]:
    # Replace 7's with 4's
    h = len(g)
    w = len(g[0])
    new_g = [row[:] for row in g]
    for comp in dark_reds:
        for r, c in comp:
            new_g[r][c] = 4
    # Simple repair: convert adjacent 1's below each dark red to 4's, limited
    for comp in dark_reds:
        rs = [p[0] for p in comp]
        cs = [p[1] for p in comp]
        y = min(rs)
        x_start = min(cs)
        x_end = max(cs)
        # Fill horizontal in y from x_start to x_end +1 if 1
        for x in range(x_start, x_end + 2):
            if x < w and new_g[y][x] == 1:
                new_g[y][x] = 4
        # Fill vertical down from ends for 2 rows
        for dy in range(1, 3):
            ry = y + dy
            if ry < h:
                if x_start < w and new_g[ry][x_start] == 1:
                    new_g[ry][x_start] = 4
                rx_end = x_end + 1
                if rx_end < w and new_g[ry][rx_end] == 1:
                    new_g[ry][rx_end] = 4
        # Fill middle in last row
        ry = y + 3
        if ry < h:
            for x in range(x_start + 1, x_end):
                if x < w and new_g[ry][x] == 1:
                    new_g[ry][x] = 4
    return new_g

def program(g: List[List[int]]) -> List[List[int]]:
    yellow_comps = find_yellow_components(g)
    if not yellow_comps:
        return g
    main_comp = identify_main_yellow(yellow_comps, g)
    minr, maxr, minc, maxc, _ = merge_small_yellows(g, main_comp, yellow_comps)
    # Crop to merged bbox
    h = len(g)
    w = len(g[0])
    cropped = [[g[r][c] for c in range(minc, maxc + 1)] for r in range(minr, maxr + 1)]
    # Handle dark reds
    dark_reds = find_dark_reds(g)
    repaired = handle_dark_red_influence(cropped, dark_reds)
    # Find main blue in repaired
    blue_comps = find_components(repaired, 1)
    main_blue = identify_main_blue(blue_comps)
    main_blue_y = get_bbox(main_blue)[0] if main_blue else 0
    small_blues = create_small_blues(g, dark_reds, main_blue_y)
    # Reconstruct with rules
    yellow_pos = [(r - minr, c - minc) for r, c in main_comp if minr <= r <= maxr and minc <= c <= maxc]
    blue_pos = [(r, c) for r, c in main_blue]
    out = reconstruct_grid(0, len(repaired) - 1, 0, len(repaired[0]) - 1, repaired, yellow_pos, blue_pos, small_blues)
    # Trim empty rows/cols if any
    # (assume no empty, as per examples)
    return out

def find_yellow_components(g: List[List[int]]) -> List[List[Tuple[int, int]]]:
    return find_components(g, 4)
```