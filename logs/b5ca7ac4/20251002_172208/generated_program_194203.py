```python
from typing import List

def flip_horizontal(g: List[List[int]]) -> List[List[int]]:
    """Flip the grid horizontally (mirror left-right)."""
    return [row[::-1] for row in g]

def program(g: List[List[int]]) -> List[List[int]]:
    """Apply horizontal flip as a simple transformation."""
    return flip_horizontal(g)
```