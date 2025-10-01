```python
from typing import List

def mark_exterior(g: List[List[int]], temp: List[List[int]], rows: int, cols: int) -> None:
    visited = [[False] * cols for _ in range(rows)]
    q = []
    # Top and bottom borders
    for j in range(cols):
        if g[0][j] == 4 and not visited[0][j]:
            q.append((0, j))
            visited[0][j] = True
            temp[0][j] = 5
        if g[rows - 1][j] == 4 and not visited[rows - 1][j]:
            q.append((rows - 1, j))
            visited[rows - 1][j] = True
            temp[rows - 1][j] = 5
    # Left and right borders
    for i in range(rows):
        if g[i][0] == 4 and not visited[i][0]:
            q.append((i, 0))
            visited[i][0] = True
            temp[i][0] = 5
        if g[i][cols - 1] == 4 and not visited[i][cols - 1]:
            q.append((i, cols - 1))
            visited[i][cols - 1] = True
            temp[i][cols - 1] = 5
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    while q:
        x, y = q.pop(0)
        for dx, dy in dirs:
            nx, ny = x + dx, y + dy
            if 0 <= nx < rows and 0 <= ny < cols and g[nx][ny] == 4 and not visited[nx][ny]:
                visited[nx][ny] = True
                temp[nx][ny] = 5
                q.append((nx, ny))

def program(g: List[List[int]]) -> List[List[int]]:
    if not g or not g[0]:
        return []
    rows = len(g)
    cols = len(g[0])
    temp = [row[:] for row in g]
    mark_exterior(g, temp, rows, cols)
    output = [row[:] for row in g]
    dirs4 = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    # Set 4s
    for i in range(rows):
        for j in range(cols):
            if g[i][j] == 4:
                output[i][j] = 4 if temp[i][j] == 5 else 6
    # Set 1s
    for i in range(rows):
        for j in range(cols):
            if g[i][j] == 1:
                has_hole = any(0 <= i + dx < rows and 0 <= j + dy < cols and temp[i + dx][j + dy] == 4
                               for dx, dy in dirs4)
                output[i][j] = 8 if has_hole else 1
    # No special adjustment for top row of holes to keep simple
    # Add borders 8-connected
    dirs8 = [(dx, dy) for dx in [-1, 0, 1] for dy in [-1, 0, 1] if dx != 0 or dy != 0]
    for i in range(rows):
        for j in range(cols):
            if g[i][j] == 1:
                for dx, dy in dirs8:
                    ni, nj = i + dx, j + dy
                    if 0 <= ni < rows and 0 <= nj < cols and g[ni][nj] == 4 and temp[ni][nj] == 5:
                        output[ni][nj] = 2
    return output
```