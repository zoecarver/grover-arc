```python
from collections import defaultdict
from typing import List, Tuple, Dict, Set

def program(g: List[List[int]]) -> List[List[int]]:
    grid = [row[:] for row in g]
    rows = len(g)
    cols_len = len(g[0])  # renamed to avoid conflict with cols variable
    return apply_rules(grid, g, rows, cols_len)

def apply_rules(grid: List[List[int]], original_g: List[List[int]], rows: int, cols: int) -> List[List[int]]:
    components = find_components(original_g, rows, cols)
    small_components = identify_small_components(components, rows, cols)
    small_pos_set = get_small_positions(small_components)
    groups = build_groups(small_components, original_g, small_pos_set, rows, cols)
    moved_positions: Set[Tuple[int, int]] = set()
    vertical_placements: List[Tuple[int, int, int]] = []  # med_c, length, color
    for (l_col, s_col), comp_lists in groups.items():
        union_pos = get_union_positions(comp_lists)
        length = compute_row_span(union_pos)
        if length == 0:
            continue
        avg_col_group = compute_average_col(union_pos)
        attached_pos = get_attached_positions(union_pos, original_g, l_col, small_pos_set, rows, cols)
        if not attached_pos:
            continue
        avg_col_l = compute_average_col(attached_pos)
        opposite = determine_opposite_side(avg_col_group, avg_col_l)
        placement_r, extreme_c, blocked = compute_extreme_for_opposite(l_col, original_g, rows, cols, opposite, length)
        # remove original
        for r, c in union_pos:
            grid[r][c] = 0
            moved_positions.add((r, c))
        if not blocked:
            place_horizontal(grid, placement_r, extreme_c, length, s_col, opposite)
        else:
            med_c = round(avg_col_group)
            if 0 <= med_c < cols:
                vertical_placements.append((med_c, length, s_col))
    # handle trapped
    handle_trapped_small(small_components, moved_positions, small_pos_set, original_g, grid, rows, cols, vertical_placements)
    # apply vertical placements
    apply_vertical_placements(grid, original_g, vertical_placements, rows, cols)
    return grid

def find_components(g: List[List[int]], rows: int, cols: int) -> Dict[int, List[List[Tuple[int, int]]]]:
    visited = [[False] * cols for _ in range(rows)]
    components: Dict[int, List[List[Tuple[int, int]]]] = defaultdict(list)
    def get_neighbors(r: int, c: int) -> List[Tuple[int, int]]:
        dirs = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        return [(r + dr, c + dc) for dr, dc in dirs if 0 <= r + dr < rows and 0 <= c + dc < cols]
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
                    for nr, nc in get_neighbors(cr, cc):
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
            if size < 6 and not touches_border:
                small.append((color, comp, comp))  # color, comp_id (unused), positions
    return small

def get_small_positions(small_components: List[Tuple[int, List[Tuple[int, int]], List[Tuple[int, int]]]]) -> Set[Tuple[int, int]]:
    return {(r, c) for _, _, positions in small_components for r, c in positions}

def build_groups(small_components: List[Tuple[int, List[Tuple[int, int]], List[Tuple[int, int]]]], g: List[List[int]], small_pos_set: Set[Tuple[int, int]], rows: int, cols: int) -> Dict[Tuple[int, int], List[List[Tuple[int, int]]]]:
    groups: Dict[Tuple[int, int], List[List[Tuple[int, int]]]] = defaultdict(list)
    def get_neighbors(r: int, c: int) -> List[Tuple[int, int]]:
        dirs = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        return [(r + dr, c + dc) for dr, dc in dirs if 0 <= r + dr < rows and 0 <= c + dc < cols]
    for color, _, positions in small_components:
        adj_counts: Dict[int, int] = defaultdict(int)
        for r, c in positions:
            for nr, nc in get_neighbors(r, c):
                lcol = g[nr][nc]
                if lcol > 0 and lcol != color and (nr, nc) not in small_pos_set:
                    adj_counts[lcol] += 1
        if adj_counts:
            best_l = max(adj_counts, key=adj_counts.get)
            groups[(best_l, color)].append(positions)
    return groups

def get_union_positions(comp_lists: List[List[Tuple[int, int]]]) -> List[Tuple[int, int]]:
    union = []
    seen = set()
    for pos_list in comp_lists:
        for p in pos_list:
            tp = tuple(p)
            if tp not in seen:
                seen.add(tp)
                union.append(p)
    return union

def compute_row_span(positions: List[Tuple[int, int]]) -> int:
    return len(set(r for r, _ in positions))

def compute_average_col(positions: List[Tuple[int, int]]) -> float:
    if not positions:
        return 0.0
    return sum(c for _, c in positions) / len(positions)

def get_attached_positions(union_pos: List[Tuple[int, int]], g: List[List[int]], l_col: int, small_pos_set: Set[Tuple[int, int]], rows: int, cols: int) -> List[Tuple[int, int]]:
    attached = []
    def get_neighbors(r: int, c: int) -> List[Tuple[int, int]]:
        dirs = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        return [(r + dr, c + dc) for dr, dc in dirs if 0 <= r + dr < rows and 0 <= c + dc < cols]
    seen = set()
    for r, c in union_pos:
        for nr, nc in get_neighbors(r, c):
            if g[nr][nc] == l_col and (nr, nc) not in small_pos_set:
                tp = (nr, nc)
                if tp not in seen:
                    seen.add(tp)
                    attached.append(tp)
    return attached

def determine_opposite_side(avg_group: float, avg_l: float) -> str:
    return 'right' if avg_group < avg_l else 'left'

def compute_extreme_for_opposite(l_col: int, g: List[List[int]], rows: int, cols: int, opposite: str, length: int) -> Tuple[int, int, bool]:
    if opposite == 'right':
        max_overall = -1
        placement_r = -1
        for r in range(rows):
            row_cols = [c for c in range(cols) if g[r][c] == l_col]
            if row_cols:
                this_max = max(row_cols)
                if this_max > max_overall:
                    max_overall = this_max
                    placement_r = r
        extreme = max_overall
        blocked = (extreme + length >= cols) if max_overall >= 0 else True
        return placement_r, extreme, blocked
    else:
        min_overall = cols
        placement_r = -1
        for r in range(rows):
            row_cols = [c for c in range(cols) if g[r][c] == l_col]
            if row_cols:
                this_min = min(row_cols)
                if this_min < min_overall:
                    min_overall = this_min
                    placement_r = r
        extreme = min_overall
        blocked = (extreme - length < 0) if min_overall < cols else True
        return placement_r, extreme, blocked

def place_horizontal(grid: List[List[int]], placement_r: int, extreme_c: int, length: int, s_col: int, opposite: str):
    if opposite == 'right':
        start_c = extreme_c + 1
        for i in range(length):
            c = start_c + i
            if 0 <= c < len(grid[0]):
                grid[placement_r][c] = s_col
    else:
        start_c = extreme_c - length
        for i in range(length):
            c = start_c + i
            if 0 <= c < len(grid[0]):
                grid[placement_r][c] = s_col

def handle_trapped_small(small_components: List[Tuple[int, List[Tuple[int, int]], List[Tuple[int, int]]]], moved_positions: Set[Tuple[int, int]], small_pos_set: Set[Tuple[int, int]], g: List[List[int]], grid: List[List[int]], rows: int, cols: int, vertical_placements: List[Tuple[int, int, int]]):
    def get_horizontal_neighbors(r: int, c: int) -> Tuple[int, int]:
        left = g[r][c - 1] if c > 0 else -1  # border as non-zero
        right = g[r][c + 1] if c < cols - 1 else -1
        return left, right
    for color, _, positions in small_components:
        if any((r, c) in moved_positions for r, c in positions):
            continue
        is_trapped = all(
            (left_blocked := (left_c != 0)) and (right_blocked := (right_c != 0))
            for r, c in positions
            for left_c, right_c in [get_horizontal_neighbors(r, c)]
        )
        if is_trapped:
            row_set = set(r for r, _ in positions)
            length = len(row_set)
            num_cells = len(positions)
            med_c = round(sum(c for _, c in positions) / num_cells)
            if 0 <= med_c < cols:
                vertical_placements.append((med_c, length, color))
            for r, c in positions:
                grid[r][c] = 0
                moved_positions.add((r, c))

def apply_vertical_placements(grid: List[List[int]], original_g: List[List[int]], vertical_placements: List[Tuple[int, int, int]], rows: int, cols: int):
    if not vertical_placements:
        return
    first_nonempty = rows
    for r in range(rows):
        if any(original_g[r][c] > 0 for c in range(cols)):
            first_nonempty = r
            break
    bottom_r = first_nonempty - 1
    lengths = [l for _, l, _ in vertical_placements]
    max_l = max(lengths)
    for med_c, length, colr in vertical_placements:
        start_r = bottom_r - length + 1
        if start_r < 0:
            start_r = 0
        for i in range(length):
            rr = start_r + i
            if 0 <= rr < rows and 0 <= med_c < cols:
                grid[rr][med_c] = colr
```