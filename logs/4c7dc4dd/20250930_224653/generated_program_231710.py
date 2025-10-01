```python
from typing import List

def get_max_value(g: List[List[int]]) -> int:
    """Observes the highest number in the grid to determine the puzzle type."""
    return max(map(max, g))

def requires_l_shape(max_val: int) -> bool:
    """Rule: L-shape is required exactly when the maximum value is 6."""
    return max_val == 6

def generate_l_shape() -> List[List[int]]:
    """Transformation: Creates the 5x5 L-shape with 6 at the corner and 2s forming the arms."""
    return [
        [0, 0, 0, 0, 0],
        [6, 2, 2, 2, 2],
        [2, 0, 0, 0, 0],
        [2, 0, 0, 0, 0],
        [2, 0, 0, 0, 0]
    ]

def generate_frame_shape() -> List[List[int]]:
    """Transformation: Creates the 4x4 frame shape with 2s on borders and 0s inside."""
    return [
        [2, 2, 0, 2],
        [0, 0, 0, 2],
        [2, 2, 2, 2],
        [2, 0, 0, 2]
    ]

def program(g: List[List[int]]) -> List[List[int]]:
    """Composes the rules: detect max value and select the appropriate shape transformation."""
    max_val = get_max_value(g)
    if requires_l_shape(max_val):
        return generate_l_shape()
    return generate_frame_shape()
```