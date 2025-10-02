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

def compute_min_max(pos: List[Tuple[int, int]]) -> Tuple[int, int, int, int]:
    if not pos:
        return 0, 0, 0, 0
    rs = [r for r, _ in pos]
    cs = [c for _, c in pos]
    return min(rs), max(rs), min(cs), max(cs)

def get_row_span(pos: List[Tuple[int, int]]) -> int:
    min_r, max_r, _, _ = compute_min_max(pos)
    return max_r - min_r + 1

def get_col_span(pos: List[Tuple[int, int]]) -> int:
    _, _, min_c, max_c = compute_min_max(pos)
    return max_c - min_c + 1

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

def get_anchor_positions(g: List[List[int]], color: int, rows: int, cols: int) -> List[Tuple[int, int]]:
    pos = []
    for r in range(rows):
        for c in range(cols):
            if g[r][c] == color:
                pos.append((r, c))
    return pos

def program(g: List[List[int]]) -> List[List[int]]:
    rows = len(g)
    cols = len(g[0])
    new_g = copy.deepcopy(g)
    components = find_components(g, rows, cols)
    static_colors = {3, 4}
    dynamic_small_comps = []
    for color in components:
        if color in static_colors:
            continue
        for comp in components[color]:
            if len(comp) < 8 and not touches_border(comp, rows, cols):
                dynamic_small_comps.append((color, comp))
    to_remove = set()
    for color, comp in dynamic_small_comps:
        for p in comp:
            to_remove.add(p)
    for r, c in to_remove:
        new_g[r][c] = 0
    attachment_groups = defaultdict(list)
    banner_comps_per_color = defaultdict(list)
    for color, comp in dynamic_small_comps:
        adj_counts = defaultdict(int)
        for r, c in comp:
            for nr, nc in get_neighbors8(r, c, rows, cols):
                ncol = g[nr][nc]
                if ncol in static_colors:
                    adj_counts[ncol] += 1
        if adj_counts:
            best_anchor = max(adj_counts, key=lambda k: (adj_counts[k], -k))
            attachment_groups[(best_anchor, color)].append(comp)
        else:
            banner_comps_per_color[color].append(comp)
    for (anchor_col, s_color), comp_list in list(attachment_groups.items()):
        union_pos = get_union_positions(comp_list)
        size = len(union_pos)
        col_span = get_col_span(union_pos)
        if size == col_span:
            anchor_pos = get_anchor_positions(g, anchor_col, rows, cols)
            avg_c_a = compute_average_col(anchor_pos)
            avg_c_s = compute_average_col(union_pos)
            if avg_c_s < avg_c_a:
                side = 'left'
                extreme = min(c for _, c in anchor_pos)
            else:
                side = 'right'
                extreme = max(c for _, c in anchor_pos)
            extreme_rows = [r for r, c in anchor_pos if (side == 'right' and c == extreme) or (side == 'left' and c == extreme)]
            avg_r_s = compute_average_row(union_pos)
            best_r = min(extreme_rows, key=lambda rr: abs(rr - avg_r_s))
            if side == 'right':
                start_c = extreme + 1
            else:
                start_c = extreme - size + 1
            can_place = 0 <= start_c <= start_c + size - 1 < cols
            blocked = False
            if can_place:
                for i in range(size):
                    cc = start_c + i
                    if new_g[best_r][cc] != 0:
                        blocked = True
                        break
            if not blocked:
                for i in range(size):
                    cc = start_c + i
                    new_g[best_r][cc] = s_color
            else:
                banner_comps_per_color[s_color].append(union_pos)
        else:
            banner_comps_per_color[s_color].append(union_pos)
    banner_subgroups = []
    for s_color, comp_list in banner_comps_per_color.items():
        if not comp_list:
            continue
        comp_infos = []
        for cpos in comp_list:
            avg_c = compute_average_col(cpos)
            comp_infos.append((avg_c, cpos))
        comp_infos.sort(key=lambda x: x[0])
        clusters = []
        if comp_infos:
            current_cluster = [comp_infos[0][1]]
            current_avg = comp_infos[0][0]
            for i in range(1, len(comp_infos)):
                this_avg = comp_infos[i][0]
                if this_avg - current_avg < 3.0:
                    current_cluster.append(comp_infos[i][1])
                else:
                    clusters.append(current_cluster)
                    current_cluster = [comp_infos[i][1]]
                    current_avg = this_avg
            clusters.append(current_cluster)
        for clus in clusters:
            union_p = get_union_positions(clus)
            rs = get_row_span(union_p)
            ac = compute_average_col(union_p)
            col_pl = round(ac)
            banner_subgroups.append((col_pl, rs, s_color))
    if banner_subgroups:
        max_h = max(rs for _, rs, _ in banner_subgroups)
        banner_subgroups.sort(key=lambda x: x[0])
        for col_pl, rs, s_color in banner_subgroups:
            start_r = max_h - rs
            placed = False
            for delta in range(-5, 6):
                test_col = col_pl + delta
                if test_col < 0 or test_col >= cols:
                    continue
                can = True
                for i in range(rs):
                    rr = start_r + i
                    if rr >= rows or new_g[rr][test_col] != 0:
                        can = False
                        break
                if can:
                    for i in range(rs):
                        rr = start_r + i
                        new_g[rr][test_col] = s_color
                    placed = True
                    break
    return new_g
```