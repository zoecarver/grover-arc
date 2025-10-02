```python
from typing import List, Tuple
from collections import Counter
import math

def get_background(g: List[List[int]]) -> int:
    flat = [cell for row in g for cell in row]
    c = Counter(flat)
    return c.most_common(1)[0][0]

def get_colors(g: List[List[int]], background: int) -> set:
    colors = set()
    for row in g:
        for cell in row:
            if cell != background:
                colors.add(cell)
    return colors

def get_positions(g: List[List[int]], color: int) -> List[Tuple[int, int]]:
    n = len(g)
    return [(i, j) for i in range(n) for j in range(n) if g[i][j] == color]

def is_vertical_aligned(positions: List[Tuple[int, int]]) -> bool:
    if not positions:
        return True
    cols = {j for _, j in positions}
    if len(cols) != 1:
        return False
    rows = sorted(i for i, _ in positions)
    if len(rows) != len(positions):
        return False
    for idx in range(1, len(rows)):
        if rows[idx] != rows[idx - 1] + 1:
            return False
    return True

def get_average_col(positions: List[Tuple[int, int]]) -> int:
    if not positions:
        return 0
    cols = [j for _, j in positions]
    return round(sum(cols) / len(cols))

def get_min_row(positions: List[Tuple[int, int]]) -> int:
    if not positions:
        return 0
    return min(i for i, _ in positions)

def preserve_positions(out: List[List[int]], positions: List[Tuple[int, int]], color: int) -> None:
    for i, j in positions:
        out[i][j] = color

def place_vertical_stack(out: List[List[int]], color: int, col: int, k: int, n: int, background: int) -> None:
    for r in range(k):
        if r < n:
            if out[r][col] == background:
                out[r][col] = color

def find_available_column_right_first(n: int, k: int, out: List[List[int]], background: int, target: int) -> int:
    # Search right from target first, then left
    for col in list(range(target, n)) + list(range(target - 1, -1, -1)):
        if all(out[r][col] == background for r in range(min(k, n))):
            return col
    # Fallback to target clamped
    return max(0, min(n - 1, target))

def program(g: List[List[int]]) -> List[List[int]]:
    n = len(g)
    background = get_background(g)
    colors = get_colors(g, background)
    out = [[background for _ in range(n)] for _ in range(n)]
    
    # First, preserve all small and vertical groups for all colors
    for color in colors:
        positions = get_positions(g, color)
        if len(positions) <= 3 or is_vertical_aligned(positions):
            preserve_positions(out, positions, color)
    
    # Collect large non-vertical colors, sort by min row
    large_non_vertical = []
    for color in colors:
        positions = get_positions(g, color)
        if len(positions) > 3 and not is_vertical_aligned(positions):
            large_non_vertical.append((color, positions))
    large_non_vertical.sort(key=lambda x: get_min_row(x[1]))
    
    # Now place the straightened stacks in order
    for color, positions in large_non_vertical:
        k = len(positions)
        target = get_average_col(positions)
        avail_col = find_available_column_right_first(n, k, out, background, target)
        place_vertical_stack(out, color, avail_col, k, n, background)
    
    return out
```