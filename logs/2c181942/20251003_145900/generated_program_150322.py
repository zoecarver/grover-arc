```python
from typing import List, Dict
from collections import defaultdict

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

def get_shape_params(n: int) -> tuple[int, int, List[int]]:
    """Compute width w, and list of row widths for the diamond shape with height 4."""
    if n == 0:
        return 0, 4, [0, 0, 0, 0]
    h = 4
    w = max(1, (n + 3) // 4)
    t = max(0, n // 2 - w)
    base = 2 * t + 2 * w
    widths = [t, w, w, t]
    remaining = n - base
    if remaining > 0:
        widths[1] += remaining // 2
        widths[2] += remaining - (remaining // 2)
    else:
        diff = base - n
        widths[1] -= diff // 2
        widths[2] -= diff - (diff // 2)
        widths = [max(0, x) for x in widths]
    return w, h, widths

def program(g: List[List[int]]) -> List[List[int]]:
    rows = len(g)
    cols = len(g[0]) if rows > 0 else 0
    out = [[8] * cols for _ in range(rows)]
    
    color_count = count_colors(g)
    if not color_count:
        return out
    
    colors = sorted(color_count.keys())
    
    # Compute params for each color
    color_ws = {}
    total_span = 0
    for color in colors:
        n = color_count[color]
        w, _, _ = get_shape_params(n)
        color_ws[color] = w
        total_span += w
    if len(colors) > 1:
        total_span += (len(colors) - 1) * 2
    start_c = (cols - total_span) // 2
    
    h = 4
    start_r = (rows - h) // 2
    
    current_c = start_c
    for color in colors:
        n = color_count[color]
        w, _, widths = get_shape_params(n)
        is_odd = (color % 2 == 1)
        
        for k in range(h):
            if start_r + k >= rows:
                break
            num = widths[k]
            if num == 0:
                continue
            left = current_c
            if not is_odd:
                left += w - num
            left = max(0, left)
            fill_num = min(num, cols - left)
            if fill_num > 0:
                out[start_r + k][left : left + fill_num] = [color] * fill_num
        
        current_c += w + 2
        if current_c >= cols:
            break
    
    return out
```