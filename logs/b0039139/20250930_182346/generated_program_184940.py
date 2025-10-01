```python
from typing import List

def get_dimensions(g: List[List[int]]) -> tuple:
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
    w = len(g[0]) if g else 0
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
        panel = g[start:sep]
        panels.append(panel)
        start = sep + 1
    if start < len(g):
        panels.append(g[start:])
    return panels

def get_panel_columns(g: List[List[int]], separators: List[int]) -> List[List[List[int]]]:
    h = len(g)
    panels = []
    start = 0
    for sep in separators:
        panel = [row[start:sep] for row in g]
        panels.append(panel)
        start = sep + 1
    if g and start < len(g[0]):
        panel = [row[start:] for row in g]
        panels.append(panel)
    return panels

def get_color(block: List[List[int]]) -> int:
    colors = set()
    for row in block:
        for cell in row:
            if cell != 0 and cell != 1:
                colors.add(cell)
    return list(colors)[0] if colors else 0

def get_block_length(panel: List[List[int]], orientation: str) -> int:
    if not panel:
        return 0
    if orientation == 'vertical':
        return len(panel)
    else:
        return len(panel[0]) if panel else 0

def get_orientation_and_cross(w: int, h: int) -> tuple:
    if h > w:
        return 'vertical', w
    else:
        return 'horizontal', h

def compute_out_main(orientation: str, block1_main: int, block2_main: int, cross: int, num_sep: int) -> int:
    if orientation == 'vertical':
        return block1_main + block2_main - 2
    else:
        if block1_main > cross:
            return block1_main + block2_main - 2
        else:
            return block1_main + block2_main + num_sep

def get_filled_pos(panel: List[List[int]], slice_idx: int, fill_value: int, is_vertical: bool, panel_main: int) -> List[int]:
    filled_pos = []
    if is_vertical:
        for r in range(panel_main):
            if panel[r][slice_idx] == fill_value:
                filled_pos.append(r)
    else:
        for j in range(panel_main):
            if panel[slice_idx][j] == fill_value:
                filled_pos.append(j)
    return filled_pos

def build_motif(filled_pos: List[int], panel_main: int, length: int, color1: int, color2: int) -> List[int]:
    if not filled_pos:
        motif = [color1 if i % 2 == 0 else color2 for i in range(length)]
        return motif
    num = len(filled_pos)
    minp = min(filled_pos)
    maxp = max(filled_pos)
    if num == maxp - minp + 1:
        block1 = num
        first = minp
        p = (first * length) // panel_main
        motif = [color2] * length
        for ii in range(block1):
            idx = p + ii
            if idx < length:
                motif[idx] = color1
        return motif
    else:
        motif = [color1 if i % 2 == 0 else color2 for i in range(length)]
        return motif

def tile_motif_to_main(motif: List[int], out_main: int, length: int) -> List[int]:
    if length == 0:
        return [motif[0]] * out_main if motif else []
    result = []
    num_full = out_main // length
    remainder = out_main % length
    for _ in range(num_full):
        result.extend(motif)
    result.extend(motif[:remainder])
    return result

def program(g: List[List[int]]) -> List[List[int]]:
    w, h = get_dimensions(g)
    if w == 0 or h == 0:
        return []
    orientation, cross = get_orientation_and_cross(w, h)
    if orientation == 'vertical':
        separators = find_horizontal_separators(g)
        panels = get_panel_rows(g, separators)
    else:
        separators = find_vertical_separators(g)
        panels = get_panel_columns(g, separators)
    if len(panels) < 4:
        return []
    panel0_main = get_block_length(panels[0], orientation)
    block1_main = get_block_length(panels[2], orientation)
    block2_main = get_block_length(panels[3], orientation)
    num_sep = len(separators)
    out_cross = cross - 2
    if out_cross < 1:
        return []
    out_main = compute_out_main(orientation, block1_main, block2_main, cross, num_sep)
    if out_main < 1:
        return []
    color1 = get_color(panels[2])
    color2 = get_color(panels[3])
    if color1 == 0 and color2 == 0:
        return []
    length = panel0_main - 1 if panel0_main > 0 else 1
    is_vertical = orientation == 'vertical'
    if is_vertical:
        out_height = out_main
        out_width = out_cross
        out_grid = [[0] * out_width for _ in range(out_height)]
        panel0 = panels[0]
        for k in range(out_width):
            input_slice = k + 1
            filled_pos = get_filled_pos(panel0, input_slice, 4, is_vertical, panel0_main)
            motif = build_motif(filled_pos, panel0_main, length, color1, color2)
            column_values = tile_motif_to_main(motif, out_height, length)
            for i in range(out_height):
                out_grid[i][k] = column_values[i]
    else:
        out_height = out_cross
        out_width = out_main
        out_grid = [[0] * out_width for _ in range(out_height)]
        panel0 = panels[0]
        for k in range(out_height):
            input_slice = k + 1
            filled_pos = get_filled_pos(panel0, input_slice, 4, is_vertical, panel0_main)
            motif = build_motif(filled_pos, panel0_main, length, color1, color2)
            row_values = tile_motif_to_main(motif, out_width, length)
            for i in range(out_width):
                out_grid[k][i] = row_values[i]
    return out_grid
```