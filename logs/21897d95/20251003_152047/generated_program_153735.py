```python
from typing import List
from collections import Counter

def compute_mode(lst: List[int]) -> int:
    """
    Computes the mode of a list of integers.
    Returns 0 for empty list; in case of ties, returns the maximum value.
    """
    if not lst:
        return 0
    count = Counter(lst)
    return max(count, key=lambda k: (count[k], k))

def smooth_row(row: List[int]) -> List[int]:
    """
    Smooths a row by replacing each value with the mode of itself and its immediate neighbors.
    Handles edges by using available neighbors.
    This rule handles local noise reduction in rows, preserving block-like structures.
    """
    if not row:
        return []
    n = len(row)
    smoothed = row[:]
    for i in range(n):
        neighbors = [row[i]]
        if i > 0:
            neighbors.append(row[i - 1])
        if i < n - 1:
            neighbors.append(row[i + 1])
        smoothed[i] = compute_mode(neighbors)
    return smoothed

def smooth_grid_vertical(g: List[List[int]]) -> List[List[int]]:
    """
    Smooths each column vertically by treating columns as rows and applying smooth_row.
    This rule handles vertical noise reduction, complementing horizontal smoothing.
    """
    if not g or not g[0]:
        return g
    n_rows = len(g)
    n_cols = len(g[0])
    smoothed = [row[:] for row in g]
    for j in range(n_cols):
        col = [g[i][j] for i in range(n_rows)]
        smoothed_col = smooth_row(col)
        for i in range(n_rows):
            smoothed[i][j] = smoothed_col[i]
    return smoothed

def transpose(g: List[List[int]]) -> List[List[int]]:
    """
    Transposes the grid, swapping rows and columns.
    This core transformation reorients the input to align vertical structures horizontally.
    """
    if not g or not g[0]:
        return []
    return [list(col) for col in zip(*g)]

def program(g: List[List[int]]) -> List[List[int]]:
    """
    Applies transposition followed by horizontal and vertical smoothing to clean and structure the grid.
    """
    t = transpose(g)
    smoothed_horizontal = [smooth_row(row) for row in t]
    result = smooth_grid_vertical(smoothed_horizontal)
    return result
```