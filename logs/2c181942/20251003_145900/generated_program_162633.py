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

def get_shape_widths(n: int, c: int) -> List[int]:
    if n <= 2:
        if c % 2 == 0:
            return [n, 0, 0, 0]
        else:
            return [0, 0, 0, n]
    is_odd = c % 2 == 1
    k = 5 if is_odd else 7
    w_mid = (n + k) // 4
    t = max(0, n // 2 - w_mid)
    widths = [t, w_mid, w_mid, t]
    base_sum = sum(widths)
    remaining = n - base_sum
    if remaining > 0:
        widths[1] += remaining // 2
        widths[2] += remaining - (remaining // 2)
    return widths

def get_box_width(widths: List[int], c: int, has_pink: bool, n: int) -> int:
    if n <= 2:
        return n
    bw = max(widths)
    if n > 2 and c % 2 == 1 and has_pink:
        return bw + 1
    return bw

def place_shape(grid: List[List[int]], widths: List[int], c: int, has_pink: bool, start_row: int, start_col: int, n: int) -> None:
    box_w = get_box_width(widths, c, has_pink, n)
    is_odd = c % 2 == 1
    h = len(grid)
    w = len(grid[0]) if h > 0 else 0
    for r in range(4):
        wi = widths[r]
        if wi == 0:
            continue
        if r == 0 or r == 3:
            offset = 0 if is_odd else box_w - wi
        else:
            offset = (box_w - wi) if (is_odd and has_pink) else (0 if is_odd else box_w - wi)
        for jj in range(wi):
            j = start_col + offset + jj
            i = start_row + r
            if 0 <= i < h and 0 <= j < w:
                grid[i][j] = c

def program(g: List[List[int]]) -> List[List[int]]:
    h = len(g)
    w = len(g[0]) if h > 0 else 0
    cleaned = remove_yellow_if_pink(g)
    counts = count_colors(cleaned)
    colors = [c for c in [1,2,3,4,6,7] if counts.get(c, 0) > 0]
    if not colors:
        return create_background_grid(h, w)
    avgs = {c: compute_avg_col(cleaned, c) for c in colors}
    sorted_colors = sorted(colors, key=lambda cc: (avgs[cc], -cc))
    has_pink = has_color(cleaned, 6)
    start_row = (h - 4) // 2
    out = create_background_grid(h, w)
    current_col = 2
    for c in sorted_colors:
        n = counts[c]
        widths = get_shape_widths(n, c)
        place_shape(out, widths, c, has_pink, start_row, current_col, n)
        box_w = get_box_width(widths, c, has_pink, n)
        current_col += box_w
    return out
```