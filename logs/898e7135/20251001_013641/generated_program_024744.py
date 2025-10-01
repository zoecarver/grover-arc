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
    while h > w:
        positions = rotate_90_cw(positions, h, w)
        positions = translate_to_origin(positions)
        h, w = get_bounding_box(positions)
    half = h // 2
    top_cells = sum(1 for r, _ in positions if r < half)
    bottom_cells = len(positions) - top_cells
    v_flipped = False
    if bottom_cells >= top_cells:
        positions = flip_vertical(positions, h)
        positions = translate_to_origin(positions)
        h, w = get_bounding_box(positions)
        v_flipped = True
    if v_flipped:
        half_r = h // 2
        half_c = w // 2
        bottom_left = sum(1 for r, c in positions if r >= half_r and c < half_c)
        bottom_total = sum(1 for r, c in positions if r >= half_r)
        bottom_right = bottom_total - bottom_left
        if bottom_right > bottom_left:
            positions = flip_horizontal(positions, w)
            positions = translate_to_origin(positions)
            h, w = get_bounding_box(positions)
    return color, positions

class Shape:
    def __init__(self, color: int, positions: List[Tuple[int, int]], h: int, w: int):
        self.color = color
        self.pos = positions
        self.h = h
        self.w = w

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
    raw_shapes = extract_all_main_shapes(g, bg)
    if not raw_shapes:
        return [[bg]]
    norm_shapes = []
    for color, orig_pos in raw_shapes:
        _, npos = normalize_shape(color, orig_pos)
        nh, nw = get_bounding_box(npos)
        norm_shapes.append(Shape(color, npos, nh, nw))
    if not norm_shapes:
        return [[bg]]
    global_max_h = max(s.h for s in norm_shapes)
    max_row_w = 2 * global_max_h
    gap = 2
    vert_gap = 0
    rows: List[List[Shape]] = []
    i = 0
    n_shapes = len(norm_shapes)
    while i < n_shapes:
        current_row: List[Shape] = []
        curr_span = 0
        j = i
        while j < n_shapes:
            this_shape = norm_shapes[j]
            this_w = this_shape.w
            if not current_row:
                add_span = this_w
            else:
                add_span = curr_span + gap + this_w
            if add_span > max_row_w:
                break
            current_row.append(this_shape)
            curr_span = add_span
            j += 1
        rows.append(current_row)
        i = j
    inner_h = 0
    row_max_hs = []
    for row_s in rows:
        if row_s:
            mh = max(s.h for s in row_s)
        else:
            mh = 0
        row_max_hs.append(mh)
        inner_h += mh
    inner_h += max(0, len(rows) - 1) * vert_gap
    inner_w = max_row_w
    inner_grid = [[bg for _ in range(inner_w)] for _ in range(inner_h)]
    current_y = 0
    prev_end = -gap
    for rid in range(len(rows)):
        row_s = rows[rid]
        if not row_s:
            continue
        row_mh = row_max_hs[rid]
        n = len(row_s)
        sum_w = sum(s.w for s in row_s)
        row_span = sum_w + max(0, n - 1) * gap
        if rid == 0:
            row_start_x = 0
        else:
            row_start_x = prev_end - row_span + 1
        place_x = row_start_x
        for s in row_s:
            for dr, dc in s.pos:
                ir = current_y + dr
                ic = place_x + dc
                if 0 <= ir < inner_h and 0 <= ic < inner_w:
                    inner_grid[ir][ic] = s.color
            place_x += s.w + gap
        prev_end = row_start_x + row_span - 1
        current_y += row_mh + vert_gap
    return add_border(inner_grid, 2, bg)
```