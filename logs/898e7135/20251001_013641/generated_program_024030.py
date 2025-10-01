```python
from typing import List, Tuple
from collections import deque, Counter

def identify_background(g: List[List[int]]) -> int:
    counts = Counter(cell for row in g for cell in row if cell != 0)
    return counts.most_common(1)[0][0] if counts else 0

def flood_fill(g: List[List[int]], sr: int, sc: int, visited: List[List[bool]], color: int) -> List[Tuple[int, int]]:
    rows, cols = len(g), len(g[0])
    queue = deque([(sr, sc)])
    visited[sr][sc] = True
    component = [(sr, sc)]
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    while queue:
        r, c = queue.popleft()
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and not visited[nr][nc] and g[nr][nc] == color:
                visited[nr][nc] = True
                queue.append((nr, nc))
                component.append((nr, nc))
    return component

def extract_all_main_shapes(g: List[List[int]], bg: int) -> List[Tuple[int, List[Tuple[int, int]]]]:
    if not g or not g[0]:
        return []
    rows, cols = len(g), len(g[0])
    visited = [[False] * cols for _ in range(rows)]
    components = []
    for r in range(rows):
        for c in range(cols):
            if g[r][c] != 0 and g[r][c] != bg and not visited[r][c]:
                color = g[r][c]
                comp = flood_fill(g, r, c, visited, color)
                if len(comp) >= 4:
                    components.append((color, comp))
    components.sort(key=lambda x: (min(rr for rr, _ in x[1]), min(cc for _, cc in x[1])))
    return components

def translate_to_origin(positions: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
    if not positions:
        return []
    min_r = min(r for r, _ in positions)
    min_c = min(c for _, c in positions)
    return [(r - min_r, c - min_c) for r, c in positions]

def get_bounding_box(positions: List[Tuple[int, int]]) -> Tuple[int, int]:
    if not positions:
        return 0, 0
    min_r = min(r for r, _ in positions)
    max_r = max(r for r, _ in positions)
    min_c = min(c for _, c in positions)
    max_c = max(c for _, c in positions)
    return max_r - min_r + 1, max_c - min_c + 1

def rotate_90_cw(positions: List[Tuple[int, int]], h: int, w: int) -> List[Tuple[int, int]]:
    return [(c, h - 1 - r) for r, c in positions]

def flip_vertical(positions: List[Tuple[int, int]], h: int) -> List[Tuple[int, int]]:
    return [(h - 1 - r, c) for r, c in positions]

def flip_horizontal(positions: List[Tuple[int, int]], w: int) -> List[Tuple[int, int]]:
    return [(r, w - 1 - c) for r, c in positions]

def normalize_shape(color: int, positions: List[Tuple[int, int]]) -> Tuple[int, List[Tuple[int, int]]]:
    positions = translate_to_origin(positions)
    h, w = get_bounding_box(positions)
    rotations = 0
    while h > w:
        positions = rotate_90_cw(positions, h, w)
        positions = translate_to_origin(positions)
        h, w = get_bounding_box(positions)
        rotations += 1
    def count_top_bottom(hh):
        half = hh // 2
        top = sum(1 for r, _ in positions if r < half)
        bottom = len(positions) - top
        return top, bottom
    top, bottom = count_top_bottom(h)
    flip_v = False
    if rotations % 2 == 0:
        if bottom >= top:
            flip_v = True
    else:
        if top >= bottom:
            flip_v = True
    if flip_v:
        positions = flip_vertical(positions, h)
        positions = translate_to_origin(positions)
        h, w = get_bounding_box(positions)
    def count_bottom_lr(hh, ww):
        half_r = hh // 2
        half_c = ww // 2
        bl = sum(1 for r, c in positions if r >= half_r and c < half_c)
        br = sum(1 for r, c in positions if r >= half_r and c >= half_c)
        return bl, br
    bl, br = count_bottom_lr(h, w)
    if br > bl:
        positions = flip_horizontal(positions, w)
        positions = translate_to_origin(positions)
        h, w = get_bounding_box(positions)
    return color, positions

def add_border(grid: List[List[int]], thickness: int, bg: int) -> List[List[int]]:
    if not grid or not grid[0]:
        return [[bg]]
    gh = len(grid)
    gw = len(grid[0])
    nh = gh + 2 * thickness
    nw = gw + 2 * thickness
    new_grid = [[bg] * nw for _ in range(nh)]
    for i in range(gh):
        for j in range(gw):
            new_grid[thickness + i][thickness + j] = grid[i][j]
    return new_grid

def program(g: List[List[int]]) -> List[List[int]]:
    bg = identify_background(g)
    components = extract_all_main_shapes(g, bg)
    if not components:
        return [[bg]]
    normalized_shapes = []
    max_h = 0
    max_w = 0
    for color, comp in components:
        ncolor, npos = normalize_shape(color, comp)
        nh, nw = get_bounding_box(npos)
        normalized_shapes.append((ncolor, npos, nh, nw))
        max_h = max(max_h, nh)
        max_w = max(max_w, nw)
    if not normalized_shapes:
        return [[bg]]
    max_row_w = max_h + max_w
    gap = 2
    rows = []
    current_row = []
    current_row_h = 0
    current_x = 0
    current_y = 0
    for s in normalized_shapes:
        color, pos, sh, sw = s
        if current_x + sw > max_row_w and len(current_row) > 0:
            rows.append(current_row)
            current_y += current_row_h
            current_row = []
            current_row_h = 0
            current_x = 0
        current_row.append((current_x, color, pos, sh, sw))
        current_row_h = max(current_row_h, sh)
        current_x += sw + gap
    if current_row:
        rows.append(current_row)
    if not rows:
        return [[bg]]
    total_h = current_y + current_row_h
    row_used_ws = []
    for row in rows:
        used_w = max(local_x + sw for local_x, _, _, _, sw in row)
        row_used_ws.append(used_w)
    total_w = max(row_used_ws) if row_used_ws else 0
    if total_h == 0 or total_w == 0:
        total_h = 1
        total_w = 1
    inner_grid = [[bg] * total_w for _ in range(total_h)]
    current_y = 0
    for i, row in enumerate(rows):
        row_used_w = row_used_ws[i]
        shift = total_w - row_used_w
        for local_x, color, pos, sh, sw in row:
            abs_x = shift + local_x
            for dr, dc in pos:
                inner_grid[current_y + dr][abs_x + dc] = color
        current_y += max(sh for _, _, _, sh, _ in row)
    thickness = 2
    output_grid = add_border(inner_grid, thickness, bg)
    return output_grid
```