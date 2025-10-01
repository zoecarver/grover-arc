```python
from typing import List

def is_all_filled(row: List[int]) -> bool:
    """Check if a row consists entirely of filled cells (1 or 7)."""
    return all(cell == 1 or cell == 7 for cell in row)

def remove_large_all_filled_row_blocks(grid: List[List[int]], min_block: int = 3) -> List[List[int]]:
    """Remove blocks of min_block or more consecutive all-filled rows, preserving smaller blocks and non-filled rows."""
    if not grid:
        return []
    n = len(grid)
    result = []
    i = 0
    while i < n:
        if is_all_filled(grid[i]):
            start = i
            while i < n and is_all_filled(grid[i]):
                i += 1
            block_size = i - start
            if block_size < min_block:
                result.extend(grid[start:i])
        else:
            result.append(grid[i])
            i += 1
    return result

def transpose(grid: List[List[int]]) -> List[List[int]]:
    """Transpose the grid (assumes rectangular input)."""
    if not grid or not grid[0]:
        return []
    h = len(grid)
    w = len(grid[0])
    return [[grid[r][c] for r in range(h)] for c in range(w)]

def process_filled_row_blocks(grid: List[List[int]]) -> List[List[int]]:
    """Remove large all-filled row blocks iteratively, including via transposition for columns (min_block=3)."""
    current = grid
    while True:
        old_h = len(current)
        old_w = len(current[0]) if current else 0
        current = remove_large_all_filled_row_blocks(current, 3)
        t = transpose(current)
        t = remove_large_all_filled_row_blocks(t, 3)
        current = transpose(t)
        new_h = len(current)
        new_w = len(current[0]) if current else 0
        if new_h == old_h and new_w == old_w:
            break
    return current

def replace_sevens_to_four(grid: List[List[int]]) -> List[List[int]]:
    """Replace all 7s with 4s."""
    return [[4 if cell == 7 else cell for cell in row] for row in grid]

def is_all_one(row: List[int]) -> bool:
    """Check if a row consists entirely of 1s."""
    return all(cell == 1 for cell in row)

def find_first_all_one_column(grid: List[List[int]]) -> int:
    """Find the index of the leftmost all-1 column, or len if none."""
    h = len(grid)
    if h == 0:
        return 0
    w = len(grid[0])
    for c in range(w):
        if all(grid[r][c] == 1 for r in range(h)):
            return c
    return w

def trim_right_from_first_all_one(grid: List[List[int]]) -> List[List[int]]:
    """Trim columns from the first all-1 column to the end (after replacing 7s to 4s)."""
    grid = replace_sevens_to_four(grid)
    first = find_first_all_one_column(grid)
    return [row[:first] for row in grid]

def program(g: List[List[int]]) -> List[List[int]]:
    """Compose rules: remove large filled blocks, replace 7s to 4s, trim right from first all-1 column."""
    temp = process_filled_row_blocks(g)
    result = trim_right_from_first_all_one(temp)
    return result
```