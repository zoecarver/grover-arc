```python
import copy
import math
from collections import Counter, deque
from typing import List, Tuple, Dict, Any

def find_components(grid: List[List[int]], target_color: int) -> List[Dict[str, Any]]:
    rows = len(grid)
    cols = len(grid[0])
    visited = [[False] * cols for _ in range(rows)]
    components = []
    dirs: List[Tuple[int, int]] = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == target_color and not visited[i][j]:
                component = []
                queue = deque([(i, j)])
                visited[i][j] = True
                while queue:
                    x, y = queue.popleft()
                    component.append((x, y))
                    for dx, dy in dirs:
                        nx = x + dx
                        ny = y + dy
                        if 0 <= nx < rows and 0 <= ny < cols and not visited[nx][ny] and grid[nx][ny] == target_color:
                            visited[nx][ny] = True
                            queue.append((nx, ny))
                if component:
                    min_r = min(r for r, c in component)
                    max_r = max(r for r, c in component)
                    min_c = min(c for r, c in component)
                    max_c = max(c for r, c in component)
                    components.append({
                        'pixels': component,
                        'bbox': (min_r, max_r, min_c, max_c),
                        'size': len(component)
                    })
    return components

def get_background_color(grid: List[List[int]]) -> int:
    flat = [cell for row in grid for cell in row]
    counter = Counter(flat)
    return counter.most_common(1)[0][0]

def get_shape_color(grid: List[List[int]], bg_color: int, red_color: int) -> int:
    flat = [cell for row in grid for cell in row]
    counter = Counter(flat)
    possible = [c for c in counter if c != bg_color and c != red_color and counter[c] > 0]
    return max(possible, key=lambda c: counter[c]) if possible else 0

def select_shapes(shape_comps: List[Dict[str, Any]]) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    shape_comps.sort(key=lambda x: x['size'], reverse=True)
    shapes = shape_comps[:2]
    shapes.sort(key=lambda x: (x['bbox'][0], x['bbox'][2]))
    return shapes[0], shapes[1] if len(shapes) == 2 else None

def find_aligned_comp_for_first(red_comps: List[Dict[str, Any]], row_c: int, col_c: int) -> Dict[str, Any]:
    for comp in red_comps:
        min_r, max_r, min_c, max_c = comp['bbox']
        if (min_c <= col_c <= max_c) or (min_r <= row_c <= max_r):
            return comp
    return None

def vertical_center_move(grid_copy: List[List[int]], comp: Dict[str, Any], row_c: int, shape_color: int, g: List[List[int]]) -> None:
    min_r, max_r, min_c, max_c = comp['bbox']
    h = max_r - min_r + 1
    target_min_r = row_c - ((h - 1) // 2)
    shift = target_min_r - min_r
    col_set = set(c for r, c in comp['pixels'])
    # set new
    for r, c in comp['pixels']:
        new_r = r + shift
        grid_copy[new_r][c] = 2
    # clear old
    for r, c in comp['pixels']:
        grid_copy[r][c] = 0
    # path
    if shift != 0:
        if shift > 0:
            path_start = max_r + 1
            path_end = (min_r + shift) - 1
        else:
            path_start = (max_r + shift) + 1
            path_end = min_r - 1
        rows_len = len(grid_copy)
        for rr in range(path_start, path_end + 1):
            if 0 <= rr < rows_len:
                for c in col_set:
                    grid_copy[rr][c] = 0
    # gap fill for up move (assume common case)
    if shift < 0:
        for c in col_set:
            shape_rs = [rr for rr in range(len(g)) if g[rr][c] == shape_color]
            if shape_rs:
                max_sr = max(shape_rs)
                min_new_for_c = min(r + shift for rr, cc in comp['pixels'] if cc == c)
                for rr in range(max_sr + 1, min_new_for_c):
                    grid_copy[rr][c] = shape_color

def horizontal_center_move(grid_copy: List[List[int]], comp: Dict[str, Any], col_c: int, shape_color: int, g: List[List[int]]) -> None:
    min_r, max_r, min_c, max_c = comp['bbox']
    w = max_c - min_c + 1
    target_min_c = col_c - ((w - 1) // 2)
    shift = target_min_c - min_c
    row_set = set(r for r, c in comp['pixels'])
    # assume single row for simplicity
    same_r = min_r  # assume
    # set new
    for r, c in comp['pixels']:
        new_c = c + shift
        grid_copy[r][new_c] = 2
    # clear old
    for r, c in comp['pixels']:
        grid_copy[r][c] = 0
    # path
    if shift != 0:
        if shift > 0:
            path_start = max_c + 1
            path_end = (min_c + shift) - 1
        else:
            path_start = (max_c + shift) + 1
            path_end = min_c - 1
        cols_len = len(grid_copy[0])
        for cc in range(path_start, path_end + 1):
            if 0 <= cc < cols_len:
                grid_copy[same_r][cc] = 0
    # gap fill for left move
    if shift < 0:
        shape_cs = [cc for cc in range(len(g[0])) if g[same_r][cc] == shape_color]
        if shape_cs:
            max_sc = max(shape_cs)
            min_new_for_r = min(c + shift for rr, c in comp['pixels'] if rr == same_r)
            for cc in range(max_sc + 1, min_new_for_r):
                grid_copy[same_r][cc] = shape_color

def handle_first_shape_move(grid_copy: List[List[int]], shape1: Dict[str, Any], red_comps: List[Dict[str, Any]], shape_color: int, g: List[List[int]]) -> None:
    min_r1, max_r1, min_c1, max_c1 = shape1['bbox']
    row_c1 = math.ceil((min_r1 + max_r1) / 2)
    col_c1 = math.ceil((min_c1 + max_c1) / 2)
    aligned_comp = find_aligned_comp_for_first(red_comps, row_c1, col_c1)
    if aligned_comp:
        min_cr, max_cr, min_cc, max_cc = aligned_comp['bbox']
        if min_cc <= col_c1 <= max_cc:
            vertical_center_move(grid_copy, aligned_comp, row_c1, shape_color, g)
        elif min_cr <= row_c1 <= max_cr:
            horizontal_center_move(grid_copy, aligned_comp, col_c1, shape_color, g)

def adjacent_vertical_move(grid_copy: List[List[int]], comp: Dict[str, Any], shape_min_r: int, shape_max_r: int, shape_color: int, g: List[List[int]]) -> None:
    min_cr, max_cr, min_cc, max_cc = comp['bbox']
    h = max_cr - min_cr + 1
    col_set = set(c for r, c in comp['pixels'])
    if max_cr < shape_min_r:  # above, move down
        min_shape_per_col = {}
        for c in col_set:
            shape_rs = [r for r in range(len(g)) if g[r][c] == shape_color]
            min_shape_per_col[c] = min(shape_rs) if shape_rs else len(g)
        placement_max_r = min(min_shape_per_col[c] for c in col_set) - 1
        placement_min_r = placement_max_r - h + 1
        shift = placement_min_r - min_cr
    else:  # below, move up
        max_shape_per_col = {}
        for c in col_set:
            shape_rs = [r for r in range(len(g)) if g[r][c] == shape_color]
            max_shape_per_col[c] = max(shape_rs) if shape_rs else -1
        placement_min_r = max(max_shape_per_col[c] for c in col_set) + 1
        shift = placement_min_r - min_cr
    # set new
    for r, c in comp['pixels']:
        new_r = r + shift
        grid_copy[new_r][c] = 2
    # clear old
    for r, c in comp['pixels']:
        grid_copy[r][c] = 0
    # path
    if shift != 0:
        if shift > 0:
            path_start = max_cr + 1
            path_end = (min_cr + shift) - 1
        else:
            path_start = (max_cr + shift) + 1
            path_end = min_cr - 1
        rows_len = len(grid_copy)
        for rr in range(path_start, path_end + 1):
            if 0 <= rr < rows_len:
                for c in col_set:
                    grid_copy[rr][c] = 0

def handle_second_shape_move(grid_copy: List[List[int]], shape2: Dict[str, Any], red_comps: List[Dict[str, Any]], shape_color: int, g: List[List[int]]) -> None:
    if not shape2:
        return
    min_r2, max_r2, min_c2, max_c2 = shape2['bbox']
    col_c2 = math.ceil((min_c2 + max_c2) / 2)
    for comp in red_comps:
        min_cr, max_cr, min_cc, max_cc = comp['bbox']
        if min_cc <= col_c2 <= max_cc and (max_cr < min_r2 or min_cr > max_r2):
            adjacent_vertical_move(grid_copy, comp, min_r2, max_r2, shape_color, g)
            break  # assume one

def handle_removed_reds(grid_copy: List[List[int]], red_comps: List[Dict[str, Any]], moved_comps: List[Dict[str, Any]], bg_color: int) -> None:
    moved_pixels = set((r, c) for comp in moved_comps for r, c in comp['pixels'])
    all_red_pixels = set((r, c) for comp in red_comps for r, c in comp['pixels'])
    removed_pixels = all_red_pixels - moved_pixels
    for r, c in removed_pixels:
        grid_copy[r][c] = bg_color

def program(g: List[List[int]]) -> List[List[int]]:
    bg_color = get_background_color(g)
    red_color = 2
    shape_color = get_shape_color(g, bg_color, red_color)
    shape_comps = find_components(g, shape_color)
    shape1, shape2 = select_shapes(shape_comps)
    red_comps = find_components(g, red_color)
    grid_copy = [row[:] for row in g]
    aligned_for_first = find_aligned_comp_for_first(red_comps, 0, 0)  # placeholder, actual in handle
    moved_comps = []
    if shape1:
        handle_first_shape_move(grid_copy, shape1, red_comps, shape_color, g)
        min_r1, max_r1, min_c1, max_c1 = shape1['bbox']
        row_c1 = math.ceil((min_r1 + max_r1) / 2)
        col_c1 = math.ceil((min_c1 + max_c1) / 2)
        aligned_comp = find_aligned_comp_for_first(red_comps, row_c1, col_c1)
        if aligned_comp:
            moved_comps.append(aligned_comp)
    if shape2:
        handle_second_shape_move(grid_copy, shape2, red_comps, shape_color, g)
        min_r2, max_r2, min_c2, max_c2 = shape2['bbox']
        col_c2 = math.ceil((min_c2 + max_c2) / 2)
        for comp in red_comps:
            min_cr, max_cr, min_cc, max_cc = comp['bbox']
            if min_cc <= col_c2 <= max_cc and (max_cr < min_r2 or min_cr > max_r2):
                moved_comps.append(comp)
                break
    handle_removed_reds(grid_copy, red_comps, moved_comps, bg_color)
    return grid_copy
```