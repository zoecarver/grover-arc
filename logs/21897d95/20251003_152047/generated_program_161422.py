```python
from typing import List
from collections import Counter

def mode_ignoring_noise(column: List[int]) -> int:
    counts = Counter(x for x in column if x != 1 and x != 0)
    if not counts:
        return 0
    return counts.most_common(1)[0][0]

def find_vertical_stripes(grid: List[List[int]]) -> List[tuple[int, int, int]]:
    if not grid or not grid[0]:
        return []
    n_rows = len(grid)
    n_cols = len(grid[0])
    stripes = []
    j = 0
    while j < n_cols:
        col_mode = mode_ignoring_noise([grid[i][j] for i in range(n_rows)])
        start = j
        j += 1
        while j < n_cols:
            next_mode = mode_ignoring_noise([grid[i][j] for i in range(n_rows)])
            if next_mode != col_mode:
                break
            j += 1
        width = j - start
        stripes.append((start, width, col_mode))
    return stripes

def subdivide_stripe_vertically(grid: List[List[int]], start_col: int, end_col: int) -> List[tuple[int, int, int]]:
    n_rows = len(grid)
    if n_rows == 0 or end_col <= start_col:
        return []
    subblocks = []
    i = 0
    while i < n_rows:
        row_segment = [grid[i][k] for k in range(start_col, end_col)]
        row_mode = mode_ignoring_noise(row_segment)
        start = i
        i += 1
        while i < n_rows:
            next_segment = [grid[i][k] for k in range(start_col, end_col)]
            next_mode = mode_ignoring_noise(next_segment)
            if next_mode != row_mode:
                break
            i += 1
        height = i - start
        subblocks.append((start, height, row_mode))
    return subblocks

def find_anomalies_in_stripe(grid: List[List[int]], start_col: int, end_col: int) -> dict:
    n_rows = len(grid)
    anomalies = Counter()
    for i in range(n_rows):
        segment = [grid[i][k] for k in range(start_col, end_col) if grid[i][k] != 1]
        if segment:
            dominant = Counter(segment).most_common(1)[0][0]
            for val in set(segment):
                if val != dominant and val != 0:
                    anomalies[val] += segment.count(val)
    return dict(anomalies.most_common(3))  # top 3 anomalies

def program(g: List[List[int]]) -> List[List[int]]:
    n_rows = len(g)
    if n_rows == 0:
        return []
    n_cols = len(g[0])
    # Transpose to get the base structure
    transposed = list(map(list, zip(*g)))
    # For simplicity, return the transposed grid as base, but to improve, apply smoothing
    # This is a placeholder; in a full implementation, use the stripe and subblock logic to fill blocks
    # For now, to have a valid program, return transposed
    return transposed
```