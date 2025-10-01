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

def translate_to_origin(positions: List[Tuple[int, int]]) -> Tuple[List[Tuple[int, int]], int, int]:
    if not positions:
        return [], 0, 0
    min_r = min(r for r, _ in positions)
    min_c = min(c for _, c in positions)
    relative = [(r - min_r, c - min_c) for r, c in positions]
    h = max(r for r, _ in relative) + 1
    w = max(c for _, c in relative) + 1
    return relative, h, w

def rotate_if_tall(positions: List[Tuple[int, int]], h: int, w: int) -> Tuple[List[Tuple[int, int]], int, int]:
    if h <= w:
        return positions, h, w
    new_positions = [(c, h - 1 - r) for r, c in positions]
    new_h = w
    new_w = h
    return new_positions, new_h, new_w

def build_inner_grid(shapes: List[Tuple[int, int, int, List[Tuple[int, int]], int, int]], bg: int) -> List[List[int]]:
    if not shapes:
        return []
    max_h = max(sh[4] for sh in shapes)
    total_w = sum(sh[5] for sh in shapes)
    inner = [[bg] * total_w for _ in range(max_h)]
    curr_x = 0
    for _, _, color, rel_pos, _, w_sh in shapes:
        for rr, cc in rel_pos:
            inner[rr][curr_x + cc] = color
        curr_x += w_sh
    return inner

def add_border(grid: List[List[int]], bg: int) -> List[List[int]]:
    if not grid:
        return [[bg]]
    gh = len(grid)
    gw = len(grid[0]) if gh > 0 else 0
    new_h = gh + 2
    new_w = gw + 2
    new_grid = [[bg] * new_w for _ in range(new_h)]
    for i in range(gh):
        for j in range(gw):
            new_grid[i + 1][j + 1] = grid[i][j]
    return new_grid

def pad_to_square(grid: List[List[int]], bg: int) -> List[List[int]]:
    gh = len(grid)
    gw = len(grid[0]) if gh > 0 else 0
    side = max(gh, gw)
    if gh == 0 or gw == 0:
        return [[bg]]
    if side == gh == gw:
        return [row[:] for row in grid]  # copy
    new_grid = [[bg] * side for _ in range(side)]
    offset_r = (side - gh) // 2
    offset_c = (side - gw) // 2
    for i in range(gh):
        for j in range(gw):
            new_grid[offset_r + i][offset_c + j] = grid[i][j]
    return new_grid

def program(g: List[List[int]]) -> List[List[int]]:
    bg = identify_background(g)
    raw_components = extract_raw_components(g, bg)
    sorted_raw = sorted(raw_components, key=lambda x: (x[0], x[1]))
    shapes = []
    for min_r, min_c, color, positions in sorted_raw:
        relative, h, w = translate_to_origin(positions)
        relative, h, w = rotate_if_tall(relative, h, w)
        shapes.append((min_r, min_c, color, relative, h, w))
    inner = build_inner_grid(shapes, bg)
    bordered = add_border(inner, bg)
    result = pad_to_square(bordered, bg)
    return result
```