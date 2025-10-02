```python
from collections import defaultdict
from typing import List, Tuple, Dict, Set
import math

def get_neighbors(r: int, c: int, rows: int, cols: int) -> List[Tuple[int, int]]:
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
                    for nr, nc in get_neighbors(cr, cc, rows, cols):
                        if g[nr][nc] == color and not visited[nr][nc]:
                            visited[nr][nc] = True
                            stack.append((nr, nc))
                components[color].append(component)
    return components

def identify_small_components(components: Dict[int, List[List[Tuple[int, int]]]], rows: int, cols: int) -> List[Tuple[int, List[Tuple[int, int]], List[Tuple[int, int]]]]:
    small: List[Tuple[int, List[Tuple[int, int]], List[Tuple[int, int]]]] = []
    for color, comps in components.items():
        for comp in comps:
            size = len(comp)
            touches_border = any(r == 0 or r == rows - 1 or c == 0 or c == cols - 1 for r, c in comp)
            if size < 8 and not touches_border:
                small.append((color, comp, comp))
    return small

def build_groups(small_components: List[Tuple[int, List[Tuple[int, int]], List[Tuple[int, int]]]], g: List[List[int]], small_pos_set: Set[Tuple[int, int]], rows: int, cols: int, total_size: Dict[int, int]) -> Dict[Tuple[int, int], List[List[Tuple[int, int]]]]:
    groups: Dict[Tuple[int, int], List[List[Tuple[int, int]]]] = defaultdict(list)
    for color, _, positions in small_components:
        current_size = len(positions)
        adj_counts: Dict[int, int] = defaultdict(int)
        for r, c in positions:
            for nr, nc in get_neighbors(r, c, rows, cols):
                lcol = g[nr][nc]
                if lcol > 0 and lcol != color and total_size.get(lcol, 0) > current_size:
                    adj_counts[lcol] += 1
        best_l = None
        if adj_counts:
            best_l = max(adj_counts, key=adj_counts.get)
        else:
            if total_size.get(color, 0) > current_size:
                best_l = color
        if best_l is not None:
            groups[(best_l, color)].append(positions)
    return groups

def get_union_positions(comp_lists: List[List[Tuple[int, int]]]) -> List[Tuple[int, int]]:
    union = []
    seen = set()
    for pos_list in comp_lists:
        for p in pos_list:
            tp = (p[0], p[1])
            if tp not in seen:
                seen.add(tp)
                union.append(p)
    return union

def compute_row_span(positions: List[Tuple[int, int]]) -> int:
    return len(set(r for r, _ in positions))

def compute_average_col(positions: List[Tuple[int, int]]) -> float:
    n = len(positions)
    if n == 0:
        return 0.0
    return sum(c for _, c in positions) / n

def program(g: List[List[int]]) -> List[List[int]]:
    rows = len(g)
    if rows == 0:
        return g
    cols = len(g[0])
    components = find_components(g, rows, cols)
    total_size = {col: sum(len(comp) for comp in comps) for col, comps in components.items()}
    small_components = identify_small_components(components, rows, cols)
    small_pos_set = set(p for _, _, poss in small_components for p in poss)
    groups = build_groups(small_components, g, small_pos_set, rows, cols, total_size)
    new_grid = [row[:] for row in g]
    for (large_col, small_col), comp_lists in groups.items():
        union_pos = get_union_positions(comp_lists)
        for r, c in union_pos:
            new_grid[r][c] = 0
        large_pos_list = components.get(large_col, [])
        large_pos = [p for comp in large_pos_list for p in comp]
        if not large_pos:
            continue
        min_r_l = min(r for r, _ in large_pos)
        max_r_l = max(r for r, _ in large_pos)
        min_c_l = min(c for _, c in large_pos)
        max_c_l = max(c for _, c in large_pos)
        h_l = max_r_l - min_r_l + 1
        w_l = max_c_l - min_c_l + 1
        n_u = len(union_pos)
        if n_u == 0:
            continue
        avg_col_s = sum(c for _, c in union_pos) / n_u
        avg_row_s = sum(r for r, _ in union_pos) / n_u
        row_span = compute_row_span(union_pos)
        length = row_span
        is_vertical = h_l >= w_l
        placed = False
        avg_col_l = sum(c for _, c in large_pos) / len(large_pos)
        if not is_vertical:
            if avg_col_s > avg_col_l:
                extreme_c = min_c_l
                start_c = extreme_c - length
            else:
                extreme_c = max_c_l
                start_c = extreme_c + 1
            extreme_rows = [r for r, c in large_pos if c == extreme_c]
            if not extreme_rows:
                extreme_rows = list(set(r for r, _ in large_pos))
            place_r = min(extreme_rows, key=lambda rr: (abs(rr - avg_row_s), rr))
            fits = all(0 <= start_c + i < cols and new_grid[place_r][start_c + i] == 0 for i in range(length))
            if fits:
                for i in range(length):
                    cc = start_c + i
                    new_grid[place_r][cc] = small_col
                placed = True
        if not placed:
            place_c = max(0, min(cols - 1, round(avg_col_s)))
            start_r = max(0, min_r_l - length)
            for i in range(length):
                rr = start_r + i
                if 0 <= rr < rows and new_grid[rr][place_c] == 0:
                    new_grid[rr][place_c] = small_col
    return new_grid
```