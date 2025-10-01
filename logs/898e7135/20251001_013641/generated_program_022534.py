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

def rotate_cw(positions: List[Tuple[int, int]], h: int, w: int) -> List[Tuple[int, int]]:
    return [(c, h - 1 - r) for r, c in positions]

def flip_vertical(positions: List[Tuple[int, int]], h: int) -> List[Tuple[int, int]]:
    return [(h - 1 - r, c) for r, c in positions]

def flip_horizontal(positions: List[Tuple[int, int]], w: int) -> List[Tuple[int, int]]:
    return [(r, w - 1 - c) for r, c in positions]

def count_in_region(positions: List[Tuple[int, int]], r_start: int, r_end: int, c_start: int, c_end: int) -> int:
    count = 0
    for r, c in positions:
        if r_start <= r < r_end and c_start <= c < c_end:
            count += 1
    return count

def is_bottom_right_heavy(positions: List[Tuple[int, int]], h: int, w: int) -> bool:
    half_r = h // 2
    half_c = w // 2
    bottom_left = count_in_region(positions, half_r, h, 0, half_c)
    bottom_right = count_in_region(positions, half_r, h, half_c, w)
    return bottom_right > bottom_left

def normalize_shape(color: int, positions: List[Tuple[int, int]]) -> Tuple[int, List[Tuple[int, int]]]:
    positions = translate_to_origin(positions)
    h, w = get_bounding_box(positions)
    if h > w:
        positions = rotate_cw(positions, h, w)
        positions = translate_to_origin(positions)
        h, w = get_bounding_box(positions)
    # Always flip vertical after possible rotation
    positions = flip_vertical(positions, h)
    positions = translate_to_origin(positions)
    h, w = get_bounding_box(positions)
    # Flip horizontal if bottom right heavy
    if is_bottom_right_heavy(positions, h, w):
        positions = flip_horizontal(positions, w)
        positions = translate_to_origin(positions)
    return color, positions

def add_border(grid: List[List[int]], bg: int, thickness: int = 2) -> List[List[int]]:
    if not grid or not grid[0]:
        return [[bg]]
    gh = len(grid)
    gw = len(grid[0])
    new_h = gh + 2 * thickness
    new_w = gw + 2 * thickness
    new_grid = [[bg] * new_w for _ in range(new_h)]
    for i in range(gh):
        for j in range(gw):
            new_grid[i + thickness][j + thickness] = grid[i][j]
    return new_grid

def program(g: List[List[int]]) -> List[List[int]]:
    if not g or not g[0]:
        return [[0]]
    bg = identify_background(g)
    components = extract_all_main_shapes(g, bg)
    if not components:
        return [[bg]]
    normalized_shapes = [normalize_shape(color, comp) for color, comp in components]
    max_h = max(get_bounding_box(pos)[0] for _, pos in normalized_shapes)
    inner_h = max_h
    current_x = 0
    placements = []
    for color, pos in normalized_shapes:
        _, w_s = get_bounding_box(pos)
        place_x = current_x
        placements.append((color, pos, place_x))
        current_x += w_s + 1  # gap of 1
    inner_w = current_x - 1 if placements else 0
    if inner_w == 0:
        inner_grid = [[bg] for _ in range(inner_h)] if inner_h > 0 else []
    else:
        inner_grid = [[bg] * inner_w for _ in range(inner_h)]
        for color, pos, place_x in placements:
            h_s, w_s = get_bounding_box(pos)
            for r, c in pos:
                if r < inner_h and place_x + c < inner_w:
                    inner_grid[r][place_x + c] = color
    output_grid = add_border(inner_grid, bg, 2)
    return output_grid
```