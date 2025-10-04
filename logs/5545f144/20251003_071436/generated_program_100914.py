```python
from typing import List
from collections import Counter

def find_background(g: List[List[int]]) -> int:
    if not g or not g[0]:
        return 0
    flat = [cell for row in g for cell in row]
    return Counter(flat).most_common(1)[0][0]

def find_divider_color(g: List[List[int]], background: int) -> int:
    R = len(g)
    if R == 0:
        return -1
    C = len(g[0])
    full_count = Counter()
    for j in range(C):
        col = [g[i][j] for i in range(R)]
        if len(set(col)) == 1 and col[0] != background:
            full_count[col[0]] += 1
    if full_count:
        return full_count.most_common(1)[0][0]
    return -1

def get_divider_columns(g: List[List[int]], D: int) -> List[int]:
    R = len(g)
    C = len(g[0]) if R > 0 else 0
    div_cols = []
    for j in range(C):
        col = [g[i][j] for i in range(R)]
        if all(x == D for x in col):
            div_cols.append(j)
    return sorted(div_cols)

def extract_panels(g: List[List[int]], divider_cols: List[int], W: int, R: int) -> List[List[List[int]]]:
    num_panels = len(divider_cols) + 1
    panels = []
    s = 0
    for i in range(num_panels):
        if i < len(divider_cols):
            e = divider_cols[i]
        else:
            e = len(g[0])
        panel = [g[r][s:e] for r in range(R)]
        panels.append(panel)
        if i < len(divider_cols):
            s = divider_cols[i] + 1
    return panels

def combine_panels(panels: List[List[List[int]]], background: int) -> List[List[int]]:
    if not panels:
        return []
    R = len(panels[0])
    W = len(panels[0][0])
    O = []
    for r in range(R):
        row_colors = [p[r] for p in panels]
        combined_row = []
        for c in range(W):
            colors = [row[c] for row in row_colors]
            count = Counter(colors)
            mode = count.most_common(1)[0][0]
            combined_row.append(mode)
        O.append(combined_row)
    return O

def program(g: List[List[int]]) -> List[List[int]]:
    if not g:
        return []
    R = len(g)
    C = len(g[0])
    background = find_background(g)
    D = find_divider_color(g, background)
    if D == -1:
        return [row[:] for row in g]
    divider_cols = get_divider_columns(g, D)
    num_dividers = len(divider_cols)
    num_panels = num_dividers + 1
    total_panel = C - num_dividers
    if total_panel % num_panels != 0:
        return [row[:] for row in g]
    W = total_panel // num_panels
    panels = extract_panels(g, divider_cols, W, R)
    return combine_panels(panels, background)
```