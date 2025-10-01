```python
from typing import List, Tuple

def get_dimensions(g: List[List[int]]) -> Tuple[int, int]:
    if not g or not g[0]:
        return 0, 0
    return len(g[0]), len(g)

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
        if start < sep:
            panels.append(g[start:sep])
        start = sep + 1
    if start < len(g):
        panels.append(g[start:])
    return panels

def get_panel_columns(g: List[List[int]], separators: List[int]) -> List[List[List[int]]]:
    if not g:
        return []
    h = len(g)
    w = len(g[0])
    panels = []
    start = 0
    for sep in separators:
        if start < sep:
            panel = [[g[i][j] for j in range(start, sep)] for i in range(h)]
            panels.append(panel)
        start = sep + 1
    if start < w:
        panel = [[g[i][j] for j in range(start, w)] for i in range(h)]
        panels.append(panel)
    return panels

def extract_panels(g: List[List[int]]) -> List[List[List[int]]]:
    w, h = get_dimensions(g)
    is_vertical_orient = h > w
    if is_vertical_orient:
        seps = find_horizontal_separators(g)
        return get_panel_rows(g, seps)
    else:
        seps = find_vertical_separators(g)
        return get_panel_columns(g, seps)

def get_color(block: List[List[int]]) -> int:
    if not block:
        return 0
    colors = set()
    for row in block:
        for cell in row:
            if cell not in (0, 1):
                colors.add(cell)
    return list(colors)[0] if colors else 0

def are_all_contiguous(template: List[List[int]], template_main: int, template_cross: int, out_cross: int) -> bool:
    if out_cross <= 0:
        return False
    for c in range(out_cross):
        slice_idx = 1 + c
        if slice_idx >= template_cross:
            return False
        filled = [j for j in range(template_main) if template[slice_idx][j] == 4]
        if filled:
            min_p = min(filled)
            max_p = max(filled)
            if max_p - min_p + 1 != len(filled):
                return False
    return True

def build_motif_vertical(template: List[List[int]], slice_idx: int, template_main: int, bg_color: int, acc_color: int) -> List[int]:
    motif = []
    for r in range(1, template_main):
        val = template[r][slice_idx]
        color = bg_color if val == 4 else acc_color
        motif.append(color)
    return motif

def build_motif_horizontal(template: List[List[int]], slice_idx: int, template_main: int, bg_color: int, acc_color: int) -> List[int]:
    motif = []
    for j in range(1, template_main):
        val = template[slice_idx][j]
        color = bg_color if val == 4 else acc_color
        motif.append(color)
    return motif

def program(g: List[List[int]]) -> List[List[int]]:
    if not g:
        return []
    panels = extract_panels(g)
    if len(panels) < 4:
        return []
    template = panels[0]
    if not template:
        return []
    bg_panel = panels[-2]
    acc_panel = panels[-1]
    bg_color = get_color(bg_panel)
    acc_color = get_color(acc_panel)
    if bg_color == 0 or acc_color == 0:
        return []
    w, h = get_dimensions(g)
    is_vertical = h > w
    if is_vertical:
        template_cross = w
        template_main = len(template)
        bg_main = len(bg_panel)
        acc_main = len(acc_panel)
        out_cross = template_cross - 2
        out_main = bg_main + acc_main - 2
        if out_cross <= 0 or out_main <= 0:
            return []
        motif_length = template_main - 1
        if motif_length <= 0:
            return []
        output = [[0] * out_cross for _ in range(out_main)]
        for k in range(out_cross):
            slice_idx = 1 + k
            if slice_idx >= template_cross:
                continue
            motif = build_motif_vertical(template, slice_idx, template_main, bg_color, acc_color)
            if len(motif) != motif_length:
                continue
            for i in range(out_main):
                pos = i % motif_length
                output[i][k] = motif[pos]
        return output
    else:
        template_cross = h
        template_main = len(template[0]) if template and template[0] else 0
        bg_main = len(bg_panel[0]) if bg_panel and bg_panel[0] else 0
        acc_main = len(acc_panel[0]) if acc_panel and acc_panel[0] else 0
        out_cross = template_cross - 2
        all_contig = are_all_contiguous(template, template_main, template_cross, out_cross)
        out_main = bg_main + acc_main - 2
        if all_contig:
            out_main += template_main
        if out_cross <= 0 or out_main <= 0:
            return []
        motif_length = template_main - 1
        if motif_length <= 0:
            return []
        output = [[0] * out_main for _ in range(out_cross)]
        for i in range(out_cross):
            slice_idx = 1 + i
            if slice_idx >= template_cross:
                continue
            motif = build_motif_horizontal(template, slice_idx, template_main, bg_color, acc_color)
            if len(motif) != motif_length:
                continue
            for k in range(out_main):
                pos = k % motif_length
                output[i][k] = motif[pos]
        return output
```