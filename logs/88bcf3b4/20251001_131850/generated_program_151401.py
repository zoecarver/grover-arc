```python
from typing import List, Tuple
from collections import Counter

def get_background(g: List[List[int]]) -> int:
    flat = [cell for row in g for cell in row]
    c = Counter(flat)
    return c.most_common(1)[0][0]

def get_colors(g: List[List[int]], background: int) -> List[int]:
    seen = set()
    order = []
    n = len(g)
    for i in range(n):
        for j in range(n):
            cell = g[i][j]
            if cell != background and cell not in seen:
                seen.add(cell)
                order.append(cell)
    return order

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
    for idx in range(1, len(rows)):
        if rows[idx] != rows[idx - 1] + 1:
            return False
    return True

def get_min_row(positions: List[Tuple[int, int]]) -> int:
    if not positions:
        return 0
    return min(i for i, _ in positions)

def get_average_col(positions: List[Tuple[int, int]]) -> int:
    if not positions:
        return 0
    k = len(positions)
    sum_j = sum(j for _, j in positions)
    return round(sum_j / k)

def program(g: List[List[int]]) -> List[List[int]]:
    n = len(g)
    background = get_background(g)
    out = [[background for _ in range(n)] for _ in range(n)]
    colors = get_colors(g, background)
    # Sort colors by min row of first appearance
    color_order = sorted(colors, key=lambda c: get_min_row(get_positions(g, c)))
    # First place all preserved
    for c in color_order:
        positions = get_positions(g, c)
        if len(positions) <= 3 or is_vertical_aligned(g, c):
            for i, j in positions:
                out[i][j] = c
    # Then place straightened groups in same order
    for c in color_order:
        positions = get_positions(g, c)
        k = len(positions)
        if k <= 3 or is_vertical_aligned(g, c):
            continue  # already placed
        target = get_average_col(positions)
        current_col = target
        for r in range(k):
            # Try current
            col = current_col
            if 0 <= col < n and out[r][col] == background:
                out[r][col] = c
            else:
                # Shift left prefer
                found = False
                for d in range(1, n + 1):
                    col = current_col - d
                    if 0 <= col < n and out[r][col] == background:
                        out[r][col] = c
                        current_col = col
                        found = True
                        break
                if not found:
                    for d in range(1, n + 1):
                        col = current_col + d
                        if 0 <= col < n and out[r][col] == background:
                            out[r][col] = c
                            current_col = col
                            found = True
                            break
                if not found:
                    # Fallback any free
                    for col in range(n):
                        if out[r][col] == background:
                            out[r][col] = c
                            current_col = col
                            break
    return out
```