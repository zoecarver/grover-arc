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

def is_large(comp: List[Tuple[int, int]], rows: int, cols: int) -> bool:
    return len(comp) >= 8 or touches_border(comp, rows, cols)

def get_large_pos(components: Dict[int, List[List[Tuple[int, int]]]], rows: int, cols: int) -> Dict[int, List[Tuple[int, int]]]:
    large_pos: Dict[int, List[Tuple[int, int]]] = defaultdict(list)
    for color, comps in components.items():
        for comp in comps:
            if is_large(comp, rows, cols):
                large_pos[color].extend(comp)
    return large_pos

def compute_min_max(pos: List[Tuple[int, int]]) -> Tuple[int, int, int, int]:
    if not pos:
        return 0, 0, 0, 0
    rs = [r for r, _ in pos]
    cs = [c for _, c in pos]
    return min(rs), max(rs), min(cs), max(cs)

def compute_span(pos: List[Tuple[int, int]]) -> Tuple[int, int]:
    min_r, max_r, min_c, max_c = compute_min_max(pos)
    return max_r - min_r + 1 if pos else 0, max_c - min_c + 1 if pos else 0

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

def get_union_pos(group_comps: List[List[Tuple[int, int]]]) -> List[Tuple[int, int]]:
    seen = set()
    union = []
    for comp in group_comps:
        for p in comp:
            if p not in seen:
                seen.add(p)
                union.append(p)
    return union

def try_horizontal_place(new_g: List[List[int]], color: int, large_pos: List[Tuple[int, int]], union_pos: List[Tuple[int, int]], rows: int, cols: int) -> bool:
    if not union_pos or not large_pos:
        return False
    large_avg_c = compute_average_col(large_pos)
    small_avg_c = compute_average_col(union_pos)
    _, col_span = compute_span(union_pos)
    if col_span == 0:
        return False
    small_avg_r = compute_average_row(union_pos)
    if small_avg_c < large_avg_c:
        edge_c = max(c for _, c in large_pos)
        start_c = edge_c + 1
        edge_rows = {r for r, c in large_pos if c == edge_c}
    else:
        edge_c = min(c for _, c in large_pos)
        start_c = edge_c - col_span
        edge_rows = {r for r, c in large_pos if c == edge_c}
    if not edge_rows:
        return False
    candidates = sorted(edge_rows, key=lambda rr: abs(rr - small_avg_r))
    for target_r in candidates:
        if not 0 <= target_r < rows:
            continue
        fits = True
        for dc in range(col_span):
            pc = start_c + dc
            if not 0 <= pc < cols or new_g[target_r][pc] != 0:
                fits = False
                break
        if fits:
            for dc in range(col_span):
                pc = start_c + dc
                new_g[target_r][pc] = color
            return True
    return False

def get_dynamic_colors(components: Dict[int, List[List[Tuple[int, int]]]], g: List[List[int]], rows: int, cols: int, large_pos_set: Set[Tuple[int, int]]) -> Set[int]:
    dynamic = set()
    for color, comps in components.items():
        has_adj_comp = False
        for comp in comps:
            if is_large(comp, rows, cols):
                continue
            for r, c in comp:
                for nr, nc in get_neighbors8(r, c, rows, cols):
                    if (nr, nc) in large_pos_set and g[nr][nc] != color:
                        has_adj_comp = True
                        break
                if has_adj_comp:
                    break
            if has_adj_comp:
                break
        if has_adj_comp:
            dynamic.add(color)
    return dynamic

def get_small_groups(g: List[List[int]], components: Dict[int, List[List[Tuple[int, int]]]], large_pos: Dict[int, List[Tuple[int, int]]], rows: int, cols: int) -> Dict[Tuple[int, int], List[List[Tuple[int, int]]]]:
    groups: Dict[Tuple[int, int], List[List[Tuple[int, int]]]] = defaultdict(list)
    large_pos_set = set()
    for pos_list in large_pos.values():
        for p in pos_list:
            large_pos_set.add(p)
    for color, comps in components.items():
        for comp in comps:
            if is_large(comp, rows, cols):
                continue
            adj_counts: Dict[int, int] = defaultdict(int)
            for r, c in comp:
                for nr, nc in get_neighbors8(r, c, rows, cols):
                    if (nr, nc) in large_pos_set and g[nr][nc] != color:
                        adj_counts[g[nr][nc]] += 1
            if adj_counts:
                best_l = min(adj_counts, key=lambda x: (-adj_counts[x], x))
                groups[(best_l, color)].append(comp)
    return groups

def program(g: List[List[int]]) -> List[List[int]]:
    if not g or not g[0]:
        return g
    rows = len(g)
    cols = len(g[0])
    components = find_components(g, rows, cols)
    large_pos = get_large_pos(components, rows, cols)
    large_pos_set = set(p for pos_list in large_pos.values() for p in pos_list)
    dynamic_colors = get_dynamic_colors(components, g, rows, cols, large_pos_set)
    groups = get_small_groups(g, components, large_pos, rows, cols)
    used_comp_ids = set()
    for gcomps in groups.values():
        for comp in gcomps:
            used_comp_ids.add(id(comp))
    new_g = copy.deepcopy(g)
    to_move_pos = set()
    for color in dynamic_colors:
        for comp in components[color]:
            if not is_large(comp, rows, cols):
                for p in comp:
                    to_move_pos.add(p)
    for r, c in to_move_pos:
        new_g[r][c] = 0
    failed_clusters: Dict[int, List[List[Tuple[int, int]]]] = defaultdict(list)
    for key, gcomps in groups.items():
        best_l, s_color = key
        union_pos = get_union_pos(gcomps)
        if not try_horizontal_place(new_g, s_color, large_pos[best_l], union_pos, rows, cols):
            failed_clusters[s_color].append(union_pos)
    for color in dynamic_colors:
        for comp in components[color]:
            if not is_large(comp, rows, cols) and id(comp) not in used_comp_ids:
                failed_clusters[color].append(comp)
    colors_with_failed = [c for c in failed_clusters if failed_clusters[c]]
    current_top = 0
    for s_color in sorted(colors_with_failed):
        cluster_list = failed_clusters[s_color]
        if not cluster_list:
            continue
        cluster_with_avg = [(compute_average_col(pos_list), pos_list) for pos_list in cluster_list]
        cluster_with_avg.sort(key=lambda x: x[0])
        clusters = []
        current = []
        for avg_c, pos in cluster_with_avg:
            if not current:
                current = [(avg_c, pos)]
            else:
                curr_avg = sum(a for a, _ in current) / len(current)
                if abs(avg_c - curr_avg) <= 3:
                    current.append((avg_c, pos))
                else:
                    clusters.append(current)
                    current = [(avg_c, pos)]
        if current:
            clusters.append(current)
        cluster_unions = []
        for cl in clusters:
            union_cl = get_union_pos([p for _, p in cl])
            row_s, _ = compute_span(union_cl)
            cl_avg_c = sum(a for a, _ in cl) / len(cl)
            place_col = max(0, min(cols - 1, round(cl_avg_c)))
            cluster_unions.append((row_s, place_col))
        if not cluster_unions:
            continue
        max_h = max(row_s for row_s, _ in cluster_unions)
        block_start = current_top
        for row_s, place_col in cluster_unions:
            start_r = block_start + max_h - row_s
            for i in range(row_s):
                r = start_r + i
                if 0 <= r < rows and new_g[r][place_col] == 0:
                    new_g[r][place_col] = s_color
        current_top += max_h
    return new_g
```