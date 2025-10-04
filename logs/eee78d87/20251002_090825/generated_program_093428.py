```python
from typing import List

def create_empty_grid(size: int = 16) -> List[List[int]]:
    return [[0] * size for _ in range(size)]

def get_pattern(typ: str) -> List[int]:
    if typ == 'A':
        return [0, 7, 7, 0, 7, 7, 0, 7, 7, 0, 7, 7, 0, 7, 7, 0]
    if typ == 'B':
        return [7, 0, 0, 7, 0, 0, 7, 0, 0, 7, 0, 0, 7, 0, 0, 7]
    raise ValueError("Unknown type")

def apply_mod(row: List[int], start_col: int = 5, end_col: int = 10):
    for c in range(start_col, end_col + 1):
        if row[c] == 0:
            row[c] = 9

def apply_solid_fill(row: List[int], start_col: int = 5, end_col: int = 10):
    for c in range(start_col, end_col + 1):
        row[c] = 9

def extract_fg_value(g: List[List[int]]) -> int:
    for row in g:
        for val in row:
            if val != 7:
                return val
    return 7  # all background

def has_consecutive_non_seven(g: List[List[int]]) -> bool:
    for r in range(6):
        for c in range(5):
            if g[r][c] != 7 and g[r][c + 1] != 7:
                return True
    return False

def draw_frame(grid: List[List[int]], base_type: str, solid: bool):
    if solid:
        pat = get_pattern(base_type)
        grid[1] = pat[:]
        grid[2] = pat[:]
        grid[13] = pat[:]
        grid[14] = pat[:]
    else:
        a_pat = get_pattern('A')
        b_pat = get_pattern(base_type)
        grid[0] = a_pat[:]
        grid[1] = b_pat[:]
        grid[2] = b_pat[:]
        grid[3] = a_pat[:]
        grid[12] = a_pat[:]
        grid[13] = b_pat[:]
        grid[14] = b_pat[:]
        grid[15] = a_pat[:]

def draw_content(grid: List[List[int]], base_type: str, solid: bool):
    base_pat = get_pattern(base_type)
    a_pat = get_pattern('A')
    # row 4: plain base
    grid[4] = base_pat[:]
    # row 5: mod base
    grid[5] = base_pat[:]
    apply_mod(grid[5])
    # row 6: connector
    if solid:
        grid[6] = [0] * 16
        apply_solid_fill(grid[6])
    else:
        grid[6] = a_pat[:]
        apply_mod(grid[6])
    # row 7: mod base
    grid[7] = base_pat[:]
    apply_mod(grid[7])
    # row 8: mod base
    grid[8] = base_pat[:]
    apply_mod(grid[8])
    # row 9: connector
    if solid:
        grid[9] = [0] * 16
        apply_solid_fill(grid[9])
    else:
        grid[9] = a_pat[:]
        apply_mod(grid[9])
    # row 10: mod base
    grid[10] = base_pat[:]
    apply_mod(grid[10])
    # row 11: plain base
    grid[11] = base_pat[:]

def program(g: List[List[int]]) -> List[List[int]]:
    fg = extract_fg_value(g)
    base_type = 'A' if fg == 3 else 'B'
    solid = has_consecutive_non_seven(g)
    grid = create_empty_grid()
    draw_frame(grid, base_type, solid)
    draw_content(grid, base_type, solid)
    return grid
```