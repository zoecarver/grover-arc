```python
from typing import List, Tuple
from collections import deque, Counter

def program(g: List[List[int]]) -> List[List[int]]:
    def identify_background(grid: List[List[int]]) -> int:
        counts = Counter()
        for row in grid:
            for cell in row:
                if cell != 0:
                    counts[cell] += 1
        return counts.most_common(1)[0][0] if counts else 0

    def flood_fill(grid: List[List[int]], sr: int, sc: int, visited: List[List[bool]], color: int) -> List[Tuple[int, int]]:
        rows, cols = len(grid), len(grid[0])
        queue = deque([(sr, sc)])
        visited[sr][sc] = True
        component = [(sr, sc)]
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        while queue:
            r, c = queue.popleft()
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and not visited[nr][nc] and grid[nr][nc] == color:
                    visited[nr][nc] = True
                    queue.append((nr, nc))
                    component.append((nr, nc))
        return component

    def extract_all_main_shapes(grid: List[List[int]], bg: int) -> List[Tuple[int, List[Tuple[int, int]]]]:
        if not grid or not grid[0]:
            return []
        rows, cols = len(grid), len(grid[0])
        visited = [[False] * cols for _ in range(rows)]
        components = []
        for r in range(rows):
            for c in range(cols):
                if grid[r][c] != 0 and grid[r][c] != bg and not visited[r][c]:
                    color = grid[r][c]
                    comp = flood_fill(grid, r, c, visited, color)
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
        half = h // 2
        top_count = sum(1 for r, _ in positions if r < half)
        bottom_count = len(positions) - top_count
        flip_v = False
        if rotations % 2 == 0:
            if bottom_count >= top_count:
                flip_v = True
        else:
            if top_count >= bottom_count:
                flip_v = True
        if flip_v:
            positions = flip_vertical(positions, h)
            positions = translate_to_origin(positions)
            h, w = get_bounding_box(positions)
        half_r = h // 2
        half_c = w // 2
        bl_count = sum(1 for r, c in positions if r >= half_r and c < half_c)
        br_count = sum(1 for r, c in positions if r >= half_r and c >= half_c)
        if br_count > bl_count:
            positions = flip_horizontal(positions, w)
            positions = translate_to_origin(positions)
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

    bg = identify_background(g)
    components = extract_all_main_shapes(g, bg)
    if not components:
        return [[bg]]
    normalized_shapes = [normalize_shape(color, pos) for color, pos in components]
    # compute max_h
    max_h = max(get_bounding_box(pos)[0] for _, pos in normalized_shapes)
    gap = 2
    v_gap = 0
    cap = 2 * max_h
    rows = []
    i = 0
    n_shapes = len(normalized_shapes)
    while i < n_shapes:
        row = []
        next_start_x = 0
        while i < n_shapes:
            _, pos = normalized_shapes[i]
            _, w_this = get_bounding_box(pos)
            proposed_start = next_start_x
            proposed_end = proposed_start + w_this
            if proposed_end > cap:
                break
            row.append(i)
            next_start_x = proposed_start + w_this + gap
            i += 1
        if row:
            rows.append(row)
    # now compute row_hs and used_ws
    row_hs = []
    used_ws = []
    for row in rows:
        row_h = max(get_bounding_box(normalized_shapes[idx][1])[0] for idx in row)
        row_hs.append(row_h)
        # compute used_w
        temp_start = 0
        used = 0
        for j in range(len(row)):
            idx = row[j]
            _, wj = get_bounding_box(normalized_shapes[idx][1])
            endj = temp_start + wj
            used = max(used, endj)
            if j < len(row) - 1:
                temp_start += wj + gap
        used_ws.append(used)
    max_used = max(used_ws) if used_ws else 0
    total_h = sum(row_hs) + max(0, len(rows) - 1) * v_gap
    inner_w = max_used
    inner = [[bg] * inner_w for _ in range(total_h)]
    curr_y = 0
    for rid in range(len(rows)):
        row = rows[rid]
        used_w = used_ws[rid]
        if len(row) == 1:
            start_x = inner_w - used_w
        else:
            start_x = 0
        place_x = start_x
        for j in range(len(row)):
            idx = row[j]
            color, pos = normalized_shapes[idx]
            sh, sw = get_bounding_box(pos)
            for dr, dc in pos:
                inner[curr_y + dr][place_x + dc] = color
            place_x += sw + gap
        curr_y += row_hs[rid] + v_gap
    result = add_border(inner, 2, bg)
    return result
```