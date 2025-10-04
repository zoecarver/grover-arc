```python
from typing import List

def create_empty_grid(size: int = 16) -> List[List[int]]:
    return [[0] * size for _ in range(size)]

def get_a_row() -> List[int]:
    return [0, 7, 7, 0] * 4

def get_b_row() -> List[int]:
    return [7, 0, 0, 7] * 4

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

def get_base_row(fg: int) -> List[int]:
    if fg == 3:
        return get_a_row()
    return get_b_row()

def build_thin_grid(base: List[int]) -> List[List[int]]:
    mod_base = apply_mod(base)
    patterns = [
        get_empty_row(),
        base[:],
        base[:],
        get_empty_row(),
        base[:],
        mod_base,
        get_fill_row(),
        mod_base,
        mod_base,
        get_fill_row(),
        mod_base,
        base[:],
        get_empty_row(),
        base[:],
        base[:],
        get_empty_row()
    ]
    return [[p[j] for j in range(16)] for p in patterns]

def build_non_thin_grid() -> List[List[int]]:
    grid = create_empty_grid()
    for r in range(16):
        if r % 3 == 0:
            row = get_a_row()
        else:
            row = get_b_row()
        if 5 <= r <= 10:
            row = apply_mod(row)
        grid[r] = row
    return grid

def program(g: List[List[int]]) -> List[List[int]]:
    is_thin = has_three_consecutive(g)
    fg = extract_fg_value(g)
    if is_thin:
        base = get_base_row(fg)
        return build_thin_grid(base)
    return build_non_thin_grid()
```