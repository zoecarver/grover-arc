```python
from typing import List, Dict
from collections import defaultdict

def has_color(g: List[List[int]], c: int) -> bool:
    for row in g:
        if c in row:
            return True
    return False

def remove_yellow_if_pink(g: List[List[int]]) -> List[List[int]]:
    new_g = [row[:] for row in g]
    if has_color(g, 6):
        rows = len(new_g)
        cols = len(new_g[0]) if rows > 0 else 0
        for i in range(rows):
            for j in range(cols):
                if new_g[i][j] == 4:
                    new_g[i][j] = 8
    return new_g

def count_colors(g: List[List[int]]) -> Dict[int, int]:
    color_count: Dict[int, int] = defaultdict(int)
    rows = len(g)
    cols = len(g[0]) if rows > 0 else 0
    for i in range(rows):
        for j in range(cols):
            c = g[i][j]
            if c != 8:
                color_count[c] += 1
    return dict(color_count)

def get_widths(n: int, c: int) -> List[int]:
    is_odd = c % 2 == 1
    if n <= 2:
        if is_odd:
            return [0, 0, 0, n]
        else:
            return [n, 0, 0, 0]
    half = n // 2
    if is_odd:
        a = (half + 2) // 3
    else:
        a = half // 3
    b = half - a
    widths = [a, b, b, a]
    remaining = n - sum(widths)
    if remaining > 0:
        widths[2] += remaining
    return widths

def program(g: List[List[int]]) -> List[List[int]]:
    rows = len(g)
    cols = len(g[0]) if rows > 0 else 0
    processed_g = remove_yellow_if_pink(g)
    color_count = count_colors(processed_g)
    if not color_count:
        return [[8] * cols for _ in range(rows)]
    colors = sorted(color_count)
    start_r = (rows - 4) // 2
    sum_maxw = 0
    max_ws = {}
    for c in colors:
        widths = get_widths(color_count[c], c)
        max_ws[c] = max(widths)
        sum_maxw += max_ws[c]
    left = (cols - sum_maxw) // 2
    current_left = left
    output_g = [[8] * cols for _ in range(rows)]
    for c in colors:
        widths = get_widths(color_count[c], c)
        for r in range(4):
            num = widths[r]
            if num > 0 and start_r + r < rows:
                col_start = current_left
                for k in range(num):
                    col = col_start + k
                    if col < cols:
                        output_g[start_r + r][col] = c
        current_left += max_ws[c]
    return output_g
```