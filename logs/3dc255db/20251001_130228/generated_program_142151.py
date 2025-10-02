```python
from collections import defaultdict
from typing import List, Tuple, Dict, Set
import copy
import math

def get_neighbors8(r: int, c: int, rows: int, cols: int) -> List[Tuple[int, int]]:
    dirs = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    return [(r + dr, c + dc) for dr, dc in dirs if 0 <= r + dr < rows and 0 <= c + dc < cols]

def touches_border(comp: List[Tuple[int, int]], rows: int, cols: int) -> bool:
    return any(r == 0 or r == rows - 1 or c == 0 or c == cols - 1 for r, c in comp)

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

def get_union_positions(comp_lists: List[List[Tuple[int, int]]]) -> List[Tuple[int, int]]:
    seen = set()
    union = []
    for pos_list in comp_lists:
        for p in pos_list:
            tp = (p[0], p[1])
            if tp not in seen:
                seen.add(tp)
                union.append(p)
    return union

def program(g: List[List[int]]) -> List[List[int]]:
    if not g or not g[0]:
        return g
    rows = len(g)
    cols = len(g[0])
    components = find_components(g, rows, cols)
    current_fixed_sets: Dict[int, Set[Tuple[int, int]]] = defaultdict(set)
    small_per_color: Dict[int, List[List[Tuple[int, int]]]] = defaultdict(list)
    for color, comps in components.items():
        for comp in comps:
            if len(comp) >= 8 or touches_border(comp, rows, cols):
                for p in comp:
                    current_fixed_sets[color].add(p)
            else:
                small_per_color[color].append(comp)
    groups_to_place = []
    to_remove = set()
    for color in sorted(components.keys()):
        if color not in small_per_color:
            continue
        small_comps = small_per_color[color]
        group_dict: Dict[int, List[List[Tuple[int, int]]]] = defaultdict(list)
        stayed_comps = []
        for comp in small_comps:
            adj_counts: Dict[int, int] = defaultdict(int)
            for r, c in comp:
                for nr, nc in get_neighbors8(r, c, rows, cols):
                    cell_color = g[nr][nc]
                    if cell_color != 0 and cell_color != color:
                        for fcolor, fset in current_fixed_sets.items():
                            if fcolor == cell_color and (nr, nc) in fset:
                                adj_counts[fcolor] += 1
                                break
            if adj_counts:
                best_fcolor = max(adj_counts, key=adj_counts.get)
                if adj_counts[best_fcolor] > 0:
                    group_dict[best_fcolor].append(comp)
                else:
                    stayed_comps.append(comp)
            else:
                stayed_comps.append(comp)
        for comp in stayed_comps:
            for p in comp:
                current_fixed_sets[color].add(p)
        for best_fcolor, comp_lists in group_dict.items():
            if comp_lists:
                union_pos = get_union_positions(comp_lists)
                groups_to_place.append((color, best_fcolor, union_pos))
                for p in union_pos:
                    to_remove.add(p)
    new_g = copy.deepcopy(g)
    for r, c in to_remove:
        new_g[r][c] = 0
    for small_color, anchor_color, pos_list in groups_to_place:
        size = len(pos_list)
        if size == 0:
            continue
        avg_r = compute_average_row(pos_list)
        avg_c = compute_average_col(pos_list)
        anchor_pos = list(current_fixed_sets[anchor_color])
        if not anchor_pos:
            continue
        a_min_r = min(r for r, _ in anchor_pos)
        a_max_r = max(r for r, _ in anchor_pos)
        a_min_c = min(c for _, c in anchor_pos)
        a_max_c = max(c for _, c in anchor_pos)
        a_row_span = a_max_r - a_min_r + 1
        a_col_span = a_max_c - a_min_c + 1
        a_avg_r = compute_average_row(anchor_pos)
        a_avg_c = compute_average_col(anchor_pos)
        prefer_horizontal = a_col_span > a_row_span
        placed = False
        for horizontal in [prefer_horizontal, not prefer_horizontal]:
            if placed:
                break
            if horizontal:
                if avg_c < a_avg_c:
                    side_c = a_max_c
                    p_start_c = side_c + 1
                    p_end_c = side_c + size
                    if p_end_c >= cols:
                        continue
                    extreme_rows = [r for r, c in anchor_pos if c == a_max_c]
                    if not extreme_rows:
                        continue
                    target_r = min(extreme_rows, key=lambda rr: abs(rr - avg_r))
                    can_place = all(new_g[target_r][p_start_c + i] == 0 for i in range(size))
                    if can_place:
                        for i in range(size):
                            new_g[target_r][p_start_c + i] = small_color
                        placed = True
                else:
                    side_c = a_min_c
                    p_start_c = side_c - size
                    p_end_c = side_c - 1
                    if p_start_c < 0:
                        continue
                    extreme_rows = [r for r, c in anchor_pos if c == a_min_c]
                    if not extreme_rows:
                        continue
                    target_r = min(extreme_rows, key=lambda rr: abs(rr - avg_r))
                    can_place = all(new_g[target_r][p_start_c + i] == 0 for i in range(size))
                    if can_place:
                        for i in range(size):
                            new_g[target_r][p_start_c + i] = small_color
                        placed = True
            else:
                target_c = max(0, min(cols - 1, round(avg_c)))
                extreme_cols = [c for r, c in anchor_pos if r == a_min_r]
                if extreme_cols:
                    target_c = min(extreme_cols, key=lambda cc: abs(cc - avg_c))
                p_start_r = max(0, a_min_r - size)
                p_end_r = a_min_r - 1
                if p_start_r > p_end_r:
                    continue
                available = p_end_r - p_start_r + 1
                num_place = min(size, available)
                can_place = all(new_g[p_start_r + i][target_c] == 0 for i in range(num_place))
                if can_place:
                    for i in range(num_place):
                        new_g[p_start_r + i][target_c] = small_color
                    placed = True
        if not placed:
            target_c = max(0, min(cols - 1, round(avg_c)))
            num_place = 0
            for rr in range(rows):
                if new_g[rr][target_c] == 0 and num_place < size:
                    new_g[rr][target_c] = small_color
                    num_place += 1
                elif new_g[rr][target_c] != 0:
                    break
    return new_g
```