```python
from typing import List

def copy_grid(g: List[List[int]]) -> List[List[int]]:
    """Copy the input grid as is."""
    return [row[:] for row in g]

def program(g: List[List[int]]) -> List[List[int]]:
    """The main program that applies the rules by copying the grid."""
    return copy_grid(g)
```