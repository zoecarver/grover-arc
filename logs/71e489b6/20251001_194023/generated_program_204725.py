```python
from typing import List, Tuple, Set
from copy import deepcopy
from collections import deque

directions_4: List[Tuple[int, int]] = [(-1, 0), (1, 0), (0, -1), (0, 1)]
directions_8: List[Tuple[int, int]] = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]

def count_neighbors(grid: List[List[int]], i: int, j: int, rows: int, cols: int, directions: List[Tuple[int, int]], target_values: Tuple[int, ...] = (1,)) -> int:
    """Count adjacent cells matching target_values in given directions."""
    return sum(1 for di, dj in directions 
               if 0 <= i + di < rows and 0 <= j + dj < cols and grid[i + di][j + dj] in target_values)

def is_on_border(i: int, j: int, rows: int, cols: int) -> bool:
    """Check if cell is on grid border."""
    return i == 0 or i == rows - 1 or j == 0 or j == cols - 1

def remove_isolated(grid: List[List[int]]) -> List[List[int]]:
    """Remove isolated 1s (0 orthogonal 1-neighbors) iteratively until no changes."""
    if not grid or not grid[0]:
        return []
    rows, cols = len(grid), len(grid[0])
    output = [row[:] for row in grid]
    changed = True
    while changed:
        changed = False
        new_output = [row[:] for row in output]
        for ii in range(rows):
            for jj in range(cols):
                if output[ii][jj] == 1 and count_neighbors(output, ii, jj, rows, cols, directions_4, (1,)) == 0:
                    new_output[ii][jj] = 0
                    changed = True
        output = new_output
    return output

def identify_background(grid: List[List[int]]) -> Set[Tuple[int, int]]:
    """Flood fill from border 0s to identify background using 4-connectivity."""
    rows, cols = len(grid), len(grid[0])
    if rows == 0 or cols == 0:
        return set()
    background: Set[Tuple[int, int]] = set()
    visited = [[False] * cols for _ in range(rows)]
    q = deque()
    # Seed border 0s
    for i in range(rows):
        for edge_j in [0, cols - 1]:
            if grid[i][edge_j] == 0 and not visited[i][edge_j]:
                q.append((i, edge_j))
                visited[i][edge_j] = True
                background.add((i, edge_j))
    for j in range(cols):
        for edge_i in [0, rows - 1]:
            if grid[edge_i][j] == 0 and not visited[edge_i][j]:
                q.append((edge_i, j))
                visited[edge_i][j] = True
                background.add((edge_i, j))
    while q:
        x, y = q.popleft()
        for di, dj in directions_4:
            nx, ny = x + di, y + dj
            if 0 <= nx < rows and 0 <= ny < cols and grid[nx][ny] == 0 and not visited[nx][ny]:
                visited[nx][ny] = True
                background.add((nx, ny))
                q.append((nx, ny))
    return background

def mark_boundaries_around_enclosed_holes(grid: List[List[int]]) -> List[List[int]]:
    """Mark 1s adjacent (8-dir) to internal 0s (non-background with >=3 1 neighbors) as 7."""
    if not grid or not grid[0]:
        return []
    rows, cols = len(grid), len(grid[0])
    background = identify_background(grid)
    output = [row[:] for row in grid]
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == 0 and (i, j) not in background:
                n1 = count_neighbors(grid, i, j, rows, cols, directions_4, (1,))
                if n1 >= 3 or (n1 >= 2 and is_on_border(i, j, rows, cols)):
                    # Mark adjacent 1s in 8 directions to 7
                    for di, dj in directions_8:
                        ni, nj = i + di, j + dj
                        if 0 <= ni < rows and 0 <= nj < cols and grid[ni][nj] == 1:
                            output[ni][nj] = 7
    return output

def fill_and_mark_small_dents(grid: List[List[int]]) -> List[List[int]]:
    """For background 0s with high 1 neighbors, mark adjacent 1s to 7 and fill adjacent low-1 0s to 7."""
    if not grid or not grid[0]:
        return []
    rows, cols = len(grid), len(grid[0])
    background = identify_background(grid)
    output = [row[:] for row in grid]
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == 0 and (i, j) in background:
                n1 = count_neighbors(grid, i, j, rows, cols, directions_4, (1,))
                threshold = 2 if is_on_border(i, j, rows, cols) else 3
                if n1 >= threshold:
                    # Mark adjacent 1s to 7 and fill adjacent background 0s with 0 1-neighbors to 7
                    for di, dj in directions_8:
                        ni, nj = i + di, j + dj
                        if 0 <= ni < rows and 0 <= nj < cols:
                            if grid[ni][nj] == 1:
                                output[ni][nj] = 7
                            elif grid[ni][nj] == 0 and (ni, nj) in background:
                                neigh1 = count_neighbors(grid, ni, nj, rows, cols, directions_4, (1,))
                                if neigh1 == 0:
                                    output[ni][nj] = 7
    return output

def program(g: List[List[int]]) -> List[List[int]]:
    """Main program: clean isolated, mark enclosed holes, fill/mark dents."""
    if not g or not g[0]:
        return []
    # Step 1: Remove isolated 1s
    cleaned = remove_isolated(g)
    # Step 2: Mark boundaries around enclosed holes
    marked_holes = mark_boundaries_around_enclosed_holes(cleaned)
    # Step 3: Fill and mark small dents
    final = fill_and_mark_small_dents(marked_holes)
    return final
```