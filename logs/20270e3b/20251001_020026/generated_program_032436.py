```python
from typing import List

def replace_sevens_to_four(grid: List[List[int]]) -> List[List[int]]:
    return [[4 if cell == 7 else cell for cell in row] for row in grid]

def is_all_one(row: List[int]) -> bool:
    return all(cell == 1 for cell in row)

def is_all_four(row: List[int]) -> bool:
    return all(cell == 4 for cell in row)

def remove_all_one_row_blocks(grid: List[List[int]], min_block: int) -> List[List[int]]:
    result = []
    i = 0
    n = len(grid)
    while i < n:
        if is_all_one(grid[i]):
            start = i
            while i < n and is_all_one(grid[i]):
                i += 1
            if i - start < min_block:
                result += grid[start:i]
        else:
            result.append(grid[i])
            i += 1
    return result

def remove_all_four_row_blocks(grid: List[List[int]], min_block: int) -> List[List[int]]:
    result = []
    i = 0
    n = len(grid)
    while i < n:
        if is_all_four(grid[i]):
            start = i
            while i < n and is_all_four(grid[i]):
                i += 1
            if i - start < min_block:
                result += grid[start:i]
        else:
            result.append(grid[i])
            i += 1
    return result

def transpose(grid: List[List[int]]) -> List[List[int]]:
    h = len(grid)
    w = len(grid[0]) if h > 0 else 0
    return [[grid[r][c] for r in range(h)] for c in range(w)]

def remove_all_one_column_blocks(grid: List[List[int]], min_block: int) -> List[List[int]]:
    t = transpose(grid)
    t_processed = remove_all_one_row_blocks(t, min_block)
    return transpose(t_processed)

def remove_all_four_column_blocks(grid: List[List[int]], min_block: int) -> List[List[int]]:
    t = transpose(grid)
    t_processed = remove_all_four_row_blocks(t, min_block)
    return transpose(t_processed)

def program(g: List[List[int]]) -> List[List[int]]:
    g = replace_sevens_to_four(g)
    changed = True
    while changed:
        old_h = len(g)
        old_w = len(g[0]) if old_h > 0 else 0
        g = remove_all_one_row_blocks(g, 2)
        g = remove_all_four_row_blocks(g, 3)
        t = transpose(g)
        t = remove_all_one_row_blocks(t, 2)
        t = remove_all_four_row_blocks(t, 3)
        g = transpose(t)
        new_h = len(g)
        new_w = len(g[0]) if new_h > 0 else 0
        changed = (new_h * new_w != old_h * old_w)
    return g
```