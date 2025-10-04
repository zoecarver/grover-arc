```python
from typing import List

def has_zero_left(g: List[List[int]]) -> bool:
    return any(g[r][c] == 0 for r in range(1, 4) for c in range(2, 5))

def full_zero_left(g: List[List[int]]) -> bool:
    return all(g[r][c] == 0 for r in range(1, 4) for c in range(2, 5))

def has_one_mid(g: List[List[int]]) -> bool:
    return any(g[r][c] == 1 for r in range(1, 4) for c in range(7, 11))

def has_full_u_mid(g: List[List[int]]) -> bool:
    if not all(g[1][c] == 1 for c in range(7, 10)):
        return False
    if g[2][8] != 1:
        return False
    if not all(g[3][c] == 1 for c in range(7, 10)):
        return False
    return True

def has_two_left(g: List[List[int]]) -> bool:
    return any(g[r][c] == 2 for r in range(1, 4) for c in range(2, 5))

def has_two_mid(g: List[List[int]]) -> bool:
    return any(g[r][c] == 2 for r in range(1, 4) for c in range(7, 11))

def has_four_mid(g: List[List[int]]) -> bool:
    return any(g[r][c] == 4 for r in range(1, 4) for c in range(7, 11))

def has_seven_right(g: List[List[int]]) -> bool:
    return any(g[r][c] == 7 for r in range(1, 4) for c in range(12, 16))

def has_six_far(g: List[List[int]]) -> bool:
    return any(g[r][c] == 6 for r in range(1, 4) for c in range(17, 21))

def has_two_far(g: List[List[int]]) -> bool:
    return any(g[r][c] == 2 for r in range(1, 4) for c in range(17, 21))

def has_six_right(g: List[List[int]]) -> bool:
    return any(g[r][c] == 6 for r in range(1, 4) for c in range(12, 16))

def is_nine_right(g: List[List[int]]) -> bool:
    non_eight = [g[r][c] for r in range(1, 4) for c in range(12, 16) if g[r][c] != 8]
    return len(non_eight) > 0 and all(x == 9 for x in non_eight)

def fill_region(out: List[List[int]], row_start: int, row_end: int, col_start: int, col_end: int, val: int) -> None:
    for r in range(row_start, row_end + 1):
        for c in range(col_start, col_end + 1):
            if out[r][c] == 8:
                out[r][c] = val

def fill_top_if_zero_and_one(out: List[List[int]]) -> None:
    if has_zero_left(out) and has_one_mid(out):
        fill_region(out, 0, 4, 0, 21, 3)

def fill_bottom_if_zero_and_one(out: List[List[int]]) -> None:
    if has_zero_left(out) and has_one_mid(out):
        fill_region(out, 28, 29, 0, 21, 3)
    else:
        fill_region(out, 28, 29, 0, 21, 2)

def fill_big_block_if_full_combo(out: List[List[int]]) -> None:
    if full_zero_left(out) and has_full_u_mid(out) and has_seven_right(out) and has_six_far(out):
        fill_region(out, 13, 17, 1, 20, 3)

def fill_vertical_mid_if_partial_zero_full_u_six_two_far(out: List[List[int]]) -> None:
    if has_zero_left(out) and not full_zero_left(out) and has_full_u_mid(out) and has_six_right(out) and has_two_far(out):
        fill_region(out, 8, 26, 6, 10, 3)

def fill_upper_left_if_two_left(out: List[List[int]]) -> None:
    if has_two_left(out):
        fill_region(out, 8, 11, 1, 5, 3)

def fill_upper_far_right_if_nine_right(out: List[List[int]]) -> None:
    if is_nine_right(out):
        fill_region(out, 8, 11, 16, 20, 3)

def fill_middle_left_if_full_zero_not_full_u(out: List[List[int]]) -> None:
    if full_zero_left(out) and not has_full_u_mid(out):
        fill_region(out, 12, 16, 1, 5, 3)

def fill_middle_mid_if_one_not_full_u(out: List[List[int]]) -> None:
    if has_one_mid(out) and not has_full_u_mid(out):
        fill_region(out, 12, 16, 6, 10, 3)

def fill_middle_right_if_seven_right(out: List[List[int]]) -> None:
    if has_seven_right(out):
        fill_region(out, 12, 16, 11, 20, 3)

def fill_lower_left_if_four_mid(out: List[List[int]]) -> None:
    if has_four_mid(out):
        fill_region(out, 18, 21, 1, 5, 3)

def fill_lower_mid_if_two_or_four_mid(out: List[List[int]]) -> None:
    if has_two_mid(out):
        fill_region(out, 17, 21, 6, 10, 3)
    elif has_four_mid(out):
        fill_region(out, 18, 21, 6, 10, 3)

def fill_lower_right_c_if_nine_right(out: List[List[int]]) -> None:
    if is_nine_right(out):
        fill_region(out, 17, 21, 16, 20, 3)

def fill_d_right_if_two_far_not_one_mid(out: List[List[int]]) -> None:
    if has_two_far(out) and not has_one_mid(out):
        fill_region(out, 23, 26, 16, 20, 3)

def program(g: List[List[int]]) -> List[List[int]]:
    out = [row[:] for row in g]
    fill_top_if_zero_and_one(out)
    fill_bottom_if_zero_and_one(out)
    fill_big_block_if_full_combo(out)
    fill_vertical_mid_if_partial_zero_full_u_six_two_far(out)
    fill_upper_left_if_two_left(out)
    fill_upper_far_right_if_nine_right(out)
    fill_middle_left_if_full_zero_not_full_u(out)
    fill_middle_mid_if_one_not_full_u(out)
    fill_middle_right_if_seven_right(out)
    fill_lower_left_if_four_mid(out)
    fill_lower_mid_if_two_or_four_mid(out)
    fill_lower_right_c_if_nine_right(out)
    fill_d_right_if_two_far_not_one_mid(out)
    return out
```