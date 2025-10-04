```python
from typing import List, Tuple
from collections import Counter, defaultdict

def get_background(g: List[List[int]]) -> int:
    flat = [cell for row in g for cell in row]
    return Counter(flat).most_common(1)[0][0]

def find_connected_components(g: List[List[int]], b: int) -> List[Tuple[int, List[Tuple[int, int]]]]:
    h = len(g)
    w = len(g[0])
    visited = [[False] * w for _ in range(h)]
    components = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for r in range(h):
        for c in range(w):
            if not visited[r][c] and g[r][c] != b:
                color = g[r][c]
                component = []
                stack = [(r, c)]
                visited[r][c] = True
                while stack:
                    cr, cc = stack.pop()
                    component.append((cr, cc))
                    for dr, dc in directions:
                        nr = cr + dr
                        nc = cc + dc
                        if 0 <= nr < h and 0 <= nc < w and not visited[nr][nc] and g[nr][nc] == color:
                            visited[nr][nc] = True
                            stack.append((nr, nc))
                components.append((color, component))
    return components

def get_bbox(positions: List[Tuple[int, int]]) -> Tuple[int, int, int, int]:
    if not positions:
        return 0, 0, 0, 0
    min_r = min(r for r, c in positions)
    max_r = max(r for r, c in positions)
    min_c = min(c for r, c in positions)
    max_c = max(c for r, c in positions)
    return min_r, max_r, min_c, max_c

def get_gap_positions(g: List[List[int]], b: int, min_r: int, max_r: int, min_c: int, max_c: int) -> List[Tuple[int, int]]:
    gaps = []
    h = len(g)
    w = len(g[0])
    for r in range(max(0, min_r), min(h, max_r + 1)):
        for c in range(max(0, min_c), min(w, max_c + 1)):
            if g[r][c] == b:
                gaps.append((r, c))
    return gaps

def get_relative_shape(positions: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
    if not positions:
        return []
    min_r = min(r for r, c in positions)
    min_c = min(c for r, c in positions)
    rel = sorted((r - min_r, c - min_c) for r, c in positions)
    return rel

def is_touching_border(comp: List[Tuple[int, int]], h: int, w: int) -> bool:
    for r, c in comp:
        if r == 0 or r == h - 1 or c == 0 or c == w - 1:
            return True
    return False

def program(g: List[List[int]]) -> List[List[int]]:
    if not g or not g[0]:
        return g
    h = len(g)
    w = len(g[0])
    b = get_background(g)
    components = find_connected_components(g, b)
    color_comps: Dict[int, List[List[Tuple[int, int]]]] = defaultdict(list)
    for color, comp in components:
        color_comps[color].append(comp)
    new_g = [row[:] for row in g]
    for host_color in list(color_comps):
        comps = color_comps[host_color]
        if len(comps) < 2:
            continue
        all_pos = [p for comp in comps for p in comp]
        min_r, max_r, min_c, max_c = get_bbox(all_pos)
        gaps = get_gap_positions(new_g, b, min_r, max_r, min_c, max_c)
        if len(gaps) == 0:
            continue
        gap_rel = get_relative_shape(gaps)
        for filler_color in list(color_comps):
            if filler_color == host_color:
                continue
            filler_comps = color_comps[filler_color]
            if len(filler_comps) != 1:
                continue
            filler_comp = filler_comps[0]
            if len(filler_comp) != len(gaps):
                continue
            filler_rel = get_relative_shape(filler_comp)
            if filler_rel == gap_rel:
                f_min_r, _, f_min_c, _ = get_bbox(filler_comp)
                g_min_r, _, g_min_c, _ = get_bbox(gaps)
                dy = g_min_r - f_min_r
                dx = g_min_c - f_min_c
                for fr, fc in filler_comp:
                    new_g[fr][fc] = b
                placed = 0
                for gr, gc in gaps:
                    new_g[gr][gc] = filler_color
                    placed += 1
                if placed == len(gaps):
                    del color_comps[filler_color]
                break
    components = find_connected_components(new_g, b)
    for color, comp in components:
        if is_touching_border(comp, h, w):
            continue
        min_r, _, min_c, _ = get_bbox(comp)
        dy = 1
        dx = 6
        for r, c in comp:
            new_g[r][c] = b
        for r, c in comp:
            nr = r + dy
            nc = c + dx
            if 0 <= nr < h and 0 <= nc < w:
                new_g[nr][nc] = color
    return new_g
```