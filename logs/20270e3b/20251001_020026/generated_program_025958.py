```python
from typing import List

def replace_sevens_to_four(grid: List[List[int]]) -> List[List[int]]:
    """Replace all 7s with 4s to remove dark red elements while preserving yellow pixel positions."""
    return [[4 if cell == 7 else cell for cell in row] for row in grid]

def is_all_one(row: List[int]) -> bool:
    """Check if a row consists entirely of 1s for detecting uniform filler blocks (blue masses to remove)."""
    return all(cell == 1 for cell in row)

def is_all_four(row: List[int]) -> bool:
    """Check if a row consists entirely of 4s for detecting uniform background blocks to condense or remove."""
    return all(cell == 4 for cell in row)

def remove_filled_row_blocks(grid: List[List[int]], min_block: int = 1) -> List[List[int]]:
    """Remove blocks of min_block or more consecutive all-1 rows (filled blue), preserving smaller and non-uniform."""
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
            if block_size >= min_block:
                # Remove the block entirely
                continue
            else:
                for j in range(start, i):
                    result.append(grid[j])
        else:
            result.append(grid[i])
            i += 1
    return result

def remove_empty_row_blocks(grid: List[List[int]], min_block: int = 1) -> List[List[int]]:
    """Remove blocks of min_block or more consecutive all-4 rows (empty yellow), preserving smaller and non-uniform."""
    if not grid:
        return []
    n = len(grid)
    result = []
    i = 0
    while i < n:
        if is_all_four(grid[i]):
            start = i
            while i < n and is_all_four(grid[i]):
                i += 1
            block_size = i - start
            if block_size >= min_block:
                # Remove the block entirely
                continue
            else:
                for j in range(start, i):
                    result.append(grid[j])
        else:
            result.append(grid[i])
            i += 1
    return result

def transpose(grid: List[List[int]]) -> List[List[int]]:
    """Transpose the grid to process columns as rows, padding with 4s if ragged (for robustness)."""
    if not grid or not grid[0]:
        return []
    h = len(grid)
    w = len(grid[0])
    t = [[4 for _ in range(h)] for _ in range(w)]
    for r in range(h):
        for c in range(min(w, len(grid[r]))):
            t[c][r] = grid[r][c]
    return t

def remove_filled_column_blocks(grid: List[List[int]], min_block: int = 1) -> List[List[int]]:
    """Remove blocks of min_block or more consecutive all-1 columns by transposing, processing, transposing back."""
    t = transpose(grid)
    t_processed = remove_filled_row_blocks(t, min_block)
    return transpose(t_processed)

def remove_empty_column_blocks(grid: List[List[int]], min_block: int = 1) -> List[List[int]]:
    """Remove blocks of min_block or more consecutive all-4 columns by transposing, processing, transposing back."""
    t = transpose(grid)
    t_processed = remove_empty_row_blocks(t, min_block)
    return transpose(t_processed)

def program(g: List[List[int]]) -> List[List[int]]:
    """Main program: replace 7s with 4s, then iteratively remove uniform filled (1) and empty (4) blocks until stable, merging yellow components and adjusting blue enclosures while approximately conserving yellow pixels through selective removal."""
    grid = replace_sevens_to_four(g)
    previous_size = 0
    while True:
        current_size = len(grid) * len(grid[0]) if grid else 0
        if current_size == previous_size:
            break
        previous_size = current_size
        # Remove empty row blocks first (background simplification)
        grid = remove_empty_row_blocks(grid, min_block=1)
        # Remove filled row blocks (filler removal)
        grid = remove_filled_row_blocks(grid, min_block=1)
        # Remove empty column blocks
        grid = remove_empty_column_blocks(grid, min_block=1)
        # Remove filled column blocks
        grid = remove_filled_column_blocks(grid, min_block=1)
    return grid
```