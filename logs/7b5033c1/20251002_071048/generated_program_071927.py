```python
from typing import List
from collections import deque

def get_background(grid: List[List[int]]) -> int:
    """Identify the background color as the top-left cell."""
    return grid[0][0]

def flood_fill_size(grid: List[List[int]], start_i: int, start_j: int, target_color: int, visited: List[List[bool]]) -> int:
    """Compute the size of the connected component starting from (start_i, start_j) of target_color using BFS, marking visited. Handles 4-way connectivity."""
    h, w = len(grid), len(grid[0])
    q = deque([(start_i, start_j)])
    visited[start_i][start_j] = True
    size = 1
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    while q:
        x, y = q.popleft()
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < h and 0 <= ny < w and not visited[nx][ny] and grid[nx][ny] == target_color:
                visited[nx][ny] = True
                q.append((nx, ny))
                size += 1
    return size

def find_ordered_components(grid: List[List[int]], bg: int) -> List[tuple[int, int]]:
    """Find monochromatic connected components of non-background cells in row-major discovery order, returning list of (color, size)."""
    h, w = len(grid), len(grid[0])
    visited = [[False for _ in range(w)] for _ in range(h)]
    components = []
    for i in range(h):
        for j in range(w):
            if grid[i][j] != bg and not visited[i][j]:
                color = grid[i][j]
                size = flood_fill_size(grid, i, j, color, visited)
                components.append((color, size))
    return components

def build_output(components: List[tuple[int, int]]) -> List[List[int]]:
    """Build the output grid by stacking vertical bars for each component: [color] repeated size times."""
    output = []
    for color, size in components:
        for _ in range(size):
            output.append([color])
    return output

def program(g: List[List[int]]) -> List[List[int]]:
    """Main program: compose background detection, component finding, and output building."""
    bg = get_background(g)
    components = find_ordered_components(g, bg)
    return build_output(components)
```