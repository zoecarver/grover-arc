```python
from typing import List, Dict, Tuple
from collections import deque, defaultdict

def copy_grid(g: List[List[int]]) -> List[List[int]]:
    """Create a deep copy of the input grid to avoid mutating the original."""
    return [row[:] for row in g]

def flood_fill_same(g: List[List[int]], sr: int, sc: int, visited: List[List[bool]], color: int) -> List[Tuple[int, int]]:
    """Flood fill to find all connected cells (4-directional) with exactly the given color value."""
    rows, cols = len(g), len(g[0])
    if not (0 <= sr < rows and 0 <= sc < cols) or g[sr][sc] != color or visited[sr][sc]:
        return []
    stack = deque([(sr, sc)])
    visited[sr][sc] = True
    cells: List[Tuple[int, int]] = [(sr, sc)]
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    while stack:
        x, y = stack.popleft()
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < rows and 0 <= ny < cols and not visited[nx][ny] and g[nx][ny] == color:
                visited[nx][ny] = True
                stack.append((nx, ny))
                cells.append((nx, ny))
    return cells

def flood_fill_high(g: List[List[int]], sr: int, sc: int, visited: List[List[bool]]) -> List[Tuple[int, int]]:
    """Flood fill to find all connected cells (4-directional) with value > 4 (any high value)."""
    rows, cols = len(g), len(g[0])
    if not (0 <= sr < rows and 0 <= sc < cols) or g[sr][sc] <= 4 or visited[sr][sc]:
        return []
    stack = deque([(sr, sc)])
    visited[sr][sc] = True
    cells: List[Tuple[int, int]] = [(sr, sc)]
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    while stack:
        x, y = stack.popleft()
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < rows and 0 <= ny < cols and not visited[nx][ny] and g[nx][ny] > 4:
                visited[nx][ny] = True
                stack.append((nx, ny))
                cells.append((nx, ny))
    return cells

def count_holes(grid: List[List[int]], component_cells: List[Tuple[int, int]]) -> int:
    """Compute the number of connected components of 0-cells fully enclosed by the component (not reachable from grid border via paths of only 0-cells)."""
    rows, cols = len(grid), len(grid[0])
    is_barrier = [[False] * cols for _ in range(rows)]
    for r, c in component_cells:
        is_barrier[r][c] = True
    visited = [[False] * cols for _ in range(rows)]
    q = deque()
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    # Enqueue border 0-cells that are not barriers
    for r in range(rows):
        for c in (0, cols - 1):
            if 0 <= r < rows and 0 <= c < cols and grid[r][c] == 0 and not is_barrier[r][c] and not visited[r][c]:
                visited[r][c] = True
                q.append((r, c))
    for c in range(1, cols - 1):  # Avoid corner duplication
        for r in (0, rows - 1):
            if 0 <= r < rows and 0 <= c < cols and grid[r][c] == 0 and not is_barrier[r][c] and not visited[r][c]:
                visited[r][c] = True
                q.append((r, c))
    # Flood fill exterior through only 0-cells
    while q:
        x, y = q.popleft()
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < rows and 0 <= ny < cols and not visited[nx][ny] and grid[nx][ny] == 0 and not is_barrier[nx][ny]:
                visited[nx][ny] = True
                q.append((nx, ny))
    # Count connected components of unvisited enclosed 0-cells
    hole_count = 0
    for r in range(rows):
        for c in range(cols):
            if not visited[r][c] and grid[r][c] == 0 and not is_barrier[r][c]:
                hole_count += 1
                qq = deque([(r, c)])
                visited[r][c] = True
                while qq:
                    x, y = qq.popleft()
                    for dx, dy in directions:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < rows and 0 <= ny < cols and not visited[nx][ny] and grid[nx][ny] == 0 and not is_barrier[nx][ny]:
                            visited[nx][ny] = True
                            qq.append((nx, ny))
    return hole_count

def find_all_low_components(g: List[List[int]]) -> List[Dict[str, int]]:
    """Identify all connected components of cells with values 1-4 (same value within component) and compute their enclosed hole counts."""
    rows, cols = len(g), len(g[0])
    visited = [[False] * cols for _ in range(rows)]
    components: List[Dict[str, int]] = []
    for r in range(rows):
        for c in range(cols):
            color = g[r][c]
            if 1 <= color <= 4 and not visited[r][c]:
                cells = flood_fill_same(g, r, c, visited, color)
                if cells:
                    holes = count_holes(g, cells)
                    components.append({'color': color, 'holes': holes})
    return components

def build_hole_to_color_mapping(components: List[Dict[str, int]]) -> Dict[int, int]:
    """Build mapping from hole count to the highest color (1-4) among all low components with that hole count."""
    hole_to_colors = defaultdict(list)
    for comp in components:
        hole_to_colors[comp['holes']].append(comp['color'])
    mapping = {}
    for h, colors in hole_to_colors.items():
        mapping[h] = max(colors)
    return mapping

def find_high_components(g: List[List[int]]) -> List[List[Tuple[int, int]]]:
    """Identify all connected components of cells with values >4 (connected regardless of exact high value)."""
    rows, cols = len(g), len(g[0])
    visited = [[False] * cols for _ in range(rows)]
    components: List[List[Tuple[int, int]]] = []
    for r in range(rows):
        for c in range(cols):
            if g[r][c] > 4 and not visited[r][c]:
                cells = flood_fill_high(g, r, c, visited)
                if cells:
                    components.append(cells)
    return components

def apply_color_to_cells(output: List[List[int]], cells: List[Tuple[int, int]], color: int) -> None:
    """Apply the given color to all cells in the component within the output grid."""
    for r, c in cells:
        output[r][c] = color

def program(g: List[List[int]]) -> List[List[int]]:
    """Main program: Copy grid, build hole-to-color mapping from low components, identify high components, recolor them based on their hole counts using the mapping (default 0 if no match), preserve all other cells."""
    output = copy_grid(g)
    low_components = find_all_low_components(g)
    mapping = build_hole_to_color_mapping(low_components)
    high_components = find_high_components(g)
    for cells in high_components:
        holes = count_holes(g, cells)
        color = mapping.get(holes, 0)
        apply_color_to_cells(output, cells, color)
    return output
```