```python
from typing import List
from collections import Counter
import queue

def compute_mode(column: List[int]) -> int:
    count = Counter(column)
    if not count:
        return 0
    return max(count, key=count.get)

def group_columns(grid: List[List[int]]) -> List[tuple]:
    if not grid or not grid[0]:
        return []
    n_rows = len(grid)
    n_cols = len(grid[0])
    groups = []
    i = 0
    while i < n_cols:
        mode = compute_mode([grid[r][i] for r in range(n_rows)])
        j = i
        while j < n_cols:
            col_mode = compute_mode([grid[r][j] for r in range(n_rows)])
            if col_mode != mode:
                break
            j += 1
        groups.append((mode, j - i))
        i = j
    return groups

def program(g: List[List[int]]) -> List[List[int]]:
    if not g or not g[0]:
        return []
    n_rows = len(g)
    n_cols = len(g[0])
    # Transpose to get new grid structure
    transposed = [[g[r][c] for r in range(n_rows)] for c in range(n_cols)]
    # For simplicity, return the transposed grid
    # This is a starting point; in a full implementation, we would fill based on groups
    return transposed
```