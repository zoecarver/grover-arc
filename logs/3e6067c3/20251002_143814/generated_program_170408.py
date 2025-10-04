```python
from typing import List, Tuple, Dict, Set, DefaultDict
from collections import defaultdict

def find_components(grid: List[List[int]], color: int, rows: int, cols: int) -> List[List[Tuple[int, int]]]:
    visited = [[False] * cols for _ in range(rows)]
    components = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == color and not visited[i][j]:
                comp = []
                stack = [(i, j)]
                visited[i][j] = True
                while stack:
                    x, y = stack.pop()
                    comp.append((x, y))
                    for dx, dy in directions:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < rows and 0 <= ny < cols and grid[nx][ny] == color and not visited[nx][ny]:
                            visited[nx][ny] = True
                            stack.append((nx, ny))
                components.append(comp)
    return components

def find_bottom_isolates(grid: List[List[int]], bg: int, rows: int, cols: int) -> List[Tuple[int, int]]:
    max_isol = 0
    best_isol = []
    best_r = -1
    for r in range(rows):
        isol = []
        for j in range(1, cols - 1):
            if grid[r][j] != bg and grid[r][j - 1] == bg and grid[r][j + 1] == bg:
                isol.append((j, grid[r][j]))
        if len(isol) > max_isol:
            max_isol = len(isol)
            best_isol = isol
            best_r = r
    return best_isol if max_isol >= 3 else []

def get_all_pos(bottom_isol: List[Tuple[int, int]]) -> DefaultDict[int, List[int]]:
    all_pos: DefaultDict[int, List[int]] = defaultdict(list)
    for idx, (_, color) in enumerate(bottom_isol):
        all_pos[color].append(idx + 1)
    return all_pos

def get_chosen_color(c1: int, c2: int, all_pos: DefaultDict[int, List[int]]) -> Tuple[int, int]:
    pos1 = all_pos[c1]
    pos2 = all_pos[c2]
    adjacent = []
    for p1 in pos1:
        for p2 in pos2:
            if abs(p1 - p2) == 1:
                minp = min(p1, p2)
                col_of_min = c1 if p1 == minp else c2
                adjacent.append((minp, col_of_min))
    if not adjacent:
        return None, None
    adjacent.sort(key=lambda x: x[0])
    return adjacent[0][1], adjacent[0][0]  # chosen_c, its minp

def identify_outers(grid: List[List[int]], frame_color: int, bg: int, rows: int, cols: int) -> List[Dict]:
    frame_comps = find_components(grid, frame_color, rows, cols)
    outers = []
    for fcomp in frame_comps:
        rs = [p[0] for p in fcomp]
        cs = [p[1] for p in fcomp]
        min_r, max_r = min(rs), max(rs)
        min_c, max_c = min(cs), max(cs)
        # find inners in bbox
        fset = set(fcomp)
        inners = []
        vis = set(fset)
        for i in range(min_r, max_r + 1):
            for j in range(min_c, max_c + 1):
                if (i, j) not in vis and grid[i][j] != frame_color and grid[i][j] != bg:
                    icolor = grid[i][j]
                    icomp = []
                    stack = [(i, j)]
                    vis.add((i, j))
                    while stack:
                        x, y = stack.pop()
                        icomp.append((x, y))
                        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                            nx, ny = x + dx, y + dy
                            if min_r <= nx <= max_r and min_c <= ny <= max_c and grid[nx][ny] == icolor and (nx, ny) not in vis:
                                vis.add((nx, ny))
                                stack.append((nx, ny))
                    if 1 <= len(icomp) <= 8:
                        inners.append((icolor, icomp))
        if len(inners) == 1:
            icolor, ipos = inners[0]
            colored_rows = {r for r, _ in ipos}
            min_ic = min(c for _, c in ipos)
            max_ic = max(c for _, c in ipos)
            outers.append({
                'bbox': (min_r, max_r, min_c, max_c),
                'inner_color': icolor,
                'inner_pos': ipos,
                'colored_rows': colored_rows,
                'inner_min_c': min_ic,
                'inner_max_c': max_ic
            })
    return outers

def get_pairs(outers: List[Dict], all_pos: DefaultDict[int, List[int]], is_horizontal: bool) -> List[Dict]:
    if is_horizontal:
        sorted_outers = sorted(outers, key=lambda o: o['bbox'][2])
        idx1, idx2, gap_calc = 2, 3, lambda b1, b2: b2[2] - b1[3] - 1
        overlap_check = lambda b1, b2: max(b1[0], b2[0]) <= min(b1[1], b2[1])
        o1_key, o2_key = 'fill_min_c', 'fill_max_c'
        fill_pos = lambda b1, b2: (b1[3] + 1, b2[2] - 1)
        fill_from_o = lambda o: o['colored_rows']
    else:
        sorted_outers = sorted(outers, key=lambda o: o['bbox'][0])
        idx1, idx2, gap_calc = 0, 1, lambda b1, b2: b2[0] - b1[1] - 1
        overlap_check = lambda b1, b2: max(b1[2], b2[2]) <= min(b1[3], b2[3])
        o1_key, o2_key = 'fill_min_r', 'fill_max_r'
        fill_pos = lambda b1, b2: (b1[1] + 1, b2[0] - 1)
        fill_from_o = lambda o: range(o['inner_min_c'], o['inner_max_c'] + 1)
    pairs = []
    for i in range(len(sorted_outers) - 1):
        o1 = sorted_outers[i]
        o2 = sorted_outers[i + 1]
        b1 = o1['bbox']
        b2 = o2['bbox']
        if not overlap_check(b1, b2):
            continue
        gap = gap_calc(b1, b2)
        if 0 < gap < 4:
            c1 = o1['inner_color']
            c2 = o2['inner_color']
            chosen_c, _ = get_chosen_color(c1, c2, all_pos)
            if chosen_c is not None:
                chosen_o = o1 if chosen_c == c1 else o2
                f_min, f_max = fill_pos(b1, b2)
                pair = {'type': 'horizontal' if is_horizontal else 'vertical', 'color': chosen_c}
                pair[o1_key] = f_min
                pair[o2_key] = f_max
                if is_horizontal:
                    pair['fill_rows'] = sorted(o1['colored_rows'] | o2['colored_rows'])
                else:
                    pair['fill_cols'] = list(fill_from_o(chosen_o))
                pairs.append(pair)
    return pairs

def apply_fills(grid: List[List[int]], pairs: List[Dict], bg: int, rows: int, cols: int) -> List[List[int]]:
    out_grid = [row[:] for row in grid]
    for pair in pairs:
        color = pair['color']
        typ = pair['type']
        if typ == 'horizontal':
            f_min_c = pair['fill_min_c']
            f_max_c = pair['fill_max_c']
            for r in pair['fill_rows']:
                for c in range(f_min_c, f_max_c + 1):
                    if out_grid[r][c] == bg:
                        out_grid[r][c] = color
        else:
            f_min_r = pair['fill_min_r']
            f_max_r = pair['fill_max_r']
            for r in range(f_min_r, f_max_r + 1):
                for c in pair['fill_cols']:
                    if 0 <= c < cols and out_grid[r][c] == bg:
                        out_grid[r][c] = color
    return out_grid

def program(g: List[List[int]]) -> List[List[int]]:
    if not g or not g[0]:
        return g
    rows = len(g)
    cols = len(g[0])
    bg = g[0][0]
    # find frame_color
    cell_set = set()
    for row in g:
        for val in row:
            cell_set.add(val)
    possible_cs = [c for c in range(1, 10) if c != bg and c in cell_set]
    frame_color = None
    max_num_medium = 0
    for c in possible_cs:
        comps = find_components(g, c, rows, cols)
        num_medium = sum(1 for comp in comps if 5 < len(comp) < 50)
        if num_medium > max_num_medium:
            max_num_medium = num_medium
            frame_color = c
    if frame_color is None:
        return g
    # find bottom isolates
    bottom_isol = find_bottom_isolates(g, bg, rows, cols)
    all_pos = get_all_pos(bottom_isol)
    # identify outers
    outers = identify_outers(g, frame_color, bg, rows, cols)
    # get pairs
    h_pairs = get_pairs(outers, all_pos, True)
    v_pairs = get_pairs(outers, all_pos, False)
    all_pairs = h_pairs + v_pairs
    # apply
    return apply_fills(g, all_pairs, bg, rows, cols)
```