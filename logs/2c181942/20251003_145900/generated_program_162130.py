```python
from typing import List, Dict
from collections import defaultdict

def create_background_grid(h: int, w: int) -> List[List[int]]:
    return [[8] * w for _ in range(h)]

def has_color(g: List[List[int]], c: int) -> bool:
    return any(c in row for row in g)

def remove_yellow_if_pink(g: List[List[int]]) -> List[List[int]]:
    new_g = [row[:] for row in g]
    if has_color(new_g, 6):
        for i in range(len(new_g)):
            for j in range(len(new_g[i])):
                if new_g[i][j] == 4:
                    new_g[i][j] = 8
    return new_g

def count_colors(g: List[List[int]]) -> Dict[int, int]:
    counts = defaultdict(int)
    for row in g:
        for cell in row:
            if cell != 8:
                counts[cell] += 1
    return dict(counts)

def compute_avg_col(g: List[List[int]], c: int) -> float:
    total = 0.0
    cnt = 0
    for i in range(len(g)):
        for j in range(len(g[i])):
            if g[i][j] == c:
                total += j
                cnt += 1
    return total / cnt if cnt > 0 else float('inf')

def get_color_order(g: List[List[int]]) -> List[int]:
    cleaned = remove_yellow_if_pink(g)
    counts = count_colors(cleaned)
    colors = [k for k in counts if counts[k] > 0]
    avgs = {k: compute_avg_col(cleaned, k) for k in colors}
    def key_func(k: int) -> tuple:
        return (avgs[k], -k)
    return sorted(colors, key=key_func)

def get_shape_widths(n: int, c: int) -> List[int]:
    if n <= 2:
        if c % 2 == 1:
            return [0, 0, 0, n]
        return [n, 0, 0, 0]
    is_odd = c % 2 == 1
    k = 5 if is_odd else 7
    w = (n + k) // 4
    t = max(0, n // 2 - w)
    widths = [t, w, w, t]
    base_sum = sum(widths)
    rem = n - base_sum
    if rem > 0:
        widths[1] += rem // 2
        widths[2] += rem // 2 + (rem % 2)
    return widths

def program(g: List[List[int]]) -> List[List[int]]:
    h = len(g)
    w = len(g[0]) if h > 0 else 0
    if h == 0 or w == 0:
        return []
    cleaned = remove_yellow_if_pink(g)
    colors = get_color_order(cleaned)
    if not colors:
        return create_background_grid(h, w)
    counts = count_colors(cleaned)
    shape_widths = [get_shape_widths(counts[c], c) for c in colors]
    bws = [max(ws) for ws in shape_widths]
    sep = 1
    total_width = sum(bws) + max(0, len(colors) - 1) * sep
    left_margin = (w - total_width) // 2
    grid = create_background_grid(h, w)
    start_row = h // 2 - 2
    current_offset = 0
    for idx, c in enumerate(colors):
        ws = shape_widths[idx]
        bw = bws[idx]
        box_start = left_margin + current_offset
        is_odd = c % 2 == 1
        for r in range(4):
            row_i = start_row + r
            if 0 <= row_i < h:
                wi = ws[r]
                if wi > 0:
                    off = 0 if is_odd else bw - wi
                    for k in range(wi):
                        col_i = box_start + off + k
                        if 0 <= col_i < w:
                            grid[row_i][col_i] = c
        current_offset += bw + sep
    return grid
```