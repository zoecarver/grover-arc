```python
from typing import List, Tuple
from collections import Counter

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

def is_vertical_aligned(g: List[List[int]], color: int, background: int) -> bool:
    positions = [(i, j) for i in range(len(g)) for j in range(len(g)) if g[i][j] == color]
    if not positions:
        return True
    cols = {j for _, j in positions}
    if len(cols) != 1:
        return False
    col = next(iter(cols))
    rows = sorted(set(i for i, _ in positions))
    if len(rows) != len(positions):
        return False
    for k in range(1, len(rows)):
        if rows[k] != rows[k - 1] + 1:
            return False
    return True

def get_positions(g: List[List[int]], color: int) -> List[Tuple[int, int]]:
    n = len(g)
    return [(i, j) for i in range(n) for j in range(n) if g[i][j] == color]

def get_average_col(positions: List[Tuple[int, int]]) -> float:
    if not positions:
        return 0.0
    cols = [j for _, j in positions]
    return sum(cols) / len(cols)

def find_available_column(n: int, k: int, out: List[List[int]], background: int, target: int) -> int:
    col = max(0, round(target))
    while col < n:
        if all(out[r][col] == background for r in range(k)):
            return col
        col += 1
    return 0  # Fallback to leftmost if no space

def program(g: List[List[int]]) -> List[List[int]]:
    n = len(g)
    background = get_background(g)
    colors = get_colors(g, background)
    out = [[background] * n for _ in range(n)]
    # Preserve vertical stacks
    for color in sorted(colors):
        if is_vertical_aligned(g, color, background):
            positions = get_positions(g, color)
            for i, j in positions:
                out[i][j] = color
    # Straighten non-vertical globally per color
    non_vertical = [c for c in colors if not is_vertical_aligned(g, c, background)]
    # Order by decreasing size
    non_vertical.sort(key=lambda c: -len(get_positions(g, c)))
    for color in non_vertical:
        positions = get_positions(g, color)
        k = len(positions)
        if k == 0:
            continue
        avg_col = get_average_col(positions)
        col = find_available_column(n, k, out, background, avg_col)
        for r in range(k):
            out[r][col] = color
    return out
```