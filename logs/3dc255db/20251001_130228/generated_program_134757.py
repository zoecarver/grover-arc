```python
from collections import defaultdict
from typing import List, Tuple, Dict, Set
import copy
import math

def get_neighbors(r: int, c: int, rows: int, cols: int) -> List[Tuple[int, int]]:
    """8-way neighbors for adjacency and component finding."""
    dirs = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    return [(r + dr, c + dc) for dr, dc in dirs if 0 <= r + dr < rows and 0 <= c + dc < cols]

def find_components(g: List[List[int]], rows: int, cols: int) -> Dict[int, List[List[Tuple[int, int]]]]:
    """Finds connected components using 8-way connectivity per color."""
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

def identify_small_components(components: Dict[int, List[List[Tuple[int, int]]]], rows: int, cols: int) -> Tuple[List[Tuple[int, List[Tuple[int, int]]]], Set[Tuple[int, int]]]:
    """Identifies small components (<8 cells, no border touch) and their positions set."""
    small: List[Tuple[int, List[Tuple[int, int]]]] = []
    small_pos: Set[Tuple[int, int]] = set()
    for color, comps in components.items():
        for comp in comps:
            size = len(comp)
            touches_border = any(r == 0 or r == rows - 1 or c == 0 or c == cols - 1 for r, c in comp)
            if size < 8 and not touches_border:
                small.append((color, comp))
                for p in comp:
                    small_pos.add(p)
    return small, small_pos

def get_best_large(color: int, positions: List[Tuple[int, int]], g: List[List[int]], small_pos: Set[Tuple[int, int]], rows: int, cols: int) -> int:
    """Finds the best large color adjacent (8-way) to the positions, excluding small positions."""
    adj_counts: Dict[int, int] = defaultdict(int)
    for r, c in positions:
        for nr, nc in get_neighbors(r, c, rows, cols):
            lcol = g[nr][nc]
            if lcol > 0 and lcol != color and (nr, nc) not in small_pos:
                adj_counts[lcol] += 1
    if adj_counts:
        return max(adj_counts, key=adj_counts.get)
    return None

def get_union_positions(comp_lists: List[List[Tuple[int, int]]]) -> List[Tuple[int, int]]:
    """Unions positions from multiple components, deduplicating."""
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
    """Computes average column position."""
    n = len(positions)
    if n == 0:
        return 0.0
    return sum(c for _, c in positions) / n

def compute_average_row(positions: List[Tuple[int, int]]) -> float:
    """Computes average row position."""
    n = len(positions)
    if n == 0:
        return 0.0
    return sum(r for r, _ in positions) / n

def program(g: List[List[int]]) -> List[List[int]]:
    """Main program to solve the puzzle by moving small components to attached positions or top fallback."""
    if not g or not g[0]:
        return g
    rows = len(g)
    cols = len(g[0])
    components = find_components(g, rows, cols)
    small, small_pos_set = identify_small_components(components, rows, cols)
    groups: Dict[Tuple[int, int], List[List[Tuple[int, int]]]] = defaultdict(list)
    for color, pos in small:
        best_l = get_best_large(color, pos, g, small_pos_set, rows, cols)
        # Check for self-attachment if no best_l
        self_l = None
        if best_l is None:
            for l_comp in components[color]:
                size = len(l_comp)
                touches_border = any(r == 0 or r == rows - 1 or c == 0 or c == cols - 1 for r, c in l_comp)
                if size >= 8 or touches_border:
                    self_l = color
                    break
        key = (self_l or best_l, color)
        groups[key].append(pos)
    new_grid = copy.deepcopy(g)
    for key, comp_lists in groups.items():
        best_l, s_color = key
        union_pos = get_union_positions(comp_lists)
        # Remove original positions
        for r, c in union_pos:
            new_grid[r][c] = 0
        if not union_pos:
            continue
        length = len(union_pos)
        avg_r_s = compute_average_row(union_pos)
        avg_c_s = compute_average_col(union_pos)
        if best_l is None:
            # Fallback to top vertical linear placement, find fitting column
            avg_c = math.round(avg_c_s)
            found = False
            for dc in range(-5, 6):  # try nearby columns
                nc = max(0, min(cols - 1, avg_c + dc))
                fits = True
                for i in range(length):
                    nr = i
                    if nr >= rows or new_grid[nr][nc] != 0:
                        fits = False
                        break
                if fits:
                    for i in range(length):
                        new_grid[i][nc] = s_color
                    found = True
                    break
            if not found:
                # Place skipping occupied
                nc = max(0, min(cols - 1, math.round(avg_c_s)))
                for i in range(length):
                    nr = i
                    if nr < rows and new_grid[nr][nc] == 0:
                        new_grid[nr][nc] = s_color
            continue
        # Find chosen large component
        l_comps = components[best_l]
        max_adj = 0
        chosen_large = None
        l_set = None
        for l_comp in l_comps:
            adj = 0
            lset = set(l_comp)
            for r, c in union_pos:
                for nr, nc in get_neighbors(r, c, rows, cols):
                    if (nr, nc) in lset:
                        adj += 1
            if adj > max_adj:
                max_adj = adj
                chosen_large = l_comp
                l_set = lset
        if chosen_large is None:
            # Fallback same as above
            avg_c = math.round(avg_c_s)
            found = False
            for dc in range(-5, 6):
                nc = max(0, min(cols - 1, avg_c + dc))
                fits = True
                for i in range(length):
                    nr = i
                    if nr >= rows or new_grid[nr][nc] != 0:
                        fits = False
                        break
                if fits:
                    for i in range(length):
                        new_grid[i][nc] = s_color
                    found = True
                    break
            continue
        # Attachment logic
        avg_c_l = compute_average_col(chosen_large)
        is_left = avg_c_s > avg_c_l
        if is_left:
            extreme_c = min(c for _, c in chosen_large)
            start_c = extreme_c - length
        else:
            extreme_c = max(c for _, c in chosen_large)
            start_c = extreme_c + 1
        # Choose place_row
        possible_rows = [r for r, c in chosen_large if c == extreme_c]
        if possible_rows:
            place_row = min(possible_rows, key=lambda rr: abs(rr - avg_r_s))
        else:
            place_row = math.round(compute_average_row(chosen_large))
        # Check fit for horizontal linear
        fits = True
        for i in range(length):
            nc = start_c + i
            nr = place_row
            if not (0 <= nr < rows and 0 <= nc < cols and new_grid[nr][nc] == 0):
                fits = False
                break
        if fits:
            for i in range(length):
                nc = start_c + i
                nr = place_row
                new_grid[nr][nc] = s_color
        else:
            # Fallback vertical linear, find fitting column
            avg_c = math.round(avg_c_s)
            found = False
            for dc in range(-5, 6):
                nc = max(0, min(cols - 1, avg_c + dc))
                fits = True
                for i in range(length):
                    nr = i
                    if nr >= rows or new_grid[nr][nc] != 0:
                        fits = False
                        break
                if fits:
                    for i in range(length):
                        new_grid[i][nc] = s_color
                    found = True
                    break
            if not found:
                # Place skipping
                nc = max(0, min(cols - 1, math.round(avg_c_s)))
                for i in range(length):
                    nr = i
                    if nr < rows and new_grid[nr][nc] == 0:
                        new_grid[nr][nc] = s_color
    return new_grid
```