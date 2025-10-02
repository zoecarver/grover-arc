```python
from typing import List

def get_top_color(grid: List[List[int]]) -> int:
    """Extract the top color from grid[0][0]."""
    return grid[0][0]

def remove_top_color_instances(grid: List[List[int]], color: int) -> List[List[int]]:
    """Remove all instances of the top color from rows 1 to 11, keeping row 0 intact."""
    new_grid = [row[:] for row in grid]
    for r in range(1, len(new_grid)):
        for c in range(len(new_grid[r])):
            if new_grid[r][c] == color:
                new_grid[r][c] = 0
    return new_grid

def apply_column_gravity(grid: List[List[int]]) -> List[List[int]]:
    """Apply gravity to each column independently for rows 1 to 11, preserving order."""
    new_grid = [row[:] for row in grid]
    n = len(new_grid)
    for c in range(n):
        pieces = []
        for r in range(1, n):
            if new_grid[r][c] != 0:
                pieces.append(new_grid[r][c])
        # Place pieces at the bottom, original order preserved (first piece at top of stack)
        write_pos = n - 1
        for piece in reversed(pieces):
            new_grid[write_pos][c] = piece
            write_pos -= 1
        # Clear the upper positions
        for r in range(1, write_pos + 1):
            new_grid[r][c] = 0
    return new_grid

def program(g: List[List[int]]) -> List[List[int]]:
    """Main program: remove top color instances and apply column gravity."""
    color = get_top_color(g)
    g_after_removal = remove_top_color_instances(g, color)
    return apply_column_gravity(g_after_removal)
```