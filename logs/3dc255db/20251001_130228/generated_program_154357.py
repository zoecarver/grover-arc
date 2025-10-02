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

def program(g: List[List[int]]) -> List[List[int]]:
    rows = len(g)
    cols = len(g[0])
    components = find_components(g, rows, cols)
    small_comps = []
    small_pos = set()
    for color, comps_list in components.items():
        for comp in comps_list:
            if len(comp) < 8 and not touches_border(comp, rows, cols):
                small_comps.append((color, comp))
                for p in comp:
                    small_pos.add(p)
    new_g = copy.deepcopy(g)
    for r, c in small_pos:
        new_g[r][c] = 0
    groups: Dict[Tuple[int, int], List[List[Tuple[int, int]]]] = defaultdict(list)
    for color, comp in small_comps:
        adj_counts: Dict[int, int] = defaultdict(int)
        for r, c in comp:
            for nr, nc in get_neighbors8(r, c, rows, cols):
                if (nr, nc) not in small_pos and g[nr][nc] > 0:
                    adj_counts[g[nr][nc]] += 1
        best_anchor = 0
        if adj_counts:
            best_anchor = max(adj_counts, key=adj_counts.get)
        groups[(best_anchor, color)].append(comp)
    top_vertical_placements = []  # list of (color, target_col, length)
    for (anchor, color), comp_lists in groups.items():
        union_pos = get_union_positions(comp_lists)
        if not union_pos:
            continue
        row_span = get_row_span(union_pos)
        col_span = get_col_span(union_pos)
        avg_row_s = compute_average_row(union_pos)
        avg_col_s = compute_average_col(union_pos)
        is_horizontal_preferred = col_span >= row_span
        length = col_span if is_horizontal_preferred else row_span
        placed = False
        if anchor != 0:
            large_comps = [comp for comp in components[anchor] if len(comp) >= 8 or touches_border(comp, rows, cols)]
            if not large_comps:
                anchor = 0
            else:
                large_pos = get_union_positions(large_comps)
                avg_row_l = compute_average_row(large_pos)
                avg_col_l = compute_average_col(large_pos)
                min_r_l, max_r_l, min_c_l, max_c_l = compute_min_max(large_pos)
                if is_horizontal_preferred:
                    # horizontal attachment
                    if avg_col_s > avg_col_l:
                        # left
                        edge_col = min_c_l
                        edge_rows_set = {r for r, c in large_pos if c == edge_col}
                        candidate_rows = sorted(edge_rows_set, key=lambda rr: abs(rr - avg_row_s))
                        for target_row in candidate_rows:
                            start_col = edge_col - length
                            if start_col < 0:
                                continue
                            can_place = all(new_g[target_row][start_col + i] == 0 for i in range(length))
                            if can_place:
                                for i in range(length):
                                    new_g[target_row][start_col + i] = color
                                placed = True
                                break
                    else:
                        # right
                        edge_col = max_c_l
                        edge_rows_set = {r for r, c in large_pos if c == edge_col}
                        candidate_rows = sorted(edge_rows_set, key=lambda rr: abs(rr - avg_row_s))
                        for target_row in candidate_rows:
                            start_col = edge_col + 1
                            if start_col + length > cols:
                                continue
                            can_place = all(new_g[target_row][start_col + i] == 0 for i in range(length))
                            if can_place:
                                for i in range(length):
                                    new_g[target_row][start_col + i] = color
                                placed = True
                                break
                else:
                    # vertical attachment preferred
                    if avg_row_s < avg_row_l:
                        # above
                        edge_row = min_r_l
                        edge_cols_set = {c for r, c in large_pos if r == edge_row}
                        candidate_cols = sorted(edge_cols_set, key=lambda cc: abs(cc - avg_col_s))
                        for target_col in candidate_cols:
                            start_row = edge_row - length
                            if start_row < 0:
                                # fallback to top banner
                                top_vertical_placements.append((color, round(avg_col_s), length))
                                placed = True  # mark as placed later
                                break
                            can_place = all(new_g[start_row + i][target_col] == 0 for i in range(length))
                            if can_place:
                                for i in range(length):
                                    new_g[start_row + i][target_col] = color
                                placed = True
                                break
                    else:
                        # below
                        edge_row = max_r_l
                        edge_cols_set = {c for r, c in large_pos if r == edge_row}
                        candidate_cols = sorted(edge_cols_set, key=lambda cc: abs(cc - avg_col_s))
                        for target_col in candidate_cols:
                            start_row = edge_row + 1
                            if start_row + length > rows:
                                continue
                            can_place = all(new_g[start_row + i][target_col] == 0 for i in range(length))
                            if can_place:
                                for i in range(length):
                                    new_g[start_row + i][target_col] = color
                                placed = True
                                break
        if not placed:
            # banner vertical top
            target_col = round(avg_col_s)
            if 0 <= target_col < cols:
                top_vertical_placements.append((color, target_col, length))
            else:
                # skip or clamp
                pass
    # now place the top vertical with alignment
    if top_vertical_placements:
        max_len = max(length for _, _, length in top_vertical_placements)
        bottom_row = max_len - 1
        for color, target_col, length in top_vertical_placements:
            start_row = bottom_row - length + 1
            if start_row < 0:
                start_row = 0
            # find free col near target_col if blocked
            placed_col = target_col
            can_place = all(new_g[start_row + i][placed_col] == 0 for i in range(length)) if start_row + length <= rows else False
            if not can_place:
                for delta in range(1, cols):
                    for sign in [-1, 1]:
                        tc = target_col + sign * delta
                        if 0 <= tc < cols:
                            can_place = all(new_g[start_row + i][tc] == 0 for i in range(length)) if start_row + length <= rows else False
                            if can_place:
                                placed_col = tc
                                break
                    if can_place:
                        break
            if can_place and start_row + length <= rows:
                for i in range(length):
                    new_g[start_row + i][placed_col] = color
    return new_g
```