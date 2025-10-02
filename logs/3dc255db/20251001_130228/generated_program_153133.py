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

def get_row_span(pos: List[Tuple[int, int]]) -> int:
    min_r, max_r, _, _ = compute_min_max(pos)
    return max_r - min_r + 1

def get_col_span(pos: List[Tuple[int, int]]) -> int:
    _, _, min_c, max_c = compute_min_max(pos)
    return max_c - min_c + 1

def get_fixed_positions(g: List[List[int]], components: Dict[int, List[List[Tuple[int, int]]]], rows: int, cols: int) -> Set[Tuple[int, int]]:
    fixed_pos = set()
    for color in components:
        if color in {3, 4}:
            for comp in components[color]:
                for p in comp:
                    fixed_pos.add(p)
        else:
            for comp in components[color]:
                if touches_border(comp, rows, cols) or len(comp) >= 8:
                    for p in comp:
                        fixed_pos.add(p)
    return fixed_pos

def get_small_comps(components: Dict[int, List[List[Tuple[int, int]]]], rows: int, cols: int) -> List[Tuple[int, List[Tuple[int, int]]]]:
    small = []
    for color in components:
        if color in {3, 4}:
            continue
        for comp in components[color]:
            if len(comp) < 8 and not touches_border(comp, rows, cols):
                small.append((color, comp))
    return small

def has_adj_to_fixed(comp: List[Tuple[int, int]], fixed_pos: Set[Tuple[int, int]], rows: int, cols: int) -> bool:
    for r, c in comp:
        for nr, nc in get_neighbors8(r, c, rows, cols):
            if (nr, nc) in fixed_pos:
                return True
    return False

def get_movable_colors(small_comps: List[Tuple[int, List[Tuple[int, int]]]], fixed_pos: Set[Tuple[int, int]], rows: int, cols: int) -> Set[int]:
    movable = set()
    for color, comp in small_comps:
        if has_adj_to_fixed(comp, fixed_pos, rows, cols):
            movable.add(color)
    return movable

def remove_movable(g: List[List[int]], components: Dict[int, List[List[Tuple[int, int]]]], movable_colors: Set[int], rows: int, cols: int) -> List[List[int]]:
    new_g = copy.deepcopy(g)
    for color in movable_colors:
        for comp in components[color]:
            if len(comp) < 8 and not touches_border(comp, rows, cols):
                for r, c in comp:
                    new_g[r][c] = 0
    return new_g

def get_sub_groups(color_small_comps: List[List[Tuple[int, int]]], rows: int, cols: int) -> List[List[Tuple[int, int]]]:
    small_pos = set()
    for comp in color_small_comps:
        for p in comp:
            small_pos.add(p)
    visited = set()
    sub_groups = []
    for r, c in small_pos:
        if (r, c) in visited:
            continue
        sub = []
        stack = [(r, c)]
        visited.add((r, c))
        while stack:
            cr, cc = stack.pop()
            sub.append((cr, cc))
            for nr, nc in get_neighbors8(cr, cc, rows, cols):
                if (nr, nc) in small_pos and (nr, nc) not in visited:
                    visited.add((nr, nc))
                    stack.append((nr, nc))
        sub_groups.append(sub)
    return sub_groups

def get_adj_anchors(sub: List[Tuple[int, int]], g: List[List[int]], fixed_pos: Set[Tuple[int, int]], rows: int, cols: int) -> Tuple[int, Dict[int, int]]:
    adj_count = 0
    anchors = defaultdict(int)
    for r, c in sub:
        for nr, nc in get_neighbors8(r, c, rows, cols):
            if (nr, nc) in fixed_pos:
                adj_count += 1
                anchors[g[nr][nc]] += 1
    best = max(anchors, key=anchors.get) if anchors else 0
    return adj_count, best

def get_anchor_pos(g: List[List[int]], color: int, rows: int, cols: int) -> List[Tuple[int, int]]:
    pos = []
    for r in range(rows):
        for c in range(cols):
            if g[r][c] == color:
                pos.append((r, c))
    return pos

def try_place_horizontal(new_g: List[List[int]], color: int, length: int, side: str, target_r: int, start_c: int, rows: int, cols: int) -> bool:
    if start_c < 0 or start_c + length > cols:
        return False
    if target_r < 0 or target_r >= rows:
        return False
    for i in range(length):
        if new_g[target_r][start_c + i] != 0:
            return False
    for i in range(length):
        new_g[target_r][start_c + i] = color
    return True

