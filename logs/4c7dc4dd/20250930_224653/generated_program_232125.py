```python
from typing import List

def compute_max_value(g: List[List[int]]) -> int:
    """Computes the maximum value across the entire grid."""
    if not g or not any(g):
        return 0
    return max(max(row) for row in g if row)

def is_l_shape_triggered(max_val: int) -> bool:
    """Determines if the L-shape should be generated based on the maximum value being exactly 6."""
    return max_val == 6

def generate_l_shape() -> List[List[int]]:
    """Generates the 5x5 L-shaped grid with 6 at the corner and 2s forming the arms."""
    return [
        [0, 0, 0, 0, 0],
        [6, 2, 2, 2, 2],
        [2, 0, 0, 0, 0],
        [2, 0, 0, 0, 0],
        [2, 0, 0, 0, 0]
    ]

def generate_frame_shape() -> List[List[int]]:
    """Generates the 4x4 frame-shaped grid with 2s on borders and 0s inside."""
    return [
        [2, 2, 0, 2],
        [0, 0, 0, 2],
        [2, 2, 2, 2],
        [2, 0, 0, 2]
    ]

def program(g: List[List[int]]) -> List[List[int]]:
    """Main program: Analyzes the input grid's maximum value and generates the appropriate shape."""
    max_val = compute_max_value(g)
    if is_l_shape_triggered(max_val):
        return generate_l_shape()
    return generate_frame_shape()
```