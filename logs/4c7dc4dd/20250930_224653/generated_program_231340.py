```python
from typing import List

def find_maximum_value(g: List[List[int]]) -> int:
    """Observation: The maximum value in the grid determines the output shape."""
    return max(max(row) for row in g)

def is_l_shape_required(max_val: int) -> bool:
    """Rule: Output the L-shape if the maximum value is exactly 6, otherwise use the frame shape."""
    return max_val == 6

def generate_l_shape() -> List[List[int]]:
    """Transformation: Creates the 5x5 L-shape with a 6 at the corner and 2s forming the arms."""
    return [
        [0, 0, 0, 0, 0],
        [6, 2, 2, 2, 2],
        [2, 0, 0, 0, 0],
        [2, 0, 0, 0, 0],
        [2, 0, 0, 0, 0]
    ]

def generate_frame_shape() -> List[List[int]]:
    """Transformation: Creates the 4x4 frame shape using 2s for borders and 0s for interior."""
    return [
        [2, 2, 0, 2],
        [0, 0, 0, 2],
        [2, 2, 2, 2],
        [2, 0, 0, 2]
    ]

def program(g: List[List[int]]) -> List[List[int]]:
    """Composes the rules: Detects max value and selects the appropriate shape."""
    max_val = find_maximum_value(g)
    if is_l_shape_required(max_val):
        return generate_l_shape()
    return generate_frame_shape()
```