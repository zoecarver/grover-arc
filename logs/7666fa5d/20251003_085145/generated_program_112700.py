```python
from collections import deque
from typing import List

def program(g: List[List[int]]) -> List[List[int]]:
    grid = [row[:] for row in g]
    rows = len(grid)
    cols = len(grid[0])
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    visited = set()
    q = deque()
    # Add border cells that are 8 to queue
    for i in range(rows):
        if grid[i][0] == 8:
            pos = (i, 0)
            if pos not in visited:
                visited.add(pos)
                q.append(pos)
        if grid[i][cols - 1] == 8:
            pos = (i, cols - 1)
            if pos not in visited:
                visited.add(pos)
                q.append(pos)
    for j in range(cols):
        if grid[0][j] == 8:
            pos = (0, j)
            if pos not in visited:
                visited.add(pos)
                q.append(pos)
        if grid[rows - 1][j] == 8:
            pos = (rows - 1, j)
            if pos not in visited:
                visited.add(pos)
                q.append(pos)
    # Flood fill background 8's
    while q:
        x, y = q.popleft()
        for dx, dy in directions:
            nx = x + dx
            ny = y + dy
            if 0 <= nx < rows and 0 <= ny < cols and grid[nx][ny] == 8:
                pos = (nx, ny)
                if pos not in visited:
                    visited.add(pos)
                    q.append(pos)
    # Fill unvisited 8's with 2 (interiors)
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == 8:
                pos = (i, j)
                if pos not in visited:
                    grid[i][j] = 2
    return grid
```