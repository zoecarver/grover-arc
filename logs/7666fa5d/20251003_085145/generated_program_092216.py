```python
from typing import List

def program(g: List[List[int]]) -> List[List[int]]:
    special = None
    for row in g:
        for cell in row:
            if cell != 8:
                special = cell
                break
        if special is not None:
            break
    if special is None:
        return [row[:] for row in g]
    grid = [row[:] for row in g]
    for r in range(1, len(g)):
        # Vertical propagation from non-8 in previous row
        for c in range(len(grid[r])):
            if grid[r][c] == 8 and grid[r - 1][c] != 8:
                grid[r][c] = 2
        # Horizontal extension once, using copy to avoid chaining beyond one cell
        row_copy = grid[r][:]
        for c in range(len(grid[r]) - 1):
            if row_copy[c] != 8 and grid[r][c + 1] == 8:
                grid[r][c + 1] = 2
    return grid
```