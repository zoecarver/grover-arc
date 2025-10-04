```python
from typing import List

def transpose(g: List[List[int]]) -> List[List[int]]:
    """Transpose the grid, swapping rows and columns."""
    if not g or not g[0]:
        return []
    return [list(col) for col in zip(*g)]

def program(g: List[List[int]]) -> List[List[int]]:
    return transpose(g)
```