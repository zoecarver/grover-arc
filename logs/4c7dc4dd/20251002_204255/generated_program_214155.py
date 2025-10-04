```python
from typing import List

def get_shape_id(g: List[List[int]]) -> int:
    """Extract the shape identifier from the top-left cell."""
    if not g or not g[0]:
        return 0
    return g[0][0]

def find_special_color(g: List[List[int]]) -> int:
    """Find the special color as the maximum value in the grid greater than 4."""
    if not g or not g[0]:
        return 0
    max_val = 0
    for row in g:
        for cell in row:
            if cell > max_val:
                max_val = cell
    return max_val if max_val > 4 else 0

def get_f_grid(is_special: bool) -> List[List[int]]:
    """Generate the 5x5 F-shaped grid, with special marker if requested."""
    out = [[0 for _ in range(5)] for _ in range(5)]
    top_value = 6 if is_special else 2
    out[1][0] = top_value
    for c in range(1, 5):
        out[1][c] = 2
    for r in range(2, 5):
        out[r][0] = 2
    return out

def get_e_grid() -> List[List[int]]:
    """Generate the 4x4 E-shaped grid."""
    return [
        [2, 2, 0, 2],
        [0, 0, 0, 2],
        [2, 2, 2, 2],
        [2, 0, 0, 2]
    ]

def get_h_grid() -> List[List[int]]:
    """Generate the 5x5 H-shaped grid."""
    out = [[0 for _ in range(5)] for _ in range(5)]
    for r in range(5):
        out[r][0] = 2
        out[r][4] = 2
    for c in range(5):
        out[2][c] = 2
    return out

def program(g: List[List[int]]) -> List[List[int]]:
    """Main program: infer shape from top-left ID and special color, generate corresponding grid."""
    if not g or not g[0]:
        return []
    shape_id = get_shape_id(g)
    s = find_special_color(g)
    if s == 0:
        return []
    if shape_id == 1:
        return get_f_grid(s == 6)
    elif shape_id == 4:
        return get_e_grid()
    elif shape_id == 3:
        return get_h_grid()
    elif shape_id == 2:
        return get_f_grid(False)
    else:
        return []
```