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

def get_union_positions(comps: List[List[Tuple[int, int]]]) -> List[Tuple[int, int]]:
    seen = set()
    union = []
    for comp in comps:
        for p in comp:
            tp = (p[0], p[1])
            if tp not in seen:
                seen.add(tp)
                union.append(p)
    return union

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

def compute_min_max(pos: List[Tuple[int, int]]) -> Tuple[int, int, int, int]:
    if not pos:
        return 0, 0, 0, 0
    rs = [r for r, _ in pos]
    cs = [c for _, c in pos]
    return min(rs), max(rs), min(cs), max(cs)

def program(g: List[List[int]]) -> List[List[int]]:
    rows = len(g)
    cols = len(g[0]) if rows > 0 else 0
    new_g = copy.deepcopy(g)
    components = find_components(g, rows, cols)
    large_pos: Dict[int, List[Tuple[int, int]]] = defaultdict(list)
    small_movable: List[Tuple[int, List[Tuple[int, int]]]] = []
    all_small_pos = set()
    for color, comps in components.items():
        is_static = color in (3, 4)
        for comp in comps:
            touches = touches_border(comp, rows, cols)
            size = len(comp)
            if is_static or size >= 8 or touches:
                large_pos[color].extend(comp)
            else:
                small_movable.append((color, comp))
                for p in comp:
                    all_small_pos.add(p)
    for r, c in all_small_pos:
        new_g[r][c] = 0
    groups: Dict[Tuple[int, int], List[List[Tuple[int, int]]]] = defaultdict(list)
    for small_color, comp in small_movable:
        adj_counts = defaultdict(int)
        for r, c in comp:
            for nr, nc in get_neighbors8(r, c, rows, cols):
                if (nr, nc) not in all_small_pos:
                    l_color = g[nr][nc]
                    if l_color > 0:
                        adj_counts[l_color] += 1
        best_anchor = None
        max_adj = 0
        if adj_counts:
            best = max(adj_counts, key=adj_counts.get)
            max_adj = adj_counts[best]
            if max_adj > 0 and best in large_pos:
                best_anchor = best
        key = (best_anchor, small_color) if best_anchor is not None else (None, small_color)
        groups[key].append(comp)
    banner_groups = []
    for key, comp_list in groups.items():
        anchor, s_color = key
        union_pos = get_union_positions(comp_list)
        avg_r_s = compute_average_row(union_pos)
        avg_c_s = compute_average_col(union_pos)
        distinct_rows_s = len(set(r for r, _ in union_pos))
        distinct_cols_s = len(set(c for _, c in union_pos))
        if anchor is None:
            banner_groups.append((s_color, union_pos, avg_c_s, distinct_rows_s))
            continue
        anchor_pos = large_pos[anchor]
        if not anchor_pos:
            banner_groups.append((s_color, union_pos, avg_c_s, distinct_rows_s))
            continue
        avg_r_a = compute_average_row(anchor_pos)
        avg_c_a = compute_average_col(anchor_pos)
        min_r_a, max_r_a, min_c_a, max_c_a = compute_min_max(anchor_pos)
        prefer_horizontal = distinct_cols_s > distinct_rows_s
        if distinct_cols_s == distinct_rows_s:
            prefer_horizontal = True
        placed = False
        if prefer_horizontal:
            length = distinct_cols_s
            is_right = avg_c_s < avg_c_a
            edge_c = max_c_a + 1 if is_right else min_c_a - 1
            edge_ref_c = max_c_a if is_right else min_c_a
            candidate_rows = [r for r, c in anchor_pos if c == edge_ref_c]
            candidate_rows = sorted(set(candidate_rows), key=lambda rr: abs(rr - avg_r_s))
            for cand_r in candidate_rows:
                start_c = edge_c if is_right else edge_c - length + 1
                if start_c < 0 or start_c + length > cols:
                    continue
                free = all(new_g[cand_r][cc] == 0 for cc in range(start_c, start_c + length))
                if free:
                    for i in range(length):
                        new_g[cand_r][start_c + i] = s_color
                    placed = True
                    break
        else:
            length = distinct_rows_s
            is_below = avg_r_s > avg_r_a
            edge_r = max_r_a + 1 if is_below else min_r_a - 1
            edge_ref_r = max_r_a if is_below else min_r_a
            candidate_cols = [c for r, c in anchor_pos if r == edge_ref_r]
            candidate_cols = sorted(set(candidate_cols), key=lambda cc: abs(cc - avg_c_s))
            for cand_c in candidate_cols:
                start_r = edge_r if is_below else edge_r - length + 1
                if start_r < 0 or start_r + length > rows:
                    continue
                free = all(new_g[rr][cand_c] == 0 for rr in range(start_r, start_r + length))
                if free:
                    for i in range(length):
                        new_g[start_r + i][cand_c] = s_color
                    placed = True
                    break
                else:
                    # try the other side for vertical
                    other_is_below = not is_below
                    other_edge_r = max_r_a + 1 if other_is_below else min_r_a - 1
                    other_edge_ref_r = max_r_a if other_is_below else min_r_a
                    other_candidate_cols = [c for r, c in anchor_pos if r == other_edge_ref_r]
                    other_candidate_cols = sorted(set(other_candidate_cols), key=lambda cc: abs(cc - avg_c_s))
                    for other_cand_c in other_candidate_cols:
                        other_start_r = other_edge_r if other_is_below else other_edge_r - length + 1
                        if other_start_r < 0 or other_start_r + length > rows:
                            continue
                        free = all(new_g[rr][other_cand_c] == 0 for rr in range(other_start_r, other_start_r + length))
                        if free:
                            for i in range(length):
                                new_g[other_start_r + i][other_cand_c] = s_color
                            placed = True
                            break
                    if placed:
                        break
        if not placed:
            banner_groups.append((s_color, union_pos, avg_c_s, distinct_rows_s))
    if banner_groups:
        max_h = max(h for _, _, _, h in banner_groups)
        banner_groups.sort(key=lambda x: x[2])
        for s_color, _, avg_c, length in banner_groups:
            target_c = round(avg_c)
            start_r = max_h - length
            placed = False
            deltas = range(cols)
            for delta in deltas:
                for sign in [0, -1, 1]:
                    if sign == 0:
                        c = target_c
                    else:
                        c = target_c + sign * (delta + 1)
                    if 0 <= c < cols:
                        free = all(new_g[start_r + i][c] == 0 for i in range(length) if 0 <= start_r + i < rows)
                        if free:
                            for i in range(length):
                                rr = start_r + i
                                if 0 <= rr < rows:
                                    new_g[rr][c] = s_color
                            placed = True
                            break
                if placed:
                    break
    return new_g
```