def try_place_vertical(new_g: List[List[int]], color: int, length: int, side: str, target_c: int, start_r: int, rows: int, cols: int) -> bool:
    if target_c < 0 or target_c >= cols:
        return False
    if start_r < 0 or start_r + length > rows:
        return False
    for i in range(length):
        if new_g[start_r + i][target_c] != 0:
            return False
    for i in range(length):
        new_g[start_r + i][target_c] = color
    return True

def place_attached(new_g: List[List[int]], g: List[List[int]], sub: List[Tuple[int, int]], best_anchor: int, avg_r: float, avg_c: float, row_s: int, col_s: int, rows: int, cols: int, fixed_pos: Set[Tuple[int, int]]) -> bool:
    anchor_pos = get_anchor_pos(g, best_anchor, rows, cols)
    a_min_r, a_max_r, a_min_c, a_max_c = compute_min_max(anchor_pos)
    a_avg_r = compute_average_row(anchor_pos)
    a_avg_c = compute_average_col(anchor_pos)
    a_row_s = get_row_span(anchor_pos)
    a_col_s = get_col_span(anchor_pos)
    prefer_vertical = a_row_s > a_col_s
    orientations = [(False, col_s), (True, row_s)] if prefer_vertical else [(False, col_s), (True, row_s)]
    for is_vertical, length in orientations:
        if is_vertical:
            if avg_r < a_avg_r:
                side = 'below'
                start = a_max_r + 1
                edge = a_max_r
            else:
                side = 'above'
                start = a_min_r - length
                edge = a_min_r
            edge_cols = [c for r, c in anchor_pos if r == edge]
            if not edge_cols:
                edge_cols = list(set(c for _, c in anchor_pos))
            candidate_cols = sorted(set(edge_cols), key=lambda c: abs(c - avg_c))
            for target_c in candidate_cols[:3]:  # limit to avoid nested deep
                if try_place_vertical(new_g, g[0][0] wait no, color, length, side, target_c, start, rows, cols):
                    return True
        else:
            if avg_c < a_avg_c:
                side = 'right'
                start = a_max_c + 1
                edge = a_max_c
            else:
                side = 'left'
                start = a_min_c - length
                edge = a_min_c
            edge_rows = [r for r, c in anchor_pos if c == edge]
            if not edge_rows:
                edge_rows = list(set(r for r, _ in anchor_pos))
            candidate_rows = sorted(set(edge_rows), key=lambda r: abs(r - avg_r))
            for target_r in candidate_rows[:3]:
                if try_place_horizontal(new_g, color, length, side, target_r, start, rows, cols):
                    return True
    return False

def place_banner(new_g: List[List[int]], color: int, banner_sub: List[Tuple[float, float, int]], rows: int, cols: int):
    if not banner_sub:
        return
    max_length = max(row_s for _, _, row_s in banner_sub)
    sorted_banner = sorted(banner_sub, key=lambda x: x[1])  # by avg_c
    for avg_r, avg_c, row_s in sorted_banner:
        length = row_s
        start_r = max_length - length
        if start_r + length > rows:
            start_r = 0
        target_c = round(avg_c)
        delta = 0
        while delta < cols:
            for sign in [-1, 1]:
                c = target_c + sign * delta
                if 0 <= c < cols:
                    if all(new_g[start_r + i][c] == 0 for i in range(length) if start_r + i < rows):
                        for i in range(length):
                            if start_r + i < rows:
                                new_g[start_r + i][c] = color
                        return
            delta += 1

def program(g: List[List[int]]) -> List[List[int]]:
    if not g or not g[0]:
        return g
    rows = len(g)
    cols = len(g[0])
    components = find_components(g, rows, cols)
    fixed_pos = get_fixed_positions(g, components, rows, cols)
    small_comps = get_small_comps(components, rows, cols)
    movable_colors = get_movable_colors(small_comps, fixed_pos, rows, cols)
    new_g = remove_movable(g, components, movable_colors, rows, cols)
    for color in sorted(movable_colors):
        color_small_comps = [comp for c, comp in small_comps if c == color]
        sub_groups = get_sub_groups(color_small_comps, rows, cols)
        banner_sub = []
        for sub in sub_groups:
            avg_r = compute_average_row(sub)
            avg_c = compute_average_col(sub)
            row_s = get_row_span(sub)
            col_s = get_col_span(sub)
            adj_count, best_anchor = get_adj_anchors(sub, g, fixed_pos, rows, cols)
            placed = False
            if adj_count > 0 and best_anchor != 0:
                placed = place_attached(new_g, g, sub, best_anchor, avg_r, avg_c, row_s, col_s, rows, cols, fixed_pos)
            if not placed:
                banner_sub.append((avg_r, avg_c, row_s))
        place_banner(new_g, color, banner_sub, rows, cols)
    return new_g
```