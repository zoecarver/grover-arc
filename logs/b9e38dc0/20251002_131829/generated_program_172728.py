```python
from typing import List
from collections import Counter, deque
from copy import deepcopy

def identify_background(g: List[List[int]]) -> int:
    flat = [cell for row in g for cell in row]
    counts = Counter(flat)
    return counts.most_common(1)[0][0]

def identify_fill_color(g: List[List[int]], b: int) -> int:
    counts = Counter(cell for row in g for cell in row if cell != b)
    if not counts:
        return b
    return min(counts, key=counts.get)

def flood_fill(g: List[List[int]], f: int, b: int) -> List[List[int]]:
    grid = deepcopy(g)
    height = len(grid)
    if height == 0:
        return grid
    width = len(grid[0])
    visited = [[False] * width for _ in range(height)]
    q = deque()
    for i in range(height):
        for j in range(width):
            if grid[i][j] == f and not visited[i][j]:
                q.append((i, j))
                visited[i][j] = True
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    while q:
        x, y = q.popleft()
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < height and 0 <= ny < width and not visited[nx][ny] and grid[nx][ny] == b:
                grid[nx][ny] = f
                visited[nx][ny] = True
                q.append((nx, ny))
    return grid

def program(g: List[List[int]]) -> List[List[int]]:
    b = identify_background(g)
    f = identify_fill_color(g, b)
    return flood_fill(g, f, b)
```