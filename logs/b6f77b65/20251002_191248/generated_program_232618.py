```python
def get_origin_color(grid: list[list[int]]) -> int:
    """Extract the color at the origin position (0, 0)."""
    return grid[0][0]

def find_connected_components(grid: list[list[int]], color: int) -> list[set[tuple[int, int]]]:
    """
    Find all 4-connected components of the given color in the grid.
    Returns a list of sets, each containing (row, col) positions of a component.
    """
    rows = len(grid)
    cols = len(grid[0])
    visited = [[False] * cols for _ in range(rows)]
    components = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == color and not visited[i][j]:
                component = set()
                stack = [(i, j)]
                visited[i][j] = True
                component.add((i, j))
                while stack:
                    x, y = stack.pop()
                    for dx, dy in directions:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < rows and 0 <= ny < cols and grid[nx][ny] == color and not visited[nx][ny]:
                            visited[nx][ny] = True
                            stack.append((nx, ny))
                            component.add((nx, ny))
                components.append(component)
    return components

def remove_other_matching_color_components(grid: list[list[int]], color: int) -> list[list[int]]:
    """
    Remove all connected components of the given color except the one containing the origin (0, 0).
    Modifies a copy of the grid and returns it.
    """
    new_grid = [row[:] for row in grid]
    components = find_connected_components(new_grid, color)
    origin_pos = (0, 0)
    for component in components:
        if origin_pos not in component:
            for i, j in component:
                new_grid[i][j] = 0
    return new_grid

def program(g: list[list[int]]) -> list[list[int]]:
    """
    Main program: infer origin color, remove other matching color components.
    """
    color = get_origin_color(g)
    if color == 0:
        return [row[:] for row in g]
    return remove_other_matching_color_components(g, color)
```