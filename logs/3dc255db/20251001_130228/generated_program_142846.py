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

def identify_small_components(components: Dict[int, List[List[Tuple[int, int]]]], rows: int, cols: int) -> List[Tuple[int, List[Tuple[int, int]]]]:
    small: List[Tuple[int, List[Tuple[int, int]]]] = []
    for color, comps in components.items():
        for comp in comps:
            size = len(comp)
            if size < 8 and not touches_border(comp, rows, cols):
                small.append((color, comp))
    return small

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

def get_large_positions(components: Dict[int, List[List[Tuple[int, int]]]], rows: int, cols: int) -> Dict[int, List[Tuple[int, int]]]:
    large_pos: Dict[int, List[Tuple[int, int]]] = defaultdict(list)
    for color, comps in components.items():
        for comp in comps:
            if len(comp) >= 8 or touches_border(comp, rows, cols):
                large_pos[color].extend(comp)
    return large_pos

def program(g: List[List[int]]) -> List[List[int]]:
    if not g or not g[0]:
        return g
    rows = len(g)
    cols = len(g[0])
    components = find_components(g, rows, cols)
    small_comps = identify_small_components(components, rows, cols)
    large_pos = get_large_positions(components, rows, cols)
    large_set = {color: set(pos) for color, pos in large_pos.items()}
    groups: Dict[Tuple[int, int], List[List[Tuple[int, int]]]] = defaultdict(list)
    for color_s, comp in small_comps:
        adj_counts: Dict[int, int] = defaultdict(int)
        for r, c in comp:
            for nr, nc in get_neighbors8(r, c, rows, cols):
                l_color = g[nr][nc]
                if l_color != 0 and l_color != color_s and (nr, nc) in large_set.get(l_color, set()):
                    adj_counts[l_color] += 1
        if adj_counts:
            best_anchor = min(adj_counts, key=lambda col: (-adj_counts[col], col))
            key = (best_anchor, color_s)
        else:
            key = (None, color_s)
        groups[key].append(comp)
    new_g = [row[:] for row in g]
    for _, comp in small_comps:
        for r, c in comp:
            new_g[r][c] = 0
    # Sort groups by anchor (None last), then color_s
    sorted_groups = sorted(groups.items(), key=lambda kv: (999 if kv[0][0] is None else kv[0][0], kv[0][1]))
    for key, group_comps in sorted_groups:
        anchor, color_s = key
        union_pos = get_union_positions(group_comps)
        if not union_pos:
            continue
        avg_row_s = compute_average_row(union_pos)
        avg_col_s = compute_average_col(union_pos)
        row_sp = len(set(r for r, _ in union_pos))
        col_sp = len(set(c for _, c in union_pos))
        if anchor is None:
            # Banner: vertical from top
            col_place = round(avg_col_s)
            height = row_sp
            start_r = 0
            end_r = start_r + height - 1
            if end_r >= rows:
                continue
            # Try col_place, then nearby
            deltas = [0, -1, 1, -2, 2, -3, 3]
            placed = False
            for delta in deltas:
                test_col = col_place + delta
                if not (0 <= test_col < cols):
                    continue
                fits = all(new_g[rr][test_col] == 0 for rr in range(start_r, end_r + 1))
                if fits:
                    for rr in range(start_r, end_r + 1):
                        new_g[rr][test_col] = color_s
                    placed = True
                    break
            continue
        large_positions = large_pos[anchor]
        if not large_positions:
            continue
        avg_col_l = compute_average_col(large_positions)
        do_vertical = abs(avg_col_s - avg_col_l) < 0.5
        placed = False
        if not do_vertical:
            length = col_sp
            if avg_col_s < avg_col_l:
                side = 'right'
                ext_col = max(c for _, c in large_positions)
                ext_rows = [r for r, c in large_positions if c == ext_col]
            else:
                side = 'left'
                ext_col = min(c for _, c in large_positions)
                ext_rows = [r for r, c in large_positions if c == ext_col]
            # Sort ext_rows by distance to avg_row_s
            ext_rows = sorted(set(ext_rows), key=lambda rr: abs(rr - avg_row_s))
            for target_row in ext_rows:
                if side == 'right':
                    start_c = ext_col + 1
                    end_c = start_c + length - 1
                    if end_c >= cols:
                        continue
                    fits = all(new_g[target_row][cc] == 0 for cc in range(start_c, end_c + 1))
                    if fits:
                        for cc in range(start_c, end_c + 1):
                            new_g[target_row][cc] = color_s
                        placed = True
                        break
                else:
                    end_c = ext_col - 1
                    start_c = end_c - length + 1
                    if start_c < 0:
                        continue
                    fits = all(new_g[target_row][cc] == 0 for cc in range(start_c, end_c + 1))
                    if fits:
                        for cc in range(start_c, end_c + 1):
                            new_g[target_row][cc] = color_s
                        placed = True
                        break
        if not placed:
            # Vertical above
            top_r_l = min(r for r, _ in large_positions)
            col_place = round(avg_col_s)
            height = row_sp
            start_r = top_r_l - height
            if start_r < 0:
                start_r = 0
            end_r = start_r + height - 1
            if end_r >= top_r_l:
                continue
            if not (0 <= col_place < cols):
                continue
            fits = all(new_g[rr][col_place] == 0 for rr in range(start_r, end_r + 1))
            if fits:
                for rr in range(start_r, end_r + 1):
                    new_g[rr][col_place] = color_s
    return new_g
```