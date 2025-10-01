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
    """Transpose the grid to process columns as rows."""
    if not grid or not grid[0]:
        return []
    h = len(grid)
    w = len(grid[0])
    return [[grid[r][c] for r in range(h)] for c in range(w)]

def process_filled_blocks(grid: List[List[int]]) -> List[List[int]]:
    """Iteratively remove large all-filled blocks in rows and columns until stable."""
    current = grid
    while True:
        old_h = len(current)
        old_w = len(current[0]) if current else 0
        current = remove_large_all_filled_row_blocks(current)
        t = transpose(current)
        t = remove_large_all_filled_row_blocks(t)
        current = transpose(t)
        new_h = len(current)
        new_w = len(current[0]) if current else 0
        if new_h == old_h and new_w == old_w:
            break
    return current

def clean_right_of_sevens(grid: List[List[int]]) -> List[List[int]]:
    """Set 7s to 4 and the following consecutive 1s to 4 in each row."""
    new_grid = [row[:] for row in grid]
    for r in range(len(new_grid)):
        i = 0
        while i < len(new_grid[r]):
            if new_grid[r][i] == 7:
                new_grid[r][i] = 4
                i += 1
                # Set up to 2 following 1s to 4
                count = 0
                while i < len(new_grid[r]) and new_grid[r][i] == 1 and count < 2:
                    new_grid[r][i] = 4
                    i += 1
                    count += 1
                continue
            i += 1
    return new_grid

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

def trim_to_first_all_one(grid: List[List[int]]) -> List[List[int]]:
    """Trim the grid to the left of the first all-1 column."""
    first = find_first_all_one_column(grid)
    return [row[:first] for row in grid]

def program(g: List[List[int]]) -> List[List[int]]:
    """Main program composing the rules for puzzle solving."""
    g = process_filled_blocks(g)
    g = clean_right_of_sevens(g)
    temp = [[1 if cell == 7 else cell for cell in row] for row in g]  # For detection
    g = [[4 if cell == 7 else cell for cell in row] for row in g]  # Replace remaining 7s
    g = trim_to_first_all_one(temp)  # Use temp for trim detection, but apply to g
    g = [row[:len(temp[0])] for row in g] if temp else []  # Align length
    return g
```