```python
from typing import List

def transpose_grid(grid: List[List[int]]) -> List[List[int]]:
    """Transpose the input grid, swapping rows and columns."""
    return [list(row) for row in zip(*grid)]

def program(g: List[List[int]]) -> List[List[int]]:
    return transpose_grid(g)
```