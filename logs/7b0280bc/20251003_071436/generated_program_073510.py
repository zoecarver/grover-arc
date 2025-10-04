```python
from typing import List

def copy_grid(g: List[List[int]]) -> List[List[int]]:
    """Copy the input grid."""
    return [row[:] for row in g]

def fill_zeros_with_orange(g: List[List[int]]) -> List[List[int]]:
    """Fill all empty cells (0) with orange (5), based on observation that empty spaces are filled in outputs."""
    h = copy_grid(g)
    for i in range(len(h)):
        h[i] = [5 if cell == 0 else cell for cell in h[i]]
    return h

def program(g: List[List[int]]) -> List[List[int]]:
    """Compose transformations: copy and fill zeros with orange."""
    return fill_zeros_with_orange(g)
```