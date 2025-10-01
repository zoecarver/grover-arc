```python
from typing import List, Tuple

def get_dimensions(g: List[List[int]]) -> Tuple[int, int]:
    if not g:
        return 0, 0
    h = len(g)
    w = len(g[0]) if h > 0 and g[0] else 0
    return w, h

def find_horizontal_separators(g: List[List[int]]) -> List[int]:
    h = len(g)
    return [i for i in range(h) if all(cell == 1 for cell in g[i])]

def find_vertical_separators(g: List[List[int]]) -> List[int]:
    if not g:
        return []
    w = len(g[0])
    h = len(g)
    return [j for j in range(w) if all(g[i][j] == 1 for i in range(h))]

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

def get_color(block: List[List[int]]) -> int:
    colors = {cell for row in block for cell in row if cell not in {0, 1}}
    return list(colors)[0] if colors else 0

def is_vertical(g: List[List[int]]) -> bool:
    w, h = get_dimensions(g)
    return h > w

def extract_panels(g: List[List[int]]) -> List[List[List[int]]]:
    if is_vertical(g):
        seps = find_horizontal_separators(g)
        return get_panel_rows(g, seps)
    else:
        seps = find_vertical_separators(g)
        return get_panel_columns(g, seps)

def get_template_main_cross(panels: List[List[List[int]]], is_vertical: bool) -> Tuple[int, int]:
    template = panels[0] if panels else []
    if not template:
        return 0, 0
    if is_vertical:
        main = len(template)
        cross = len(template[0]) if template[0] else 0
    else:
        main = len(template[0]) if template and template[0] else 0
        cross = len(template)
    return main, cross

def get_panel_main(pan: List[List[int]], is_vertical: bool) -> int:
    if not pan:
        return 0
    if is_vertical:
        return len(pan)
    else:
        return len(pan[0]) if pan[0] else 0

def are_all_contiguous(template: List[List[int]], main: int, cross: int, out_cross: int) -> bool:
    if out_cross <= 0:
        return False
    for c in range(out_cross):
        slice_idx = 1 + c
        if slice_idx >= cross:
            return False
        filled = [j for j in range(main) if template[slice_idx][j] == 4]
        if filled:
            min_p = min(filled)
            max_p = max(filled)
            if max_p - min_p + 1 != len(filled):
                return False
    return True

def build_motif(template: List[List[int]], slice_idx: int, main: int, bg: int, acc: int, is_vertical: bool) -> List[int]:
    motif = []
    if is_vertical:
        for r in range(1, main):
            val = template[r][slice_idx]
            motif.append(bg if val == 4 else acc)
    else:
        for j in range(1, main):
            val = template[slice_idx][j]
            motif.append(bg if val == 4 else acc)
    return motif

def program(g: List[List[int]]) -> List[List[int]]:
    if not g:
        return []
    panels = extract_panels(g)
    if len(panels) < 4:
        return []
    template = panels[0]
    bg_panel = panels[-2]
    acc_panel = panels[-1]
    bg = get_color(bg_panel)
    acc = get_color(acc_panel)
    if bg == 0 or acc == 0:
        return []
    vert = is_vertical(g)
    main, cross = get_template_main_cross(panels, vert)
    out_cross = cross - 2
    if out_cross <= 0:
        return []
    motif_len = main - 1
    if motif_len <= 0:
        return []
    bg_m = get_panel_main(bg_panel, vert)
    acc_m = get_panel_main(acc_panel, vert)
    out_main = bg_m + acc_m - 2
    if out_main <= 0:
        return []
    if not vert:
        if are_all_contiguous(template, main, cross, out_cross):
            out_main += main
    if out_main <= 0:
        return []
    if vert:
        out_h = out_main
        out_w = out_cross
        output = [[0] * out_w for _ in range(out_h)]
        for k in range(out_w):
            slice_idx = 1 + k
            if slice_idx >= cross:
                continue
            motif = build_motif(template, slice_idx, main, bg, acc, vert)
            for i in range(out_h):
                if i % motif_len < len(motif):
                    output[i][k] = motif[i % motif_len]
    else:
        out_h = out_cross
        out_w = out_main
        output = [[0] * out_w for _ in range(out_h)]
        for c in range(out_h):
            slice_idx = 1 + c
            if slice_idx >= cross:
                continue
            motif = build_motif(template, slice_idx, main, bg, acc, vert)
            for i in range(out_w):
                if i % motif_len < len(motif):
                    output[c][i] = motif[i % motif_len]
    return output
```