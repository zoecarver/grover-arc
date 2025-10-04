```python
from typing import List
from collections import Counter, deque

def find_background_color(grid: List[List[int]]) -> int:
    flat = [cell for row in grid for cell in row]
    return Counter(flat).most_common(1)[0][0]

def compute_component_size(grid: List[List[int]], visited: List[List[bool]], r: int, c: int, color: int) -> int:
    rows, cols = len(grid), len(grid[0])
    queue = deque([(r, c)])
    visited[r][c] = True
    size = 1
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    while queue:
        x, y = queue.popleft()
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < rows and 0 <= ny < cols and not visited[nx][ny] and grid[nx][ny] == color:
                visited[nx][ny] = True
                queue.append((nx, ny))
                size += 1
    return size

def extract_components(grid: List[List[int]], bg: int) -> List[tuple[int, int]]:
    rows, cols = len(grid), len(grid[0])
    visited = [[False] * cols for _ in range(rows)]
    components = []
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] != bg and not visited[i][j]:
                color = grid[i][j]
                size = compute_component_size(grid, visited, i, j, color)
                components.append((color, size))
    return components

def build_output(components: List[tuple[int, int]]) -> List[List[int]]:
    output = []
    for color, size in components:
        for _ in range(size):
            output.append([color])
    return output

def program(g: List[List[int]]) -> List[List[int]]:
    bg = find_background_color(g)
    comps = extract_components(g, bg)
    return build_output(comps)
```