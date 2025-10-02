```python
from collections import defaultdict
from typing import List, Tuple, Dict, Set

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

def program(g: List[List[int]]) -> List[List[int]]:
    if not g or not g[0]:
        return g
    rows = len(g)
    cols = len(g[0])
    components = find_components(g, rows, cols)
    small_comps = []
    small_pos = set()
    for color, comps_list in components.items():
        for comp in comps_list:
            size = len(comp)
            touches = touches_border(comp, rows, cols)
            if size < 6 and not touches:
                small_comps.append((color, comp))
                for p in comp:
                    small_pos.add(p)
    new_g = [row[:] for row in g]
    for _, comp in small_comps:
        for r, c in comp:
            new_g[r][c] = 0
    large_pos_per_color = defaultdict(set)
    for color, comps_list in components.items():
        for comp in comps_list:
            size = len(comp)
            touches = touches_border(comp, rows, cols)
            if size >= 6 or touches:
                for r, c in comp:
                    large_pos_per_color[color].add((r, c))
    attach_groups = defaultdict(list)  # (best_l, color) -> list of comps
    fallback_per_color = defaultdict(list)  # color -> list of comps
    for color, comp in small_comps:
        adj_counts = defaultdict(int)
        for r, c in comp:
            for nr, nc in get_neighbors8(r, c, rows, cols):
                lcol = g[nr][nc]
                if lcol > 0 and lcol != color and (nr, nc) in large_pos_per_color[lcol]:
                    adj_counts[lcol] += 1
        best_l = None
        adj_to_best = 0
        if adj_counts:
            best_l = max(adj_counts, key=adj_counts.get)
            adj_to_best = adj_counts[best_l]
        size_comp = len(comp)
        large_max_size = 0
        if best_l in components:
            large_max_size = max((len(cmp) for cmp in components[best_l] if len(cmp) >= 6 or touches_border(cmp, rows, cols)), default=0)
        if best_l and adj_to_best >= 1 and large_max_size >= size_comp:
            attach_groups[(best_l, color)].append(comp)
        else:
            fallback_per_color[color].append(comp)
    # Place attach groups
    for (best_l, color), comp_lists in attach_groups.items():
        union_pos = get_union_positions(comp_lists)
        col_span_s = max((c for _, c in union_pos), default=0) - min((c for _, c in union_pos), default=0) + 1
        row_span_s = max((r for r, _ in union_pos), default=0) - min((r for r, _ in union_pos), default=0) + 1
        avg_row_s = compute_average_row(union_pos)
        avg_col_s = compute_average_col(union_pos)
        large_comps = [comp for comp in components[best_l] if len(comp) >= 6 or touches_border(comp, rows, cols)]
        if not large_comps:
            continue
        large_comp = max(large_comps, key=len)
        large_pos = large_comp
        avg_row_l = compute_average_row(large_pos)
        avg_col_l = compute_average_col(large_pos)
        min_col_l = min(c for _, c in large_pos)
        max_col_l = max(c for _, c in large_pos)
        min_row_l = min(r for r, _ in large_pos)
        max_row_l = max(r for r, _ in large_pos)
        # Horizontal placement
        if avg_col_s < avg_col_l:
            extreme_col = min_col_l
            extreme_rows_set = {r for r, c in large_pos if c == min_col_l}
            extreme_row = min(extreme_rows_set, key=lambda rr: abs(rr - avg_row_s)) if extreme_rows_set else round(avg_row_l)
            start_col = extreme_col - col_span_s
            cols_list = list(range(start_col, extreme_col))
        else:
            extreme_col = max_col_l
            extreme_rows_set = {r for r, c in large_pos if c == max_col_l}
            extreme_row = min(extreme_rows_set, key=lambda rr: abs(rr - avg_row_s)) if extreme_rows_set else round(avg_row_l)
            start_col = extreme_col + 1
            cols_list = list(range(start_col, start_col + col_span_s))
        fit = all(0 <= cc < cols and new_g[extreme_row][cc] == 0 for cc in cols_list)
        if fit:
            for cc in cols_list:
                new_g[extreme_row][cc] = color
            continue
        # Vertical placement
        if avg_row_s < avg_row_l:
            extreme_row_v = min_row_l
            extreme_cols_set = {c for r, c in large_pos if r == min_row_l}
            extreme_col_v = min(extreme_cols_set, key=lambda cc: abs(cc - avg_col_s)) if extreme_cols_set else round(avg_col_l)
            start_row_v = extreme_row_v - row_span_s
            rows_list = list(range(start_row_v, extreme_row_v))
        else:
            extreme_row_v = max_row_l
            extreme_cols_set = {c for r, c in large_pos if r == max_row_l}
            extreme_col_v = min(extreme_cols_set, key=lambda cc: abs(cc - avg_col_s)) if extreme_cols_set else round(avg_col_l)
            start_row_v = extreme_row_v + 1
            rows_list = list(range(start_row_v, start_row_v + row_span_s))
        fit = all(0 <= rr < rows and new_g[rr][extreme_col_v] == 0 for rr in rows_list)
        if fit:
            for rr in rows_list:
                new_g[rr][extreme_col_v] = color
            continue
        # Fallback to top vertical
        col_place = max(0, min(cols - 1, round(avg_col_s)))
        current_r = 0
        fit = False
        while current_r + row_span_s <= rows:
            if all(new_g[current_r + i][col_place] == 0 for i in range(row_span_s)):
                fit = True
                break
            current_r += 1
        if fit:
            for i in range(row_span_s):
                new_g[current_r + i][col_place] = color
    # Place fallback
    colors = sorted(fallback_per_color.keys())
    current_top = 0
    for color in colors:
        fallback_comps = fallback_per_color[color]
        if not fallback_comps:
            continue
        comp_with_avg = [(compute_average_col(comp), comp) for comp in fallback_comps]
        comp_with_avg.sort(key=lambda x: x[0])
        clusters = []
        current_cluster_comps = [comp_with_avg[0][1]]
        for i in range(1, len(comp_with_avg)):
            prev_avg = compute_average_col(get_union_positions(current_cluster_comps))
            curr_avg, curr_comp = comp_with_avg[i]
            if abs(curr_avg - prev_avg) < 3.0:
                current_cluster_comps.append(curr_comp)
            else:
                clusters.append(current_cluster_comps)
                current_cluster_comps = [curr_comp]
        if current_cluster_comps:
            clusters.append(current_cluster_comps)
        cluster_infos = []
        max_banner = 0
        for clus_comps in clusters:
            u_pos = get_union_positions(clus_comps)
            rs = max(r for r, _ in u_pos) - min(r for r, _ in u_pos) + 1 if u_pos else 0
            ac = compute_average_col(u_pos)
            cluster_infos.append((rs, ac, u_pos))
            max_banner = max(max_banner, rs)
        banner_start = current_top
        for rs, ac, u_pos in cluster_infos:
            col_p = max(0, min(cols - 1, round(ac)))
            start_r_c = banner_start + max_banner - rs
            fit = all(start_r_c + i < rows and new_g[start_r_c + i][col_p] == 0 for i in range(rs))
            if fit:
                for i in range(rs):
                    new_g[start_r_c + i][col_p] = color
        current_top += max_banner
    return new_g
```