```python
from typing import List, Tuple
from collections import Counter

def find_background_color(grid: List[List[int]]) -> int:
    """
    Identifies the background color as the most frequent color in the grid.
    """
    if not grid or not grid[0]:
        return 0
    flat = [cell for row in grid for cell in row]
    counts = Counter(flat)
    return counts.most_common(1)[0][0]

def has_five_present(grid: List[List[int]]) -> bool:
    """
    Checks if the color 5 is present anywhere in the grid.
    """
    return any(5 in row for row in grid)

def decide_direction(color: int, bg: int, has_five: bool) -> str:
    """
    Decides placement: if has_five, 1/4 to bottom else top; else even to bottom, odd to top.
    Returns None if color is background.
    """
    if color == bg:
        return None
    if has_five:
        if color == 1 or color == 4:
            return "bottom"
        else:
            return "top"
    else:
        if color % 2 == 0:
            return "bottom"
        else:
            return "top"

def find_connected_components(grid: List[List[int]], bg: int) -> List[Tuple[int, List[Tuple[int, int]]]]:
    """
    Finds all 8-connected components of non-bg colors, returning (color, list of (row, col) positions).
    Uses DFS with stack for traversal.
    """
    if not grid or not grid[0]:
        return []
    rows, cols = len(grid), len(grid[0])
    visited = [[False] * cols for _ in range(rows)]
    components = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] != bg and not visited[i][j]:
                color = grid[i][j]
                component = []
                stack = [(i, j)]
                visited[i][j] = True
                while stack:
                    x, y = stack.pop()
                    component.append((x, y))
                    for dx, dy in directions:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < rows and 0 <= ny < cols and not visited[nx][ny] and grid[nx][ny] == color:
                            visited[nx][ny] = True
                            stack.append((nx, ny))
                components.append((color, component))
    return components

def program(g: List[List[int]]) -> List[List[int]]:
    """
    Main transformation: extract bg, check for 5, find components, decide directions, place at top/bottom.
    Preserves component shape and x-positions.
    """
    if not g or not g[0]:
        return g
    num_rows, num_cols = len(g), len(g[0])
    bg = find_background_color(g)
    has_five = has_five_present(g)
    components = find_connected_components(g, bg)
    new_grid = [[bg] * num_cols for _ in range(num_rows)]
    for color, comp in components:
        direction = decide_direction(color, bg, has_five)
        if direction is None or not comp:
            continue
        rs = [r for r, _ in comp]
        min_r, max_r = min(rs), max(rs)
        height = max_r - min_r + 1
        base_r = 0 if direction == "top" else num_rows - height
        for r, c in comp:
            rel_r = r - min_r
            new_r = base_r + rel_r
            if 0 <= new_r < num_rows:
                new_grid[new_r][c] = color
    return new_grid
```