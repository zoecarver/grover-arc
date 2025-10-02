```python
from typing import List

def get_top_color(g: List[List[int]]) -> int:
    """Extract the top color from the first cell of the first row."""
    return g[0][0]

def remove_top_color_cells(g: List[List[int]], color: int) -> List[List[int]]:
    """Remove all cells matching the top color from rows 1 to 11."""
    new_g = [row[:] for row in g]
    for i in range(1, 12):
        for j in range(12):
            if new_g[i][j] == color:
                new_g[i][j] = 0
    return new_g

def apply_gravity_to_column(column: List[int]) -> List[int]:
    """Apply gravity to a single column by collecting non-zero values and placing them at the bottom, preserving order."""
    non_zero = [x for x in column if x != 0]
    num_zeros = 12 - len(non_zero)
    return [0] * num_zeros + non_zero

def apply_gravity(g: List[List[int]]) -> List[List[int]]:
    """Apply gravity to every column of the grid."""
    new_g = [[0] * 12 for _ in range(12)]
    for j in range(12):
        column = [g[i][j] for i in range(12)]
        new_column = apply_gravity_to_column(column)
        for i in range(12):
            new_g[i][j] = new_column[i]
    return new_g

def program(g: List[List[int]]) -> List[List[int]]:
    """Main program: remove top color cells and apply gravity."""
    color = get_top_color(g)
    g_removed = remove_top_color_cells(g, color)
    g_final = apply_gravity(g_removed)
    return g_final
```