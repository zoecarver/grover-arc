```python
from typing import List, Tuple, Set
from copy import deepcopy

def num_ortho_ones(grid: List[List[int]], i: int, j: int, rows: int, cols: int) -> int:
    count = 0
    directions: List[Tuple[int, int]] = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for di, dj in directions:
        ni = i + di
        nj = j + dj
        if 0 <= ni < rows and 0 <= nj < cols and grid[ni][nj] == 1:
            count += 1
    return count

def identify_cores(grid: List[List[int]]) -> Set[Tuple[int, int]]:
    rows = len(grid)
    if rows == 0:
        return set()
    cols = len(grid[0])
    cores: Set[Tuple[int, int]] = set()
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == 0 and num_ortho_ones(grid, i, j, rows, cols) >= 3:
                cores.add((i, j))
    return cores

def remove_thin_protrusions(grid: List[List[int]]) -> List[List[int]]:
    rows = len(grid)
    if rows == 0:
        return []
    cols = len(grid[0])
    out = deepcopy(grid)
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == 1 and num_ortho_ones(grid, i, j, rows, cols) < 2:
                out[i][j] = 0
    return out

def get_neighbor_deltas() -> List[Tuple[int, int]]:
    deltas: List[Tuple[int, int]] = []
    for di in [-1, 0, 1]:
        for dj in [-1, 0, 1]:
            if di != 0 or dj != 0:
                deltas.append((di, dj))
    return deltas

def set_dark_red_around_holes(grid: List[List[int]], cores: Set[Tuple[int, int]]) -> List[List[int]]:
    rows = len(grid)
    if rows == 0:
        return []
    cols = len(grid[0])
    out = deepcopy(grid)
    deltas = get_neighbor_deltas()
    for ci, cj in cores:
        for di, dj in deltas:
            ni = ci + di
            nj = cj + dj
            if 0 <= ni < rows and 0 <= nj < cols:
                pi, pj = ni, nj
                if (pi, pj) in cores:
                    continue
                ortho_count = num_ortho_ones(grid, pi, pj, rows, cols)
                if grid[pi][pj] == 1 or (grid[pi][pj] == 0 and ortho_count < 2):
                    out[pi][pj] = 7
    return out

def program(g: List[List[int]]) -> List[List[int]]:
    cores = identify_cores(g)
    temp_grid = remove_thin_protrusions(g)
    result = set_dark_red_around_holes(g, cores)
    # Override the thin removals with red settings where applicable
    rows = len(g)
    if rows == 0:
        return []
    cols = len(g[0])
    for i in range(rows):
        for j in range(cols):
            if temp_grid[i][j] == 0 and g[i][j] == 1 and num_ortho_ones(g, i, j, rows, cols) < 2:
                # Only keep as 0 if not set to 7 in result
                if result[i][j] != 7:
                    result[i][j] = 0
    return result
```