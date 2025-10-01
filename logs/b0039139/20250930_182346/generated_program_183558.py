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

def get_block_length(panel: List[List[int]], orientation: str) -> int:
    if not panel:
        return 0
    if orientation == 'vertical':
        return len(panel)
    else:
        return len(panel[0]) if panel else 0

def get_color(block: List[List[int]]) -> int:
    colors = set()
    for row in block:
        for cell in row:
            if cell != 0 and cell != 1:
                colors.add(cell)
    return list(colors)[0] if colors else 0

def program(g: List[List[int]]) -> List[List[int]]:
    w, h = get_dimensions(g)
    if h > w:
        orientation = 'vertical'
        separators = find_horizontal_separators(g)
        panels = get_panel_rows(g, separators)
    else:
        orientation = 'horizontal'
        separators = find_vertical_separators(g)
        panels = get_panel_columns(g, separators)
    if len(panels) < 4:
        return []
    template_a = panels[0]
    template_b = panels[1]
    block_a = panels[2]
    block_b = panels[3]
    a = get_color(block_a)
    b = get_color(block_b)
    cross = w if orientation == 'vertical' else h
    large_a = get_block_length(block_a, orientation)
    large_b = get_block_length(block_b, orientation)
    out_cross = cross - 2
    out_large = large_a + large_b - 2
    if out_cross <= 0 or out_large <= 0:
        return []
    if orientation == 'vertical':
        out_g = [[a for _ in range(out_cross)] for _ in range(out_large)]
        for i in range(out_large):
            for j in range(out_cross):
                if (i + j) % 2 == 1:
                    out_g[i][j] = b
    else:
        out_g = [[a for _ in range(out_large)] for _ in range(out_cross)]
        for i in range(out_cross):
            for j in range(out_large):
                if (i + j) % 2 == 1:
                    out_g[i][j] = b
    return out_g
```