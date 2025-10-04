```python
from typing import List
from collections import Counter

def transpose(g: List[List[int]]) -> List[List[int]]:
    """Transpose the grid, swapping rows and columns."""
    if not g or not g[0]:
        return []
    return [list(col) for col in zip(*g)]

def compute_mode(values: List[int]) -> int:
    """
    Computes the mode of a list of integers.
    Returns 0 for empty list; in case of ties, returns the maximum value.
    """
    if not values:
        return 0
    count = Counter(values)
    return max(count, key=lambda k: (count[k], k))

def smooth_grid_2d(g: List[List[int]]) -> List[List[int]]:
    """
    Applies 2D smoothing to the grid by replacing each cell with the mode of its 3x3 neighborhood.
    Handles edges by using available neighbors.
    This rule promotes uniform regions by propagating dominant local values.
    """
    if not g or not g[0]:
        return g
    n = len(g)
    m = len(g[0])
    new_g = [[0] * m for _ in range(n)]
    for i in range(n):
        for j in range(m):
            neighbors = []
            for di in range(-1, 2):
                for dj in range(-1, 2):
                    ni = i + di
                    nj = j + dj
                    if 0 <= ni < n and 0 <= nj < m:
                        neighbors.append(g[ni][nj])
            new_g[i][j] = compute_mode(neighbors)
    return new_g

def program(g: List[List[int]]) -> List[List[int]]:
    """
    Main program: Transposes non-square grids to match output dimensions, then applies iterative 2D smoothing
    to denoise and fill regions into blocky structures.
    For square grids, smooths directly without transposition.
    Number of iterations scales with grid size for sufficient propagation.
    """
    if not g or not g[0]:
        return []
    n_rows = len(g)
    n_cols = len(g[0])
    if n_rows != n_cols:
        result = transpose(g)
    else:
        result = [row[:] for row in g]
    size = max(n_rows, n_cols)
    num_iter = size // 6 + 1
    for _ in range(num_iter):
        result = smooth_grid_2d(result)
    return result
```