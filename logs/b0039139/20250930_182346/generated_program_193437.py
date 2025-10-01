```python
from typing import List

def get_dimensions(g: List[List[int]]) -> tuple:
    if not g:
        return 0, 0
    h = len(g)
    w = len(g[0]) if g[0] else 0
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

def extract_panels(g: List[List[int]]) -> List[List[List[int]]]:
    if not g:
        return []
    w, h = get_dimensions(g)
    orientation = 'vertical' if h > w else 'horizontal'
    if orientation == 'vertical':
        seps = find_horizontal_separators(g)
        return get_panel_rows(g, seps)
    else:
        seps = find_vertical_separators(g)
        return get_panel_columns(g, seps)

def get_color(block: List[List[int]]) -> int:
    colors = {cell for row in block for cell in row if cell not in {0, 1}}
    return list(colors)[0] if colors else 0

def get_block_length(block: List[List[int]], orientation: str) -> int:
    if not block:
        return 0
    if orientation == 'vertical':
        return len(block)
    else:
        return len(block[0]) if block else 0

def get_filled_pos(panel: List[List[int]], slice_idx: int, fill_value: int, is_vertical: bool, panel_main: int) -> List[int]:
    filled_pos = []
    if is_vertical:
        for r in range(panel_main):
            if panel[r][slice_idx] == fill_value:
                filled_pos.append(r)
    else:
        if slice_idx >= len(panel):
            return []
        row = panel[slice_idx]
        for j in range(panel_main):
            if row[j] == fill_value:
                filled_pos.append(j)
    return filled_pos

def build_motif(filled: List[int], motif_len: int, acc: int, bg: int) -> List[int]:
    if not filled:
        return [bg] * motif_len
    minp = min(filled)
    maxp = max(filled)
    l = len(filled)
    is_contig = (maxp - minp + 1 == l) and l > 0
    motif = [bg] * motif_len
    if is_contig:
        block_l = motif_len - l
        if block_l > 0:
            start = maxp
            for off in range(block_l):
                jj = (start + off) % motif_len
                motif[jj] = acc
    else:
        for p in filled:
            jj = p % motif_len
            motif[jj] = acc
    return motif

def program(g: List[List[int]]) -> List[List[int]]:
    panels = extract_panels(g)
    if len(panels) < 4:
        return []
    template = panels[0]
    if not template:
        return []
    bg = get_color(panels[2])
    acc = get_color(panels[3])
    if bg == 0 or acc == 0:
        return []
    w, h = get_dimensions(g)
    is_vertical = h > w
    ori = 'vertical' if is_vertical else 'horizontal'
    template_main = get_block_length(template, ori)
    template_cross = get_block_length(template, 'horizontal' if is_vertical else 'vertical')
    out_cross = max(0, template_cross - 2)
    if out_cross == 0:
        return []
    motif_len = max(1, template_main - 1)
    p1m = get_block_length(panels[1], ori) if len(panels) > 1 else 0
    p2m = get_block_length(panels[2], ori)
    p3m = get_block_length(panels[3], ori)
    out_main = max(0, p2m + p3m - 2)
    if not is_vertical and p1m >= 7:
        out_main += p1m - 2
    if out_main == 0:
        return []
    if is_vertical:
        out_g = [[0] * out_cross for _ in range(out_main)]
    else:
        out_g = [[0] * out_main for _ in range(out_cross)]
    for k in range(out_cross):
        filled = get_filled_pos(template, k, 4, is_vertical, template_main)
        motif = build_motif(filled, motif_len, acc, bg)
        for i in range(out_main):
            color = motif[i % motif_len]
            if is_vertical:
                out_g[i][k] = color
            else:
                out_g[k][i] = color
    return out_g
```