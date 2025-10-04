```python
from typing import List
from itertools import zip_longest

def transpose_grid(g: List[List[int]]) -> List[List[int]]:
    """Transpose the input grid, swapping rows and columns."""
    return [list(row) for row in zip(*g)]

def program(g: List[List[int]]) -> List[List[int]]:
    """Main program: transpose the grid to swap dimensions."""
    return transpose_grid(g)
```