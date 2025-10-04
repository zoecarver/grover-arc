```python
from typing import List

def reverse_rows(g: List[List[int]]) -> List[List[int]]:
    """Reverse the order of rows in the grid."""
    return g[::-1]

def transpose_grid(g: List[List[int]]) -> List[List[int]]:
    """Transpose the grid by swapping rows and columns."""
    if not g or not g[0]:
        return []
    return [list(row) for row in zip(*g)]

def rotate90_clockwise(g: List[List[int]]) -> List[List[int]]:
    """Rotate the grid 90 degrees clockwise by reversing rows and transposing."""
    reversed_g = reverse_rows(g)
    rotated = transpose_grid(reversed_g)
    return rotated

def program(g: List[List[int]]) -> List[List[int]]:
    """Apply 90-degree clockwise rotation to the input grid."""
    return rotate90_clockwise(g)
```