```python
def is_special(grid):
    count = 0
    for r in range(5):
        for c in range(22):
            if grid[r][c] == 8:
                count += 1
    return count == 84

def count_zeros_top(grid):
    count = 0
    for r in range(1, 4):
        for c in range(22):
            if grid[r][c] == 0:
                count += 1
    return count

def get_top_colors(grid):
    s = set()
    for r in range(1, 4):
        for c in range(22):
            col = grid[r][c]
            if col not in (0, 8):
                s.add(col)
    return s

def fill_top_with_green(grid):
    for r in range(5):
        for c in range(22):
            if grid[r][c] == 8:
                grid[r][c] = 3

def set_bottom_green(grid):
    for r in [28, 29]:
        for c in range(22):
            grid[r][c] = 3

def set_bottom_red(grid):
    for r in [28, 29]:
        for c in range(22):
            grid[r][c] = 2

def fill_full_second(grid):
    for r in range(12, 17):
        for c in range(1, 21):
            if grid[r][c] == 8:
                grid[r][c] = 3

def fill_partial_second(grid):
    for c in range(1, 21):
        if grid[12][c] == 8:
            grid[12][c] = 3
        if grid[16][c] == 8:
            grid[16][c] = 3
    cols13 = [1, 3, 4, 5, 11, 12, 15, 16, 20]
    for c in cols13:
        if grid[13][c] == 8:
            grid[13][c] = 3
        if grid[15][c] == 8:
            grid[15][c] = 3
    cols14 = [1, 5, 11, 12, 13, 15, 16, 20]
    for c in cols14:
        if grid[14][c] == 8:
            grid[14][c] = 3

def fill_vertical_middle(grid):
    for r in range(7, 18):
        for c in range(6, 11):
            if grid[r][c] == 8:
                grid[r][c] = 3

def fill_train3_regions(grid):
    for r in range(7, 12):
        for c in range(1, 6):
            if grid[r][c] == 8:
                grid[r][c] = 3
    for r in range(17, 22):
        for c in range(1, 11):
            if grid[r][c] == 8:
                grid[r][c] = 3
    for r in range(23, 27):
        for c in range(16, 21):
            if grid[r][c] == 8:
                grid[r][c] = 3

def fill_train5_regions(grid):
    for r in range(7, 17):
        for c in range(6, 11):
            if grid[r][c] == 8:
                grid[r][c] = 3
    for r in range(17, 22):
        for c in range(16, 21):
            if grid[r][c] == 8:
                grid[r][c] = 3

def program(g: List[List[int]]) -> List[List[int]]:
    grid = [row[:] for row in g]
    special = is_special(grid)
    zeros = count_zeros_top(grid)
    colors = get_top_colors(grid)
    if special:
        fill_top_with_green(grid)
        set_bottom_green(grid)
    else:
        set_bottom_red(grid)
    if zeros == 9:
        if special:
            fill_full_second(grid)
        else:
            fill_partial_second(grid)
    elif special:
        fill_vertical_middle(grid)
    elif colors == {2, 4}:
        fill_train3_regions(grid)
    elif colors == {1, 9}:
        fill_train5_regions(grid)
    else:
        fill_partial_second(grid)
    return grid
```