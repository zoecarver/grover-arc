```python
from typing import List

def has_blue_h(grid: List[List[int]]) -> bool:
    return (grid[1][7:10] == [1, 1, 1] and
            grid[2][7:10] == [8, 1, 8] and
            grid[3][7:10] == [1, 1, 1])

def has_pink_u(grid: List[List[int]]) -> bool:
    return (grid[1][12:15] == [6, 6, 6] and
            grid[2][12:15] == [6, 8, 6] and
            grid[3][12:15] == [6, 8, 6])

def has_red_u(grid: List[List[int]]) -> bool:
    return (grid[1][12:15] == [2, 2, 8] and
            grid[2][12:15] == [2, 2, 2] and
            grid[3][12:15] == [8, 2, 8])

def has_lightblue_c(grid: List[List[int]]) -> bool:
    return (grid[1][12:15] == [9, 8, 9] and
            grid[2][12:15] == [9, 9, 8] and
            grid[3][12:15] == [9, 9, 9])

def has_full_left_0(grid: List[List[int]]) -> bool:
    positions = [(1,2), (1,3), (1,4), (2,2), (2,3), (2,4), (3,2), (3,3), (3,4)]
    return all(grid[r][c] == 0 for r, c in positions)

def has_any_left_0(grid: List[List[int]]) -> bool:
    positions = [(1,2), (1,3), (1,4), (2,2), (2,3), (2,4), (3,2), (3,3), (3,4)]
    return any(grid[r][c] == 0 for r, c in positions)

def has_blue_in_middle_left(grid: List[List[int]]) -> bool:
    for r in range(1, 4):
        if 1 in grid[r][7:10]:
            return True
    return False

def has_red_bowtie_top(grid: List[List[int]]) -> bool:
    r1 = grid[1][2] == 2 and grid[1][3] == 8 and grid[1][4] == 2
    r2 = grid[2][2] == 8 and grid[2][3] == 2 and grid[2][4] == 8
    r3 = grid[3][2] == 2 and grid[3][3] == 8 and grid[3][4] == 2
    return r1 and r2 and r3

def has_red_top_right(grid: List[List[int]]) -> bool:
    for r in range(1, 4):
        if 2 in grid[r][17:20]:
            return True
    return False

def has_red_top_middle_left(grid: List[List[int]]) -> bool:
    for r in range(1, 4):
        if 2 in grid[r][7:10]:
            return True
    return False

def has_red_top_middle_right(grid: List[List[int]]) -> bool:
    for r in range(1, 4):
        if 2 in grid[r][12:15]:
            return True
    return False

def program(g: List[List[int]]) -> List[List[int]]:
    grid = [row[:] for row in g]
    top_filled = has_blue_h(grid)
    if top_filled:
        for r in range(5):
            for c in range(22):
                if grid[r][c] == 8:
                    grid[r][c] = 3
    bottom_color = 3 if top_filled else 2
    for r in range(28, 30):
        for c in range(22):
            grid[r][c] = bottom_color
    # Upper middle fills
    if has_pink_u(grid):
        for r in range(7, 12):
            for c in range(6, 11):
                if grid[r][c] == 8:
                    grid[r][c] = 3
    if has_red_u(grid):
        for r in range(8, 12):
            for c in range(1, 6):
                if grid[r][c] == 8:
                    grid[r][c] = 3
    if has_lightblue_c(grid):
        pos = [(8,16),(8,18),(8,20),(9,16),(9,19),(9,20),(10,16),(10,20)]
        for r, c in pos:
            if grid[r][c] == 8:
                grid[r][c] = 3
    # Lower middle fills
    blue_trigger = has_blue_in_middle_left(grid)
    any0 = has_any_left_0(grid)
    full0 = has_full_left_0(grid)
    full_lower_fill = full0 and top_filled
    if full_lower_fill:
        for r in range(12, 17):
            for c in range(1, 21):
                if grid[r][c] == 8:
                    grid[r][c] = 3
    else:
        if blue_trigger:
            for r in range(12, 17):
                for c in range(6, 11):
                    if grid[r][c] == 8:
                        grid[r][c] = 3
        if any0:
            if not full0:
                for c in [1, 5]:
                    if grid[14][c] == 8:
                        grid[14][c] = 3
        if full0:
            side_pos = [(13,1),(13,3),(13,4),(13,5),(15,1),(15,3),(15,4),(15,5),(14,1),(14,5)]
            for r, c in side_pos:
                if grid[r][c] == 8:
                    grid[r][c] = 3
            if not top_filled:
                for r in [12, 16]:
                    for c in range(11, 21):
                        if grid[r][c] == 8:
                            grid[r][c] = 3
                for r in range(13, 16):
                    for c in [11, 12, 15, 16, 20]:
                        if grid[r][c] == 8:
                            grid[r][c] = 3
    # Third block fills
    fill_left = has_red_bowtie_top(grid)
    fill_red = (has_red_top_right(grid) or has_red_top_middle_left(grid) or has_red_top_middle_right(grid))
    fill_right = has_lightblue_c(grid)
    # row21
    for c in list(range(1,6)) * fill_left + list(range(6,11)) * fill_red + list(range(16,21)) * fill_right:
        if grid[21][c] == 8:
            grid[21][c] = 3
    # row17 red fill
    do_row17_red = (top_filled and has_red_top_right(grid)) or (not top_filled and has_red_top_middle_left(grid))
    if do_row17_red:
        for c in range(6, 11):
            if grid[17][c] == 8:
                grid[17][c] = 3
    # partial rows18-20 red
    if fill_red:
        red_pos = [(18,6),(18,9),(18,10),(19,6),(19,10),(20,6),(20,7),(20,9),(20,10)]
        for r, c in red_pos:
            if grid[r][c] == 8:
                grid[r][c] = 3
    # partial left
    if fill_left:
        left_pos = [(18,1),(18,3),(18,5),(19,1),(19,3),(19,5),(20,1),(20,5)]
        for r, c in left_pos:
            if grid[r][c] == 8:
                grid[r][c] = 3
    # partial right
    if fill_right:
        right_pos = [(18,16),(18,18),(18,20),(19,16),(19,19),(19,20),(20,16),(20,18),(20,20)]
        for r, c in right_pos:
            if grid[r][c] == 8:
                grid[r][c] = 3
    return grid
```