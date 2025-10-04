```python
from typing import List

def copy_grid(g: List[List[int]]) -> List[List[int]]:
    """Rule: Copy the input grid unchanged, as a baseline transformation."""
    return [row[:] for row in g]

def program(g: List[List[int]]) -> List[List[int]]:
    return copy_grid(g)
```