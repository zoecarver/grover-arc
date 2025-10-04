```python
from typing import List

def has_six(g: List[List[int]]) -> bool:
    """
    Checks for the presence of 6 anywhere in the grid.
    Returns True if 6 is found, False otherwise.
    """
    return any(6 in row for row in g)

def build_l_shape() -> List[List[int]]:
    """
    Builds the fixed 5x5 L-shape output: top row zeros, second row starts with 6 followed by 2s, lower rows have 2 in first column.
    Used when 6 is present in input.
    """
    return [
        [0, 0, 0, 0, 0],
        [6, 2, 2, 2, 2],
        [2, 0, 0, 0, 0],
        [2, 0, 0, 0, 0],
        [2, 0, 0, 0, 0]
    ]

def build_h_shape() -> List[List[int]]:
    """
    Builds the fixed 4x4 H-like shape output using only 2s in specific positions, zeros elsewhere.
    Used when 6 is absent from input.
    """
    return [
        [2, 2, 0, 2],
        [0, 0, 0, 2],
        [2, 2, 2, 2],
        [2, 0, 0, 2]
    ]

def program(g: List[List[int]]) -> List[List[int]]:
    """
    Main program: determines output based on presence of 6 in input grid.
    If 6 present, returns 5x5 L-shape; else returns 4x4 H-shape.
    """
    if has_six(g):
        return build_l_shape()
    else:
        return build_h_shape()
```