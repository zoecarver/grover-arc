```python
from typing import List
from copy import deepcopy

# Directions for 4-connectivity (orthogonal neighbors)
directions_4 = [(-1, 0), (1, 0), (0, -1), (0, 1)]

# Directions for 8-connectivity (including diagonals)
directions_8 = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]

def count_neighbors(grid: List[List[int]], i: int, j: int, rows: int, cols: int, directions: List[tuple], target_values: tuple = (1,)) -> int:
    """Count adjacent cells matching target_values in given directions."""
    return sum(1 for di, dj in directions 
               if 0 <= i + di < rows and 0 <= j + dj < cols and grid[i + di][j + dj] in target_values)

def extract_blobs(grid: List[List[int]]) -> List[List[List[int]]]:
    """Extract connected components (blobs) of 1s using 4-connectivity; useful for processing objects separately."""
    rows, cols = len(grid), len(grid[0]) if grid else 0
    visited = [[False] * cols for _ in range(rows)]
    blobs = []
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == 1 and not visited[i][j]:
                blob = []
                stack = [(i, j)]
                visited[i][j] = True
                while stack:
                    x, y = stack.pop()
                    blob.append((x, y))
                    for di, dj in directions_4:
                        ni, nj = x + di, y + dj
                        if 0 <= ni < rows and 0 <= nj < cols and grid[ni][nj] == 1 and not visited[ni][nj]:
                            visited[ni][nj] = True
                            stack.append((ni, nj))
                blobs.append(blob)
    return blobs  # List of lists of (i,j) positions for each blob

def remove_isolated(grid: List[List[int]]) -> List[List[int]]:
    """Set isolated 1s (0 orthogonal 1-neighbors) to 0."""
    rows, cols = len(grid), len(grid[0])
    new_grid = [row[:] for row in grid]
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == 1 and count_neighbors(grid, i, j, rows, cols, directions_4, (1,)) == 0:
                new_grid[i][j] = 0
    return new_grid

def extract_internal_holes(grid: List[List[int]]) -> List[List[List[int]]]:
    """Extract small internal 0 components (size <=2, 4-connectivity, not touching border)."""
    rows, cols = len(grid), len(grid[0])
    visited = [[False] * cols for _ in range(rows)]
    holes = []
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == 0 and not visited[i][j]:
                hole = []
                stack = [(i, j)]
                visited[i][j] = True
                hole.append((i, j))
                touches_border = (i == 0 or i == rows - 1 or j == 0 or j == cols - 1)
                while stack:
                    x, y = stack.pop()
                    for di, dj in directions_4:
                        ni, nj = x + di, y + dj
                        if 0 <= ni < rows and 0 <= nj < cols and grid[ni][nj] == 0 and not visited[ni][nj]:
                            visited[ni][nj] = True
                            stack.append((ni, nj))
                            hole.append((ni, nj))
                            if ni == 0 or ni == rows - 1 or nj == 0 or nj == cols - 1:
                                touches_border = True
                if not touches_border and len(hole) <= 2:
                    holes.append(hole)
    return holes

def process_internal_holes(grid: List[List[int]], holes: List[List[List[int]]]) -> List[List[int]]:
    """Process small internal holes: mark adjacent for size 1, sides and below bar for size 2."""
    rows, cols = len(grid), len(grid[0])
    new_grid = [row[:] for row in grid]
    for hole in holes:
        if len(hole) == 1:
            i, j = hole[0]
            for di, dj in directions_8:
                ni, nj = i + di, j + dj
                if 0 <= ni < rows and 0 <= nj < cols and new_grid[ni][nj] == 1:
                    new_grid[ni][nj] = 7
        elif len(hole) == 2:
            ps = sorted(hole, key=lambda p: p[1])
            if ps[0][0] == ps[1][0] and ps[1][1] == ps[0][1] + 1:
                i = ps[0][0]
                j1, j2 = ps[0][1], ps[1][1]
                # sides
                for sj in [j1 - 1, j2 + 1]:
                    if 0 <= sj < cols and new_grid[i][sj] == 1:
                        new_grid[i][sj] = 7
                # below bar
                bi = i + 1
                if bi < rows:
                    for bj in range(j1 - 1, j2 + 2):
                        if 0 <= bj < cols and (new_grid[bi][bj] == 0 or new_grid[bi][bj] == 1):
                            new_grid[bi][bj] = 7
    return new_grid

def process_dents(grid: List[List[int]], input_grid: List[List[int]]) -> List[List[int]]:
    """Process external dents (0s with exactly 3 1-neighbors in current grid): mark adjacent 1s, fill perpendicular 3 in open dir."""
    rows, cols = len(grid), len(grid[0])
    new_grid = [row[:] for row in grid]
    for i in range(rows):
        for j in range(cols):
            if input_grid[i][j] == 0:
                n = count_neighbors(grid, i, j, rows, cols, directions_4, (1,))
                if n == 3:
                    # mark adjacent 1s
                    for di, dj in directions_4:
                        ni, nj = i + di, j + dj
                        if 0 <= ni < rows and 0 <= nj < cols and new_grid[ni][nj] == 1:
                            new_grid[ni][nj] = 7
                    # find open dir (where neighbor not 1 in current)
                    open_di, open_dj = None, None
                    for di, dj in directions_4:
                        ni, nj = i + di, j + dj
                        if not (0 <= ni < rows and 0 <= nj < cols) or grid[ni][nj] != 1:
                            open_di, open_dj = di, dj
                            break
                    if open_di is not None and open_dj is not None:
                        if open_dj == 0:  # vertical open (up or down)
                            fi = i + open_di
                            if 0 <= fi < rows:
                                for djj in [-1, 0, 1]:
                                    fj = j + djj
                                    if 0 <= fj < cols and (new_grid[fi][fj] == 0 or new_grid[fi][fj] == 1):
                                        new_grid[fi][fj] = 7
                        else:  # horizontal open (left or right)
                            fj = j + open_dj
                            if 0 <= fj < cols:
                                for dii in [-1, 0, 1]:
                                    fi = i + dii
                                    if 0 <= fi < rows and (new_grid[fi][fj] == 0 or new_grid[fi][fj] == 1):
                                        new_grid[fi][fj] = 7
    return new_grid

def process_border_gaps(grid: List[List[int]], input_grid: List[List[int]]) -> List[List[int]]:
    """Process border-touching 0s with exactly 2 1-neighbors: mark adjacent 1s."""
    rows, cols = len(grid), len(grid[0])
    new_grid = [row[:] for row in grid]
    for i in range(rows):
        for j in range(cols):
            if input_grid[i][j] == 0 and (i == 0 or i == rows - 1 or j == 0 or j == cols - 1):
                n = count_neighbors(input_grid, i, j, rows, cols, directions_4, (1,))
                if n == 2:
                    # mark adjacent 1s
                    for di, dj in directions_4:
                        ni, nj = i + di, j + dj
                        if 0 <= ni < rows and 0 <= nj < cols and new_grid[ni][nj] == 1:
                            new_grid[ni][nj] = 7
    return new_grid

def final_boundary_mark(input_grid: List[List[int]], grid: List[List[int]]) -> List[List[int]]:
    """Final pass: set remaining 1s with 1-2 input 0s in 8-neighborhood to 7."""
    rows, cols = len(grid), len(grid[0])
    new_grid = [row[:] for row in grid]
    for i in range(rows):
        for j in range(cols):
            if new_grid[i][j] == 1:
                num_zeros = count_neighbors(input_grid, i, j, rows, cols, directions_8, (0,))
                if 1 <= num_zeros <= 2:
                    new_grid[i][j] = 7
    return new_grid

def program(g: List[List[int]]) -> List[List[int]]:
    input_grid = [row[:] for row in g]
    grid = remove_isolated(input_grid)
    internal_holes = extract_internal_holes(grid)
    grid = process_internal_holes(grid, internal_holes)
    grid = process_dents(grid, input_grid)
    grid = process_border_gaps(grid, input_grid)
    grid = final_boundary_mark(input_grid, grid)
    return grid
```