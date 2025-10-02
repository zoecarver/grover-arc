```python
from collections import defaultdict
from typing import List, Tuple, Dict, Set
import copy
import math

def get_neighbors4(r: int, c: int, rows: int, cols: int) -> List[Tuple[int, int]]:
    """4-way neighbors for connected component discovery."""
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    return [(r + dr, c + dc) for dr, dc in dirs if 0 <= r + dr < rows and 0 <= c + dc < cols]

def get_neighbors8(r: int, c: int, rows: int, cols: int) -> List[Tuple[int, int]]:
    """8-way neighbors for adjacency and union checks."""
    dirs = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    return [(r + dr, c + dc) for dr, dc in dirs if 0 <= r + dr < rows and 0 <= c + dc < cols]

def find_components(g: List[List[int]], rows: int, cols: int) -> Dict[int, List[List[Tuple[int, int]]]]:
    """Discovers connected components per color using 4-way connectivity."""
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
    """Checks if any cell in the component touches the grid border."""
    return any(r == 0 or r == rows - 1 or c == 0 or c == cols - 1 for r, c in comp)

def get_small_comps(components: Dict[int, List[List[Tuple[int, int]]]], rows: int, cols: int, color: int) -> List[List[Tuple[int, int]]]:
    """Extracts small components (<8 cells, no border touch) for a specific color."""
    return [comp for comp in components.get(color, []) if len(comp) < 8 and not touches_border(comp, rows, cols)]

def compute_min_max(pos: List[Tuple[int, int]]) -> Tuple[int, int, int, int]:
    """Computes min/max row and column for positions."""
    if not pos:
        return 0, 0, 0, 0
    rs = [r for r, _ in pos]
    cs = [c for _, c in pos]
    return min(rs), max(rs), min(cs), max(cs)

def compute_average_row(pos: List[Tuple[int, int]]) -> float:
    """Computes average row position."""
    n = len(pos)
    if n == 0:
        return 0.0
    return sum(r for r, _ in pos) / n

def compute_average_col(pos: List[Tuple[int, int]]) -> float:
    """Computes average column position."""
    n = len(pos)
    if n == 0:
        return 0.0
    return sum(c for _, c in pos) / n

def get_row_span(pos: List[Tuple[int, int]]) -> int:
    """Computes row span (max_r - min_r + 1) for vertical placement length."""
    min_r, _, _, _ = compute_min_max(pos)
    max_r, _, _, _ = compute_min_max(pos)
    return max_r - min_r + 1

def get_col_span(pos: List[Tuple[int, int]]) -> int:
    """Computes column span (max_c - min_c + 1) for horizontal placement length."""
    _, _, min_c, max_c = compute_min_max(pos)
    return max_c - min_c + 1

def get_anchor_positions(g: List[List[int]], color: int, rows: int, cols: int) -> List[Tuple[int, int]]:
    """Gathers all positions of a given anchor color from the grid."""
    pos = []
    for r in range(rows):
        for c in range(cols):
            if g[r][c] == color:
                pos.append((r, c))
    return pos

def compute_best_anchor(pos_s: List[Tuple[int, int]], g: List[List[int]], color_s: int, rows: int, cols: int, static_colors: Set[int]) -> int:
    """Computes the best anchor color based on adjacency count, preferring static or lower colors."""
    adj_count = defaultdict(int)
    s_set = set(pos_s)
    for r, c in pos_s:
        for nr, nc in get_neighbors8(r, c, rows, cols):
            lcol = g[nr][nc]
            if lcol != 0 and lcol != color_s and (nr, nc) not in s_set:
                adj_count[lcol] += 1
    if not adj_count:
        return -1  # No anchor
    # Prefer static or lower color
    possible = [(lc, adj_count[lc]) for lc in adj_count if adj_count[lc] > 0]
    possible.sort(key=lambda x: (0 if x[0] in static_colors else 1, x[0]))
    return possible[0][0]

def place_horizontal(new_g: List[List[int]], pos_s: List[Tuple[int, int]], color: int, avg_r_s: float, avg_c_s: float, anchor_pos: List[Tuple[int, int]], rows: int, cols: int) -> bool:
    """Places a horizontal linear block attached to the anchor, preferring opposite side."""
    avg_r_l = compute_average_row(anchor_pos)
    avg_c_l = compute_average_col(anchor_pos)
    min_r_l, max_r_l, min_c_l, max_c_l = compute_min_max(anchor_pos)
    length = get_col_span(pos_s)
    side = 'right' if avg_c_s < avg_c_l else 'left'
    possible_rows = sorted(set(r for r, _ in anchor_pos), key=lambda r: abs(r - avg_r_s))
    placed = False
    if side == 'right':
        for r in possible_rows:
            # Max c in this row for anchor
            row_max_c = max((c for rr, c in anchor_pos if rr == r), default=min_c_l)
            start_c = row_max_c + 1
            end_c = start_c + length - 1
            if end_c < cols and all(new_g[r][cc] == 0 for cc in range(start_c, end_c + 1)):
                for cc in range(start_c, end_c + 1):
                    new_g[r][cc] = color
                placed = True
                break
    else:
        for r in possible_rows:
            row_min_c = min((c for rr, c in anchor_pos if rr == r), default=max_c_l)
            start_c = row_min_c - length
            end_c = row_min_c - 1
            if start_c >= 0 and all(new_g[r][cc] == 0 for cc in range(start_c, end_c + 1)):
                for cc in range(start_c, end_c + 1):
                    new_g[r][cc] = color
                placed = True
                break
    return placed

def place_vertical(new_g: List[List[int]], pos_s: List[Tuple[int, int]], color: int, avg_r_s: float, avg_c_s: float, anchor_pos: List[Tuple[int, int]], rows: int, cols: int) -> bool:
    """Places a vertical linear block attached to the anchor, preferring opposite side, with clamping and partial if blocked."""
    avg_r_l = compute_average_row(anchor_pos)
    avg_c_l = compute_average_col(anchor_pos)
    min_r_l, max_r_l, min_c_l, max_c_l = compute_min_max(anchor_pos)
    length = get_row_span(pos_s)
    side = 'above' if avg_r_s > avg_r_l else 'below'
    possible_cols = sorted(set(c for _, c in anchor_pos), key=lambda c: abs(c - avg_c_s))
    placed = False
    if side == 'above':
        for c in possible_cols:
            # Min r in this col for anchor
            col_min_r = min((r for r, cc in anchor_pos if cc == c), default=max_r_l)
            start_r = col_min_r - length
            if start_r < 0:
                start_r = 0
            # Place from start_r down length cells, but stop if blocked
            placed_cells = 0
            for rr in range(start_r, rows):
                if placed_cells >= length:
                    break
                if new_g[rr][c] == 0:
                    new_g[rr][c] = color
                    placed_cells += 1
                else:
                    break  # Stop at block
            if placed_cells > 0:
                placed = True
                break
    else:
        for c in possible_cols:
            col_max_r = max((r for r, cc in anchor_pos if cc == c), default=min_r_l)
            start_r = col_max_r + 1
            end_r = start_r + length - 1
            if end_r < rows and all(new_g[rr][c] == 0 for rr in range(start_r, end_r + 1)):
                for rr in range(start_r, end_r + 1):
                    new_g[rr][c] = color
                placed = True
                break
    return placed

def place_banner(new_g: List[List[int]], pos_s: List[Tuple[int, int]], color: int, rows: int, cols: int) -> None:
    """Places a vertical linear banner from the top in rounded average column."""
    length = get_row_span(pos_s)
    avg_c = round(compute_average_col(pos_s))
    avg_c = max(0, min(cols - 1, avg_c))
    start_r = 0
    for c in [avg_c] + [avg_c + i for i in range(1, cols)] + [avg_c - i for i in range(1, cols) if avg_c - i >= 0]:
        if c < 0 or c >= cols:
            continue
        placed_cells = 0
        for rr in range(start_r, rows):
            if placed_cells >= length:
                break
            if new_g[rr][c] == 0:
                new_g[rr][c] = color
                placed_cells += 1
            else:
                break
        if placed_cells >= length:
            return

def program(g: List[List[int]]) -> List[List[int]]:
    """Main program: Processes the grid by moving small components of dynamic colors to attach to best anchors or banners."""
    rows = len(g)
    cols = len(g[0]) if rows > 0 else 0
    if rows == 0 or cols == 0:
        return g
    new_g = copy.deepcopy(g)
    components = find_components(g, rows, cols)
    static_colors = {3, 4}
    dynamic_colors = sorted(set(c for c in components if c not in static_colors))
    for color in dynamic_colors:
        small_comps = get_small_comps(components, rows, cols, color)
        if not small_comps:
            continue
        # Group small comps by their best anchor
        groups_by_anchor = defaultdict(list)
        for comp in small_comps:
            best_l = compute_best_anchor(comp, g, color, rows, cols, static_colors)
            groups_by_anchor[best_l].append(comp)
        # For each anchor group, collect all positions
        for best_l, comps_list in groups_by_anchor.items():
            if best_l == -1:
                # Banner for the whole group
                all_pos = []
                for comp in comps_list:
                    all_pos.extend(comp)
                # Remove
                for r, c in all_pos:
                    new_g[r][c] = 0
                place_banner(new_g, all_pos, color, rows, cols)
                continue
            # Collect all pos for this anchor group
            all_pos = []
            for comp in comps_list:
                all_pos.extend(comp)
            # Remove
            for r, c in all_pos:
                new_g[r][c] = 0
            # Get anchor positions
            anchor_pos = get_anchor_positions(g, best_l, rows, cols)
            if not anchor_pos:
                place_banner(new_g, all_pos, color, rows, cols)
                continue
            avg_r_s = compute_average_row(all_pos)
            avg_c_s = compute_average_col(all_pos)
            height_l = get_row_span(anchor_pos)
            width_l = get_col_span(anchor_pos)
            placed = False
            if width_l >= height_l:
                placed = place_horizontal(new_g, all_pos, color, avg_r_s, avg_c_s, anchor_pos, rows, cols)
                if not placed:
                    placed = place_vertical(new_g, all_pos, color, avg_r_s, avg_c_s, anchor_pos, rows, cols)
            else:
                placed = place_vertical(new_g, all_pos, color, avg_r_s, avg_c_s, anchor_pos, rows, cols)
                if not placed:
                    placed = place_horizontal(new_g, all_pos, color, avg_r_s, avg_c_s, anchor_pos, rows, cols)
            if not placed:
                place_banner(new_g, all_pos, color, rows, cols)
    return new_g
```