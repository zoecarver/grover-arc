```python
from collections import Counter
from typing import List, Dict, Tuple

def get_background(grid: List[List[int]]) -> int:
    """Identify the background color as the most frequent color in the grid."""
    flat = [cell for row in grid for cell in row]
    return Counter(flat).most_common(1)[0][0]

def find_connected_components(grid: List[List[int]], bg: int) -> List[Dict]:
    """Find 4-connected components of non-background cells, preserving color, pixels, min_y, max_y for height invariance."""
    H = len(grid)
    W = len(grid[0])
    visited = [[False] * W for _ in range(H)]
    components = []
    directions: List[Tuple[int, int]] = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for y in range(H):
        for x in range(W):
            if grid[y][x] != bg and not visited[y][x]:
                color = grid[y][x]
                pixels: List[Tuple[int, int]] = []
                min_y = H
                max_y = 0
                stack = [(y, x)]
                visited[y][x] = True
                while stack:
                    cy, cx = stack.pop()
                    pixels.append((cy, cx))
                    min_y = min(min_y, cy)
                    max_y = max(max_y, cy)
                    for dy, dx in directions:
                        ny = cy + dy
                        nx = cx + dx
                        if 0 <= ny < H and 0 <= nx < W and not visited[ny][nx] and grid[ny][nx] == color:
                            visited[ny][nx] = True
                            stack.append((ny, nx))
                components.append({'color': color, 'pixels': pixels, 'min_y': min_y, 'max_y': max_y})
    return components

def create_new_grid(H: int, W: int, bg: int) -> List[List[int]]:
    """Create a new grid filled with background color, preserving background invariance."""
    return [[bg for _ in range(W)] for _ in range(H)]

def place_components_to_top(new_grid: List[List[int]], components: List[Dict], H: int, W: int) -> None:
    """Place all components to the top by shifting y by -min_y, preserving x positions, heights, colors, and pixel counts (overwriting if conflict, as unknown rule leads to top placement)."""
    for comp in components:
        shift = -comp['min_y']
        for y, x in comp['pixels']:
            new_y = y + shift
            if 0 <= new_y < H:  # Ensure within bounds, preserving hole invariance indirectly.
                new_grid[new_y][x] = comp['color']

def program(g: List[List[int]]) -> List[List[int]]:
    """Main program composing rules: identify background, find components, place to top preserving invariants."""
    H = len(g)
    W = len(g[0])
    bg = get_background(g)
    components = find_connected_components(g, bg)
    new_grid = create_new_grid(H, W, bg)
    place_components_to_top(new_grid, components, H, W)
    return new_grid
```