```python
from typing import List, Tuple
from collections import deque, Counter

def identify_background(g: List[List[int]]) -> int:
    counts = Counter()
    for row in g:
        for cell in row:
            if cell != 0:
                counts[cell] += 1
    return max(counts, key=counts.get) if counts else 0

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

def extract_raw_components(g: List[List[int]], bg: int) -> List[Tuple[int, int, int, List[Tuple[int, int]]]]:
    rows = len(g)
    if rows == 0:
        return []
    cols = len(g[0])
    visited = [[False] * cols for _ in range(rows)]
    components = []
    for r in range(rows):
        for c in range(cols):
            if not visited[r][c] and g[r][c] != 0 and g[r][c] != bg:
                color = g[r][c]
                comp = flood_fill(g, r, c, visited, color)
                if len(comp) >= 4:
                    min_r = min(rr for rr, _ in comp)
                    min_c = min(cc for _, cc in comp)
                    components.append((min_r, min_c, color, comp))
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

def is_bottom_heavy(positions: List[Tuple[int, int]], h: int) -> bool:
    if h <= 1:
        return False
    half = h // 2
    top_count = sum(1 for r, _ in positions if r < half)
    bottom_count = len(positions) - top_count
    return bottom_count >= top_count

def flip_vertical(positions: List[Tuple[int, int]], h: int) -> List[Tuple[int, int]]:
    return [(h - 1 - r, c) for r, c in positions]

def is_bottom_right_heavy(positions: List[Tuple[int, int]], h: int, w: int) -> bool:
    if h <= 1 or w <= 1:
        return False
    half_r = h // 2
    half_c = w // 2
    left_count = sum(1 for r, c in positions if r >= half_r and c < half_c)
    right_count = sum(1 for r, c in positions if r >= half_r and c >= half_c)
    return right_count > left_count

def flip_horizontal(positions: List[Tuple[int, int]], w: int) -> List[Tuple[int, int]]:
    return [(r, w - 1 - c) for r, c in positions]

def rotate_90_cw(positions: List[Tuple[int, int]], h: int, w: int) -> List[Tuple[int, int]]:
    return [(c, h - 1 - r) for r, c in positions]

def normalize_shape(color: int, positions: List[Tuple[int, int]]) -> Tuple[int, List[Tuple[int, int]]]:
    positions = translate_to_origin(positions)
    h, w = get_bounding_box(positions)
    rotated = False
    if h > w:
        positions = rotate_90_cw(positions, h, w)
        rotated = True
        positions = translate_to_origin(positions)
        h, w = get_bounding_box(positions)
    do_v_flip = rotated or is_bottom_heavy(positions, h)
    if do_v_flip:
        positions = flip_vertical(positions, h)
        positions = translate_to_origin(positions)
        h, w = get_bounding_box(positions)
    if is_bottom_right_heavy(positions, h, w):
        positions = flip_horizontal(positions, w)
        positions = translate_to_origin(positions)
        h, w = get_bounding_box(positions)
    return color, positions

def arrange_shapes(shapes: List[Tuple[int, List[Tuple[int, int]]]], bg: int) -> List[List[int]]:
    if not shapes:
        return [[bg]]
    max_w = max(get_bounding_box(pos)[1] for _, pos in shapes)
    max_h = max(get_bounding_box(pos)[0] for _, pos in shapes)
    capacity = max_w + max_h
    gap_h = 2
    gap_v = 0
    rows = []
    current_y = 0
    current_row_items = []
    current_row_width = 0
    current_row_height = 0
    for shape in shapes:
        color, pos = shape
        sh, sw = get_bounding_box(pos)
        if current_row_items and current_row_width + gap_h + sw > capacity:
            rows.append((current_y, current_row_height, current_row_width, current_row_items[:]))
            current_y += current_row_height + gap_v
            current_row_items = []
            current_row_width = 0
            current_row_height = 0
        x_start = 0 if not current_row_items else current_row_width + gap_h
        current_row_items.append((x_start, color, pos))
        current_row_width = x_start + sw
        current_row_height = max(current_row_height, sh)
    if current_row_items:
        rows.append((current_y, current_row_height, current_row_width, current_row_items))
    if not rows:
        return [[bg]]
    total_h = max(r[0] + r[1] for r in rows)
    total_w = max(r[2] for r in rows)
    inner = [[bg for _ in range(total_w)] for _ in range(total_h)]
    for row_y, row_h, _, items in rows:
        for x_start, color, pos in items:
            for lr, lc in pos:
                if row_y + lr < total_h and x_start + lc < total_w:
                    inner[row_y + lr][x_start + lc] = color
    return inner

def add_border(grid: List[List[int]], thickness: int, bg: int) -> List[List[int]]:
    if not grid or not grid[0]:
        return [[bg]]
    gh = len(grid)
    gw = len(grid[0])
    nh = gh + 2 * thickness
    nw = gw + 2 * thickness
    new_grid = [[bg for _ in range(nw)] for _ in range(nh)]
    for i in range(gh):
        for j in range(gw):
            new_grid[thickness + i][thickness + j] = grid[i][j]
    return new_grid

def program(g: List[List[int]]) -> List[List[int]]:
    if not g or not g[0]:
        return [[0]]
    bg = identify_background(g)
    raw_comps = extract_raw_components(g, bg)
    raw_comps.sort(key=lambda x: (x[0], x[1]))
    shapes = [normalize_shape(comp[2], comp[3]) for comp in raw_comps]
    inner = arrange_shapes(shapes, bg)
    output = add_border(inner, 2, bg)
    return output
```