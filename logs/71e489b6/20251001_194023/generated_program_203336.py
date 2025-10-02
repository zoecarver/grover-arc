```python
from typing import List
from copy import deepcopy

directions_4 = [(-1, 0), (1, 0), (0, -1), (0, 1)]
directions_8 = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]

def count_neighbors(grid: List[List[int]], i: int, j: int, rows: int, cols: int, directions: List[tuple], target_values: tuple = (1,)) -> int:
    return sum(1 for di, dj in directions
               if 0 <= i + di < rows and 0 <= j + dj < cols and grid[i + di][j + dj] in target_values)

def clean_thin_protrusions(grid: List[List[int]]) -> List[List[int]]:
    rows = len(grid)
    cols = len(grid[0]) if rows else 0
    current = [row[:] for row in grid]
    changed = True
    while changed:
        changed = False
        new_grid = [row[:] for row in current]
        for i in range(rows):
            for j in range(cols):
                if current[i][j] == 1:
                    n = count_neighbors(current, i, j, rows, cols, directions_4, (1,))
                    if n < 2:
                        new_grid[i][j] = 0
                        changed = True
        current = new_grid
    return current

def mark_small_zero_runs(cleaned: List[List[int]], output: List[List[int]]):
    rows = len(cleaned)
    cols = len(cleaned[0]) if rows else 0
    for i in range(rows):
        j = 0
        while j < cols:
            if cleaned[i][j] == 0:
                start = j
                while j < cols and cleaned[i][j] == 0:
                    j += 1
                end = j - 1
                run_size = end - start + 1
                if run_size <= 2:
                    for k in range(start, end + 1):
                        for di, dj in directions_8:
                            ni = i + di
                            nj = k + dj
                            if 0 <= ni < rows and 0 <= nj < cols and cleaned[ni][nj] == 1:
                                output[ni][nj] = 7
            else:
                j += 1

def fill_single_gaps(cleaned: List[List[int]], output: List[List[int]]):
    rows = len(cleaned)
    cols = len(cleaned[0]) if rows else 0
    for i in range(rows):
        j = 0
        while j < cols:
            if cleaned[i][j] == 0:
                start = j
                while j < cols and cleaned[i][j] == 0:
                    j += 1
                end = j - 1
                run_size = end - start + 1
                if run_size == 1:
                    jj = start
                    if jj > 0 and jj < cols - 1 and cleaned[i][jj - 1] == 1 and cleaned[i][jj + 1] == 1:
                        # fill below
                        if i + 1 < rows:
                            if all(cleaned[i + 1][k] == 0 for k in range(jj - 1, jj + 2)):
                                for k in range(jj - 1, jj + 2):
                                    output[i + 1][k] = 7
                        # fill above
                        if i - 1 >= 0:
                            if all(cleaned[i - 1][k] == 0 for k in range(jj - 1, jj + 2)):
                                for k in range(jj - 1, jj + 2):
                                    output[i - 1][k] = 7
            else:
                j += 1

def program(g: List[List[int]]) -> List[List[int]]:
    if not g or not g[0]:
        return []
    cleaned = clean_thin_protrusions(g)
    output = [row[:] for row in cleaned]
    fill_single_gaps(cleaned, output)
    mark_small_zero_runs(cleaned, output)
    return output
```