```python
from typing import List, Tuple
from collections import deque, Counter

def identify_background(g: List[List[int]]) -> int:
    counts = Counter()
    for row in g:
        for cell in row:
            if cell != 0:
                counts[cell] += 1
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

def normalize_shape(color: int, positions: List[Tuple[int, int]]) -> Tuple[int, List[Tuple[int, int]], int, int]:
    positions = translate_to_origin(positions)
    h, w = get_bounding_box(positions)
    rotations = 0
    while h > w:
        positions = rotate_90_cw(positions, h, w)
        positions = translate_to_origin(positions)
        h, w = get_bounding_box(positions)
        rotations += 1
    half = h // 2
    top = sum(1 for r, _ in positions if r < half)
    bottom = len(positions) - top
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
    half_r = h // 2
    half_c = w // 2
    bl = sum(1 for r, c in positions if r >= half_r and c < half_c)
    br = sum(1 for r, c in positions if r >= half_r and c >= half_c)
    if br > bl:
        positions = flip_horizontal(positions, w)
        positions = translate_to_origin(positions)
        h, w = get_bounding_box(positions)
    return color, positions, h, w

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
    if not g or not g[0]:
        return [[0]]
    bg = identify_background(g)
    raw_shapes = extract_all_main_shapes(g, bg)
    if not raw_shapes:
        return [[bg]]
    normalized = []
    max_h = 0
    for color, pos in raw_shapes:
        _, npos, nh, nw = normalize_shape(color, pos)
        normalized.append((color, npos, nh, nw))
        max_h = max(max_h, nh)
    cap = 2 * max_h
    gap = 2
    placements = []
    current_y = 0
    current_x = 0
    current_row_h = 0
    current_row_end = -1
    last_row_end = -1
    for color, npos, nh, nw in normalized:
        w = nw
        h = nh
        if current_x + w > cap:
            last_row_end = current_row_end
            current_y += current_row_h
            current_row_h = h
            place_x = 0 if last_row_end < 0 else max(0, last_row_end - w + 1)
            current_row_end = place_x + w - 1
            current_x = place_x + w + gap
        else:
            place_x = current_x
            current_row_h = max(current_row_h, h)
            current_row_end = max(current_row_end, place_x + w - 1)
            current_x += w + gap
        placements.append((current_y, place_x, color, npos))
    total_h = current_y + current_row_h
    total_w = 0
    for y_off, x_off, color, npos in placements:
        _, this_w = get_bounding_box(npos)
        total_w = max(total_w, x_off + this_w)
    if total_h == 0 or total_w == 0:
        return [[bg]]
    inner = [[bg for _ in range(total_w)] for _ in range(total_h)]
    for y_off, x_off, color, npos in placements:
        for r, c in npos:
            inner[y_off + r][x_off + c] = color
    return add_border(inner, 2, bg)
```