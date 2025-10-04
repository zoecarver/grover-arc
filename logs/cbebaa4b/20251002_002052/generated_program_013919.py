```python
from typing import List, Tuple, Dict

directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

def flood(start_i: int, start_j: int, c: int, g: List[List[int]], visited: List[List[bool]], n: int) -> List[Tuple[int, int, int]]:
    # Rule: Standard 4-direction flood fill for connected cells of the same non-2 color.
    stack = [(start_i, start_j)]
    visited[start_i][start_j] = True
    component = []
    while stack:
        i, j = stack.pop()
        if g[i][j] != c:
            continue
        component.append((i, j, c))
        for di, dj in directions:
            ni, nj = i + di, j + dj
            if 0 <= ni < n and 0 <= nj < n and not visited[ni][nj] and g[ni][nj] == c:
                visited[ni][nj] = True
                stack.append((ni, nj))
    return component

def find_components(g: List[List[int]]) -> List[List[Tuple[int, int, int]]]:
    # Rule: Extract connected components of the same non-2 positive value using flood fill.
    n = len(g)
    visited = [[False] * n for _ in range(n)]
    components = []
    for i in range(n):
        for j in range(n):
            if g[i][j] > 0 and g[i][j] != 2 and not visited[i][j]:
                comp = flood(i, j, g[i][j], g, visited, n)
                components.append(comp)
    return components

def process_component(main_comp: List[Tuple[int, int, int]], g: List[List[int]], n: int) -> Dict:
    # Rule: Augment main component with lower attached 2's via flood fill, count upper 2's for potential extra, compute flags and relative shape; extra 2's added below only if upper 2's touch row 0.
    if not main_comp:
        return {}
    min_r_main = min(r for r, _, _ in main_comp)
    max_r_main = max(r for r, _, _ in main_comp)
    min_c_main = min(c for _, c, _ in main_comp)
    # Upper 2's count and check edge touch
    upper_set = set()
    for r, c, _ in main_comp:
        for di, dj in directions:
            nr, nc = r + di, c + dj
            if 0 <= nr < n and 0 <= nc < n and g[nr][nc] == 2 and nr < min_r_main:
                upper_set.add((nr, nc))
    upper_count = len(upper_set)
    is_top_edge_touch = upper_count > 0 and any(r == 0 for r, _ in upper_set)
    # Attached lower 2's (starting from adjacent >= min_r_main, flood connected 2's)
    start_2s = set()
    for r, c, _ in main_comp:
        for di, dj in directions:
            nr, nc = r + di, c + dj
            if 0 <= nr < n and 0 <= nc < n and g[nr][nc] == 2 and nr >= min_r_main:
                start_2s.add((nr, nc))
    visited_2 = [[False] * n for _ in range(n)]
    attached = []
    stack = list(start_2s)
    for i, j in start_2s:
        visited_2[i][j] = True
    while stack:
        i, j = stack.pop()
        if g[i][j] != 2 or visited_2[i][j]:
            continue
        visited_2[i][j] = True
        attached.append((i, j, 2))
        for di, dj in directions:
            ni, nj = i + di, j + dj
            if 0 <= ni < n and 0 <= nj < n and g[ni][nj] == 2 and not visited_2[ni][nj]:
                visited_2[ni][nj] = True
                stack.append((ni, nj))
    # Bottom touch with attached
    max_r = max_r_main
    if attached:
        max_r = max(max_r, max(r for r, _, _ in attached))
    is_bottom_touch = max_r >= n - 2
    centroid = sum(r for r, _, _ in main_comp) / len(main_comp)
    # Extra 2's for top edge touch (below main bottom, in bottom cols up to upper_count)
    extra_abs = []
    if is_top_edge_touch:
        bottom_rel = max_r_main - min_r_main
        bottom_abs_cols = set(c for r, c, _ in main_comp if r - min_r_main == bottom_rel)
        num = min(upper_count, len(bottom_abs_cols))
        sorted_cols = sorted(bottom_abs_cols)
        extra_r = min_r_main + bottom_rel + 1
        for ii in range(num):
            extra_c = sorted_cols[ii]
            extra_abs.append((extra_r, extra_c, 2))
    # Relative component (all together)
    all_cells_abs = [(r, c, v) for r, c, v in main_comp] + [(r, c, 2) for r, c, _ in attached] + extra_abs
    if all_cells_abs:
        min_r_all = min(r for r, _, _ in all_cells_abs)
        min_c_all = min(c for _, c, _ in all_cells_abs)
    else:
        min_r_all = min_r_main
        min_c_all = min_c_main
    rel_comp = [(r - min_r_all, c - min_c_all, v) for r, c, v in all_cells_abs]
    return {
        'rel_comp': rel_comp,
        'min_r_main': min_r_main,
        'centroid': centroid,
        'is_bottom_touch': is_bottom_touch,
        'is_top_edge_touch': is_top_edge_touch
    }

def get_all_processed(g: List[List[int]]) -> List[Dict]:
    # Rule: Find all main components and process each for 2's attachment and flags.
    components = find_components(g)
    n = len(g)
    processed = []
    for comp in components:
        p = process_component(comp, g, n)
        p['main_comp'] = comp  # For centroid if needed, but already computed
        processed.append(p)
    return processed

def can_place(rel_comp: List[Tuple[int, int, int]], dy: int, left: int, out: List[List[int]], n: int) -> bool:
    # Rule: Check if component can be placed at dy, left without conflicting overlaps (allow same value or empty).
    for rel_r, rel_c, val in rel_comp:
        nr = dy + rel_r
        nc = left + rel_c
        if 0 <= nr < n and 0 <= nc < n:
            if out[nr][nc] != 0 and out[nr][nc] != val:
                return False
    return True

def do_place(rel_comp: List[Tuple[int, int, int]], dy: int, left: int, out: List[List[int]], n: int):
    # Rule: Place the component at dy, left, setting cells (skip out of bounds).
    for rel_r, rel_c, val in rel_comp:
        nr = dy + rel_r
        nc = left + rel_c
        if 0 <= nr < n and 0 <= nc < n:
            out[nr][nc] = val

def program(g: List[List[int]]) -> List[List[int]]:
    # Rule: Main program - extract and process components, order with special handling for bottom and top edge, place with packing for remaining to handle overlaps via shift.
    n = len(g)
    out = [[0] * n for _ in range(n)]
    processed = get_all_processed(g)
    # Identify bottom touch component (largest centroid if multiple)
    bottom = None
    max_cent = -float('inf')
    for p in processed[:]:
        if p['is_bottom_touch'] and p['centroid'] > max_cent:
            max_cent = p['centroid']
            bottom = p
    if bottom:
        processed.remove(bottom)
    # Identify top edge touch component (smallest centroid if multiple)
    top = None
    min_cent = float('inf')
    for p in processed[:]:
        if p['is_top_edge_touch'] and p['centroid'] < min_cent:
            min_cent = p['centroid']
            top = p
    if top:
        processed.remove(top)
    # Remaining sorted by descending centroid (bottom first)
    processed.sort(key=lambda p: -p['centroid'])
    to_place = []
    if bottom:
        to_place.append(bottom)
    if top:
        to_place.append(top)
    to_place += processed
    # Placement
    current_max_r = 0
    allowance = 4
    max_shift = 10
    for p in to_place:
        rel_comp = p['rel_comp']
        if not rel_comp:
            continue
        h = max(r for r, _, _ in rel_comp) + 1
        w = max(c for _, c, _ in rel_comp) + 1
        center_left = (n - w) // 2
        # For special (bottom and top), fixed placement
        if p is bottom or p is top:
            if p is bottom:
                dy = 4
            else:
                dy = current_max_r + 1
            if can_place(rel_comp, dy, center_left, out, n):
                do_place(rel_comp, dy, center_left, out, n)
            current_max_r = max(current_max_r, dy + h - 1)
            continue
        # For remaining, packing with allowance and shift
        start_dy = max(4, current_max_r - allowance)
        dy = start_dy
        placed = False
        while dy < n - h + 1 and not placed:
            # Try center
            if can_place(rel_comp, dy, center_left, out, n):
                do_place(rel_comp, dy, center_left, out, n)
                placed = True
            else:
                # Try right shifts
                for k in range(1, max_shift + 1):
                    left = center_left + k
                    if left + w - 1 >= n:
                        break
                    if can_place(rel_comp, dy, left, out, n):
                        do_place(rel_comp, dy, left, out, n)
                        placed = True
                        break
            if not placed:
                dy += 1
        if placed:
            current_max_r = max(current_max_r, dy + h - 1)
    return out
```