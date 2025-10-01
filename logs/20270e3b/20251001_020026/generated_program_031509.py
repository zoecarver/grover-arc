```python
from typing import List

def replace_sevens_to_one(grid: List[List[int]]) -> List[List[int]]:
    """Replace all 7s with 1s to treat them as filled cells for block detection."""
    return [[1 if cell == 7 else cell for cell in row] for row in grid]

def is_all_one(row: List[int]) -> bool:
    """Check if a row consists entirely of 1s for detecting uniform filler blocks."""
    return all(cell == 1 for cell in row)

def remove_all_one_row_blocks(grid: List[List[int]]) -> List[List[int]]:
    """Remove all consecutive all-1 rows (min_block=1), preserving non-uniform rows."""
    if not grid:
        return []
    n = len(grid)
    result = []
    i = 0
    while i < n:
        if is_all_one(grid[i]):
            # Skip the block (size >=1)
            while i < n and is_all_one(grid[i]):
                i += 1
        else:
            result.append(grid[i])
            i += 1
    return result

def transpose(grid: List[List[int]]) -> List[List[int]]:
    """Transpose the grid to process columns as rows, padding with 4s if ragged."""
    if not grid or not grid[0]:
        return []
    h = len(grid)
    w = max((len(row) for row in grid), default=0)
    t = [[4 for _ in range(h)] for _ in range(w)]
    for r in range(h):
        for c in range(min(w, len(grid[r]))):
            t[c][r] = grid[r][c]
    return t

def remove_all_one_column_blocks(grid: List[List[int]]) -> List[List[int]]:
    """Remove all consecutive all-1 columns (min_block=1) by transposing, processing, and transposing back."""
    t = transpose(grid)
    t_processed = remove_all_one_row_blocks(t)
    return transpose(t_processed)

def program(g: List[List[int]]) -> List[List[int]]:
    """Main program: iteratively remove all-1 blocks in rows and columns until stable."""
    g = replace_sevens_to_one(g)
    prev_h, prev_w = -1, -1
    while True:
        old_h = len(g)
        old_w = len(g[0]) if g else 0
        if old_h == prev_h and old_w == prev_w:
            break
        prev_h, prev_w = old_h, old_w
        g = remove_all_one_row_blocks(g)
        g = remove_all_one_column_blocks(g)
    return g
```