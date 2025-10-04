```python
from typing import List
from copy import deepcopy

def copy_grid(g: List[List[int]]) -> List[List[int]]:
    """Copy the input grid."""
    return deepcopy(g)

def is_valid(x: int, y: int, size: int) -> bool:
    """Check if position is within grid bounds."""
    return 0 <= x < size and 0 <= y < size

def flood_fill(h: List[List[int]], visited: List[List[bool]], g: List[List[int]], x: int, y: int, color: int, size: int):
    """Flood fill a connected component of cells >4 with the given color using stack (non-recursive)."""
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    stack = [(x, y)]
    visited[x][y] = True
    h[x][y] = color
    while stack:
        cx, cy = stack.pop()
        for dx, dy in directions:
            nx, ny = cx + dx, cy + dy
            if is_valid(nx, ny, size) and g[nx][ny] > 4 and not visited[nx][ny]:
                visited[nx][ny] = True
                h[nx][ny] = color
                stack.append((nx, ny))

def assign_colors_to_components(g: List[List[int]]) -> List[List[int]]:
    """Assign colors 1-4 to connected components of cells >4 in raster order."""
    size = len(g)
    h = copy_grid(g)
    visited = [[False for _ in range(size)] for _ in range(size)]
    component_id = 0
    for i in range(size):
        for j in range(size):
            if g[i][j] > 4 and not visited[i][j]:
                component_id += 1
                color = (component_id % 4) + 1
                flood_fill(h, visited, g, i, j, color, size)
    return h

def program(g: List[List[int]]) -> List[List[int]]:
    """Main program: leave cells <=4 unchanged, color connected components of >4 cells with 1-4 cycling by discovery order."""
    return assign_colors_to_components(g)
```