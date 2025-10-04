```python
from typing import List

def copy_grid(g: List[List[int]]) -> List[List[int]]:
    return [row[:] for row in g]

def fill_zeros(g: List[List[int]], color: int = 5) -> List[List[int]]:
    return [[color if cell == 0 else cell for cell in row] for row in g]

def program(g: List[List[int]]) -> List[List[int]]:
    grid = copy_grid(g)
    grid = fill_zeros(grid)
    return grid
```