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

def program(g: List[List[int]]) -> List[List[int]]:
    if not g or not g[0]:
        return []
    w, h = get_dimensions(g)
    orientation = 'vertical' if h > w else 'horizontal'
    if orientation == 'vertical':
        seps = find_horizontal_separators(g)
        panels = get_panel_rows(g, seps)
    else:
        seps = find_vertical_separators(g)
        panels = get_panel_columns(g, seps)
    if len(panels) < 4:
        return []
    template = panels[0]
    bg = get_color(panels[-2])
    acc = get_color(panels[-1])
    if bg == 0 or acc == 0:
        return []
    main_dim = get_block_length(template, orientation)
    cross_dim = get_block_length(template, 'horizontal' if orientation == 'vertical' else 'vertical')
    motif_len = main_dim
    out_cross = cross_dim - 2
    out_main = get_block_length(panels[-2], orientation) + get_block_length(panels[-1], orientation) - 2
    if out_main <= 0 or out_cross <= 0 or motif_len <= 0:
        return []
    if orientation == 'vertical':
        grid = [[bg for _ in range(out_cross)] for _ in range(out_main)]
        for j in range(out_cross):
            filled = [i for i in range(main_dim) if template[i][j + 1] == 4]
            for i in range(out_main):
                pos = i % motif_len
                if pos in filled:
                    grid[i][j] = acc
    else:
        grid = [[bg for _ in range(out_main)] for _ in range(out_cross)]
        for j in range(out_cross):
            row = template[j + 1]
            filled = [k for k in range(main_dim) if row[k] == 4]
            for i in range(out_main):
                pos = i % motif_len
                if pos in filled:
                    grid[j][i] = acc
    return grid
```