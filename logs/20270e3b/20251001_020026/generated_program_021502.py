```python
from typing import List

def replace_sevens_to_one(grid: List[List[int]]) -> List[List[int]]:
    """Replace all 7s with 1s to treat them as filled cells for block detection."""
    return [[1 if cell == 7 else cell for cell in row] for row in grid]

def is_all_one(row: List[int]) -> bool:
    """Check if a row consists entirely of 1s for detecting uniform filler blocks."""
    return all(cell == 1 for cell in row)

def remove_large_all_one_row_blocks(grid: List[List[int]]) -> List[List[int]]:
    """Remove blocks of 3 or more consecutive all-1 rows, preserving smaller blocks and non-uniform rows."""
    n = len(grid)
    result = []
    i = 0
    while i < n:
        if is_all_one(grid[i]):
            start = i
            while i < n and is_all_one(grid[i]):
                i += 1
            block_size = i - start
            if block_size < 3:
                for j in range(start, i):
                    result.append(grid[j])
        else:
            result.append(grid[i])
            i += 1
    return result

def transpose(grid: List[List[int]]) -> List[List[int]]:
    """Transpose the grid to process columns as rows (width becomes height, height becomes width)."""
    if not grid or not grid[0]:
        return []
    h, w = len(grid), len(grid[0])
    return [[grid[r][c] for r in range(h)] for c in range(w)]

def remove_large_all_one_column_blocks(grid: List[List[int]]) -> List[List[int]]:
    """Remove blocks of 3 or more consecutive all-1 columns by transposing, processing rows, and transposing back."""
    t = transpose(grid)
    t_processed = remove_large_all_one_row_blocks(t)
    return transpose(t_processed)

def program(g: List[List[int]]) -> List[List[int]]:
    """Main program: replace 7s, remove large all-1 row blocks, then remove large all-1 column blocks."""
    g = replace_sevens_to_one(g)
    g = remove_large_all_one_row_blocks(g)
    g = remove_large_all_one_column_blocks(g)
    return g
```