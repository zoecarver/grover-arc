```python
from typing import List, Dict
from collections import defaultdict

def has_color(g: List[List[int]], c: int) -> bool:
    return any(c in row for row in g)

def count_colors(g: List[List[int]]) -> Dict[int, int]:
    count = defaultdict(int)
    for row in g:
        for cell in row:
            if cell != 8:
                count[cell] += 1
    return dict(count)

def get_shape_params(n: int, c: int) -> tuple[List[int], int]:
    if n <= 2:
        is_odd = (c % 2 == 1)
        if is_odd:
            widths = [0, 0, 0, n]
        else:
            widths = [n, 0, 0, 0]
        return widths, n
    is_odd = (c % 2 == 1)
    k = 5 if is_odd else 7
    w = (n + k) // 4
    t = max(0, n // 2 - w)
    widths = [t, w, w, t]
    base = sum(widths)
    remaining = n - base
    if remaining > 0:
        widths[1] += remaining // 2
        widths[2] += remaining - (remaining // 2)
    elif remaining < 0:
        diff = -remaining
        widths[1] -= diff // 2
        widths[2] -= diff - (diff // 2)
        widths = [max(0, x) for x in widths]
    bw = max(widths) if any(widths) else 0
    return widths, bw

def program(g: List[List[int]]) -> List[List[int]]:
    rows = len(g)
    cols = len(g[0])
    out = [[8 for _ in range(cols)] for _ in range(rows)]
    count = count_colors(g)
    if has_color(g, 6):
        count[4] = 0
    active = sorted([c for c in count if count[c] > 0], reverse=True)
    if not active:
        return out
    start_r = (rows - 4) // 2
    shape_params = {c: get_shape_params(count[c], c) for c in active}
    sep = 1
    total_width = sum(bw for _, bw in shape_params.values()) + max(0, len(active) - 1) * sep
    left_margin = (cols - total_width) // 2
    current_left = left_margin
    for c in active:
        widths, bw = shape_params[c]
        for r in range(4):
            w = widths[r]
            if w > 0:
                row = start_r + r
                if 0 <= row < rows:
                    offset = (bw - w) // 2
                    fill_start = current_left + offset
                    for k in range(w):
                        j = fill_start + k
                        if 0 <= j < cols:
                            out[row][j] = c
        current_left += bw + sep
    return out
```