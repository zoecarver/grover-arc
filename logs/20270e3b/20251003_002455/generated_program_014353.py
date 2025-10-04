```python
from typing import List

def has_four(row: List[int]) -> bool:
    return 4 in row

def replace_sevens_in_block(grid: List[List[int]], start_r: int, end_r: int) -> None:
    cols = len(grid[0]) if grid else 0
    for i in range(start_r, end_r + 1):
        for j in range(cols):
            if grid[i][j] == 7:
                grid[i][j] = 4

def get_blocks(grid: List[List[int]]) -> List[tuple[int, int]]:
    blocks = []
    n = len(grid)
    i = 0
    while i < n:
        if has_four(grid[i]):
            start = i
            while i < n and has_four(grid[i]):
                i += 1
            blocks.append((start, i - 1))
        else:
            i += 1
    return blocks

def fill_single_gaps(rows: List[List[int]]) -> List[List[int]]:
    new_rows = []
    for row in rows:
        new_row = row[:]
        w = len(new_row)
        i = 1
        while i < w - 1:
            if new_row[i] == 1 and new_row[i - 1] == 4 and new_row[i + 1] == 4:
                new_row[i] = 4
            i += 1
        new_rows.append(new_row)
    return new_rows

def program(g: List[List[int]]) -> List[List[int]]:
    if not g:
        return []
    grid = [row[:] for row in g]
    blocks = get_blocks(grid)
    kept_rows = []
    for start, end in blocks:
        replace_sevens_in_block(grid, start, end)
        for r in range(start, end + 1):
            kept_rows.append(grid[r])
    if not kept_rows:
        return []
    h = len(kept_rows)
    w = len(kept_rows[0])
    # Find first all-1s column
    crop_w = w
    for c in range(w):
        is_all1 = True
        for r in range(h):
            if kept_rows[r][c] != 1:
                is_all1 = False
                break
        if is_all1:
            crop_w = c
            break
    # Crop
    cropped = [row[:crop_w] for row in kept_rows]
    # Fill single gaps
    result = fill_single_gaps(cropped)
    return result
```