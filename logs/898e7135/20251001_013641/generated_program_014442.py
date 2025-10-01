```python
from typing import List, Tuple
from collections import deque, Counter

def program(g: List[List[int]]) -> List[List[int]]:
    bg = identify_background(g)
    shapes = extract_main_shapes(g, bg)
    normalized_shapes = [normalize_shape(color, positions) for color, positions in shapes]
    canvas = arrange_shapes(normalized_shapes, bg, len(g), len(g[0]) if g else 0)
    return canvas

def identify_background(g: List[List[int]]) -> int:
    counts = Counter()
    for row in g:
        for cell in row:
            if cell != 0:
                counts[cell] += 1
    return max(counts, key=counts.get) if counts else 0

def extract_main_shapes(g: List[List[int]], bg: int) -> List[Tuple[int, List[Tuple[int, int]]]]:
    if not g or not g[0]:
        return []
    rows, cols = len(g), len(g[0])
    visited = [[False] * cols for _ in range(rows)]
    components_by_color = {}
    for r in range(rows):
        for c in range(cols):
            if g[r][c] != 0 and g[r][c] != bg and not visited[r][c]:
                color = g[r][c]
                component = flood_fill(g, r, c, visited, color)
                size = len(component)
                if size >= 4:
                    if color not in components_by_color or size > len(components_by_color[color][1]):
                        components_by_color[color] = (color, component)
    shapes = list(components_by_color.values())
    shapes.sort(key=lambda x: min(pr for pr, pc in x[1]))
    return shapes

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

def normalize_shape(color: int, positions: List[Tuple[int, int]]) -> Tuple[int, List[Tuple[int, int]]]:
    if not positions:
        return color, []
    min_r = min(r for r, c in positions)
    min_c = min(c for r, c in positions)
    max_r = max(r for r, c in positions)
    max_c = max(c for r, c in positions)
    h = max_r - min_r + 1
    w = max_c - min_c + 1
    grid = [[0] * w for _ in range(h)]
    for r, c in positions:
        grid[r - min_r][c - min_c] = color
    if h >= w:
        grid = rotate_90_cw(grid)
        h, w = w, h
    if is_bottom_heavy(grid, h, w):
        grid = flip_vertical(grid)
    min_r_new = min(i for i in range(h) if any(grid[i]))
    min_c_new = min(j for j in range(w) if any(grid[i][j] for i in range(h)))
    new_positions = [(i - min_r_new, j - min_c_new) for i in range(h) for j in range(w) if grid[i][j] == color]
    return color, new_positions

def rotate_90_cw(grid: List[List[int]]) -> List[List[int]]:
    old_h = len(grid)
    if old_h == 0:
        return grid
    old_w = len(grid[0])
    new_grid = [[0] * old_h for _ in range(old_w)]
    for r in range(old_h):
        for c in range(old_w):
            new_grid[c][old_h - 1 - r] = grid[r][c]
    return new_grid

def flip_vertical(grid: List[List[int]]) -> List[List[int]]:
    return [row[:] for row in reversed(grid)]

def is_bottom_heavy(grid: List[List[int]], h: int, w: int) -> bool:
    half = h // 2
    top_count = sum(sum(1 for c in range(w) if grid[r][c] != 0) for r in range(half))
    bottom_count = sum(sum(1 for c in range(w) if grid[r][c] != 0) for r in range(h - half, h))
    return bottom_count > top_count

def arrange_shapes(shapes: List[Tuple[int, List[Tuple[int, int]]]], bg: int, input_rows: int, input_cols: int) -> List[List[int]]:
    if not shapes:
        return [[bg]]
    total_h = 0
    max_w = 0
    for _, pos in shapes:
        sh = max(r for r, c in pos) + 1 if pos else 0
        sw = max(c for r, c in pos) + 1 if pos else 0
        total_h += sh
        max_w = max(max_w, sw)
    inner_side = max(total_h, max_w)
    inner = [[bg] * inner_side for _ in range(inner_side)]
    current_r = 0
    for color, pos in shapes:
        if not pos:
            continue
        offset_r = max(r for r, c in pos) + 1
        offset_c = max(c for r, c in pos) + 1
        for r, c in pos:
            if current_r + r < inner_side and c < inner_side:
                inner[current_r + r][c] = color
        current_r += offset_r
    border = 1
    out_side = inner_side + 2 * border
    out = [[bg] * out_side for _ in range(out_side)]
    for r in range(inner_side):
        for c in range(inner_side):
            out[r + border][c + border] = inner[r][c]
    return out
```