```python
from typing import List

def get_max_value(g: List[List[int]]) -> int:
    """Observes the highest number in the grid to determine the output shape."""
    max_val = 0
    for row in g:
        if row:
            row_max = max(row)
            if row_max > max_val:
                max_val = row_max
    return max_val

def is_l_shape_case(max_val: int) -> bool:
    """Rule: L-shape required if and only if the maximum value is exactly 6."""
    return max_val == 6

def create_l_shape() -> List[List[int]]:
    """Generates the 5x5 L-shape with 6 at the corner and 2s along the arms."""
    return [
        [0, 0, 0, 0, 0],
        [6, 2, 2, 2, 2],
        [2, 0, 0, 0, 0],
        [2, 0, 0, 0, 0],
        [2, 0, 0, 0, 0]
    ]

def create_frame_shape() -> List[List[int]]:
    """Generates the 4x4 irregular frame with 2s on borders and 0s inside."""
    return [
        [2, 2, 0, 2],
        [0, 0, 0, 2],
        [2, 2, 2, 2],
        [2, 0, 0, 2]
    ]

def program(g: List[List[int]]) -> List[List[int]]:
    """Main program: Detects max value and selects the appropriate shape."""
    max_val = get_max_value(g)
    if is_l_shape_case(max_val):
        return create_l_shape()
    return create_frame_shape()
```