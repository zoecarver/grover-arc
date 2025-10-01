```python
from typing import List, Tuple
from collections import deque, Counter

class Shape:
    def __init__(self, color: int, positions: List[Tuple[int, int]], h: int, w: int):
        self.color = color
        self.positions = positions
        self.h = h
        self.w = w

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

def normalize(color: int, positions: List[Tuple[int, int]]) -> Tuple[int, List[Tuple[int, int]], int, int]:
    positions = translate_to_origin(positions)
    h, w = get_bounding_box(positions)
    if h > w:
        positions = rotate_90_cw(positions, h, w)
        positions = translate_to_origin(positions)
        h, w = get_bounding_box(positions)
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

def pack_shapes(shapes: List[Shape], gap: int, cap: int) -> List[List[Shape]]:
    if not shapes:
        return []
    packed = []
    curr_row = []
    curr_used = 0
    for s in shapes:
        sw = s.w
        add_used = sw if not curr_row else gap + sw
        if curr_used + add_used > cap:
            packed.append(curr_row)
            curr_row = [s]
            curr_used = sw
        else:
            curr_row.append(s)
            curr_used += add_used
    if curr_row:
        packed.append(curr_row)
    return packed

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
    components = extract_all_main_shapes(g, bg)
    if not components:
        return [[bg]]
    shapes: List[Shape] = []
    max_hh = 0
    for color, pos in components:
        _, npos, nh, nw = normalize(color, pos)
        shapes.append(Shape(color, npos, nh, nw))
        max_hh = max(max_hh, nh)
    cap = 2 * max_hh
    gap = 2
    packed_rows = pack_shapes(shapes, gap, cap)
    inner_w = 0
    for roww in packed_rows:
        numm = len(roww)
        usedd = sum(s.w for s in roww) + max(0, numm - 1) * gap
        inner_w = max(inner_w, usedd)
    inner_h = sum(max((s.h for s in roww), default=0) for roww in packed_rows)
    if inner_h == 0 or inner_w == 0:
        return [[bg]]
    inner_grid = [[bg] * inner_w for _ in range(inner_h)]
    curr_y = 0
    for roww in packed_rows:
        if not roww:
            continue
        row_hh = max(s.h for s in roww)
        numm = len(roww)
        start_x = 0 if numm > 1 else inner_w - roww[0].w
        x = start_x
        for ii in range(numm):
            s = roww[ii]
            for prr, pcc in s.positions:
                inner_grid[curr_y + prr][x + pcc] = s.color
            x += s.w
            if ii < numm - 1:
                x += gap
        curr_y += row_hh
    return add_border(inner_grid, 2, bg)
```