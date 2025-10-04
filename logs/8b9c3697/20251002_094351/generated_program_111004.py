```python
import copy
from typing import List, Tuple, Dict
from collections import Counter

def get_red_components(g: List[List[int]], h: int, w: int) -> List[Dict]:
    visited = [[False] * w for _ in range(h)]
    components = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for r in range(h):
        for c in range(w):
            if g[r][c] == 2 and not visited[r][c]:
                component = []
                stack = [(r, c)]
                visited[r][c] = True
                min_r, max_r = r, r
                min_c, max_c = c, c
                while stack:
                    cr, cc = stack.pop()
                    component.append((cr, cc))
                    min_r = min(min_r, cr)
                    max_r = max(max_r, cr)
                    min_c = min(min_c, cc)
                    max_c = max(max_c, cc)
                    for dr, dc in directions:
                        nr, nc = cr + dr, cc + dc
                        if 0 <= nr < h and 0 <= nc < w and g[nr][nc] == 2 and not visited[nr][nc]:
                            visited[nr][nc] = True
                            stack.append((nr, nc))
                components.append({
                    'positions': component,
                    'bbox': (min_r, max_r, min_c, max_c),
                    'p': len(component)
                })
    return components

def get_blocky_components(g: List[List[int]], h: int, w: int, bg: int) -> List[Dict]:
    visited = [[False] * w for _ in range(h)]
    components = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for r in range(h):
        for c in range(w):
            if g[r][c] != bg and g[r][c] != 2 and not visited[r][c]:
                color = g[r][c]
                component = []
                stack = [(r, c)]
                visited[r][c] = True
                min_r, max_r = r, r
                min_c, max_c = c, c
                while stack:
                    cr, cc = stack.pop()
                    component.append((cr, cc))
                    min_r = min(min_r, cr)
                    max_r = max(max_r, cr)
                    min_c = min(min_c, cc)
                    max_c = max(max_c, cc)
                    for dr, dc in directions:
                        nr, nc = cr + dr, cc + dc
                        if 0 <= nr < h and 0 <= nc < w and g[nr][nc] == color and not visited[nr][nc]:
                            visited[nr][nc] = True
                            stack.append((nr, nc))
                components.append({
                    'positions': component,
                    'bbox': (min_r, max_r, min_c, max_c),
                    'p': len(component)
                })
    return components

def can_place(g: List[List[int]], minr: int, maxr: int, minc: int, maxc: int, bg: int) -> bool:
    for r in range(minr, maxr + 1):
        for c in range(minc, maxc + 1):
            if g[r][c] != bg:
                return False
    return True

def has_adjacent_blocky(g: List[List[int]], minr: int, maxr: int, minc: int, maxc: int, bg: int, h: int, w: int) -> bool:
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for r in range(minr, maxr + 1):
        for c in range(minc, maxc + 1):
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if 0 <= nr < h and 0 <= nc < w and g[nr][nc] != bg and g[nr][nc] != 2:
                    return True
    return False

def path_ok(g: List[List[int]], clear_min: int, clear_max: int, fixed: int, is_vertical: bool, min_other: int, max_other: int, original_set: set, bg: int) -> bool:
    if is_vertical:
        for r in range(clear_min, clear_max + 1):
            for c in range(min_other, max_other + 1):
                if (r, c) not in original_set and g[r][c] != bg:
                    return False
    else:
        for c in range(clear_min, clear_max + 1):
            r = fixed
            if (r, c) not in original_set and g[r][c] != bg:
                return False
    return True

def program(g: List[List[int]]) -> List[List[int]]:
    if not g or not g[0]:
        return g
    grid = copy.deepcopy(g)
    h = len(grid)
    w = len(grid[0])
    flat = [cell for row in grid for cell in row]
    bg = Counter(flat).most_common(1)[0][0]
    red_comps = get_red_components(grid, h, w)
    blocky_comps = get_blocky_components(grid, h, w, bg)
    for red in red_comps:
        original_positions = set(red['positions'])
        minr, maxr, minc, maxc = red['bbox']
        h_red = maxr - minr + 1
        w_red = maxc - minc + 1
        possible = []
        for b in blocky_comps:
            b_minr, b_maxr, b_minc, b_maxc = b['bbox']
            # vertical
            if minc >= b_minc and maxc <= b_maxc:
                # move up (red below)
                if minr > b_maxr + 1:
                    for new_maxr in range(b_maxr, b_minr + h_red - 2, -1):
                        new_minr = new_maxr - h_red + 1
                        if new_minr < b_minr:
                            break
                        if can_place(grid, new_minr, new_maxr, minc, maxc, bg):
                            clear_minr = new_maxr + 1
                            clear_maxr = maxr
                            if path_ok(grid, clear_minr, clear_maxr, 0, True, minc, maxc, original_positions, bg) and has_adjacent_blocky(grid, new_minr, new_maxr, minc, maxc, bg, h, w):
                                dist = abs(new_minr - minr)
                                possible.append({
                                    'type': 'v_up',
                                    'new_minr': new_minr,
                                    'new_minc': minc,
                                    'dist': dist,
                                    'clear_minr': clear_minr,
                                    'clear_maxr': clear_maxr
                                })
                                break
                # move down (red above)
                if maxr < b_minr - 1:
                    for new_minr in range(b_minr, b_maxr - h_red + 2):
                        new_maxr = new_minr + h_red - 1
                        if new_maxr > b_maxr:
                            break
                        if can_place(grid, new_minr, new_maxr, minc, maxc, bg):
                            clear_minr = minr
                            clear_maxr = new_minr - 1
                            if path_ok(grid, clear_minr, clear_maxr, 0, True, minc, maxc, original_positions, bg) and has_adjacent_blocky(grid, new_minr, new_maxr, minc, maxc, bg, h, w):
                                dist = abs(new_minr - minr)
                                possible.append({
                                    'type': 'v_down',
                                    'new_minr': new_minr,
                                    'new_minc': minc,
                                    'dist': dist,
                                    'clear_minr': clear_minr,
                                    'clear_maxr': clear_maxr
                                })
                                break
            # horizontal (only if h_red == 1)
            if h_red == 1 and minr >= b_minr and maxr <= b_maxr:
                r = minr
                # move right (red left)
                if maxc < b_minc - 1:
                    for new_minc in range(b_minc, b_maxc - w_red + 2):
                        new_maxc = new_minc + w_red - 1
                        if new_maxc > b_maxc:
                            break
                        if can_place(grid, r, r, new_minc, new_maxc, bg):  # can_place works for single row
                            clear_minc = minc
                            clear_maxc = new_minc - 1
                            if path_ok(grid, clear_minc, clear_maxc, r, False, 0, 0, original_positions, bg) and has_adjacent_blocky(grid, r, r, new_minc, new_maxc, bg, h, w):
                                dist = abs(new_minc - minc)
                                possible.append({
                                    'type': 'h_right',
                                    'new_minr': r,
                                    'new_minc': new_minc,
                                    'dist': dist,
                                    'clear_minc': clear_minc,
                                    'clear_maxc': clear_maxc,
                                    'row': r
                                })
                                break
                # move left (red right)
                if minc > b_maxc + 1:
                    for new_maxc in range(b_maxc, b_minc + w_red - 2, -1):
                        new_minc = new_maxc - w_red + 1
                        if new_minc < b_minc:
                            break
                        if can_place(grid, r, r, new_minc, new_maxc, bg):
                            clear_minc = new_maxc + 1
                            clear_maxc = maxc
                            if path_ok(grid, clear_minc, clear_maxc, r, False, 0, 0, original_positions, bg) and has_adjacent_blocky(grid, r, r, new_minc, new_maxc, bg, h, w):
                                dist = abs(new_minc - minc)
                                possible.append({
                                    'type': 'h_left',
                                    'new_minr': r,
                                    'new_minc': new_minc,
                                    'dist': dist,
                                    'clear_minc': clear_minc,
                                    'clear_maxc': clear_maxc,
                                    'row': r
                                })
                                break
        if possible:
            possible.sort(key=lambda x: x['dist'])
            chosen = possible[0]
            new_minr = chosen['new_minr']
            new_maxr = new_minr + h_red - 1
            new_minc = chosen['new_minc']
            new_maxc = new_minc + w_red - 1
            # set target
            for rr in range(new_minr, new_maxr + 1):
                for cc in range(new_minc, new_maxc + 1):
                    grid[rr][cc] = 2
            # clear path
            if chosen['type'] in ['v_up', 'v_down']:
                clear_minr = chosen['clear_minr']
                clear_maxr = chosen['clear_maxr']
                for rr in range(clear_minr, clear_maxr + 1):
                    for cc in range(minc, maxc + 1):
                        grid[rr][cc] = 0
            else:
                r = chosen['row']
                clear_minc = chosen['clear_minc']
                clear_maxc = chosen['clear_maxc']
                for cc in range(clear_minc, clear_maxc + 1):
                    grid[r][cc] = 0
    # now remove remaining small or edge touching reds
    remaining_reds = get_red_components(grid, h, w)
    for red in remaining_reds:
        minr, maxr, minc, maxc = red['bbox']
        touches_edge = (minr == 0 or maxr == h - 1 or minc == 0 or maxc == w - 1)
        if red['p'] <= 2 or touches_edge:
            for pr, pc in red['positions']:
                grid[pr][pc] = bg
    return grid
```