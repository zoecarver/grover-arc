```python
from typing import List
from collections import Counter

def flatten_grid(g: List[List[int]]) -> List[int]:
    return [cell for row in g for cell in row]

def identify_background(g: List[List[int]]) -> int:
    flat = flatten_grid(g)
    if not flat:
        return 0
    return Counter(flat).most_common(1)[0][0]

def find_divider_columns(g: List[List[int]], bg: int) -> List[int]:
    h = len(g)
    if h == 0:
        return []
    w = len(g[0])
    div_cols = []
    for j in range(w):
        first = g[0][j]
        if first != bg and all(g[r][j] == first for r in range(1, h)):
            div_cols.append(j)
    return sorted(div_cols)

def compute_num_panels(div_cols: List[int]) -> int:
    return len(div_cols) + 1

def compute_panel_width(w: int, num_panels: int) -> int:
    return w // num_panels if num_panels > 0 else w

def get_panel_ranges(div_cols: List[int], w: int) -> List[tuple[int, int]]:
    ranges = []
    prev_end = 0
    for dc in div_cols:
        ranges.append((prev_end, dc))
        prev_end = dc + 1
    ranges.append((prev_end, w))
    return ranges

def extract_panel(g: List[List[int]], start: int, end: int) -> List[List[int]]:
    h = len(g)
    return [[g[r][j] for j in range(start, end)] for r in range(h)]

def compute_consensus(panels: List[List[List[int]]]) -> List[List[int]]:
    if not panels:
        return []
    h = len(panels[0])
    w = len(panels[0][0]) if h > 0 else 0
    num_p = len(panels)
    result = []
    for r in range(h):
        row = []
        for c in range(w):
            values = [panels[k][r][c] for k in range(num_p)]
            if not values:
                row.append(0)
                continue
            count = Counter(values)
            mode = count.most_common(1)[0][0]
            row.append(mode)
        result.append(row)
    return result

def program(g: List[List[int]]) -> List[List[int]]:
    if not g or not g[0]:
        return g
    bg = identify_background(g)
    div_cols = find_divider_columns(g, bg)
    num_panels = compute_num_panels(div_cols)
    w = len(g[0])
    panel_w = compute_panel_width(w, num_panels)
    ranges = get_panel_ranges(div_cols, w)
    panels = []
    for start, end in ranges:
        # Truncate or pad if necessary, but examples match
        actual_w = end - start
        if actual_w != panel_w:
            # For robustness, take first panel_w cols
            end = min(end, start + panel_w)
        panel = extract_panel(g, start, end)
        # If shorter, pad with bg
        if len(panel[0]) < panel_w and h > 0:
            for row in panel:
                row.extend([bg] * (panel_w - len(row)))
        panels.append(panel)
    # If wrong number, adjust
    while len(panels) < num_panels:
        panels.append([[bg] * panel_w for _ in range(len(g))])
    output = compute_consensus(panels[:num_panels])
    return output
```