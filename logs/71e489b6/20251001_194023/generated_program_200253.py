```python
from typing import List, Tuple
from copy import deepcopy
from collections import deque

directions_4: List[Tuple[int, int]] = [(-1, 0), (1, 0), (0, -1), (0, 1)]
directions_8: List[Tuple[int, int]] = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]

def count_neighbors(grid: List[List[int]], i: int, j: int, rows: int, cols: int, directions: List[Tuple[int, int]], target_values: Tuple[int, ...] = (1,)) -> int:
    return sum(1 for di, dj in directions
               if 0 <= i + di < rows and 0 <= j + dj < cols and grid[i + di][j + dj] in target_values)

def is_on_border(i: int, j: int, rows: int, cols: int) -> bool:
    return i == 0 or i == rows - 1 or j == 0 or j == cols - 1

def program(g: List[List[int]]) -> List[List[int]]:
    if not g or not g[0]:
        return []
    rows = len(g)
    cols = len(g[0])
    output = deepcopy(g)
    
    # Step 1: Remove isolated 1s (those with 0 orthogonal 1-neighbors)
    for i in range(rows):
        for j in range(cols):
            if output[i][j] == 1 and count_neighbors(output, i, j, rows, cols, directions_4, (1,)) == 0:
                output[i][j] = 0
    
    # Step 2: Flood fill to identify background 0s from borders
    background = set()
    visited = [[False] * cols for _ in range(rows)]
    q = deque()
    for i in range(rows):
        for j in range(cols):
            if is_on_border(i, j, rows, cols) and output[i][j] == 0 and not visited[i][j]:
                q.append((i, j))
                visited[i][j] = True
                background.add((i, j))
    while q:
        x, y = q.popleft()
        for di, dj in directions_4:
            nx, ny = x + di, y + dj
            if 0 <= nx < rows and 0 <= ny < cols and output[nx][ny] == 0 and not visited[nx][ny]:
                visited[nx][ny] = True
                background.add((nx, ny))
                q.append((nx, ny))
    
    # Step 3: Create fixed grid for neighbor counting (after removal, before 7s)
    fixed_grid = deepcopy(output)
    
    # Step 4: Process each original 0 cell
    for i in range(rows):
        for j in range(cols):
            if fixed_grid[i][j] == 0:
                num_1_neigh = count_neighbors(fixed_grid, i, j, rows, cols, directions_4, (1,))
                threshold = 2 if is_on_border(i, j, rows, cols) else 3
                if num_1_neigh >= threshold:
                    is_bg = (i, j) in background
                    for di, dj in directions_8:
                        ni, nj = i + di, j + dj
                        if 0 <= ni < rows and 0 <= nj < cols:
                            if output[ni][nj] == 1:
                                output[ni][nj] = 7
                            elif output[ni][nj] == 0 and is_bg:
                                output[ni][nj] = 7
    
    return output
```