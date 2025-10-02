```python
from collections import defaultdict
from typing import List, Tuple, Dict, Set
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

def identify_small_components(components: Dict[int, List[List[Tuple[int, int]]]], rows: int, cols: int) -> List[Tuple[int, List[Tuple[int, int]], List[Tuple[int, int]]]]:
    small: List[Tuple[int, List[Tuple[int, int]], List[Tuple[int, int]]]] = []
    for color, comps in components.items():
        for comp in comps:
            size = len(comp)
            touches_border = any(r == 0 or r == rows - 1 or c == 0 or c == cols - 1 for r, c in comp)
            if size < 8 and not touches_border:
                small.append((color, comp, comp))
    return small

def build_groups(small_components: List[Tuple[int, List[Tuple[int, int]], List[Tuple[int, int]]]], g: List[List[int]], small_pos_set: Set[Tuple[int, int]], rows: int, cols: int) -> Dict[Tuple[int, int], List[List[Tuple[int, int]]]]:
    groups: Dict[Tuple[int, int], List[List[Tuple[int, int]]]] = defaultdict(list)
    def get_neighbors(r: int, c: int) -> List[Tuple[int, int]]:
        return get_neighbors8(r, c, rows, cols)
    for color, _, positions in small_components:
        adj_counts: Dict[int, int] = defaultdict(int)
        for r, c in positions:
            for nr, nc in get_neighbors(r, c):
                lcol = g[nr][nc]
                if lcol > 0 and (nr, nc) not in small_pos_set:
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

def compute_average_col(positions: List[Tuple[int, int]]) -> float:
    if not positions:
        return 0.0
    return sum(c for _, c in positions) / len(positions)

def program(g: List[List[int]]) -> List[List[int]]:
    rows = len(g)
    cols = len(g[0])
    components = find_components(g, rows, cols)
    small_components = identify_small_components(components, rows, cols)
    small_pos_set = set(p for _, _, pos in small_components for p in pos)
    # Union small components of same color if adjacent 8-way
    color_to_comps = defaultdict(list)
    for i, (color, _, pos) in enumerate(small_components):
        color_to_comps[color].append((i, pos))
    parent = list(range(len(small_components)))
    def find(x: int) -> int:
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]
    def union(x: int, y: int):
        px = find(x)
        py = find(y)
        if px != py:
            parent[px] = py
    for color, comps_list in color_to_comps.items():
        for i in range(len(comps_list)):
            for j in range(i + 1, len(comps_list)):
                id1, pos1 = comps_list[i]
                id2, pos2 = comps_list[j]
                pos2_set = set(pos2)
                connected = any((nr, nc) in pos2_set for r, c in pos1 for nr, nc in get_neighbors8(r, c, rows, cols))
                if connected:
                    union(id1, id2)
    # Group unioned comps per color
    color_to_union_groups = defaultdict(list)
    for color, comps_list in color_to_comps.items():
        group = defaultdict(list)
        for id1, pos1 in comps_list:
            root = find(id1)
            group[root].append(pos1)
        for root, pos_lists in group.items():
            color_to_union_groups[color].append(pos_lists)
    # Now build groups for attached union groups
    groups: Dict[Tuple[int, int], List[List[Tuple[int, int]]]] = defaultdict(list)
    for color, union_groups_list in color_to_union_groups.items():
        for union_pos_lists in union_groups_list:
            adj_counts: Dict[int, int] = defaultdict(int)
            all_pos = []
            for pos_list in union_pos_lists:
                all_pos.extend(pos_list)
            for r, c in all_pos:
                for nr, nc in get_neighbors8(r, c, rows, cols):
                    lcol = g[nr][nc]
                    if lcol > 0 and (nr, nc) not in small_pos_set:
                        adj_counts[lcol] += 1
            if adj_counts:
                best_l = max(adj_counts, key=adj_counts.get)
                groups[(best_l, color)].append(union_pos_lists)
    new_g = [row[:] for row in g]
    for (large_col, small_col), union_groups_list in groups.items():
        all_union_lists = []
        for union_pos_lists in union_groups_list:
            all_union_lists.extend(union_pos_lists)
        union_pos = get_union_positions(all_union_lists)
        if not union_pos:
            continue
        # remove
        for r, c in union_pos:
            new_g[r][c] = 0
        # large_pos non-small of large_col
        large_pos = [(r, c) for r in range(rows) for c in range(cols) if g[r][c] == large_col and (r, c) not in small_pos_set]
        if not large_pos:
            continue
        large_avg_c = compute_average_col(large_pos)
        small_avg_c = compute_average_col(union_pos)
        small_avg_r = sum(r for r, _ in union_pos) / len(union_pos)
        large_min_c = min(c for _, c in large_pos)
        large_max_c = max(c for _, c in large_pos)
        unique_cols_set = set(c for _, c in union_pos)
        unique_rows_set = set(r for r, _ in union_pos)
        unique_cols = len(unique_cols_set)
        unique_rows = len(unique_rows_set)
        # Decide if try horizontal or direct vertical
        if unique_cols >= unique_rows:
            # try horizontal
            is_left = small_avg_c > large_avg_c
            if is_left:
                extreme_c = large_min_c
                starting_c = large_min_c - unique_cols
            else:
                extreme_c = large_max_c
                starting_c = large_max_c + 1
            blocked = starting_c < 0 or starting_c + unique_cols - 1 >= cols
            # find placement_row closest extreme pos
            extreme_pos_list = [(r, c) for r, c in large_pos if c == extreme_c]
            placement_row = -1
            if extreme_pos_list:
                extreme_pos_list.sort(key=lambda p: abs(p[0] - small_avg_r))
                placement_row = extreme_pos_list[0][0]
                # check overlap in new_g
                overlap = any(0 <= starting_c + i < cols and new_g[placement_row][starting_c + i] != 0 for i in range(unique_cols))
                blocked = blocked or overlap
            else:
                blocked = True
            if not blocked:
                # place horizontal
                for i in range(unique_cols):
                    c_place = starting_c + i
                    if 0 <= c_place < cols:
                        new_g[placement_row][c_place] = small_col
            else:
                # vertical fallback
                place_col = round(small_avg_c)
                place_col = max(0, min(cols - 1, place_col))
                start_r = 0
                while start_r < rows and new_g[start_r][place_col] != 0:
                    start_r += 1
                placed = 0
                for i in range(unique_rows):
                    r = start_r + i
                    if r < rows and new_g[r][place_col] == 0:
                        new_g[r][place_col] = small_col
                        placed += 1
                    if placed == unique_rows:
                        break
        else:
            # direct vertical
            place_col = round(small_avg_c)
            place_col = max(0, min(cols - 1, place_col))
            start_r = 0
            while start_r < rows and new_g[start_r][place_col] != 0:
                start_r += 1
            placed = 0
            for i in range(unique_rows):
                r = start_r + i
                if r < rows and new_g[r][place_col] == 0:
                    new_g[r][place_col] = small_col
                    placed += 1
                if placed == unique_rows:
                    break
    return new_g
```