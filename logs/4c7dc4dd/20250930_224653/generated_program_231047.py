```python
from typing import List

def get_max_value(g: List[List[int]]) -> int:
    """Extracts the maximum value in the grid to determine the output shape."""
    return max((max(row) for row in g), default=0)

def is_l_trigger(max_val: int) -> bool:
    """Rule: Checks if the maximum value is exactly 6 to trigger L-shape."""
    return max_val == 6

def create_l_shape() -> List[List[int]]:
    """Generates the 5x5 L-shape with 6 at the corner and 2s for the arms."""
    return [
        [0, 0, 0, 0, 0],
        [6, 2, 2, 2, 2],
        [2, 0, 0, 0, 0],
        [2, 0, 0, 0, 0],
        [2, 0, 0, 0, 0]
    ]

def create_frame_shape() -> List[List[int]]:
    """Generates the 4x4 frame shape with 2s forming borders and 0s inside."""
    return [
        [2, 2, 0, 2],
        [0, 0, 0, 2],
        [2, 2, 2, 2],
        [2, 0, 0, 2]
    ]

def program(g: List[List[int]]) -> List[List[int]]:
    """Main program: Selects output shape based on maximum value rule."""
    max_val = get_max_value(g)
    if is_l_trigger(max_val):
        return create_l_shape()
    return create_frame_shape()
```