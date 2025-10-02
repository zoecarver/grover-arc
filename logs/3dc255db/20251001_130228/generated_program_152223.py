```python
from collections import defaultdict
from typing import List, Tuple, Dict, Set
import copy
import math

def get_neighbors4(r: int, c: int, rows: int, cols: int) -> List[Tuple[int, int]]:
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    return [(r + dr, c + dc) for dr, dc in dirs if 0 <= r + dr < rows and 0 <= c + dc < cols]

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
                    for nr, nc in get_neighbors4(cr, cc, rows, cols):
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

def program(g: List[List[int]]) -> List[List[int]]:
    rows = len(g)
    if rows == 0:
        return g
    cols = len(g[0])
    new_g = copy.deepcopy(g)
    components = find_components(g, rows, cols)
    static_colors = {3, 4}
    fixed_pos: Dict[int, Set[Tuple[int, int]]] = defaultdict(set)
    for color, comps in components.items():
        is_static = color in static_colors
        for comp in comps:
            if is_static or len(comp) >= 8 or touches_border(comp, rows, cols):
                for p in comp:
                    fixed_pos[color].add(p)
    small_comps = []
    for color, comps in components.items():
        if color in static_colors or color == 0:
            continue
        for comp in comps:
            if len(comp) < 8 and not touches_border(comp, rows, cols):
                small_comps.append((color, list(comp)))
    groups: Dict[int, Dict[int, List[List[Tuple[int, int]]]]] = defaultdict(lambda: defaultdict(list))
    special_singles = []
    to_remove = set()
    for color, pos in small_comps:
        adj_counts = defaultdict(int)
        for r, c in pos:
            for nr, nc in get_neighbors8(r, c, rows, cols):
                acolor = g[nr][nc]
                if acolor != 0 and acolor != color and (nr, nc) in fixed_pos[acolor]:
                    adj_counts[acolor] += 1
        max_adj = max(adj_counts.values()) if adj_counts else 0
        to_move_flag = max_adj > 0 or len(pos) == 1
        if to_move_flag:
            for p in pos:
                to_remove.add(p)
            if max_adj > 0:
                candidates = sorted(adj_counts, key=lambda ac: (-adj_counts[ac], 0 if ac in static_colors else 1, ac))
                best_ac = candidates[0]
                groups[best_ac][color].append(pos)
            else:
                # size 1, no adj
                special_singles.append((color, pos[0][1]))
    for r, c in to_remove:
        new_g[r][c] = 0
    banner_groups = []
    color_to_bottom = {}
    for acolor, small_groups in groups.items():
        a_pos_list = list(fixed_pos[acolor])
        if not a_pos_list:
            continue
        a_minr, a_maxr, a_minc, a_maxc = compute_min_max(a_pos_list)
        a_avg_r = compute_average_row(a_pos_list)
        a_avg_c = compute_average_col(a_pos_list)
        for scolor, pos_lists in small_groups.items():
            union_pos = get_union_positions(pos_lists)
            if not union_pos:
                continue
            minr, maxr, minc, maxc = compute_min_max(union_pos)
            row_s = maxr - minr + 1
            col_s = maxc - minc + 1
            avg_r = compute_average_row(union_pos)
            avg_c = compute_average_col(union_pos)
            prefer_v = row_s > col_s
            success = False
            for is_vertical in [prefer_v, not prefer_v]:
                length = row_s if is_vertical else col_s
                if length == 0:
                    continue
                preferred_bottom = avg_r < a_avg_r if is_vertical else avg_c < a_avg_c
                for do_preferred in [True, False]:
                    if is_vertical:
                        bottom = preferred_bottom if do_preferred else not preferred_bottom
                        if bottom:
                            edge_r = a_maxr
                            start = a_maxr + 1
                            end = start + length - 1
                            candidates_cols = {cc for rr, cc in a_pos_list if rr == edge_r}
                        else:
                            edge_r = a_minr
                            start = a_minr - length
                            end = a_minr - 1
                            candidates_cols = {cc for rr, cc in a_pos_list if rr == edge_r}
                        if not candidates_cols:
                            continue
                        best_col = min(candidates_cols, key=lambda cc: (abs(cc - avg_c), cc))
                        actual_start = max(0, start)
                        actual_end = min(rows - 1, end)
                        actual_l = actual_end - actual_start + 1 if actual_start <= actual_end else 0
                        if actual_l < length:
                            continue
                        fit = all(new_g[rr][best_col] == 0 for rr in range(actual_start, actual_end + 1))
                        if fit:
                            for rr in range(actual_start, actual_end + 1):
                                new_g[rr][best_col] = scolor
                            color_to_bottom[scolor] = max(color_to_bottom.get(scolor, -100), actual_end)
                            success = True
                            break
                    else:
                        right_side = preferred_bottom if do_preferred else not preferred_bottom  # reuse name
                        if right_side:
                            edge_c = a_maxc
                            start = a_maxc + 1
                            end = start + length - 1
                            candidates_rows = {rr for rr, cc in a_pos_list if cc == edge_c}
                        else:
                            edge_c = a_minc
                            start = a_minc - length
                            end = a_minc - 1
                            candidates_rows = {rr for rr, cc in a_pos_list if cc == edge_c}
                        if not candidates_rows:
                            continue
                        best_row = min(candidates_rows, key=lambda rr: (abs(rr - avg_r), rr))
                        actual_start = max(0, start)
                        actual_end = min(cols - 1, end)
                        actual_l = actual_end - actual_start + 1 if actual_start <= actual_end else 0
                        if actual_l < length:
                            continue
                        fit = all(new_g[best_row][cc] == 0 for cc in range(actual_start, actual_end + 1))
                        if fit:
                            for cc in range(actual_start, actual_end + 1):
                                new_g[best_row][cc] = scolor
                            color_to_bottom[scolor] = max(color_to_bottom.get(scolor, -100), best_row)
                            success = True
                            break
                    if success:
                        break
                if success:
                    break
            if not success:
                banner_groups.append((scolor, union_pos))
    # banner phase
    banner_groups.sort(key=lambda x: compute_average_col(x[1]))
    current_r = 0
    for scolor, union_pos in banner_groups:
        minr, maxr, minc, maxc = compute_min_max(union_pos)
        row_s = maxr - minr + 1
        length = row_s
        if length == 0:
            continue
        avg_c = compute_average_col(union_pos)
        base_col = round(avg_c)
        placed = False
        for delta in range(cols):
            for s in [0] + list(range(1, delta + 1)):
                for sign in [-1, 1]:
                    trial_c = base_col + sign * s if s > 0 else base_col
                    if 0 <= trial_c < cols:
                        start_rr = current_r
                        end_rr = current_r + length - 1
                        if end_rr >= rows:
                            continue
                        fit = all(new_g[rr][trial_c] == 0 for rr in range(start_rr, end_rr + 1))
                        if fit:
                            for rr in range(start_rr, end_rr + 1):
                                new_g[rr][trial_c] = scolor
                            color_to_bottom[scolor] = max(color_to_bottom.get(scolor, -100), end_rr)
                            current_r = end_rr + 1
                            placed = True
                            break
                if placed:
                    break
            if placed:
                break
    # special singles
    for scolor, orig_c in special_singles:
        place_r = color_to_bottom.get(scolor, 0)
        if 0 <= place_r < rows and 0 <= orig_c < cols and new_g[place_r][orig_c] == 0:
            new_g[place_r][orig_c] = scolor
    return new_g
```