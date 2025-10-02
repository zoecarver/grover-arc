```python
from typing import List, Tuple
from collections import Counter

def get_background(g: List[List[int]]) -> int:
    """Identify the background color as the most frequent value."""
    flat = [cell for row in g for cell in row]
    c = Counter(flat)
    return c.most_common(1)[0][0]

def get_colors(g: List[List[int]], background: int) -> List[int]:
    """Get all non-background colors, sorted by first appearance in row-major order."""
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
    """Get all positions of a specific color."""
    n = len(g)
    return [(i, j) for i in range(n) for j in range(n) if g[i][j] == color]

def is_vertical_aligned(g: List[List[int]], color: int, background: int) -> bool:
    """Check if all blocks of a color are vertically aligned in one column without gaps."""
    positions = get_positions(g, color)
    if not positions:
        return True
    cols = {j for _, j in positions}
    if len(cols) != 1:
        return False
    col = next(iter(cols))
    rows = sorted(set(i for i, _ in positions))
    if len(rows) != len(positions):
        return False
    for idx in range(1, len(rows)):
        if rows[idx] != rows[idx - 1] + 1:
            return False
    return True

def is_small(positions: List[Tuple[int, int]]) -> bool:
    """Check if the group has <=3 cells for exact preservation."""
    return len(positions) <= 3

def preserve_group(out: List[List[int]], g: List[List[int]], color: int) -> None:
    """Copy exact positions for small or vertical groups to output."""
    n = len(g)
    for i in range(n):
        for j in range(n):
            if g[i][j] == color:
                out[i][j] = color

def get_average_col(positions: List[Tuple[int, int]]) -> int:
    """Compute rounded average column for target placement."""
    if not positions:
        return 0
    avg = sum(j for _, j in positions) / len(positions)
    return round(avg)

def find_target_column(n: int, k: int, out: List[List[int]], background: int, target: int) -> int:
    """Find the preferred column near target with top k free rows, biasing right."""
    best_col = -1
    min_dist = float('inf')
    for d in range(n):
        # Bias right: try target + d first
        col = target + d
        if 0 <= col < n and all(out[r][col] == background for r in range(min(k, n))):
            dist = abs(col - target)
            if dist < min_dist:
                min_dist = dist
                best_col = col
                break  # Found the rightmost closest
        # Then left if needed
        col = target - d
        if 0 <= col < n and all(out[r][col] == background for r in range(min(k, n))):
            dist = abs(col - target)
            if dist < min_dist:
                min_dist = dist
                best_col = col
    return best_col if best_col != -1 else max(0, min(n-1, target))

def place_vertical_stack(out: List[List[int]], color: int, col: int, k: int, n: int, background: int) -> None:
    """Place a vertical stack of k cells from row 0 in the given column, skipping occupied."""
    placed = 0
    for r in range(n):
        if placed == k:
            break
        if out[r][col] == background:
            out[r][col] = color
            placed += 1

def program(g: List[List[int]]) -> List[List[int]]:
    """Main program: preserve small/vertical groups, straighten large non-vertical into vertical stacks near average column, biasing right for placement."""
    n = len(g)
    background = get_background(g)
    out = [[background] * n for _ in range(n)]
    colors = get_colors(g, background)
    for color in colors:
        positions = get_positions(g, color)
        k = len(positions)
        if is_small(positions) or is_vertical_aligned(g, color, background):
            preserve_group(out, g, color)
        else:
            target = get_average_col(positions)
            col = find_target_column(n, k, out, background, target)
            if col != -1:
                place_vertical_stack(out, color, col, k, n, background)
    return out
```