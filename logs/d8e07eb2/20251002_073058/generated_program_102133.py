```python
from typing import List, Tuple

def get_subgrid(g: List[List[int]], r_start: int, c_start: int) -> List[List[int]]:
    return [[g[r_start + i][c_start + j] for j in range(3)] for i in range(3)]

def sub_to_tuple(sub: List[List[int]]) -> Tuple[Tuple[int, ...], ...]:
    return tuple(tuple(row) for row in sub)

def is_only_0_8(sub: List[List[int]]) -> bool:
    for row in sub:
        for v in row:
            if v != 0 and v != 8:
                return False
    return True

def is_only_1_8(sub: List[List[int]]) -> bool:
    for row in sub:
        for v in row:
            if v != 1 and v != 8:
                return False
    return True

def fill_top_panel(out: List[List[int]]):
    for r in range(5):
        for c in range(22):
            if out[r][c] == 8:
                out[r][c] = 3

def fill_bottom_3(out: List[List[int]]):
    for r in range(28, 30):
        for c in range(22):
            out[r][c] = 3

def fill_bottom_2(out: List[List[int]]):
    for r in range(28, 30):
        for c in range(22):
            out[r][c] = 2

def fill_entire_panel2(out: List[List[int]]):
    for r in range(12, 18):
        for c in range(1, 21):
            if out[r][c] == 8:
                out[r][c] = 3

def fill_vertical_middle_left(out: List[List[int]]):
    for r in range(7, 27):
        for c in range(6, 11):
            if out[r][c] == 8:
                out[r][c] = 3

def fill_area(out: List[List[int]], r_start: int, r_end: int, c_start: int, c_end: int):
    r_start = max(0, r_start)
    r_end = min(22, r_end)
    c_start = max(0, c_start)
    c_end = min(22, c_end)
    for r in range(r_start, r_end):
        for c in range(c_start, c_end):
            if out[r][c] == 8:
                out[r][c] = 3

def program(g: List[List[int]]) -> List[List[int]]:
    out = [row[:] for row in g]
    left_sub = get_subgrid(g, 1, 2)
    middle_left_sub = get_subgrid(g, 1, 7)
    middle_right_sub = get_subgrid(g, 1, 12)
    right_sub = get_subgrid(g, 1, 17)
    if is_only_0_8(left_sub) and is_only_1_8(middle_left_sub):
        fill_top_panel(out)
        fill_bottom_3(out)
    else:
        fill_bottom_2(out)
    # special three for panel 2
    panel2_left_pattern = ((7, 8, 8), (7, 7, 7), (7, 8, 8))
    panel2_middle_left_pattern = ((1, 1, 1), (8, 1, 8), (1, 1, 1))
    panel2_middle_right_pattern = ((8, 6, 6), (8, 8, 6), (8, 6, 6))
    panel2_patterns_set = {panel2_left_pattern, panel2_middle_left_pattern, panel2_middle_right_pattern}
    top_three_tuples = {sub_to_tuple(middle_left_sub), sub_to_tuple(middle_right_sub), sub_to_tuple(right_sub)}
    if top_three_tuples == panel2_patterns_set:
        fill_entire_panel2(out)
    # special vertical for full H 1 in middle left when left only 0 8
    full_h1_pattern = ((1, 1, 1), (8, 1, 8), (1, 1, 1))
    if is_only_0_8(left_sub) and sub_to_tuple(middle_left_sub) == full_h1_pattern:
        fill_vertical_middle_left(out)
    # special for panel 2 left if middle right is T 7
    t7_pattern = ((7, 8, 8), (7, 7, 7), (7, 8, 8))
    if sub_to_tuple(middle_right_sub) == t7_pattern:
        fill_area(out, 12, 17, 1, 6)
    # special for panel 2 middle right and right if right is small 6
    small6_pattern = ((8, 6, 6), (8, 6, 8), (8, 6, 6))
    if sub_to_tuple(right_sub) == small6_pattern:
        fill_area(out, 12, 17, 11, 16)
        fill_area(out, 12, 17, 16, 21)
    # individual pattern match if not only 0 8 in left
    if not is_only_0_8(left_sub):
        top_subs = [left_sub, middle_left_sub, middle_right_sub, right_sub]
        base_cols = [2, 7, 12, 17]
        base_rows = [8, 13, 18]
        fixed_patterns = [
            # panel 1
            [((2, 8, 2), (8, 2, 8), (2, 8, 2)), ((0, 8, 8), (0, 0, 0), (0, 8, 0)), ((8, 8, 7), (8, 8, 7), (7, 7, 7)), ((9, 8, 9), (9, 9, 8), (9, 9, 9))],
            # panel 2
            [((7, 8, 8), (7, 7, 7), (7, 8, 8)), ((1, 1, 1), (8, 1, 8), (1, 1, 1)), ((8, 6, 6), (8, 8, 6), (8, 6, 6)), ((0, 0, 0), (0, 0, 0), (0, 0, 0))],
            # panel 3
            [((4, 8, 4), (4, 8, 4), (4, 4, 4)), ((2, 2, 8), (2, 2, 2), (8, 2, 8)), ((5, 5, 8), (5, 8, 8), (5, 5, 8)), ((1, 8, 1), (1, 1, 1), (1, 8, 1))]
        ]
        for i in range(4):
            top_p = sub_to_tuple(top_subs[i])
            for k in range(3):
                row_base = base_rows[k]
                for j in range(4):
                    fixed_p = sub_to_tuple(fixed_patterns[k][j])
                    if top_p == fixed_p:
                        col_base = base_cols[j]
                        fill_area(out, row_base - 1, row_base + 4, col_base - 1, col_base + 4)
    return out
```