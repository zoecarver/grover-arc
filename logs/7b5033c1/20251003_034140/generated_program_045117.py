```python
from typing import List
from collections import Counter, deque

def find_background_color(grid: List[List[int]]) -> int:
    """
    Identifies the background color as the most frequent color in the grid.
    Rule: Background is the dominant color by pixel count.
    """
    flat = [cell for row in grid for cell in row]
    counts = Counter(flat)
    return counts.most_common(1)[0][0]

def flood_fill_size(grid: List[List[int]], visited: List[List[bool]], start_r: int, start_c: int, color: int) -> int:
    """
    Computes the size of a 4-connected component of the given color starting from (start_r, start_c).
    Rule: Components are 4-connected (orthogonal adjacency) groups of the exact same non-background color.
    Uses BFS to explore and mark visited cells.
    """
    rows, cols = len(grid), len(grid[0])
    queue = deque([(start_r, start_c)])
    visited[start_r][start_c] = True
    size = 1
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # 4-connectivity
    while queue:
        r, c = queue.popleft()
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and not visited[nr][nc] and grid[nr][nc] == color:
                visited[nr][nc] = True
                queue.append((nr, nc))
                size += 1
    return size

def extract_ordered_components(grid: List[List[int]], bg: int) -> List[tuple[int, int]]:
    """
    Extracts connected components in row-major discovery order, returning (color, size) for each.
    Rule: Scan top-to-bottom, left-to-right; start a new component at each unvisited non-background cell.
    """
    rows, cols = len(grid), len(grid[0])
    visited = [[False] * cols for _ in range(rows)]
    components = []
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] != bg and not visited[r][c]:
                color = grid[r][c]
                size = flood_fill_size(grid, visited, r, c, color)
                components.append((color, size))
    return components

def build_stacked_output(components: List[tuple[int, int]]) -> List[List[int]]:
    """
    Builds the output by stacking [color] lists, repeating each by the component's size in discovery order.
    Rule: Output is a vertical sequence of single-pixel rows for all non-background pixels, grouped by component.
    """
    output = []
    for color, size in components:
        for _ in range(size):
            output.append([color])
    return output

def program(g: List[List[int]]) -> List[List[int]]:
    """
    Main program: Compose background identification, component extraction, and output building.
    """
    background = find_background_color(g)
    components = extract_ordered_components(g, background)
    return build_stacked_output(components)
```