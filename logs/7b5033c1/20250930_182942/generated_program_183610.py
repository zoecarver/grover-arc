```python
from typing import List
from collections import Counter, deque


def find_background(grid: List[List[int]]) -> int:
    """
    Identifies the background color as the most frequent value in the grid.
    """
    all_values = []
    for row in grid:
        all_values.extend(row)
    counts = Counter(all_values)
    return counts.most_common(1)[0][0]


def find_connected_components(grid: List[List[int]], background: int) -> List[List[int]]:
    """
    Finds connected components (4-connected) of non-background cells, discovered in row-major order.
    For each component, collects colors of its cells sorted in row-major order.
    """
    if not grid or not grid[0]:
        return []
    rows, cols = len(grid), len(grid[0])
    visited = set()
    components = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] != background and (i, j) not in visited:
                comp_cells = []
                queue = deque([(i, j)])
                visited.add((i, j))
                while queue:
                    x, y = queue.popleft()
                    comp_cells.append((x, y))
                    for dx, dy in directions:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < rows and 0 <= ny < cols and grid[nx][ny] != background and (nx, ny) not in visited:
                            visited.add((nx, ny))
                            queue.append((nx, ny))
                comp_cells.sort(key=lambda p: (p[0], p[1]))
                comp_colors = [grid[r][c] for r, c in comp_cells]
                components.append(comp_colors)
    return components


def program(g: List[List[int]]) -> List[List[int]]:
    """
    Main program: finds background, extracts connected components of non-background cells in discovery order,
    serializes each component's colors in row-major cell order as singleton rows.
    """
    background = find_background(g)
    components = find_connected_components(g, background)
    result = []
    for comp in components:
        for color in comp:
            result.append([color])
    return result
```