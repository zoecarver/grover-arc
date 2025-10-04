```python
from typing import List
from collections import Counter

def get_background(g: List[List[int]]) -> int:
    flat = [cell for row in g for cell in row]
    if not flat:
        return 0
    return Counter(flat).most_common(1)[0][0]

def get_line_columns(g: List[List[int]], background: int) -> List[int]:
    if not g:
        return []
    h = len(g)
    w = len(g[0]) if g and g[0] else 0
    lines = []
    for c in range(w):
        if w <= c:
            break
        col_val = g[0][c]
        if col_val != background:
            is_line = True
            for r in range(1, h):
                if g[r][c] != col_val:
                    is_line = False
                    break
            if is_line:
                lines.append(c)
    return sorted(lines)

def extract_left_panel(g: List[List[int]], line_cols: List[int]) -> List[List[int]]:
    if not g:
        return []
    h = len(g)
    w = len(g[0]) if g and g[0] else 0
    if not line_cols:
        return [row[:] for row in g]
    start = 0
    end = line_cols[0]
    if end > w:
        end = w
    output = []
    for r in range(h):
        panel_row = []
        for c in range(start, end):
            if c < w:
                panel_row.append(g[r][c])
        output.append(panel_row)
    return output

def program(g: List[List[int]]) -> List[List[int]]:
    background = get_background(g)
    line_cols = get_line_columns(g, background)
    return extract_left_panel(g, line_cols)
```