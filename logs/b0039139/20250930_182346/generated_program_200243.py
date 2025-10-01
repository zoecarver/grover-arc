```python
from typing import List, Tuple

def get_dimensions(g: List[List[int]]) -> Tuple[int, int]:
    if not g:
        return 0, 0
    h = len(g)
    w = len(g[0]) if h > 0 else 0
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
            panels.append([[g[i][j] for j in range(start, sep)] for i in range(h)])
        start = sep + 1
    if start < len(g[0]):
        panels.append([[g[i][j] for j in range(start, len(g[0]))] for i in range(h)])
    return panels

def get_color(block: List[List[int]]) -> int:
    colors = set(cell for row in block for cell in row if cell not in {0, 1})
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

def get_template_main_cross(template: List[List[int]], is_vertical: bool) -> Tuple[int, int]:
    if not template:
        return 0, 0
    if is_vertical:
        main = len(template)
        cross = len(template[0]) if template else 0
    else:
        main = len(template[0]) if template else 0
        cross = len(template)
    return main, cross

def get_panel_main(panel: List[List[int]], is_vertical: bool) -> int:
    if not panel:
        return 0
    if is_vertical:
        return len(panel)
    else:
        return len(panel[0]) if panel and panel[0] else 0

def program(g: List[List[int]]) -> List[List[int]]:
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
    is_vert = is_vertical(g)
    main, cross = get_template_main_cross(template, is_vert)
    l = main - 1
    out_cross_num = cross - 2
    if l <= 0 or out_cross_num <= 0:
        return []
    bg_main = get_panel_main(bg_panel, is_vert)
    acc_main = get_panel_main(acc_panel, is_vert)
    out_main_num = bg_main + acc_main - 2
    if out_main_num <= 0:
        return []
    # build motif
    if is_vert:
        motif = [[0] * out_cross_num for _ in range(l)]
        for rr in range(l):
            row_idx = rr + 1
            for cc in range(out_cross_num):
                col_idx = cc + 1
                cell = template[row_idx][col_idx]
                motif[rr][cc] = bg if cell == 4 else acc
        out_g = [[0] * out_cross_num for _ in range(out_main_num)]
        for i in range(out_main_num):
            rid = i % l
            out_g[i] = motif[rid][:]
    else:
        motif = [[0] * l for _ in range(out_cross_num)]
        for kk in range(out_cross_num):
            row_idx = kk + 1
            for jj in range(l):
                col_idx = jj + 1
                cell = template[row_idx][col_idx]
                motif[kk][jj] = bg if cell == 4 else acc
        out_g = [[0] * out_main_num for _ in range(out_cross_num)]
        for kk in range(out_cross_num):
            mrow = motif[kk]
            for j in range(out_main_num):
                out_g[kk][j] = mrow[j % l]
    return out_g
```