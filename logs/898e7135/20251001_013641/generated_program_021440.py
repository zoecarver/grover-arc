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
    # Sort by min row, then min col
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

def count_cells_in_half(positions: List[Tuple[int, int]], h: int, bottom: bool) -> int:
    half = h // 2
    start = half if bottom else 0
    end = h if bottom else half
    return sum(1 for r, _ in positions if start <= r < end)

def is_bottom_heavy(positions: List[Tuple[int, int]], h: int) -> bool:
    top_count = count_cells_in_half(positions, h, False)
    bottom_count = count_cells_in_half(positions, h, True)
    return bottom_count >= top_count

def flip_vertical(positions: List[Tuple[int, int]], h: int) -> List[Tuple[int, int]]:
    return [(h - 1 - r, c) for r, c in positions]

def count_bottom_left_right(positions: List[Tuple[int, int]], h: int, w: int) -> Tuple[int, int]:
    half_h = h // 2
    half_w = w // 2
    bottom_positions = [(r, c) for r, c in positions if r >= half_h]
    left_count = sum(1 for r, c in bottom_positions if c < half_w)
    right_count = len(bottom_positions) - left_count
    return left_count, right_count

def is_bottom_right_heavy(positions: List[Tuple[int, int]], h: int, w: int) -> bool:
    left, right = count_bottom_left_right(positions, h, w)
    return right > left

def flip_horizontal(positions: List[Tuple[int, int]], w: int) -> List[Tuple[int, int]]:
    return [(r, w - 1 - c) for r, c in positions]

def normalize_shape(color: int, positions: List[Tuple[int, int]]) -> Tuple[int, List[Tuple[int, int]]]:
    positions = translate_to_origin(positions)
    h, w = get_bounding_box(positions)
    # Rotate if tall to landscape
    if h > w:
        positions = [(c, h - 1 - r) for r, c in positions]
        h, w = w, h
        positions = translate_to_origin(positions)
    # Flip vertical if bottom heavy (including equal)
    h, w = get_bounding_box(positions)
    if is_bottom_heavy(positions, h):
        positions = flip_vertical(positions, h)
        positions = translate_to_origin(positions)
        h, w = get_bounding_box(positions)
    # Flip horizontal if bottom right heavy
    if is_bottom_right_heavy(positions, h, w):
        positions = flip_horizontal(positions, w)
        positions = translate_to_origin(positions)
    return color, positions

def place_shape(grid: List[List[int]], color: int, positions: List[Tuple[int, int]], offset_r: int, offset_c: int) -> None:
    for r, c in positions:
        if 0 <= offset_r + r < len(grid) and 0 <= offset_c + c < len(grid[0]):
            grid[offset_r + r][offset_c + c] = color

def arrange_shapes_horizontal(shapes: List[Tuple[int, List[Tuple[int, int]]]], bg: int) -> List[List[int]]:
    if not shapes:
        return [[bg]]
    max_h = max(get_bounding_box(pos[1])[0] for pos in shapes)
    total_w = sum(get_bounding_box(pos[1])[1] for pos in shapes) + max(0, len(shapes) - 1)
    inner = [[bg for _ in range(total_w)] for _ in range(max_h)]
    current_c = 0
    for color, positions in shapes:
        place_shape(inner, color, positions, 0, current_c)
        current_c += get_bounding_box(positions)[1] + 1 if current_c > 0 else 0
    return inner

def add_border(grid: List[List[int]], bg: int, border_size: int = 2) -> List[List[int]]:
    if not grid:
        return [[bg]]
    gh, gw = len(grid), len(grid[0])
    new_h = gh + 2 * border_size
    new_w = gw + 2 * border_size
    new_grid = [[bg for _ in range(new_w)] for _ in range(new_h)]
    for i in range(gh):
        for j in range(gw):
            new_grid[i + border_size][j + border_size] = grid[i][j]
    return new_grid

def pad_to_max_dimension(grid: List[List[int]], bg: int) -> List[List[int]]:
    gh = len(grid)
    gw = len(grid[0]) if gh > 0 else 0
    side = max(gh, gw)
    if gh >= side and gw >= side:
        return [row[:] for row in grid]
    new_grid = [[bg for _ in range(side)] for _ in range(side)]
    offset_r = (side - gh) // 2
    offset_c = (side - gw) // 2
    for i in range(gh):
        for j in range(gw):
            new_grid[offset_r + i][offset_c + j] = grid[i][j]
    return new_grid

def program(g: List[List[int]]) -> List[List[int]]:
    bg = identify_background(g)
    raw_shapes = extract_all_main_shapes(g, bg)
    normalized_shapes = [normalize_shape(color, positions) for color, positions in raw_shapes]
    inner = arrange_shapes_horizontal(normalized_shapes, bg)
    bordered = add_border(inner, bg, 1)
    output = pad_to_max_dimension(bordered, bg)
    return output
```