```python
from typing import List

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

def has_three_consecutive(g: List[List[int]]) -> tuple[bool, int]:
    has = False
    min_start = 6
    for r in range(6):
        for i in range(4):
            if g[r][i] != 7 and g[r][i + 1] != 7 and g[r][i + 2] != 7:
                has = True
                min_start = min(min_start, i)
    return has, min_start

def program(g: List[List[int]]) -> List[List[int]]:
    has_three, min_start = has_three_consecutive(g)
    output: List[List[int]] = [[0] * 16 for _ in range(16)]
    if not has_three:
        # mixed style
        for rr in range(16):
            if rr % 3 == 0:
                base = get_a_row()
            else:
                base = get_b_row()
            if 5 <= rr <= 10:
                output[rr] = apply_mod(base)
            else:
                output[rr] = base[:]
    else:
        # thin style
        is_left = min_start <= 1
        line_row = get_b_row() if is_left else get_a_row()
        # top
        output[0] = get_empty_row()
        output[1] = line_row[:]
        output[2] = line_row[:]
        output[3] = get_empty_row()
        # middle
        output[4] = line_row[:]
        output[5] = apply_mod(line_row[:])
        output[6] = get_fill_row()
        output[7] = apply_mod(line_row[:])
        output[8] = apply_mod(line_row[:])
        output[9] = get_fill_row()
        output[10] = apply_mod(line_row[:])
        output[11] = line_row[:]
        # bottom
        output[12] = get_empty_row()
        output[13] = line_row[:]
        output[14] = line_row[:]
        output[15] = get_empty_row()
    return output
```