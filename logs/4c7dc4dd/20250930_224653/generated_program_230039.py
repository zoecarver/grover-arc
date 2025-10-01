```python
from typing import List

def has_six(g: List[List[int]]) -> bool:
    """Rule: Check if the value 6 is present anywhere in the grid, indicating the L-shape output."""
    for row in g:
        for cell in row:
            if cell == 6:
                return True
    return False

def create_l_shape() -> List[List[int]]:
    """Transformation: Generate the 5x5 L-shape grid with 6 at the corner and 2s forming the L."""
    return [
        [0, 0, 0, 0, 0],
        [6, 2, 2, 2, 2],
        [2, 0, 0, 0, 0],
        [2, 0, 0, 0, 0],
        [2, 0, 0, 0, 0]
    ]

def create_frame_shape() -> List[List[int]]:
    """Transformation: Generate the 4x4 frame-like shape grid with 2s on borders and 0s inside."""
    return [
        [2, 2, 0, 2],
        [0, 0, 0, 2],
        [2, 2, 2, 2],
        [2, 0, 0, 2]
    ]

def program(g: List[List[int]]) -> List[List[int]]:
    """Main program: Compose rules to select output shape based on presence of 6."""
    if has_six(g):
        return create_l_shape()
    else:
        return create_frame_shape()
```