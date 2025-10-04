```python
from typing import List, Tuple, Set
from collections import Counter

def get_background_color(grid: List[List[int]]) -> int:
    """Identify the background color as the most frequent color in the grid."""
    flat = [cell for row in grid for cell in row]
    return Counter(flat).most_common(1)[0][0]

def get_dimensions(grid: List[List[int]]) -> Tuple[int, int]:
    """Get height and width of the grid."""
    if not grid:
        return 0, 0
    h = len(grid)
    w = len(grid[0])
    return h, w

def is_tall_canvas(h: int, w: int) -> bool:
    """Determine if the canvas is taller than wide (primary translation in x)."""
    return h > w

def get_direction(is_tall: bool) -> str:
    """Get the primary translation direction based on canvas aspect ratio."""
    return 'x' if is_tall else 'y'

def get_dim_and_target(h: int, w: int, direction: str) -> Tuple[int, int]:
    """Compute dimension and target position for primary direction."""
    dim = w if direction == 'x' else h
    target = 9 - (dim // 2)
    return dim, target

def get_special_colors(grid: List[List[int]], bg: int) -> Tuple[int, Set[int]]:
    """Identify main special color (highest numbered with exactly 4 pixels) and minor specials."""
    count = Counter(cell for row in grid for cell in row if cell != bg)
    specials = [c for c, cnt in count.items() if cnt == 4]
    if not specials:
        return None, set()
    main = max(specials)
    minors = set(specials) - {main}
    return main, minors

def find_connected_components(grid: List[List[int]], bg: int) -> List[List[Tuple[int, int, int]]]:
    """Find connected components of non-background cells (4-connected, color-agnostic)."""
    h, w = get_dimensions(grid)
    visited = [[False] * w for _ in range(h)]
    components = []
    dirs: List[Tuple[int, int]] = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for i in range(h):
        for j in range(w):
            if grid[i][j] != bg and not visited[i][j]:
                component = []
                stack = [(i, j)]
                visited[i][j] = True
                while stack:
                    x, y = stack.pop()
                    component.append((x, y, grid[x][y]))
                    for dx, dy in dirs:
                        nx = x + dx
                        ny = y + dy
                        if 0 <= nx < h and 0 <= ny < w and not visited[nx][ny] and grid[nx][ny] != bg:
                            visited[nx][ny] = True
                            stack.append((nx, ny))
                components.append(component)
    return components

def get_delta_for_component(component: List[Tuple[int, int, int]], main: int, minors: Set[int],
                            target: int, direction: str) -> Tuple[int, int]:
    """Compute primary and secondary deltas for the component."""
    primary_is_col = (direction == 'x')  # Primary coord: col (y) for 'x', row (x) for 'y'
    # Main special primary positions
    main_primaries = [y if primary_is_col else x for x, y, c in component if c == main]
    if main_primaries:
        pos_p = min(main_primaries)
        delta_p = target - pos_p
    else:
        # Minor special primary positions (assume at most one per component)
        minor_primary = None
        for x, y, c in component:
            if c in minors:
                if minor_primary is not None:
                    # Multiple minors: take min (rare case)
                    minor_primary = min(minor_primary, y if primary_is_col else x)
                else:
                    minor_primary = y if primary_is_col else x
        if minor_primary is not None:
            pos_p = minor_primary
            delta_p = target - pos_p
        else:
            delta_p = 0
    has_minor = any(c in minors for _, _, c in component)
    delta_s = 0
    if delta_p > 0 and has_minor:
        delta_s = -delta_p
    return delta_p, delta_s

def program(g: List[List[int]]) -> List[List[int]]:
    """Main program to transform the grid according to inferred puzzle rules."""
    h, w = get_dimensions(g)
    bg = get_background_color(g)
    is_tall = is_tall_canvas(h, w)
    direction = get_direction(is_tall)
    _, target = get_dim_and_target(h, w, direction)
    main, minors = get_special_colors(g, bg)
    if main is None:
        return [row[:] for row in g]
    components = find_connected_components(g, bg)
    new_grid = [[bg for _ in range(w)] for _ in range(h)]
    for component in components:
        delta_p, delta_s = get_delta_for_component(component, main, minors, target, direction)
        if direction == 'x':
            dx = delta_p
            dy = delta_s
        else:
            dx = delta_s
            dy = delta_p
        for x, y, c in component:
            nx = x + dy
            ny = y + dx
            if 0 <= nx < h and 0 <= ny < w:
                new_grid[nx][ny] = c
    return new_grid
```