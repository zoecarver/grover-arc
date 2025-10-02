```python
from collections import defaultdict
from typing import List, Tuple, Dict, Set
import copy

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

def get_small_comps(components: Dict[int, List[List[Tuple[int, int]]]], rows: int, cols: int, color: int) -> List[List[Tuple[int, int]]]:
    return [comp for comp in components.get(color, []) if len(comp) < 8 and not touches_border(comp, rows, cols)]

def compute_average_row(positions: List[Tuple[int, int]]) -> float:
    n = len(positions)
    if n == 0:
        return 0.0
    return sum(r for r, _ in positions) / n

def compute_average_col(positions: List[Tuple[int, int]]) -> float:
    n = len(positions)
    if n == 0:
        return 0.0
    return sum(c for _, c in positions) / n

def get_union_positions(pos_lists: List[List[Tuple[int, int]]]) -> List[Tuple[int, int]]:
    seen = set()
    union = []
    for pos_list in pos_lists:
        for p in pos_list:
            tp = (p[0], p[1])
            if tp not in seen:
                seen.add(tp)
                union.append(p)
    return union

def get_large_pos(components: Dict[int, List[List[Tuple[int, int]]]], color: int, rows: int, cols: int) -> List[Tuple[int, int]]:
    for comp in components.get(color, []):
        if len(comp) >= 8 or touches_border(comp, rows, cols):
            return comp
    return []

def get_adj_anchor_comps(g: List[List[int]], components: Dict[int, List[List[Tuple[int, int]]]], best_l: int, small_pos: List[Tuple[int, int]], rows: int, cols: int) -> List[Tuple[int, int]]:
    adj_cells = set()
    for r, c in small_pos:
        for nr, nc in get_neighbors8(r, c, rows, cols):
            if g[nr][nc] == best_l:
                adj_cells.add((nr, nc))
    if not adj_cells:
        return []
    union_anchor = []
    for comp in components.get(best_l, []):
        if any((rr, cc) in adj_cells for rr, cc in comp):
            union_anchor += comp
    return list(set(union_anchor))  # dedup if any

def program(g: List[List[int]]) -> List[List[int]]:
    rows = len(g)
    cols = len(g[0]) if rows > 0 else 0
    new_g = copy.deepcopy(g)
    components = find_components(g, rows, cols)
    static_colors = {3, 4}
    dynamic_colors = sorted(set(components.keys()) - static_colors)
    to_remove = set()
    placement_groups = []  # list of (color, union_pos, best_l, small_comps_list)
    small_comps_per_color = {}
    large_pos_per_color = {}
    for color in components:
        small_comps_per_color[color] = get_small_comps(components, rows, cols, color)
        large_pos_per_color[color] = get_large_pos(components, color, rows, cols)
    for current_color in dynamic_colors:
        small_comps = small_comps_per_color[current_color]
        color_groups = defaultdict(list)  # best_l -> list of comp positions to union
        for positions in small_comps:
            adj_counts = defaultdict(int)
            for r, c in positions:
                for nr, nc in get_neighbors8(r, c, rows, cols):
                    lcol = g[nr][nc]
                    if lcol > 0 and lcol != current_color and (lcol in static_colors or lcol < current_color):
                        adj_counts[lcol] += 1
            if adj_counts:
                best_l = max(adj_counts, key=adj_counts.get)
                color_groups[best_l].append(positions)
                for p in positions:
                    to_remove.add(p)
            else:
                # check self large
                if large_pos_per_color[current_color]:
                    best_l = current_color
                    color_groups[best_l].append(positions)
                    for p in positions:
                        to_remove.add(p)
        # now for each group in color_groups
        for best_l, pos_lists in color_groups.items():
            if pos_lists:
                union_pos = get_union_positions(pos_lists)
                placement_groups.append((current_color, union_pos, best_l, pos_lists))
    # remove all to_remove
    for r, c in to_remove:
        new_g[r][c] = 0
    # now place in order of dynamic colors
    for group in placement_groups:
        color, union_pos, best_l, _ = group
        avg_r = compute_average_row(union_pos)
        avg_c = compute_average_col(union_pos)
        row_span = len(set(r for r, _ in union_pos))
        col_span = len(set(c for _, c in union_pos))
        if large_pos_per_color[best_l]:
            anchor_pos = large_pos_per_color[best_l]
        else:
            anchor_pos = get_adj_anchor_comps(g, components, best_l, union_pos, rows, cols)
        if not anchor_pos:
            continue  # skip if no anchor
        large_avg_r = compute_average_row(anchor_pos)
        large_avg_c = compute_average_col(anchor_pos)
        large_min_r = min(r for r, _ in anchor_pos)
        large_min_c = min(c for _, c in anchor_pos)
        large_max_c = max(c for _, c in anchor_pos)
        blocked = True
        if col_span >= row_span:
            # try horizontal
            side = 'left' if avg_c > large_avg_c else 'right'
            attach_c = large_min_c if side == 'left' else large_max_c
            attach_rows = [r for r, cc in anchor_pos if cc == attach_c]
            attach_r = min(attach_rows, key=lambda rr: abs(rr - avg_r)) if attach_rows else round(large_avg_r)
            length = col_span
            if side == 'left':
                start_c = attach_c - length
                end_c = attach_c - 1
            else:
                start_c = attach_c + 1
                end_c = attach_c + length
            if 0 <= start_c and end_c < cols and all(new_g[attach_r][cc] == 0 for cc in range(start_c, end_c + 1)):
                for cc in range(start_c, end_c + 1):
                    new_g[attach_r][cc] = color
                blocked = False
        if blocked:
            # try vertical top
            length = row_span
            attach_cols = [cc for rr, cc in anchor_pos if rr == large_min_r]
            attach_c = min(attach_cols, key=lambda cc: abs(cc - avg_c)) if attach_cols else round(large_avg_c)
            start_r = large_min_r - length
            if start_r >= 0 and all(new_g[rr][attach_c] == 0 for rr in range(start_r, large_min_r)):
                for rr in range(start_r, large_min_r):
                    new_g[rr][attach_c] = color
                blocked = False
        if blocked:
            # final fallback top vertical
            col = round(avg_c)
            placed = 0
            for rr in range(rows):
                if 0 <= col < cols and new_g[rr][col] == 0:
                    new_g[rr][col] = color
                    placed += 1
                    if placed == row_span:
                        break
    return new_g
```