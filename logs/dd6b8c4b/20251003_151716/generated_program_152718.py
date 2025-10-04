```python
from typing import List

def has_adjacent_9(grid: List[List[int]], r: int, c: int) -> bool:
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for dr, dc in directions:
        nr, nc = r + dr, c + dc
        if 0 <= nr < 11 and 0 <= nc < 11 and grid[nr][nc] == 9:
            return True
    return False

def remove_isolated_upper(grid: List[List[int]]) -> List[List[int]]:
    new_grid = [row[:] for row in grid]
    for r in range(4):
        for c in range(11):
            if new_grid[r][c] == 9 and not has_adjacent_9(new_grid, r, c):
                new_grid[r][c] = 7
    return new_grid

def adjust_eyes(grid: List[List[int]]) -> List[List[int]]:
    new_grid = [row[:] for row in grid]
    r0 = new_grid[0]
    i = 0
    while i < 11:
        if r0[i] == 9:
            start = i
            while i < 11 and r0[i] == 9:
                i += 1
            end = i - 1
            length = end - start + 1
            if length >= 3:
                middle = start + (length // 2)
                for cc in range(start, end + 1):
                    if cc != middle:
                        new_grid[1][cc] = 7
        else:
            i += 1
    return new_grid

def central_fill(grid: List[List[int]]) -> List[List[int]]:
    new_grid = [row[:] for row in grid]
    grounded = all(new_grid[r][3] == 6 and new_grid[r][7] == 6 for r in range(4, 7))
    if grounded:
        bottom_open = all(new_grid[7][c] == 7 for c in range(4, 7))
        if bottom_open:
            for r in range(4, 7):
                for c in range(4, 7):
                    new_grid[r][c] = 9
            for r in range(4, 7):
                for c in range(0, 3):
                    if new_grid[r][c] == 9:
                        new_grid[r][c] = 7
                for c in range(8, 11):
                    if new_grid[r][c] == 9:
                        new_grid[r][c] = 7
        else:
            count = 0
            for c in range(1, 8):
                if grid[2][c] == 9 and grid[3][c] == 6:
                    count += 1
            for i in range(min(count, 3)):
                cc = 4 + i
                if new_grid[4][cc] == 3:
                    new_grid[4][cc] = 9
    else:
        for c in range(4, 7):
            if new_grid[4][c] == 3:
                new_grid[4][c] = 9
        for c in range(4, 7):
            if new_grid[5][c] != 3:
                break
            new_grid[5][c] = 9
    return new_grid

def clear_lower(grid: List[List[int]]) -> List[List[int]]:
    new_grid = [row[:] for row in grid]
    for r in range(8, 11):
        for c in range(11):
            if new_grid[r][c] == 9:
                new_grid[r][c] = 7
    return new_grid

def program(g: List[List[int]]) -> List[List[int]]:
    grid = remove_isolated_upper(g)
    grid = adjust_eyes(grid)
    grid = central_fill(grid)
    grid = clear_lower(grid)
    return grid
```