```python
from typing import List, Tuple
from collections import Counter

def identify_background(g: List[List[int]]) -> int:
    """Rule: Background is the most frequent value in the grid."""
    flat = [cell for row in g for cell in row]
    c = Counter(flat)
    return c.most_common(1)[0][0]

def extract_non_background_colors(g: List[List[int]], bg: int) -> List[int]:
    """Rule: Extract non-background colors in order of first appearance (row-major scan)."""
    seen = set()
    order = []
    n = len(g)
    for i in range(n):
        for j in range(n):
            cell = g[i][j]
            if cell != bg and cell not in seen:
                seen.add(cell)
                order.append(cell)
    return order

def extract_positions(g: List[List[int]], color: int) -> List[Tuple[int, int]]:
    """Observation: Collect all grid positions for a given color."""
    n = len(g)
    return [(i, j) for i in range(n) for j in range(n) if g[i][j] == color]

def is_small_group(positions: List[Tuple[int, int]]) -> bool:
    """Rule: Groups with 3 or fewer cells are small and preserved exactly."""
    return len(positions) <= 3

def is_vertical_contiguous(positions: List[Tuple[int, int]]) -> bool:
    """Rule: A group is vertical if all cells are in one column with no row gaps."""
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

def preserve_group(out: List[List[int]], positions: List[Tuple[int, int]], color: int) -> None:
    """Rule: Copy exact positions of preserved groups (small or vertical) to output."""
    for i, j in positions:
        out[i][j] = color

def calculate_average_column(positions: List[Tuple[int, int]]) -> int:
    """Observation: Target column for placement is the rounded average original column."""
    if not positions:
        return 0
    avg = sum(j for _, j in positions) / len(positions)
    return round(avg)

def find_best_column_for_stack(n: int, k: int, out: List[List[int]], bg: int, target: int) -> int:
    """Rule: Find column nearest target with top k rows free, preferring right for ties."""
    candidates = []
    for col in range(n):
        if all(out[r][col] == bg for r in range(min(k, n))):
            dist = abs(col - target)
            candidates.append((dist, -col, col))  # Sort by dist asc, then col desc (prefer right)
    if candidates:
        candidates.sort()
        return candidates[0][2]
    # Fallback: nearest column, even if partial space
    return max(0, min(n - 1, target))

def place_vertical_stack(out: List[List[int]], color: int, col: int, k: int, n: int, bg: int) -> None:
    """Rule: Place vertical stack of k cells from top in chosen column, skipping occupied."""
    placed = 0
    for r in range(n):
        if placed == k:
            break
        if out[r][col] == bg:
            out[r][col] = color
            placed += 1

def program(g: List[List[int]]) -> List[List[int]]:
    """Main composition: Initialize output, process colors in appearance order, preserve or straighten."""
    n = len(g)
    bg = identify_background(g)
    out = [[bg for _ in range(n)] for _ in range(n)]
    colors = extract_non_background_colors(g, bg)
    for color in colors:
        positions = extract_positions(g, color)
        if is_small_group(positions) or is_vertical_contiguous(positions):
            preserve_group(out, positions, color)
        else:
            k = len(positions)
            target = calculate_average_column(positions)
            col = find_best_column_for_stack(n, k, out, bg, target)
            place_vertical_stack(out, color, col, k, n, bg)
    return out
```