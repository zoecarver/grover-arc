```python
from typing import List

def get_dimensions(g: List[List[int]]) -> tuple:
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
    if not g or not g[0]:
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
    bg_color = get_color(bg_panel)
    acc_color = get_color(acc_panel)
    if bg_color == 0 or acc_color == 0:
        return []
    if is_vertical:
        temp_main = len(template)
        temp_cross = len(template[0]) if template else 0
        def get_panel_main(pan: List[List[int]]) -> int:
            return len(pan)
        def get_inner_value(temp: List[List[int]], j: int, c: int) -> int:
            return temp[1 + j][1 + c]
    else:
        temp_main = len(template[0]) if template else 0
        temp_cross = len(template)
        def get_panel_main(pan: List[List[int]]) -> int:
            return len(pan[0]) if pan and pan[0] else 0
        def get_inner_value(temp: List[List[int]], j: int, c: int) -> int:
            return temp[1 + c][1 + j]
    inner_main = temp_main - 2
    if inner_main <= 0:
        return []
    out_cross = temp_cross - 2
    if out_cross <= 0:
        return []
    period = inner_main + 1
    bg_m = get_panel_main(bg_panel)
    acc_m = get_panel_main(acc_panel)
    if is_vertical:
        out_main = bg_m + acc_m - 2
    else:
        def get_filled_for_slice(c: int) -> List[int]:
            filled = []
            for j in range(inner_main):
                if get_inner_value(template, j, c) == 4:
                    filled.append(j)
            return filled
        is_all_contiguous = True
        for c in range(out_cross):
            filled = get_filled_for_slice(c)
            if filled:
                min_p = min(filled)
                max_p = max(filled)
                if max_p - min_p + 1 != len(filled):
                    is_all_contiguous = False
                    break
        if is_all_contiguous:
            out_main = temp_main + bg_m + acc_m - 2
        else:
            out_main = bg_m + acc_m - 2
    if out_main <= 0:
        return []
    motif: List[List[int]] = [[0] * period for _ in range(out_cross)]
    for k in range(out_cross):
        for p in range(inner_main):
            val = get_inner_value(template, p, k)
            motif[k][p] = bg_color if val == 4 else acc_color
        motif[k][period - 1] = acc_color
    if is_vertical:
        out_grid = [[0] * out_cross for _ in range(out_main)]
        for i in range(out_main):
            pos = i % period
            for k in range(out_cross):
                out_grid[i][k] = motif[k][pos]
    else:
        out_grid = [[0] * out_main for _ in range(out_cross)]
        for k in range(out_cross):
            for i in range(out_main):
                pos = i % period
                out_grid[k][i] = motif[k][pos]
    return out_grid
```