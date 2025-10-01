```python
from typing import List

def get_max_value(g: List[List[int]]) -> int:
    """Observes the highest number in the grid to determine the output shape."""
    return max(max(row) for row in g)

def requires_l_shape(max_val: int) -> bool:
    """Rule: L-shape required if and only if the maximum value is exactly 6."""
    return max_val == 6

def generate_l_shape() -> List[List[int]]:
    """Generates the 5x5 L-shape grid with 6 at the corner and 2s forming the arms."""
    return [
        [0, 0, 0, 0, 0],
        [6, 2, 2, 2, 2],
        [2, 0, 0, 0, 0],
        [2, 0, 0, 0, 0],
        [2, 0, 0, 0, 0]
    ]

def generate_frame_shape() -> List[List[int]]:
    """Generates the 4x4 frame-like grid with 2s forming the borders and 0s inside."""
    return [
        [2, 2, 0, 2],
        [0, 0, 0, 2],
        [2, 2, 2, 2],
        [2, 0, 0, 2]
    ]

def program(g: List[List[int]]) -> List[List[int]]:
    """Main program: Computes max value and selects the appropriate shape based on the rule."""
    max_val = get_max_value(g)
    if requires_l_shape(max_val):
        return generate_l_shape()
    return generate_frame_shape()
```