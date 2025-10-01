```python
from typing import List

def program(g: List[List[int]]) -> List[List[int]]:
    def get_dimensions(g: List[List[int]]) -> tuple[int, int]:
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
        w, h = get_dimensions(g)
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

    def extract_panels(g: List[List[int]]) -> List[List[List[int]]]:
        w, h = get_dimensions(g)
        if h > w:
            seps = find_horizontal_separators(g)
            return get_panel_rows(g, seps)
        else:
            seps = find_vertical_separators(g)
            return get_panel_columns(g, seps)

    def get_color(block: List[List[int]]) -> int:
        colors = {cell for row in block for cell in row if cell not in {0, 1}}
        return list(colors)[0] if colors else 0

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

    w, h = get_dimensions(g)
    is_vertical = h > w
    template_w, template_h = get_dimensions(template)
    template_cross = template_w if is_vertical else template_h
    template_main = template_h if is_vertical else template_w
    out_cross = max(0, template_cross - 2)
    if out_cross == 0:
        return []

    if is_vertical:
        bg_main = len(bg_panel) if bg_panel else 0
        acc_main = len(acc_panel) if acc_panel else 0
    else:
        bg_main = len(bg_panel[0]) if bg_panel and bg_panel[0] else 0
        acc_main = len(acc_panel[0]) if acc_panel and acc_panel[0] else 0

    # Check if all slices are contiguous
    fill_value = 4
    border = 1
    all_contiguous = True
    for k in range(out_cross):
        slice_idx = k + border
        if is_vertical:
            if slice_idx >= template_w:
                continue
            filled = [r for r in range(template_main) if template[r][slice_idx] == fill_value]
        else:
            if slice_idx >= template_h:
                continue
            filled = [c for c in range(template_main) if template[slice_idx][c] == fill_value]
        if not filled:
            all_contiguous = False
            break
        min_p = min(filled)
        max_p = max(filled)
        if len(filled) != max_p - min_p + 1:
            all_contiguous = False
            break

    if is_vertical or not all_contiguous:
        out_main = max(0, bg_main + acc_main - 2)
    else:
        out_main = max(0, bg_main + acc_main + template_main - 2)
    if out_main == 0:
        return []

    motif_len = max(1, template_main - 1)

    if is_vertical:
        out_g = [[bg] * out_cross for _ in range(out_main)]
    else:
        out_g = [[bg] * out_main for _ in range(out_cross)]

    for k in range(out_cross):
        slice_idx = k + border
        if is_vertical:
            if slice_idx >= template_w:
                continue
            filled_set = set(r for r in range(template_main) if template[r][slice_idx] == fill_value)
            for i in range(out_main):
                if i % motif_len in filled_set:
                    out_g[i][k] = acc
        else:
            if slice_idx >= template_h:
                continue
            filled_set = set(c for c in range(template_main) if template[slice_idx][c] == fill_value)
            for i in range(out_main):
                if i % motif_len in filled_set:
                    out_g[k][i] = acc

    return out_g
```