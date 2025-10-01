```python
from typing import List

def is_filled(cell: int) -> bool:
    """Rule: A cell is filled if it is 1 or 7."""
    return cell == 1 or cell == 7

def is_all_filled(row: List[int]) -> bool:
    """Rule: A row is all-filled if every cell is filled."""
    return all(is_filled(cell) for cell in row)

def remove_large_all_filled_row_blocks(grid: List[List[int]], min_block: int = 3) -> List[List[int]]:
    """Rule: Remove blocks of 3 or more consecutive all-filled rows, preserving smaller blocks."""
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
    """Tool: Transpose the grid to process columns as rows."""
    if not grid or not grid[0]:
        return []
    return [list(row) for row in zip(*grid)]

def iterative_remove_filled_blocks(grid: List[List[int]], min_block: int = 3) -> List[List[int]]:
    """Rule: Iteratively remove large all-filled blocks in rows and columns until stable."""
    current = [row[:] for row in grid]
    while True:
        old_h = len(current)
        old_w = len(current[0]) if current else 0
        current = remove_large_all_filled_row_blocks(current, min_block)
        t = transpose(current)
        t = remove_large_all_filled_row_blocks(t, min_block)
        current = transpose(t)
        new_h = len(current)
        new_w = len(current[0]) if current else 0
        if new_h == old_h and new_w == old_w:
            break
    return current

def initial_clean_with_temp(grid: List[List[int]], temp: int = 8) -> List[List[int]]:
    """Rule: Clean horizontal 7 blocks to 4, following up to 2 1s to 4, mark ends with temp for propagation."""
    new_grid = [row[:] for row in grid]
    for r in range(len(new_grid)):
        i = 0
        n = len(new_grid[r])
        while i < n:
            if new_grid[r][i] == 7:
                start = i
                new_grid[r][start] = temp
                i += 1
                while i < n and new_grid[r][i] == 7:
                    new_grid[r][i] = 4
                    i += 1
                count = 0
                while i < n and new_grid[r][i] == 1 and count < 2:
                    new_grid[r][i] = 4
                    i += 1
                    count += 1
                if count > 0:
                    new_grid[r][i - 1] = temp
            else:
                i += 1
    return new_grid

def simple_clean_trigger(grid: List[List[int]], triggers: List[int], max_follow: int) -> List[List[int]]:
    """Rule: Clean triggers to 4, following up to max_follow 1s to 4 (no temp marking)."""
    new_grid = [row[:] for row in grid]
    for r in range(len(new_grid)):
        i = 0
        n = len(new_grid[r])
        while i < n:
            if new_grid[r][i] in triggers:
                new_grid[r][i] = 4
                i += 1
                count = 0
                while i < n and new_grid[r][i] == 1 and count < max_follow:
                    new_grid[r][i] = 4
                    i += 1
                    count += 1
                continue
            i += 1
    return new_grid

def vertical_propagation_down(grid: List[List[int]]) -> List[List[int]]:
    """Rule: Propagate down from temp markers up to 2 steps."""
    t = transpose(grid)
    t = simple_clean_trigger(t, [7, 8], 2)
    return transpose(t)

def vertical_propagation_up(grid: List[List[int]]) -> List[List[int]]:
    """Rule: Propagate up from temp markers up to 1 step."""
    t = transpose(grid)
    t = [row[::-1] for row in t]
    t = simple_clean_trigger(t, [7, 8], 1)
    t = [row[::-1] for row in t]
    return transpose(t)

def trim_left_of_first_all1(grid: List[List[int]]) -> List[List[int]]:
    """Rule: Trim columns from the first all-1 column to the end."""
    if not grid:
        return []
    h = len(grid)
    w = len(grid[0])
    first = w
    for c in range(w):
        if all(grid[r][c] == 1 for r in range(h)):
            first = c
            break
    return [row[:first] for row in grid]

def program(g: List[List[int]]) -> List[List[int]]:
    """Main: Compose rules to process the grid."""
    grid = iterative_remove_filled_blocks(g)
    grid = initial_clean_with_temp(grid)
    grid = vertical_propagation_down(grid)
    grid = vertical_propagation_up(grid)
    grid = trim_left_of_first_all1(grid)
    return grid
```