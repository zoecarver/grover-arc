```python
from collections import defaultdict
from typing import List, Tuple, Dict, Set
import copy
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

def touches_border(comp: List[Tuple[int, int]], rows: int, cols: int) -> bool:
    return any(r == 0 or r == rows - 1 or c == 0 or c == cols - 1 for r, c in comp)

def identify_small_components(components: Dict[int, List[List[Tuple[int, int]]]], rows: int, cols: int) -> Tuple[List[Tuple[int, List[Tuple[int, int]], List[Tuple[int, int]]]], Set[Tuple[int, int]]]:
    small: List[Tuple[int, List[Tuple[int, int]], List[Tuple[int, int]]]] = []
    small_pos: Set[Tuple[int, int]] = set()
    for color, comps in components.items():
        for comp in comps:
            size = len(comp)
            touches_border_flag = touches_border(comp, rows, cols)
            if size < 8 and not touches_border_flag:
                small.append((color, comp, comp))
                for p in comp:
                    small_pos.add(p)
    return small, small_pos

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

def get_large_pos(components: Dict[int, List[List[Tuple[int, int]]]], color: int, rows: int, cols: int) -> List[Tuple[int, int]]:
    pos = []
    for comp in components.get(color, []):
        if len(comp) >= 8 or touches_border(comp, rows, cols):
            pos.extend(comp)
    return pos

def build_groups(small_components: List[Tuple[int, List[Tuple[int, int]], List[Tuple[int, int]]]], g: List[List[int]], small_pos_set: Set[Tuple[int, int]], rows: int, cols: int) -> Dict[Tuple[int, int], List[List[Tuple[int, int]]]]:
    groups: Dict[Tuple[int, int], List[List[Tuple[int, int]]]] = defaultdict(list)
    for color, _, positions in small_components:
        adj_counts: Dict[int, int] = defaultdict(int)
        for r, c in positions:
            for nr, nc in get_neighbors(r, c, rows, cols):
                lcol = g[nr][nc]
                if lcol > 0 and (nr, nc) not in small_pos_set:
                    adj_counts[lcol] += 1
        if adj_counts:
            best_l = max(adj_counts, key=adj_counts.get)
            groups[(best_l, color)].append(positions)
        else:
            groups[(0, color)].append(positions)
    return groups

def try_horizontal_attachment(new_g: List[List[int]], color: int, size: int, avg_r: float, avg_c: float, avg_c_a: float, min_c_a: int, max_c_a: int, anchor_pos: List[Tuple[int, int]], rows: int, cols: int) -> bool:
    # opposite side
    if avg_c < avg_c_a:
        # original left, place right
        edge_c = max_c_a
        start_c = max_c_a + 1
    else:
        # original right, place left
        edge_c = min_c_a
        start_c = min_c_a - size
    # edge rows: rows with anchor at edge_c
    edge_rows = {r for r, c in anchor_pos if c == edge_c}
    if not edge_rows:
        return False
    candidate_rows = sorted(edge_rows, key=lambda rr: abs(rr - avg_r))
    for r in candidate_rows:
        # check positions start_c to start_c + size -1
        can_place = True
        positions = []
        cc = start_c
        for _ in range(size):
            if not (0 <= cc < cols) or new_g[r][cc] != 0:
                can_place = False
                break
            positions.append((r, cc))
            cc += 1
        if can_place:
            for pr, pc in positions:
                new_g[pr][pc] = color
            return True
    return False

def program(g: List[List[int]]) -> List[List[int]]:
    rows = len(g)
    cols = len(g[0]) if rows > 0 else 0
    new_g = copy.deepcopy(g)
    components = find_components(g, rows, cols)
    small, small_pos_set = identify_small_components(components, rows, cols)
    # remove smalls
    for color, comp, _ in small:
        for r, c in comp:
            new_g[r][c] = 0
    groups = build_groups(small, g, small_pos_set, rows, cols)
    banner_groups = []
    for (anchor_color, small_color), comp_lists in groups.items():
        union_pos = get_union_positions(comp_lists)
        size = len(union_pos)
        if size == 0:
            continue
        avg_r = compute_average_row(union_pos)
        avg_c = compute_average_col(union_pos)
        placed = False
        if anchor_color != 0:
            anchor_pos = get_large_pos(components, anchor_color, rows, cols)
            if anchor_pos:
                avg_c_a = compute_average_col(anchor_pos)
                _, _, min_c_a, max_c_a = compute_min_max(anchor_pos)
                placed = try_horizontal_attachment(new_g, small_color, size, avg_r, avg_c, avg_c_a, min_c_a, max_c_a, anchor_pos, rows, cols)
        if not placed:
            banner_groups.append((small_color, size, avg_c))
    # now place banners with bottom alignment
    if banner_groups:
        sizes = [sz for _, sz, _ in banner_groups]
        max_size = max(sizes)
        bottom_r = min(max_size - 1, rows - 1)
        banner_groups.sort(key=lambda x: x[2])
        for color, size, avg_c in banner_groups:
            col = round(avg_c)
            placed_partial = False
            for delta in range(6):
                for sgn in [-1, 0, 1]:
                    if delta == 0 and sgn != 0:
                        continue
                    test_col = col + sgn * delta
                    if 0 <= test_col < cols:
                        start_r = max(0, bottom_r - size + 1)
                        r = start_r
                        placed_count = 0
                        while r <= bottom_r and r < rows and placed_count < size and new_g[r][test_col] == 0:
                            new_g[r][test_col] = color
                            placed_count += 1
                            r += 1
                        if placed_count > 0:
                            placed_partial = True
                            break
                if placed_partial:
                    break
    return new_g
```