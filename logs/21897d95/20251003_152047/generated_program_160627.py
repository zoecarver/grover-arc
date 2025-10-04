```python
from typing import List

def transpose_grid(grid: List[List[int]]) -> List[List[int]]:
    if not grid or not grid[0]:
        return []
    rows = len(grid)
    cols = len(grid[0])
    return [[grid[r][c] for r in range(rows)] for c in range(cols)]

def program(g: List[List[int]]) -> List[List[int]]:
    return transpose_grid(g)
```