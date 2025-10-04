```python
from typing import List

def remove_isolated_upper(grid: List[List[int]]) -> List[List[int]]:
    new_grid = [row[:] for row in grid]
    for i in range(4):
        for j in range(11):
            if new_grid[i][j] == 9:
                has_neighbor = False
                if j > 0 and new_grid[i][j - 1] == 9:
                    has_neighbor = True
                if j < 10 and new_grid[i][j + 1] == 9:
                    has_neighbor = True
                if not has_neighbor:
                    new_grid[i][j] = 7
    return new_grid

def central_fill(grid: List[List[int]]) -> List[List[int]]:
    new_grid = [row[:] for row in grid]
    trigger_positions = []
    full_trigger = False
    for r in range(4, 7):
        if grid[r][3] == 6:
            for c in range(3):
                if grid[r][c] == 9:
                    full_trigger = True
                    trigger_positions.append((r, c))
        if grid[r][7] == 6:
            for c in range(8, 11):
                if grid[r][c] == 9:
                    full_trigger = True
                    trigger_positions.append((r, c))
    grounded = all(grid[r][3] == 6 and grid[r][7] == 6 for r in range(4, 7))
    if full_trigger:
        for r in range(4, 7):
            for c in range(4, 7):
                new_grid[r][c] = 9
        for r, c in trigger_positions:
            new_grid[r][c] = 7
    elif grounded:
        count_left = 0
        for c in range(1, 8):
            if grid[3][c] == 6 and grid[2][c] == 9:
                count_left += 1
        filled = 0
        for c in range(4, 7):
            if filled < count_left and new_grid[4][c] == 3:
                new_grid[4][c] = 9
                filled += 1
            else:
                break
    else:
        for c in range(4, 7):
            if new_grid[4][c] == 3:
                new_grid[4][c] = 9
        for c in range(4, 7):
            if new_grid[5][c] != 3:
                break
            new_grid[5][c] = 9
    return new_grid

def adjust_eyes(grid: List[List[int]]) -> List[List[int]]:
    new_grid = [row[:] for row in grid]
    i = 0
    while i < 11:
        if new_grid[0][i] == 9:
            start = i
            while i < 11 and new_grid[0][i] == 9:
                i += 1
            length = i - start
            if length >= 3:
                middle = start + (length // 2)
                for c in range(start, i):
                    if new_grid[1][c] == 9 and c != middle:
                        new_grid[1][c] = 7
        else:
            i += 1
    return new_grid

def change_lower_nines(grid: List[List[int]]) -> List[List[int]]:
    new_grid = [row[:] for row in grid]
    for i in range(8, 11):
        for j in range(11):
            if new_grid[i][j] == 9:
                new_grid[i][j] = 7
    return new_grid

def program(g: List[List[int]]) -> List[List[int]]:
    grid = remove_isolated_upper(g)
    grid = central_fill(grid)
    grid = adjust_eyes(grid)
    grid = change_lower_nines(grid)
    return grid
```