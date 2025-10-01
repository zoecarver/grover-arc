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
            panels.append([row[:] for row in g[start:sep]])
        start = sep + 1
    if start < len(g):
        panels.append([row[:] for row in g[start:]])
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

def program(g: List[List[int]]) -> List[List[int]]:
    if not g:
        return []
    w, h = get_dimensions(g)
    is_vertical = h > w
    if is_vertical:
        seps = find_horizontal_separators(g)
        panels = get_panel_rows(g, seps)
    else:
        seps = find_vertical_separators(g)
        panels = get_panel_columns(g, seps)
    if len(panels) < 4:
        return []
    template = panels[0]
    bg_panel = panels[-2]
    acc_panel = panels[-1]
    bg = get_color(bg_panel)
    acc = get_color(acc_panel)
    if bg == 0 and acc == 0:
        return []
    if is_vertical:
        template_h = len(template)
        template_w = get_dimensions(template)[0]
        out_cross = template_w - 2
        if out_cross <= 0 or template_h < 3:
            return []
        motif_len = template_h - 2
        out_main = out_cross * motif_len - 1
        output = [[bg] * out_cross for _ in range(out_main)]
        inner_rows_start = 1
        inner_rows_end = template_h - 1
        for k in range(out_cross):
            c = 1 + k
            motif = [acc if template[r][c] == 0 else bg for r in range(inner_rows_start, inner_rows_end)]
            pos = 0
            for _ in range(out_cross - 1):
                for p in range(motif_len):
                    output[pos][k] = motif[p]
                    pos += 1
            for p in range(motif_len - 1):
                output[pos][k] = motif[p]
                pos += 1
        return output
    else:
        template_h = len(template)
        template_w = get_dimensions(template)[0]
        out_cross = template_h - 2
        if out_cross <= 0 or template_w < 2:
            return []
        motif_len = template_w - 1
        out_main = out_cross * motif_len - 1
        output = [[bg] * out_main for _ in range(out_cross)]
        inner_cols_start = 1
        inner_cols_end = template_w
        for k in range(out_cross):
            r = 1 + k
            motif = [acc if template[r][c] == 0 else bg for c in range(inner_cols_start, inner_cols_end)]
            pos = 0
            for _ in range(out_cross - 1):
                for p in range(motif_len):
                    output[k][pos] = motif[p]
                    pos += 1
            for p in range(motif_len - 1):
                output[k][pos] = motif[p]
                pos += 1
        return output
```