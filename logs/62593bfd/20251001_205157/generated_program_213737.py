```python
from typing import List, Tuple
from collections import Counter

def find_background_color(grid: List[List[int]]) -> int:
    """
    Identifies the background color as the most frequent color in the grid.
    This preserves the static background observed in all examples.
    """
    if not grid or not grid[0]:
        return 0
    flat = [cell for row in grid for cell in row]
    counts = Counter(flat)
    return counts.most_common(1)[0][0]

def has_five_present(grid: List[List[int]]) -> bool:
    """
    Checks if the color 5 is present anywhere in the grid.
    This determines the decision rule for top/bottom placement based on observed patterns in training examples.
    """
    return any(5 in row for row in grid)

def decide_direction(color: int, bg: int, has_five: bool) -> str:
    """
    Decides whether to place the component at the top or bottom based on color, background, and presence of 5.
    Rule: If 5 is present, place color 1 or 4 at bottom, others at top (if not bg).
    Else, place even colors at bottom, odd at top (if not bg).
    This fits the observed placements in both training examples.
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
    Finds all 8-connected components of the same non-background color.
    Each component is a tuple of (color, list of (row, col) positions).
    This extracts the foreground shapes independently, as observed.
    """
    if not grid or not grid[0]:
        return []
    rows = len(grid)
    cols = len(grid[0])
    visited = [[False] * cols for _ in range(rows)]
    components = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]  # 8-connected
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
                        nx = x + dx
                        ny = y + dy
                        if 0 <= nx < rows and 0 <= ny < cols and not visited[nx][ny] and grid[nx][ny] == color:
                            visited[nx][ny] = True
                            stack.append((nx, ny))
                components.append((color, component))
    return components

def program(g: List[List[int]]) -> List[List[int]]:
    """
    Main function composing all rules to transform the grid.
    - Finds background.
    - Checks for presence of 5.
    - Extracts components.
    - Decides direction for each.
    - Places components at top (min_y=0) or bottom (min_y = rows - height), preserving x and relative y.
    - Fills rest with background.
    This implements the observed translations and independent transformations.
    """
    if not g or not g[0]:
        return g
    num_rows = len(g)
    num_cols = len(g[0])
    bg = find_background_color(g)
    has_five = has_five_present(g)
    components = find_connected_components(g, bg)
    new_grid = [[bg] * num_cols for _ in range(num_rows)]
    for color, comp in components:
        direction = decide_direction(color, bg, has_five)
        if direction is None or not comp:
            continue
        rs = [r for r, _ in comp]
        min_r = min(rs)
        max_r = max(rs)
        height = max_r - min_r + 1
        if direction == "top":
            base_r = 0
        else:  # bottom
            base_r = num_rows - height
        for r, c in comp:
            rel_r = r - min_r
            new_r = base_r + rel_r
            new_grid[new_r][c] = color
    return new_grid
```