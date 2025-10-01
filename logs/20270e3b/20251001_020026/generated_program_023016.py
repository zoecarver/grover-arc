```python
from typing import List

def replace_sevens_to_one(grid: List[List[int]]) -> List[List[int]]:
    """Replace all 7s with 1s to treat them as filled cells for block detection."""
    return [[1 if cell == 7 else cell for cell in row] for row in grid]

def is_all_one(row: List[int]) -> bool:
    """Check if a row consists entirely of 1s for detecting uniform filler blocks."""
    return all(cell == 1 for cell in row)

def remove_large_all_one_row_blocks(grid: List[List[int]], min_block: int = 2) -> List[List[int]]:
    """Remove blocks of min_block or more consecutive all-1 rows, preserving smaller blocks and non-uniform rows."""
    if not grid:
        return []
    n = len(grid)
    result = []
    i = 0
    while i < n:
        if is_all_one(grid[i]):
            start = i
            while i < n and is_all_one(grid[i]):
                i += 1
            block_size = i - start
            if block_size < min_block:
                for j in range(start, i):
                    result.append(grid[j])
        else:
            result.append(grid[i])
            i += 1
    return result

def transpose(grid: List[List[int]]) -> List[List[int]]:
    """Transpose the grid to process columns as rows."""
    if not grid or not grid[0]:
        return []
    h = len(grid)
    w = len(grid[0])
    return [[grid[r][c] for r in range(h)] for c in range(w)]

def remove_large_all_one_column_blocks(grid: List[List[int]], min_block: int = 2) -> List[List[int]]:
    """Remove blocks of min_block or more consecutive all-1 columns by transposing, processing rows, and transposing back."""
    t = transpose(grid)
    t_processed = remove_large_all_one_row_blocks(t, min_block)
    return transpose(t_processed)

def program(g: List[List[int]]) -> List[List[int]]:
    """Compose transformations: replace 7s, iteratively remove large all-1 blocks in rows and columns until stable."""
    grid = replace_sevens_to_one(g)
    previous_len_rows = len(grid) + 1
    previous_len_cols = len(grid[0]) + 1 if grid else 1
    while previous_len_rows != len(grid) or previous_len_cols != (len(grid[0]) if grid else 0):
        previous_len_rows = len(grid)
        previous_len_cols = len(grid[0]) if grid else 0
        grid = remove_large_all_one_row_blocks(grid)
        grid = remove_large_all_one_column_blocks(grid)
    return grid
```