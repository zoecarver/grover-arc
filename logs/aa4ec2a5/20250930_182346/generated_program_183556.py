```python
from typing import List
from collections import deque

def mark_exterior(g: List[List[int]], temp: List[List[int]], rows: int, cols: int) -> None:
    if rows == 0 or cols == 0:
        return
    visited = [[False] * cols for _ in range(rows)]
    q = deque()
    # Top and bottom borders
    for j in range(cols):
        if g[0][j] == 4 and not visited[0][j]:
            q.append((0, j))
            visited[0][j] = True
            temp[0][j] = 5
        if rows > 1 and g[rows - 1][j] == 4 and not visited[rows - 1][j]:
            q.append((rows - 1, j))
            visited[rows - 1][j] = True
            temp[rows - 1][j] = 5
    # Left and right borders
    for i in range(rows):
        if g[i][0] == 4 and not visited[i][0]:
            q.append((i, 0))
            visited[i][0] = True
            temp[i][0] = 5
        if cols > 1 and g[i][cols - 1] == 4 and not visited[i][cols - 1]:
            q.append((i, cols - 1))
            visited[i][cols - 1] = True
            temp[i][cols - 1] = 5
    dirs8 = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    while q:
        x, y = q.popleft()
        for dx, dy in dirs8:
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
    # Set interior walls to 6
    for i in range(rows):
        for j in range(cols):
            if g[i][j] == 4 and temp[i][j] != 5:
                output[i][j] = 6
    # Directions
    dirs4 = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    dirs8 = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    # Initial 8s: floors adjacent (4-connected) to 6s
    for i in range(rows):
        for j in range(cols):
            if g[i][j] == 1:
                for dx, dy in dirs4:
                    ni, nj = i + dx, j + dy
                    if 0 <= ni < rows and 0 <= nj < cols and output[ni][nj] == 6:
                        output[i][j] = 8
                        break
    # Propagate 8s through connected floor components (4-connected)
    visited = [[False] * cols for _ in range(rows)]
    q = deque()
    for i in range(rows):
        for j in range(cols):
            if output[i][j] == 8 and g[i][j] == 1 and not visited[i][j]:
                q.append((i, j))
                visited[i][j] = True
    while q:
        x, y = q.popleft()
        for dx, dy in dirs4:
            nx, ny = x + dx, y + dy
            if 0 <= nx < rows and 0 <= ny < cols and g[nx][ny] == 1 and not visited[nx][ny]:
                output[nx][ny] = 8
                visited[nx][ny] = True
                q.append((nx, ny))
    # Set exterior walls adjacent (8-connected) to floors (1 or 8) to 2
    for i in range(rows):
        for j in range(cols):
            if output[i][j] == 4:
                for dx, dy in dirs8:
                    ni, nj = i + dx, j + dy
                    if 0 <= ni < rows and 0 <= nj < cols and output[ni][nj] in (1, 8):
                        output[i][j] = 2
                        break
    return output
```