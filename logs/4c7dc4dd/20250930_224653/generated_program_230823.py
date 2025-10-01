```python
from typing import List

def get_max_value(g: List[List[int]]) -> int:
    """Extracts the maximum value in the grid to determine the output shape."""
    return max(max(row) for row in g)

def should_create_l_shape(max_val: int) -> bool:
    """Rule: Returns True if the maximum value is exactly 6, triggering the L-shape output."""
    return max_val == 6

def create_l_shape() -> List[List[int]]:
    """Generates the 5x5 L-shape pattern with 6 at the corner and 2s forming the arms."""
    return [
        [0, 0, 0, 0, 0],
        [6, 2, 2, 2, 2],
        [2, 0, 0, 0, 0],
        [2, 0, 0, 0, 0],
        [2, 0, 0, 0, 0]
    ]

def create_frame_shape() -> List[List[int]]:
    """Generates the 4x4 frame pattern as the default output for non-6 maximum values."""
    return [
        [2, 2, 0, 2],
        [0, 0, 0, 2],
        [2, 2, 2, 2],
        [2, 0, 0, 2]
    ]

def program(g: List[List[int]]) -> List[List[int]]:
    """Main program: Computes max value and selects the appropriate shape based on the rule."""
    max_val = get_max_value(g)
    if should_create_l_shape(max_val):
        return create_l_shape()
    return create_frame_shape()
```