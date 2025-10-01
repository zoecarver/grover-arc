```python
from typing import List, Dict, Tuple, Set

def get_background(g: List[List[int]]) -> int:
    return g[0][0]

def find_components(g: List[List[int]], bg: int) -> List[Dict]:
    rows = len(g)
    if rows == 0:
        return []
    cols = len(g[0])
    visited = [[False] * cols for _ in range(rows)]
    components = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for r in range(rows):
        for c in range(cols):
            if g[r][c] != bg and not visited[r][c]:
                comp = {
                    'positions': [],
                    'colors': set(),
                    'minr': r,
                    'maxr': r,
                    'minc': c,
                    'maxc': c
                }
                stack: List[Tuple[int, int]] = [(r, c)]
                visited[r][c] = True
                while stack:
                    cr, cc = stack.pop()
                    comp['positions'].append((cr, cc))
                    comp['colors'].add(g[cr][cc])
                    comp['minr'] = min(comp['minr'], cr)
                    comp['maxr'] = max(comp['maxr'], cr)
                    comp['minc'] = min(comp['minc'], cc)
                    comp['maxc'] = max(comp['maxc'], cc)
                    for dr, dc in directions:
                        nr, nc = cr + dr, cc + dc
                        if 0 <= nr < rows and 0 <= nc < cols and g[nr][nc] != bg and not visited[nr][nc]:
                            visited[nr][nc] = True
                            stack.append((nr, nc))
                components.append(comp)
    return components

def program(g: List[List[int]]) -> List[List[int]]:
    bg = get_background(g)
    components = find_components(g, bg)
    multi_comps = [c for c in components if len(c['colors']) > 1]
    if len(multi_comps) != 1:
        raise ValueError("Expected one multi-color component")
    motif_comp = multi_comps[0]
    single_groups = {}
    for c in components:
        if len(c['colors']) == 1:
            colr = next(iter(c['colors']))
            if colr not in single_groups:
                single_groups[colr] = []
            single_groups[colr].append(c)
    if len(single_groups) != 1:
        raise ValueError("Expected one single-color group")
    mask_color = next(iter(single_groups))
    mask_comps = single_groups[mask_color]
    all_mask_pos = [(pr, pc) for comp in mask_comps for (pr, pc) in comp['positions']]
    if not all_mask_pos:
        raise ValueError("No mask positions")
    minr_mask = min(r for r, _ in all_mask_pos)
    maxr_mask = max(r for r, _ in all_mask_pos)
    minc_mask = min(c for _, c in all_mask_pos)
    maxc_mask = max(c for _, c in all_mask_pos)
    h_mask = maxr_mask - minr_mask + 1
    w_mask = maxc_mask - minc_mask + 1
    binary = [[1 if g[minr_mask + i][minc_mask + j] == mask_color else 0
               for j in range(w_mask)] for i in range(h_mask)]
    minr_m = motif_comp['minr']
    maxr_m = motif_comp['maxr']
    minc_m = motif_comp['minc']
    maxc_m = motif_comp['maxc']
    h_m = maxr_m - minr_m + 1
    w_m = maxc_m - minc_m + 1
    motif = [[g[minr_m + i][minc_m + j] for j in range(w_m)] for i in range(h_m)]
    output_h = h_mask * h_m
    output_w = w_mask * w_m
    out = [[bg for _ in range(output_w)] for _ in range(output_h)]
    for tile_i in range(h_mask):
        for tile_j in range(w_mask):
            if binary[tile_i][tile_j] == 1:
                for rr in range(h_m):
                    for cc in range(w_m):
                        out[tile_i * h_m + rr][tile_j * w_m + cc] = motif[rr][cc]
    return out
```