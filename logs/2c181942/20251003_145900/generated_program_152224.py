```python
from typing import List, Dict
from collections import defaultdict
import math

def has_color(g: List[List[int]], c: int) -> bool:
    """Check if color c is present anywhere in the grid."""
    for row in g:
        if any(x == c for x in row):
            return True
    return False

def count_colors(g: List[List[int]]) -> Dict[int, int]:
    """Count the number of cells for each non-8 color."""
    rows = len(g)
    cols = len(g[0]) if rows > 0 else 0
    color_count: Dict[int, int] = defaultdict(int)
    for i in range(rows):
        for j in range(cols):
            c = g[i][j]
            if c != 8:
                color_count[c] += 1
    return dict(color_count)

def get_shape_widths(n: int, is_odd: bool) -> List[int]:
    """Compute the 4 row widths for the shape based on n and color parity."""
    if n == 0:
        return [0, 0, 0, 0]
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
    return widths

def program(g: List[List[int]]) -> List[List[int]]:
    """Main function to transform input grid to output grid."""
    rows = len(g)
    if rows == 0:
        return []
    cols = len(g[0])
    color_count = count_colors(g)
    if has_color(g, 6):
        color_count[4] = 0
    colors = sorted(c for c in color_count if color_count[c] > 0)
    if not colors:
        return [[8] * cols for _ in range(rows)]
    start_r = (rows - 4) // 2
    if rows % 2 == 1:
        start_r -= 1
    shape_widths_list = []
    bounding_ws = []
    for c in colors:
        n = color_count[c]
        is_odd_c = c % 2 == 1
        if n <= 2:
            if is_odd_c:
                ws = [0, 0, 0, n]
            else:
                ws = [n, 0, 0, 0]
            bw = n
        else:
            ws = get_shape_widths(n, is_odd_c)
            bw = max(ws)
        shape_widths_list.append(ws)
        bounding_ws.append(bw)
    num_shapes = len(colors)
    sep = 1
    total_w = sum(bounding_ws) + max(0, num_shapes - 1) * sep
    left_margin = (cols - total_w) // 2
    out_g = [[8] * cols for _ in range(rows)]
    current_left = left_margin
    for idx, c in enumerate(colors):
        ws = shape_widths_list[idx]
        bw = bounding_ws[idx]
        is_odd_c = c % 2 == 1
        n = color_count[c]
        special_small = n <= 2
        for local_r in range(4):
            wi = ws[local_r]
            if wi == 0:
                continue
            r = start_r + local_r
            if r < 0 or r >= rows:
                continue
            if special_small:
                fill_start = current_left
            else:
                if is_odd_c:
                    fill_start = current_left
                else:
                    fill_start = current_left + bw - wi
            for k in range(wi):
                j = fill_start + k
                if 0 <= j < cols:
                    out_g[r][j] = c
        current_left += bw + sep
    return out_g
```