```python
from typing import List, Tuple, Set
from collections import Counter

def get_background(g: List[List[int]]) -> int:
    """Identify the background color as the most frequent value."""
    flat = [cell for row in g for cell in row]
    c = Counter(flat)
    return c.most_common(1)[0][0]

def get_colors(g: List[List[int]], background: int) -> set:
    """Get all non-background colors present."""
    colors = set()
    for row in g:
        for cell in row:
            if cell != background:
                colors.add(cell)
    return colors

def get_positions(g: List[List[int]], color: int) -> List[Tuple[int, int]]:
    """Get all positions of a specific color."""
    n = len(g)
    return [(i, j) for i in range(n) for j in range(n) if g[i][j] == color]

def get_median_col(positions: List[Tuple[int, int]]) -> int:
    """Get the median column for positions (for placement target based on central tendency)."""
    if not positions:
        return 0
    cols = sorted([j for _, j in positions])
    return cols[len(cols) // 2]

def get_connected_components(g: List[List[int]], color: int, all_positions: List[Tuple[int, int]], n: int) -> List[List[Tuple[int, int]]]:
    """Find 8-connected components for a color (rule: groups are connected including diagonals)."""
    visited: Set[Tuple[int, int]] = set()
    components: List[List[Tuple[int, int]]] = []
    deltas = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    for start_pos in all_positions:
        if start_pos in visited:
            continue
        component = []
        stack = [start_pos]
        visited.add(start_pos)
        while stack:
            x, y = stack.pop()
            component.append((x, y))
            for dx, dy in deltas:
                nx = x + dx
                ny = y + dy
                if 0 <= nx < n and 0 <= ny < n and g[nx][ny] == color and (nx, ny) not in visited:
                    visited.add((nx, ny))
                    stack.append((nx, ny))
        if component:
            components.append(component)
    return components

def is_vertical_aligned_component(component: List[Tuple[int, int]]) -> bool:
    """Check if a component is vertically aligned (rule: single column, contiguous rows, no gaps)."""
    if not component:
        return True
    cols = {j for _, j in component}
    if len(cols) != 1:
        return False
    col = next(iter(cols))
    rows = sorted(set(i for i, _ in component))
    if len(rows) != len(component):
        return False
    for idx in range(1, len(rows)):
        if rows[idx] != rows[idx - 1] + 1:
            return False
    return True

def find_available_column(n: int, k: int, out: List[List[int]], background: int, target: int) -> int:
    """Find the closest available column to target for a vertical stack of height k from top (rule: prefer near original position, check top k free)."""
    best_col = -1
    min_dist = float('inf')
    for col in range(n):
        if all(out[r][col] == background for r in range(k)):
            dist = abs(col - target)
            if dist < min_dist:
                min_dist = dist
                best_col = col
    if best_col == -1:
        # Fallback to nearest even if partial, but here return target clamped
        return max(0, min(n - 1, target))
    return best_col

def preserve_small_and_vertical_components(g: List[List[int]], out: List[List[int]], background: int):
    """Preserve positions of small (<=3 cells) or vertical components (rule: keep upright or tiny groups intact)."""
    colors = get_colors(g, background)
    for color in colors:
        all_positions = get_positions(g, color)
        components = get_connected_components(g, color, all_positions, len(g))
        for component in components:
            if len(component) <= 3 or is_vertical_aligned_component(component):
                for i, j in component:
                    out[i][j] = color

def straighten_large_non_vertical_components(g: List[List[int]], out: List[List[int]], background: int):
    """Straighten large non-vertical components to vertical stacks near median column from top (rule: reorganize messy groups into solid verticals, ordered by original top position)."""
    n = len(g)
    colors = get_colors(g, background)
    transforming = []
    for color in colors:
        all_positions = get_positions(g, color)
        components = get_connected_components(g, color, all_positions, n)
        for component in components:
            if len(component) > 3 and not is_vertical_aligned_component(component):
                min_r = min(i for i, _ in component)
                transforming.append((min_r, component, color))
    transforming.sort(key=lambda x: x[0])  # Order by original starting row
    for _, component, color in transforming:
        k = len(component)
        median_col = get_median_col(component)
        col = find_available_column(n, k, out, background, median_col)
        for i in range(k):
            r = i  # Start from top row 0
            if r < n:
                out[r][col] = color

def program(g: List[List[int]]) -> List[List[int]]:
    """Main program: fill with background, preserve small/vertical, then straighten large non-vertical in order."""
    n = len(g)
    background = get_background(g)
    out = [[background] * n for _ in range(n)]
    preserve_small_and_vertical_components(g, out, background)
    straighten_large_non_vertical_components(g, out, background)
    return out
```