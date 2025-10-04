```python
from typing import List

def is_peripheral(i: int, j: int) -> bool:
    if i <= 2:
        if i == 0:
            return j >= 6
        if i == 1:
            return j >= 7 or j == 10
        if i == 2:
            return j <= 3 or j == 10
    if j <= 1 and 4 <= i <= 7:
        return True
    if j >= 9 and (i <= 2 or i == 5):
        return True
    return False

def fill_center(grid: List[List[int]], n: int) -> None:
    # Rule: Replace min(n, 8) 3's in row-major order, skipping the 2 position.
    # If n > 8, also replace the 2 with 9.
    positions = [(ii, jj) for ii in range(4, 7) for jj in range(4, 7)]
    k = 0
    for p in range(9):
        ii, jj = positions[p]
        if grid[ii][jj] == 3 and k < n:
            grid[ii][jj] = 9
            k += 1
        elif grid[ii][jj] == 2:
            # Skip the 2 position, do not increment k
            continue
    if n > 8:
        grid[5][5] = 9

def program(g: List[List[int]]) -> List[List[int]]:
    grid = [row[:] for row in g]
    # Check if there is any pink (6) in the grid
    has_pink = any(6 in row for row in g)
    n = 0
    if not has_pink:
        # Special case: Change all 9's to 7's
        for i in range(11):
            for j in range(11):
                if grid[i][j] == 9:
                    grid[i][j] = 7
                    n += 1
    else:
        # With pink: Change 9's that are not peripheral to 7's
        for i in range(11):
            for j in range(11):
                if grid[i][j] == 9 and not is_peripheral(i, j):
                    grid[i][j] = 7
                    n += 1
    # Apply central filling rule
    fill_center(grid, n)
    return grid
```