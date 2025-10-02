```python
from collections import defaultdict
from typing import List, Tuple, Dict, Set
import copy
import math

def get_neighbors8(r: int, c: int, rows: int, cols: int) -> List[Tuple[int, int]]:
    dirs = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    return [(r + dr, c + dc) for dr, dc in dirs if 0 <= r + dr < rows and 0 <= c + dc < cols]

def find_components(g: List[List[int]], rows: int, cols: int) -> Dict[int, List[List[Tuple[int, int]]]]:
    visited = [[False] * cols for _ in range(rows)]
    components: Dict[int, List[List[Tuple[int, int]]]] = defaultdict(list)
    for r in range(rows):
        for c in range(cols):
            if g[r][c] != 0 and not visited[r][c]:
                color = g[r][c]
                component: List[Tuple[int, int]] = []
                stack: List[Tuple[int, int]] = [(r, c)]
                visited[r][c] = True
                while stack:
                    cr, cc = stack.pop()
                    component.append((cr, cc))
                    for nr, nc in get_neighbors8(cr, cc, rows, cols):
                        if g[nr][nc] == color and not visited[nr][nc]:
                            visited[nr][nc] = True
                            stack.append((nr, nc))
                components[color].append(component)
    return components

def touches_border(comp: List[Tuple[int, int]], rows: int, cols: int) -> bool:
    return any(r == 0 or r == rows - 1 or c == 0 or c == cols - 1 for r, c in comp)

def is_large_component(comp: List[Tuple[int, int]], rows: int, cols: int) -> bool:
    return len(comp) >= 8 or touches_border(comp, rows, cols)

def compute_min_max(pos: List[Tuple[int, int]]) -> Tuple[int, int, int, int]:
    if not pos:
        return 0, 0, 0, 0
    rs = [r for r, _ in pos]
    cs = [c for _, c in pos]
    return min(rs), max(rs), min(cs), max(cs)

def compute_average_row(pos: List[Tuple[int, int]]) -> float:
    n = len(pos)
    if n == 0:
        return 0.0
    return sum(r for r, _ in pos) / n

def compute_average_col(pos: List[Tuple[int, int]]) -> float:
    n = len(pos)
    if n == 0:
        return 0.0
    return sum(c for _, c in pos) / n

def get_union_positions(comps: List[List[Tuple[int, int]]]) -> List[Tuple[int, int]]:
    seen = set()
    union = []
    for pos_list in comps:
        for p in pos_list:
            tp = (p[0], p[1])
            if tp not in seen:
                seen.add(tp)
                union.append(p)
    return union

def get_large_positions(components: Dict[int, List[List[Tuple[int, int]]]], color: int, rows: int, cols: int) -> List[Tuple[int, int]]:
    pos = []
    for comp in components.get(color, []):
        if is_large_component(comp, rows, cols):
            pos.extend(comp)
    return pos

def identify_movable_smalls(components: Dict[int, List[List[Tuple[int, int]]]], g: List[List[int]], rows: int, cols: int) -> List[Tuple[int, List[Tuple[int, int]]]]:
    large_cells = [[False] * cols for _ in range(rows)]
    for color, comps in components.items():
        for comp in comps:
            if is_large_component(comp, rows, cols):
                for r, c in comp:
                    large_cells[r][c] = True
    movables = []
    for color, comps in components.items():
        for comp in comps:
            if is_large_component(comp, rows, cols):
                continue
            is_movable = False
            for r, c in comp:
                for nr, nc in get_neighbors8(r, c, rows, cols):
                    d_color = g[nr][nc]
                    if d_color != 0 and d_color != color and large_cells[nr][nc]:
                        is_movable = True
                        break
                if is_movable:
                    break
            if is_movable:
                movables.append((color, comp))
    return movables

def compute_best_anchors(movables: List[Tuple[int, List[Tuple[int, int]]]], g: List[List[int]], large_cells: List[List[bool]], rows: int, cols: int) -> Dict[Tuple[int, int], List[List[Tuple[int, int]]]]:
    groups: Dict[Tuple[int, int], List[List[Tuple[int, int]]]] = defaultdict(list)
    for color, comp in movables:
        adj_counts: Dict[int, int] = defaultdict(int)
        for r, c in comp:
            for nr, nc in get_neighbors8(r, c, rows, cols):
                d_color = g[nr][nc]
                if d_color != 0 and d_color != color and large_cells[nr][nc]:
                    adj_counts[d_color] += 1
        if adj_counts:
            best_a = max(adj_counts, key=lambda d: (adj_counts[d], -d))
            groups[(best_a, color)].append(comp)
    return groups

def is_horizontally_embedded(u_pos: List[Tuple[int, int]], anchor_color: int, g: List[List[int]]) -> bool:
    has_left = False
    has_right = False
    for r, c in u_pos:
        if c > 0 and g[r][c - 1] == anchor_color:
            has_left = True
        if c < len(g[0]) - 1 and g[r][c + 1] == anchor_color:
            has_right = True
        if has_left and has_right:
            return True
    return False

def try_horizontal_placement(new_g: List[List[int]], u_pos: List[Tuple[int, int]], a_pos: List[Tuple[int, int]], color: int, rows: int, cols: int, avg_r: float, avg_c: float, a_avg_c: float) -> bool:
    min_r_u, max_r_u, min_c_u, max_c_u = compute_min_max(u_pos)
    col_s = max_c_u - min_c_u + 1
    a_min_c, a_max_c, _, _ = compute_min_max(a_pos)
    opposite_right = avg_c < a_avg_c
    if opposite_right:
        edge_c = a_max_c
        start_c = edge_c + 1
        adj_c = a_max_c
    else:
        edge_c = a_min_c
        start_c = edge_c - col_s
        adj_c = a_min_c
    cand_rows = set(r for r, c in a_pos if c == adj_c)
    cand_rows = sorted(cand_rows, key=lambda rr: abs(rr - avg_r))
    for pr in cand_rows:
        valid = True
        pls = []
        for i in range(col_s):
            pc = start_c + i
            if not (0 <= pc < cols) or new_g[pr][pc] != 0:
                valid = False
                break
            pls.append((pr, pc))
        if valid:
            for ppr, ppc in pls:
                new_g[ppr][ppc] = color
            return True
    return False

def try_vertical_placement(new_g: List[List[int]], u_pos: List[Tuple[int, int]], a_pos: List[Tuple[int, int]], color: int, rows: int, cols: int, avg_r: float, avg_c: float, a_avg_r: float, vertical_max_span: Dict[int, int]) -> bool:
    min_r_u, max_r_u, _, _ = compute_min_max(u_pos)
    row_s = max_r_u - min_r_u + 1
    a_min_r, a_max_r, _, _ = compute_min_max(a_pos)
    opposite_above = avg_r > a_avg_r
    if opposite_above:
        edge_r = a_min_r
        start_r = edge_r - row_s
        adj_r = a_min_r
    else:
        edge_r = a_max_r
        start_r = edge_r + 1
        adj_r = a_max_r
    cand_cols = set(c for r, c in a_pos if r == adj_r)
    cand_cols = sorted(cand_cols, key=lambda cc: abs(cc - avg_c))
    for pc in cand_cols:
        valid = True
        pls = []
        for i in range(row_s):
            pr = start_r + i
            if not (0 <= pr < rows) or new_g[pr][pc] != 0:
                valid = False
                break
            pls.append((pr, pc))
        if valid:
            for ppr, ppc in pls:
                new_g[ppr][ppc] = color
            bottom_pr = max(pr for pr, _ in pls)
            vertical_max_span[color] = max(vertical_max_span.get(color, 0), row_s)
            return True
    return False

def place_banner_groups(new_g: List[List[int]], banner_groups: Dict[int, List[Tuple[int, float, int, int]]], vertical_max_span: Dict[int, int], rows: int, cols: int) -> None:
    for c, bgs in banner_groups.items():
        max_vs = vertical_max_span.get(c, 0)
        banner_row = max_vs - 1 if max_vs > 0 else 0
        for row_s, col_s, avg_c, min_c_u, max_c_u in bgs:  # assume stored min max for span
            prefer_hor = col_s >= row_s
            col_pl = round(avg_c)
            if prefer_hor:
                # horizontal at banner_row, center at col_pl
                start_c = col_pl - col_s // 2
                valid = True
                for i in range(col_s):
                    pc = start_c + i
                    if not (0 <= pc < cols) or new_g[banner_row][pc] != 0:
                        valid = False
                        break
                if valid:
                    for i in range(col_s):
                        new_g[banner_row][start_c + i] = c
                continue
            # vertical banner, bottom at banner_row
            start_r = banner_row - row_s + 1
            if start_r < 0:
                start_r = 0
            valid = True
            for i in range(row_s):
                pr = start_r + i
                if new_g[pr][col_pl] != 0:
                    valid = False
                    break
            if valid:
                for i in range(row_s):
                    new_g[start_r + i][col_pl] = c

def program(g: List[List[int]]) -> List[List[int]]:
    if not g or not g[0]:
        return g
    rows = len(g)
    cols = len(g[0])
    components = find_components(g, rows, cols)
    movables = identify_movable_smalls(components, g, rows, cols)
    large_cells = [[False] * cols for _ in range(rows)]
    for color, comps in components.items():
        for comp in comps:
            if is_large_component(comp, rows, cols):
                for r, c in comp:
                    large_cells[r][c] = True
    groups = compute_best_anchors(movables, g, large_cells, rows, cols)
    new_g = copy.deepcopy(g)
    remove_set = set()
    for color, comp in movables:
        for r, c in comp:
            remove_set.add((r, c))
    for r, c in remove_set:
        new_g[r][c] = 0
    vertical_max_span: Dict[int, int] = defaultdict(int)
    banner_groups: Dict[int, List[Tuple[int, int, float, int, int]]] = defaultdict(list)
    for (anchor_col, c), comp_lists in groups.items():
        u_pos = get_union_positions(comp_lists)
        if not u_pos:
            continue
        min_r_u, max_r_u, min_c_u, max_c_u = compute_min_max(u_pos)
        row_s = max_r_u - min_r_u + 1
        col_s = max_c_u - min_c_u + 1
        avg_r_u = compute_average_row(u_pos)
        avg_c_u = compute_average_col(u_pos)
        a_pos = get_large_positions(components, anchor_col, rows, cols)
        if not a_pos:
            banner_groups[c].append((row_s, col_s, avg_c_u, min_c_u, max_c_u))
            continue
        a_min_r, a_max_r, a_min_c, a_max_c = compute_min_max(a_pos)
        a_avg_r = compute_average_row(a_pos)
        a_avg_c = compute_average_col(a_pos)
        embedded_h = is_horizontally_embedded(u_pos, anchor_col, g)
        prefer_hor = (col_s >= row_s) and not embedded_h
        placed = False
        if prefer_hor:
            placed = try_horizontal_placement(new_g, u_pos, a_pos, c, rows, cols, avg_r_u, avg_c_u, a_avg_c)
        if not placed:
            placed = try_vertical_placement(new_g, u_pos, a_pos, c, rows, cols, avg_r_u, avg_c_u, a_avg_r, vertical_max_span)
        if not placed:
            banner_groups[c].append((row_s, col_s, avg_c_u, min_c_u, max_c_u))
    place_banner_groups(new_g, banner_groups, vertical_max_span, rows, cols)
    return new_g
```