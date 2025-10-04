```python
from typing import List, Dict, Tuple
from collections import defaultdict

def get_background(grid: List[List[int]]) -> int:
    return grid[0][0] if grid else 0

def find_components(grid: List[List[int]], bg: int) -> List[Dict]:
    height = len(grid)
    if height == 0:
        return []
    width = len(grid[0])
    visited = [[False] * width for _ in range(height)]
    components = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for r in range(height):
        for c in range(width):
            if grid[r][c] != bg and not visited[r][c]:
                color = grid[r][c]
                stack = [(r, c)]
                positions = []
                min_r, max_r = r, r
                min_c, max_c = c, c
                while stack:
                    cr, cc = stack.pop()
                    if visited[cr][cc]:
                        continue
                    visited[cr][cc] = True
                    positions.append((cr, cc))
                    min_r = min(min_r, cr)
                    max_r = max(max_r, cr)
                    min_c = min(min_c, cc)
                    max_c = max(max_c, cc)
                    for dr, dc in directions:
                        nr = cr + dr
                        nc = cc + dc
                        if 0 <= nr < height and 0 <= nc < width and not visited[nr][nc] and grid[nr][nc] == color:
                            stack.append((nr, nc))
                size = len(positions)
                components.append({
                    'color': color,
                    'positions': positions,
                    'size': size,
                    'minr': min_r,
                    'maxr': max_r,
                    'minc': min_c,
                    'maxc': max_c
                })
    return components

def process_smalls_and_larges(components: List[Dict], grid: List[List[int]], bg: int) -> List[List[int]]:
    small_pos_by_color: Dict[int, List[Tuple[int, int]]] = defaultdict(list)
    large_by_color: Dict[int, Dict] = {}
    for comp in components:
        c = comp['color']
        if comp['size'] == 25:
            large_by_color[c] = comp
        else:
            small_pos_by_color[c].extend(comp['positions'])
    for c, poss in small_pos_by_color.items():
        for r, cc in poss:
            grid[r][cc] = bg
    for c, large_comp in large_by_color.items():
        if c not in small_pos_by_color or not small_pos_by_color[c]:
            continue
        small_poss = small_pos_by_color[c]
        min_r = min(r for r, _ in small_poss)
        max_r = max(r for r, _ in small_poss)
        min_c = min(cc for _, cc in small_poss)
        max_c = max(cc for _, cc in small_poss)
        h_s = max_r - min_r + 1
        w_s = max_c - min_c + 1
        small_mask = [[False] * w_s for _ in range(h_s)]
        for r, cc in small_poss:
            small_mask[r - min_r][cc - min_c] = True
        l_minr = large_comp['minr']
        l_minc = large_comp['minc']
        temp = [[c] * 5 for _ in range(5)]
        start_r = (5 - h_s) // 2
        start_c = (5 - w_s) // 2
        for i in range(h_s):
            for j in range(w_s):
                if small_mask[i][j]:
                    temp[start_r + i][start_c + j] = bg
        for i in range(5):
            for j in range(5):
                grid[l_minr + i][l_minc + j] = temp[i][j]
    return grid

def get_output_bounds(large_comps: List[Dict]) -> Tuple[int, int, int, int]:
    if not large_comps:
        return 0, 0, 0, 0
    row_ranges = {(comp['minr'], comp['maxr']) for comp in large_comps}
    col_ranges = {(comp['minc'], comp['maxc']) for comp in large_comps}
    same_row = len(row_ranges) == 1
    same_col = len(col_ranges) == 1
    min_start_r = min(comp['minr'] for comp in large_comps)
    max_end_r = max(comp['maxr'] for comp in large_comps)
    min_start_c = min(comp['minc'] for comp in large_comps)
    max_end_c = max(comp['maxc'] for comp in large_comps)
    if same_row:
        r_start = min_start_r - 1
        r_end = max_end_r + 1
    else:
        r_start = 0
        r_end = max_end_r + 1
    if same_col:
        c_start = min_start_c - 1
        c_end = max_end_c + 1
    else:
        c_start = 0
        c_end = max_end_c + 1
    return r_start, r_end, c_start, c_end

def program(g: List[List[int]]) -> List[List[int]]:
    if not g or not g[0]:
        return []
    bg = get_background(g)
    components = find_components(g, bg)
    large_comps = [comp for comp in components if comp['size'] == 25]
    grid_copy = [row[:] for row in g]
    modified_grid = process_smalls_and_larges(components, grid_copy, bg)
    r_start, r_end, c_start, c_end = get_output_bounds(large_comps)
    height = len(g)
    width = len(g[0])
    r_start = max(0, r_start)
    r_end = min(height - 1, r_end)
    c_start = max(0, c_start)
    c_end = min(width - 1, c_end)
    out_h = r_end - r_start + 1
    out_w = c_end - c_start + 1
    out_grid = [[modified_grid[r_start + i][c_start + j] for j in range(out_w)] for i in range(out_h)]
    return out_grid
```