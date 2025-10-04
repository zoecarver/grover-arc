```python
from typing import List

def apply_row_removal(grid: List[List[int]], row: int) -> None:
    i = 0
    while i < 10:
        if grid[row][i] != 1:
            i += 1
            continue
        start = i
        while i < 10 and grid[row][i] == 1:
            i += 1
        end = i - 1
        len_ = end - start + 1
        left_b = 'edge' if start == 0 else grid[row][start - 1]
        right_b = 'edge' if end == 9 else grid[row][end + 1]
        remove = False
        if (left_b == 0 or left_b == 'edge') and (right_b == 0 or right_b == 'edge') and len_ <= 3:
            remove = True
        elif left_b != 0 and left_b != 1 and left_b != 'edge' and right_b == 0 and len_ <= 2:
            remove = True
        if remove:
            for j in range(start, end + 1):
                grid[row][j] = 0

def apply_row_filling(grid: List[List[int]], row: int) -> None:
    i = 0
    while i < 10:
        if grid[row][i] != 0:
            i += 1
            continue
        start = i
        while i < 10 and grid[row][i] == 0:
            i += 1
        end = i - 1
        len_ = end - start + 1
        if len_ > 3 or start == 0 or end == 9:
            continue
        left_c = grid[row][start - 1]
        right_c = grid[row][end + 1]
        if left_c == 0 or right_c == 0:
            continue
        if (left_c == right_c and left_c != 1) or left_c == 1 or right_c == 1:
            for j in range(start, end + 1):
                grid[row][j] = 1

def program(g: List[List[int]]) -> List[List[int]]:
    out = [row[:] for row in g]
    for r in range(10):
        apply_row_removal(out, r)
    for r in range(10):
        apply_row_filling(out, r)
    return out
```