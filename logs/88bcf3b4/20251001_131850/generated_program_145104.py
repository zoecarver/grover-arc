```python
from typing import List, Tuple
from collections import Counter

def get_background(g: List[List[int]]) -> int:
    flat = [cell for row in g for cell in row]
    c = Counter(flat)
    return c.most_common(1)[0][0]

def get_colors(g: List[List[int]], background: int) -> List[int]:
    colors = set()
    for row in g:
        for cell in row:
            if cell != background:
                colors.add(cell)
    return sorted(colors)

def get_positions(g: List[List[int]], color: int) -> List[Tuple[int, int]]:
    n = len(g)
    return [(i, j) for i in range(n) for j in range(n) if g[i][j] == color]

def is_vertical_aligned(g: List[List[int]], color: int) -> bool:
    positions = get_positions(g, color)
    if not positions:
        return True
    cols = {j for _, j in positions}
    if len(cols) != 1:
        return False
    rows = sorted(i for i, _ in positions)
    if len(rows) != len(positions):
        return False
    for k in range(1, len(rows)):
        if rows[k] != rows[k - 1] + 1:
            return False
    return True

def preserve_group(out: List[List[int]], g: List[List[int]], color: int) -> None:
    n = len(g)
    for i in range(n):
        for j in range(n):
            if g[i][j] == color:
                out[i][j] = color

def get_average_col(positions: List[Tuple[int, int]]) -> int:
    if not positions:
        return 0
    avg = sum(j for _, j in positions) / len(positions)
    return round(avg)

def find_available_column(n: int, k: int, out: List[List[int]], background: int, target: int) -> int:
    if k == 0:
        return 0
    if 0 <= target < n and all(out[r][target] == background for r in range(k)):
        return target
    for d in range(1, n):
        for sign in [1, -1]:
            col = target + sign * d
            if 0 <= col < n and all(out[r][col] == background for r in range(k)):
                return col
    for col in range(n):
        if all(out[r][col] == background for r in range(k)):
            return col
    return 0

def place_vertical_stack(out: List[List[int]], color: int, col: int, k: int, n: int) -> None:
    for r in range(k):
        if r < n:
            out[r][col] = color

def program(g: List[List[int]]) -> List[List[int]]:
    n = len(g)
    background = get_background(g)
    out = [[background] * n for _ in range(n)]
    colors = get_colors(g, background)
    for color in colors:
        positions = get_positions(g, color)
        k = len(positions)
        if k <= 3 or is_vertical_aligned(g, color):
            preserve_group(out, g, color)
        else:
            target = get_average_col(positions)
            col = find_available_column(n, k, out, background, target)
            place_vertical_stack(out, color, col, k, n)
    return out
```