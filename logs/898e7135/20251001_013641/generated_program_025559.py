```python
from collections import Counter, deque
from typing import List, Tuple

def identify_background(g: List[List[int]]) -> int:
    counts = Counter()
    for row in g:
        for cell in row:
            if cell != 0:
                counts[cell] += 1
    return counts.most_common(1)[0][0] if counts else 0

def flood_fill(g: List[List[int]], sr: int, sc: int, visited: List[List[bool]], color: int) -> List[Tuple[int, int]]:
    rows = len(g)
    cols = len(g[0])
    component = []
    queue = deque([(sr, sc)])
    visited[sr][sc] = True
    component.append((sr, sc))
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    while queue:
        r, c = queue.popleft()
        for dr, dc in directions:
            nr = r + dr
            nc = c + dc
            if 0 <= nr < rows and 0 <= nc < cols and not visited[nr][nc] and g[nr][nc] == color:
                visited[nr][nc] = True
                queue.append((nr, nc))
                component.append((nr, nc))
    return component

def extract_all_main_shapes(g: List[List[int]], bg: int) -> List[Tuple[int, List[Tuple[int, int]]]]:
    rows = len(g)
    if rows == 0:
        return []
    cols = len(g[0])
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

def translate_to_origin(pos: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
    if not pos:
        return []
    min_r = min(r for r, _ in pos)
    min_c = min(c for _, c in pos)
    return [(r - min_r, c - min_c) for r, c in pos]

def get_bounding_box(pos: List[Tuple[int, int]]) -> Tuple[int, int]:
    if not pos:
        return 0, 0
    rs = [r for r, _ in pos]
    cs = [c for _, c in pos]
    return max(rs) - min(rs) + 1, max(cs) - min(cs) + 1

def rotate_90_cw(pos: List[Tuple[int, int]], h: int, w: int) -> List[Tuple[int, int]]:
    return [(c, h - 1 - r) for r, c in pos]

def flip_vertical(pos: List[Tuple[int, int]], h: int) -> List[Tuple[int, int]]:
    return [(h - 1 - r, c) for r, c in pos]

def flip_horizontal(pos: List[Tuple[int, int]], w: int) -> List[Tuple[int, int]]:
    return [(r, w - 1 - c) for r, c in pos]

def normalize_shape(color: int, pos: List[Tuple[int, int]]) -> Tuple[int, List[Tuple[int, int]]]:
    pos = translate_to_origin(pos)
    h, w = get_bounding_box(pos)
    rotations = 0
    if h != w:
        pos = rotate_90_cw(pos, h, w)
        pos = translate_to_origin(pos)
        h, w = get_bounding_box(pos)
        rotations = 1
    half = h // 2
    top_count = sum(1 for r, _ in pos if r < half)
    bottom_count = len(pos) - top_count
    do_vflip = False
    if rotations % 2 == 0:
        if bottom_count >= top_count:
            do_vflip = True
    else:
        if top_count >= bottom_count:
            do_vflip = True
    if do_vflip:
        pos = flip_vertical(pos, h)
        pos = translate_to_origin(pos)
        h, w = get_bounding_box(pos)
    half_r = h // 2
    half_c = w // 2
    bottom_left_count = sum(1 for r, c in pos if r >= half_r and c < half_c)
    bottom_right_count = sum(1 for r, c in pos if r >= half_r and c >= half_c)
    if bottom_right_count > bottom_left_count:
        pos = flip_horizontal(pos, w)
        pos = translate_to_origin(pos)
        h, w = get_bounding_box(pos)
    return color, pos

def calculate_used(row: List[Tuple[int, int, int, int]], gap: int) -> int:
    if not row:
        return 0
    return sum(sh[3] for sh in row) + max(0, len(row) - 1) * gap

def build_rows(shapes: List[Tuple[int, int, int, int]], capacity: int, gap: int) -> List[List[Tuple[int, int, int, int]]]:
    rows = []
    current_row = []
    current_used = 0
    for sh in shapes:
        sh_w = sh[3]
        projected_used = current_used + (gap if current_row else 0) + sh_w
        if projected_used > capacity and current_row:
            rows.append(current_row)
            current_row = [sh]
            current_used = sh_w
        else:
            current_row.append(sh)
            current_used = projected_used
    if current_row:
        rows.append(current_row)
    return rows

def get_all_cells(rows: List[List[Tuple[int, int, int, int]]], row_used_ws: List[int], global_max_w: int, gap: int) -> List[Tuple[int, int, int]]:
    all_cells = []
    current_y = 0
    for idx, row in enumerate(rows):
        used = row_used_ws[idx]
        start_x = global_max_w - used
        x = start_x
        row_max_h = max(sh[2] for sh in row)
        for sh in row:
            color, pos, _, sh_w = sh
            for pr, pc in pos:
                all_cells.append((current_y + pr, x + pc, color))
            x += sh_w + gap
        current_y += row_max_h
    return all_cells

def program(g: List[List[int]]) -> List[List[int]]:
    if not g or not g[0]:
        return [[0]]
    bg = identify_background(g)
    components = extract_all_main_shapes(g, bg)
    if not components:
        return [[bg]]
    normalized_shapes = []
    for color, pos in components:
        ncolor, npos = normalize_shape(color, pos)
        h, w = get_bounding_box(npos)
        normalized_shapes.append((ncolor, npos, h, w))
    max_h = max(sh[2] for sh in normalized_shapes)
    capacity = 2 * max_h
    gap = 2
    rows = build_rows(normalized_shapes, capacity, gap)
    if not rows:
        inner = [[bg]]
    else:
        row_used_ws = [calculate_used(row, gap) for row in rows]
        global_max_w = max(row_used_ws) if row_used_ws else 0
        all_cells = get_all_cells(rows, row_used_ws, global_max_w, gap)
        inner_h = sum(max(sh[2] for sh in row) for row in rows)
        inner_w = global_max_w
        inner = [[bg] * inner_w for _ in range(inner_h)]
        for ar, ac, col in all_cells:
            if 0 <= ar < inner_h and 0 <= ac < inner_w:
                inner[ar][ac] = col
    thickness = 2
    final_h = len(inner) + 2 * thickness
    final_w = len(inner[0]) + 2 * thickness if inner else 1 + 2 * thickness
    final_grid = [[bg] * final_w for _ in range(final_h)]
    ih = len(inner)
    iw = len(inner[0]) if ih > 0 else 0
    for i in range(ih):
        for j in range(iw):
            final_grid[thickness + i][thickness + j] = inner[i][j]
    return final_grid
```