```python
from typing import List, Tuple
from collections import Counter

def get_background(g: List[List[int]]) -> int:
    """Rule: Identify the background color as the most frequent value in the grid."""
    flat = [cell for row in g for cell in row]
    c = Counter(flat)
    return c.most_common(1)[0][0]

def get_colors(g: List[List[int]], background: int) -> set:
    """Rule: Isolate all unique non-background colors present in the grid."""
    return set(cell for row in g for cell in row if cell != background)

def get_positions(g: List[List[int]], color: int) -> List[Tuple[int, int]]:
    """Rule: Extract all grid positions containing a specific color."""
    n = len(g)
    return [(i, j) for i in range(n) for j in range(n) if g[i][j] == color]

def is_vertical_aligned(g: List[List[int]], color: int) -> bool:
    """Rule: Check if all occurrences of a color form a single contiguous vertical stack in one column with no gaps."""
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

def is_small_group(g: List[List[int]], color: int) -> bool:
    """Rule: Check if the total count of a color is small enough to preserve regardless of alignment (≤3 cells)."""
    positions = get_positions(g, color)
    return len(positions) <= 3

def preserve_group(out: List[List[int]], g: List[List[int]], color: int) -> None:
    """Rule: Copy exact positions of a color to the output grid for preservation."""
    positions = get_positions(g, color)
    for i, j in positions:
        out[i][j] = color

def get_target_col(positions: List[Tuple[int, int]]) -> int:
    """Rule: Compute placement target column as the rounded average of original columns for the group."""
    if not positions:
        return 0
    k = len(positions)
    sum_j = sum(j for _, j in positions)
    return round(sum_j / k)

def find_available_col(n: int, k: int, out: List[List[int]], background: int, target: int) -> int:
    """Rule: Find column for stack placement, preferring positions rightward from target, then leftward, ensuring top k rows free."""
    # Prefer right from target
    for col in range(target, n):
        if all(out[r][col] == background for r in range(k)):
            return col
    # Then left from target
    for col in range(target - 1, -1, -1):
        if all(out[r][col] == background for r in range(k)):
            return col
    # Fallback to leftmost available
    for col in range(n):
        if all(out[r][col] == background for r in range(k)):
            return col
    return max(0, min(n - 1, target))

def place_vertical_stack(out: List[List[int]], color: int, col: int, k: int, n: int) -> None:
    """Rule: Place a vertical stack of k cells of the given color starting from the top in the specified column."""
    for r in range(min(k, n)):
        out[r][col] = color

def program(g: List[List[int]]) -> List[List[int]]:
    """Main program: Compose rules to process the grid - preserve small/vertical groups, straighten large non-vertical to vertical stacks near original positions preferring rightward placement."""
    n = len(g)
    background = get_background(g)
    out = [[background] * n for _ in range(n)]
    colors = get_colors(g, background)
    # Step 1: Preserve all small groups and vertical stacks first
    for color in sorted(colors):
        if is_small_group(g, color) or is_vertical_aligned(g, color):
            preserve_group(out, g, color)
    # Step 2: Collect and process large non-vertical groups, ordered by original topmost row (top-first)
    large_groups = []
    for color in colors:
        positions = get_positions(g, color)
        if len(positions) > 3 and not is_vertical_aligned(g, color):
            min_r = min((i for i, _ in positions), default=n)
            large_groups.append((min_r, color, positions))
    large_groups.sort(key=lambda x: x[0])  # Sort by min_row ascending
    # Step 3: Straighten each large group to vertical stack in available column near target
    for _, color, positions in large_groups:
        k = len(positions)
        target = get_target_col(positions)
        col = find_available_col(n, k, out, background, target)
        place_vertical_stack(out, color, col, k, n)
    return out
```