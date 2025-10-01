```python
from typing import List

def is_all_filled(row: List[int]) -> bool:
    """Check if a row is entirely filled (1 or 7)."""
    return all(c == 1 or c == 7 for c in row)

def remove_large_filled_row_blocks(grid: List[List[int]]) -> List[List[int]]:
    """Remove blocks of 3 or more consecutive filled rows."""
    result = []
    i = 0
    n = len(grid)
    while i < n:
        if is_all_filled(grid[i]):
            start = i
            while i < n and is_all_filled(grid[i]):
                i += 1
            if i - start < 3:
                result += grid[start:i]
        else:
            result.append(grid[i])
            i += 1
    return result

def transpose(grid: List[List[int]]) -> List[List[int]]:
    """Transpose the grid."""
    if not grid:
        return []
    return [list(row) for row in zip(*grid)]

def find_first_filled_column(grid: List[List[int]]) -> int:
    """Find the leftmost column that is entirely filled (1 or 7)."""
    h = len(grid)
    if h == 0:
        return 0
    w = len(grid[0])
    for c in range(w):
        if all(grid[r][c] == 1 or grid[r][c] == 7 for r in range(h)):
            return c
    return w

def trim_to_first_filled(grid: List[List[int]]) -> List[List[int]]:
    """Trim the grid to the left of the first filled column."""
    c = find_first_filled_column(grid)
    return [row[:c] for row in grid]

def replace_sevens_to_four(grid: List[List[int]]) -> List[List[int]]:
    """Replace all 7s with 4s."""
    return [[4 if c == 7 else c for c in row] for row in grid]

def remove_isolated_ones(grid: List[List[int]]) -> List[List[int]]:
    """Change single isolated 1s (between 4s, not on edges) to 4s."""
    h = len(grid)
    if h == 0:
        return grid
    w = len(grid[0])
    new_grid = [row[:] for row in grid]
    for r in range(h):
        i = 0
        while i < w:
            if new_grid[r][i] == 1:
                start = i
                i += 1
                while i < w and new_grid[r][i] == 1:
                    i += 1
                length = i - start
                left4 = start > 0 and new_grid[r][start - 1] == 4
                right4 = i < w and new_grid[r][i] == 4
                if length == 1 and left4 and right4:
                    new_grid[r][start] = 4
            else:
                i += 1
    return new_grid

def program(g: List[List[int]]) -> List[List[int]]:
    current = g
    # Iterative removal of large filled row blocks (no column removal for simplicity)
    changed = True
    while changed:
        changed = False
        old_h = len(current)
        current = remove_large_filled_row_blocks(current)
        if len(current) != old_h:
            changed = True
    # Trim columns to before the first filled column
    current = trim_to_first_filled(current)
    # Replace 7s to 4s
    current = replace_sevens_to_four(current)
    # Remove isolated 1s if width > 5
    if current and len(current[0]) > 5:
        current = remove_isolated_ones(current)
    return current
```