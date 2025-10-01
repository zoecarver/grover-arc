```python
from typing import List, Tuple

def get_dimensions(g: List[List[int]]) -> Tuple[int, int]:
    if not g:
        return 0, 0
    h = len(g)
    w = len(g[0])
    return w, h

def find_horizontal_separators(g: List[List[int]]) -> List[int]:
    h = len(g)
    separators = []
    for i in range(h):
        if all(cell == 1 for cell in g[i]):
            separators.append(i)
    return separators

def find_vertical_separators(g: List[List[int]]) -> List[int]:
    if not g:
        return []
    w = len(g[0])
    h = len(g)
    separators = []
    for j in range(w):
        if all(g[i][j] == 1 for i in range(h)):
            separators.append(j)
    return separators

def get_panel_rows(g: List[List[int]], separators: List[int]) -> List[List[List[int]]]:
    panels = []
    start = 0
    for sep in separators:
        if sep > start:
            panels.append(g[start:sep])
        start = sep + 1
    if start < len(g):
        panels.append(g[start:])
    return panels

def get_panel_columns(g: List[List[int]], separators: List[int]) -> List[List[List[int]]]:
    if not g:
        return []
    h = len(g)
    panels = []
    start = 0
    for sep in separators:
        if sep > start:
            panels.append([row[start:sep] for row in g])
        start = sep + 1
    if start < len(g[0]):
        panels.append([row[start:] for row in g])
    return panels

def get_orientation(g: List[List[int]]) -> str:
    w, h = get_dimensions(g)
    return 'vertical' if h > w else 'horizontal'

def extract_panels(g: List[List[int]]) -> List[List[List[int]]]:
    orientation = get_orientation(g)
    if orientation == 'vertical':
        seps = find_horizontal_separators(g)
        return get_panel_rows(g, seps)
    else:
        seps = find_vertical_separators(g)
        return get_panel_columns(g, seps)

def get_color(block: List[List[int]]) -> int:
    colors = {cell for row in block for cell in row if cell not in {0, 1}}
    return list(colors)[0] if colors else 0

def get_panel_main(panel: List[List[int]], orientation: str) -> int:
    if not panel:
        return 0
    if orientation == 'vertical':
        return len(panel)
    else:
        return len(panel[0]) if panel and panel[0] else 0

def compute_out_main(panels: List[List[List[int]]], orientation: str, p0_main: int) -> int:
    if len(panels) < 4:
        return 0
    p1m = get_panel_main(panels[1], orientation)
    p2m = get_panel_main(panels[2], orientation)
    p3m = get_panel_main(panels[3], orientation)
    if orientation == 'vertical':
        return max(0, p2m + p3m - 2)
    else:
        if p1m == p0_main + 2:
            return max(0, p1m + p2m + p3m - p0_main + 1)
        else:
            return max(0, p2m + p3m - 2)

def get_filled_pos(panel: List[List[int]], slice_idx: int, orientation: str) -> List[int]:
    if orientation == 'vertical':
        return [r for r in range(len(panel)) if panel[r][slice_idx] == 4]
    else:
        if slice_idx >= len(panel):
            return []
        row = panel[slice_idx]
        return [j for j in range(len(row)) if row[j] == 4]

def build_motif(filled_pos: List[int], motif_len: int, color1: int, color2: int) -> List[int]:
    motif = [color2] * motif_len
    for p in filled_pos:
        idx = p - 1
        if 0 <= idx < motif_len:
            motif[idx] = color1
    return motif

def tile_motif(motif: List[int], out_len: int) -> List[int]:
    if not motif or out_len <= 0:
        return [0] * out_len
    mlen = len(motif)
    tiled = []
    num_full = out_len // mlen
    for _ in range(num_full):
        tiled.extend(motif)
    rem = out_len % mlen
    tiled.extend(motif[:rem])
    return tiled

def program(g: List[List[int]]) -> List[List[int]]:
    if not g:
        return []
    panels = extract_panels(g)
    if len(panels) < 4:
        return []
    orientation = get_orientation(g)
    p0 = panels[0]
    color1 = get_color(panels[2])
    color2 = get_color(panels[3])
    if color1 == 0 and color2 == 0:
        return []
    if orientation == 'vertical':
        p0_main = get_panel_main(p0, orientation)
        _, cross_dim = get_dimensions(g)
    else:
        p0_main = get_panel_main(p0, orientation)
        cross_dim, _ = get_dimensions(g)
    out_cross = cross_dim - 2
    if out_cross < 1:
        return []
    out_main = compute_out_main(panels, orientation, p0_main)
    if out_main < 1:
        return []
    motif_len = p0_main - 1
    if motif_len < 1:
        motif_len = 1
    if orientation == 'vertical':
        out_h = out_main
        out_w = out_cross
        grid = [[0] * out_w for _ in range(out_h)]
        panel_w = len(p0[0]) if p0 else 0
        for k in range(out_w):
            j = k + 1
            if j >= panel_w:
                continue
            filled_pos = get_filled_pos(p0, j, orientation)
            motif = build_motif(filled_pos, motif_len, color1, color2)
            tiled = tile_motif(motif, out_h)
            for r in range(out_h):
                grid[r][k] = tiled[r]
    else:
        out_h = out_cross
        out_w = out_main
        grid = [[0] * out_w for _ in range(out_h)]
        panel_h = len(p0)
        for k in range(out_h):
            i = k + 1
            if i >= panel_h:
                continue
            filled_pos = get_filled_pos(p0, i, orientation)
            motif = build_motif(filled_pos, motif_len, color1, color2)
            tiled = tile_motif(motif, out_w)
            for jj in range(out_w):
                grid[k][jj] = tiled[jj]
    return grid
```