```python
from typing import List, Tuple, Dict

directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

def flood(start_i: int, start_j: int, c: int, g: List[List[int]], visited: List[List[bool]], n: int) -> List[Tuple[int, int, int]]:
    # Rule: Extract connected component of exact same non-2 value using 4-directional flood fill.
    stack = [(start_i, start_j)]
    visited[start_i][start_j] = True
    component = [(start_i, start_j, c)]
    while stack:
        i, j = stack.pop()
        for di, dj in directions:
            ni, nj = i + di, j + dj
            if 0 <= ni < n and 0 <= nj < n and not visited[ni][nj] and g[ni][nj] == c:
                visited[ni][nj] = True
                stack.append((ni, nj))
                component.append((ni, nj, c))
    return component

def extract_main_components(g: List[List[int]]) -> List[List[Tuple[int, int, int]]]:
    # Rule: Find all distinct connected components of same positive non-2 values across the grid.
    n = len(g)
    visited = [[False] * n for _ in range(n)]
    components = []
    for i in range(n):
        for j in range(n):
            if g[i][j] > 0 and g[i][j] != 2 and not visited[i][j]:
                comp = flood(i, j, g[i][j], g, visited, n)
                components.append(comp)
    return components

def attach_connected_twos(main_comp: List[Tuple[int, int, int]], g: List[List[int]], n: int) -> List[Tuple[int, int, int]]:
    # Rule: Attach all 2's connected (via other 2's) to any cell adjacent to the main component.
    seeds = set()
    for i, j, _ in main_comp:
        for di, dj in directions:
            ni, nj = i + di, j + dj
            if 0 <= ni < n and 0 <= nj < n and g[ni][nj] == 2:
                seeds.add((ni, nj))
    if not seeds:
        return []
    visited = set(seeds)
    stack = list(seeds)
    attached = []
    while stack:
        i, j = stack.pop()
        attached.append((i, j, 2))
        for di, dj in directions:
            ni, nj = i + di, j + dj
            if 0 <= ni < n and 0 <= nj < n and g[ni][nj] == 2 and (ni, nj) not in visited:
                visited.add((ni, nj))
                stack.append((ni, nj))
    return attached

def compute_component_properties(main_comp: List[Tuple[int, int, int]], attached: List[Tuple[int, int, int]], g: List[List[int]], n: int) -> Dict:
    # Rule: Compute properties including relative shape, centroid of full, top/bottom touch flags, and add extra 2's below main for top-touch components.
    if not main_comp:
        return {}
    min_r_main = min(r for r, _, _ in main_comp)
    max_r_main = max(r for r, _, _ in main_comp)
    # Upper 2's for top-touch
    upper_set = set()
    for r, c, _ in main_comp:
        for di, dj in directions:
            nr, nc = r + di, c + dj
            if 0 <= nr < n and 0 <= nc < n and g[nr][nc] == 2 and nr < min_r_main:
                upper_set.add((nr, nc))
    upper_count = len(upper_set)
    is_top_touch = upper_count > 0
    # Extra 2's for top-touch
    extra = []
    if is_top_touch:
        bottom_rel = max_r_main - min_r_main
        bottom_cols = set(c for rr, cc, _ in main_comp if rr == min_r_main + bottom_rel)
        sorted_cols = sorted(bottom_cols)
        num_extra = min(upper_count, len(sorted_cols))
        extra_r = min_r_main + bottom_rel + 1
        for ii in range(num_extra):
            extra.append((extra_r, sorted_cols[ii], 2))
    # Full cells
    all_cells = [(r, c, v) for r, c, v in main_comp] + [(r, c, 2) for r, c, _ in attached] + [(r, c, 2) for r, c, _ in extra]
    if not all_cells:
        return {}
    min_r_all = min(r for r, _, _ in all_cells)
    min_c_all = min(c for _, c, _ in all_cells)
    max_r_all = max(r for r, _, _ in all_cells)
    rel_comp = [(r - min_r_all, c - min_c_all, v) for r, c, v in all_cells]
    h = max(rr for rr, _, _ in rel_comp) + 1
    w = max(cc for _, cc, _ in rel_comp) + 1
    centroid = sum(r for r, _, _ in all_cells) / len(all_cells)
    is_bottom_touch = max_r_all >= n - 2
    return {
        'rel_comp': rel_comp,
        'centroid': centroid,
        'min_r_main': min_r_main,
        'is_top_touch': is_top_touch,
        'is_bottom_touch': is_bottom_touch,
        'h': h,
        'w': w
    }

def order_components(processed: List[Dict]) -> List[Dict]:
    # Rule: Order by prioritizing the bottom-touch component (highest centroid), then top-touch (lowest centroid), then remaining by increasing centroid.
    bottom_comps = [p for p in processed if p['is_bottom_touch']]
    top_comps = [p for p in processed if p['is_top_touch']]
    remaining = [p for p in processed if not p['is_bottom_touch'] and not p['is_top_touch']]
    bottom = max(bottom_comps, key=lambda p: p['centroid']) if bottom_comps else None
    top = min(top_comps, key=lambda p: p['centroid']) if top_comps else None
    remaining.sort(key=lambda p: p['centroid'])
    ordered = []
    if bottom:
        ordered.append(bottom)
    ordered += remaining
    if top:
        ordered.append(top)
    return ordered

def can_place(rel_comp: List[Tuple[int, int, int]], dy: int, dx: int, out: List[List[int]], n: int) -> bool:
    # Rule: Check if component can be placed at dy, dx without conflicting values (allow empty or same value).
    for rel_r, rel_c, val in rel_comp:
        nr = dy + rel_r
        nc = dx + rel_c
        if 0 <= nr < n and 0 <= nc < n:
            current = out[nr][nc]
            if current != 0 and current != val:
                return False
    return True

def do_place(rel_comp: List[Tuple[int, int, int]], dy: int, dx: int, out: List[List[int]], n: int):
    # Rule: Place the component at dy, dx, setting values (skips out-of-bounds).
    for rel_r, rel_c, val in rel_comp:
        nr = dy + rel_r
        nc = dx + rel_c
        if 0 <= nr < n and 0 <= nc < n:
            out[nr][nc] = val

def program(g: List[List[int]]) -> List[List[int]]:
    # Compose all rules to process input grid into output.
    n = len(g)
    main_comps = extract_main_components(g)
    processed = []
    for main in main_comps:
        attached = attach_connected_twos(main, g, n)
        props = compute_component_properties(main, attached, g, n)
        if props:
            processed.append(props)
    ordered = order_components(processed)
    out = [[0] * n for _ in range(n)]
    current_max_r = 3  # Baseline for row 4 start
    for p in ordered:
        rel_comp = p['rel_comp']
        h = p['h']
        w = p['w']
        center_left = (n - w) // 2
        # Try tight placement below current max
        dy_try = max(4, current_max_r + 1 - h)
        dx_try = center_left
        if can_place(rel_comp, dy_try, dx_try, out, n):
            do_place(rel_comp, dy_try, dx_try, out, n)
            current_max_r = max(current_max_r, dy_try + h - 1)
            continue
        # Search for smallest dy >= 4 allowing small horizontal shifts
        placed = False
        for dy in range(4, n - h + 1):
            # Center first
            dx = center_left
            if can_place(rel_comp, dy, dx, out, n):
                do_place(rel_comp, dy, dx, out, n)
                current_max_r = max(current_max_r, dy + h - 1)
                placed = True
                break
            # Small shifts
            for shift in range(1, 6):
                for sgn in [-1, 1]:
                    dx = center_left + sgn * shift
                    if dx >= 0 and dx + w <= n and can_place(rel_comp, dy, dx, out, n):
                        do_place(rel_comp, dy, dx, out, n)
                        current_max_r = max(current_max_r, dy + h - 1)
                        placed = True
                        break
                if placed:
                    break
            if placed:
                break
        if not placed:
            # Fallback to bottom
            dy = n - h
            dx = center_left
            do_place(rel_comp, dy, dx, out, n)
            current_max_r = max(current_max_r, dy + h - 1)
    return out
```