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
            panels.append([[g[i][j] for j in range(start, sep)] for i in range(h)])
        start = sep + 1
    if start < len(g[0]):
        panels.append([[g[i][j] for j in range(start, len(g[0]))] for i in range(h)])
    return panels

def get_color(block: List[List[int]]) -> int:
    colors = {cell for row in block for cell in row if cell not in {0, 1}}
    return list(colors)[0] if colors else 0

def program(g: List[List[int]]) -> List[List[int]]:
    w, h = get_dimensions(g)
    if h == 0 or w == 0:
        return []
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
    bg_color = get_color(bg_panel)
    acc_color = get_color(acc_panel)
    if bg_color == 0 or acc_color == 0:
        return []
    if is_vertical:
        temp_h = len(template) if template else 0
        temp_w = len(template[0]) if template and template[0] else 0
        main_dim = temp_h
        cross_dim = temp_w
        bg_main = len(bg_panel) if bg_panel else 0
        acc_main = len(acc_panel) if acc_panel else 0
    else:
        temp_h = len(template) if template else 0
        temp_w = len(template[0]) if template and template[0] else 0
        main_dim = temp_w
        cross_dim = temp_h
        bg_main = len(bg_panel[0]) if bg_panel and bg_panel[0] else 0
        acc_main = len(acc_panel[0]) if acc_panel and acc_panel[0] else 0
    if main_dim < 2 or cross_dim < 2:
        return []
    inner_main = main_dim - 2
    inner_cross = cross_dim - 2
    if inner_main <= 0 or inner_cross <= 0:
        return []
    border_main = 1
    border_cross = 1
    out_main = bg_main + acc_main - 2
    if out_main <= 0:
        return []
    all_contig = False
    if not is_vertical:
        all_contig = True
        for k in range(inner_cross):
            filled = []
            for j in range(inner_main):
                if is_vertical:
                    val = template[border_main + j][border_cross + k]
                else:
                    val = template[border_cross + k][border_main + j]
                if val == 4:
                    filled.append(j)
            if filled and max(filled) - min(filled) + 1 != len(filled):
                all_contig = False
                break
        if all_contig:
            out_main += main_dim
    if is_vertical:
        out = [[0] * inner_cross for _ in range(out_main)]
        for k in range(inner_cross):
            motif = []
            for j in range(inner_main):
                val = template[border_main + j][border_cross + k]
                motif.append(bg_color if val == 4 else acc_color)
            motif.append(acc_color)
            period = len(motif)
            for i in range(out_main):
                out[i][k] = motif[i % period]
        return out
    else:
        out = [[0] * out_main for _ in range(inner_cross)]
        for k in range(inner_cross):
            motif = []
            for j in range(inner_main):
                val = template[border_cross + k][border_main + j]
                motif.append(bg_color if val == 4 else acc_color)
            motif.append(acc_color)
            period = len(motif)
            for jj in range(out_main):
                out[k][jj] = motif[jj % period]
        return out
```