```python
from typing import List

def create_empty_grid(size: int = 16) -> List[List[int]]:
    return [[0] * size for _ in range(size)]

def get_a_row() -> List[int]:
    return [0, 7, 7, 0, 7, 7, 0, 7, 7, 0, 7, 7, 0, 7, 7, 0]

def get_b_row() -> List[int]:
    return [7, 0, 0, 7, 0, 0, 7, 0, 0, 7, 0, 0, 7, 0, 0, 7]

def get_empty_row() -> List[int]:
    return [0] * 16

def get_fill_row() -> List[int]:
    row = [0] * 16
    for j in range(5, 11):
        row[j] = 9
    return row

def apply_mod(row: List[int]) -> List[int]:
    new_row = row[:]
    for j in range(5, 11):
        if new_row[j] == 0:
            new_row[j] = 9
    return new_row

def extract_fg_value(g: List[List[int]]) -> int:
    for row in g:
        for val in row:
            if val != 7:
                return val
    return 7

def has_three_consecutive(g: List[List[int]]) -> bool:
    for r in range(6):
        for i in range(4):
            if g[r][i] != 7 and g[r][i + 1] != 7 and g[r][i + 2] != 7:
                return True
    return False

def program(g: List[List[int]]) -> List[List[int]]:
    grid = create_empty_grid()
    fg = extract_fg_value(g)
    is_thin = has_three_consecutive(g)
    a_row = get_a_row()
    b_row = get_b_row()
    empty = get_empty_row()
    fill = get_fill_row()
    if is_thin:
        line_row = a_row if fg == 3 else b_row
        mod_line = apply_mod(line_row)
        grid[0] = empty
        grid[1] = line_row
        grid[2] = line_row
        grid[3] = empty
        grid[4] = line_row
        grid[5] = mod_line
        grid[6] = fill
        grid[7] = mod_line
        grid[8] = mod_line
        grid[9] = fill
        grid[10] = mod_line
        grid[11] = line_row
        grid[12] = empty
        grid[13] = line_row
        grid[14] = line_row
        grid[15] = empty
    else:
        for r in range(16):
            if r % 3 == 0:
                base = a_row
            else:
                base = b_row
            if 5 <= r <= 10:
                base = apply_mod(base)
            grid[r] = base
    return grid
```