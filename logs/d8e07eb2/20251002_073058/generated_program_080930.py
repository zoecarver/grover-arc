```python
from typing import List

def has_zero_top(g: List[List[int]]) -> bool:
    return any(g[r][c] == 0 for r in range(1, 4) for c in range(22))

def has_one_top(g: List[List[int]]) -> bool:
    return any(g[r][c] == 1 for r in range(1, 4) for c in range(22))

def has_one_mid(g: List[List[int]]) -> bool:
    return any(g[r][c] == 1 for r in range(1, 4) for c in range(7, 11))

def full_zero_left(g: List[List[int]]) -> bool:
    return all(g[r][c] == 0 for r in range(1, 4) for c in range(2, 5))

def has_seven_right(g: List[List[int]]) -> bool:
    return any(g[r][c] == 7 for r in range(1, 4) for c in range(12, 16))

def is_nine_right(g: List[List[int]]) -> bool:
    non_eight = [g[r][c] for r in range(1, 4) for c in range(12, 16) if g[r][c] != 8]
    return bool(non_eight) and all(x == 9 for x in non_eight)

def any_two_left(g: List[List[int]]) -> bool:
    return any(g[r][c] == 2 for r in range(1, 4) for c in range(2, 6))

def any_two_far(g: List[List[int]]) -> bool:
    return any(g[r][c] == 2 for r in range(1, 4) for c in range(17, 21))

def any_four_mid(g: List[List[int]]) -> bool:
    return any(g[r][c] == 4 for r in range(1, 4) for c in range(7, 11))

def any_two_mid(g: List[List[int]]) -> bool:
    return any(g[r][c] == 2 for r in range(1, 4) for c in range(7, 11))

def fill_region(out: List[List[int]], row_start: int, row_end: int, col_start: int, col_end: int, val: int) -> None:
    for r in range(row_start, row_end):
        for c in range(col_start, col_end):
            if out[r][c] == 8:
                out[r][c] = val

def fill_top_and_bottom_if_zero_and_one(g: List[List[int]], out: List[List[int]]) -> None:
    if has_zero_top(g) and has_one_top(g):
        fill_region(out, 0, 5, 0, 22, 3)
        fill_region(out, 28, 30, 0, 22, 3)
    else:
        fill_region(out, 28, 30, 0, 22, 2)

def fill_upper_left_if_two_left(g: List[List[int]], out: List[List[int]]) -> None:
    if any_two_left(g):
        fill_region(out, 8, 12, 1, 6, 3)

def fill_long_mid_if_one_mid_and_two_far(g: List[List[int]], out: List[List[int]]) -> None:
    if has_one_mid(g) and any_two_far(g):
        fill_region(out, 7, 27, 6, 11, 3)

def fill_upper_far_if_nine_right(g: List[List[int]], out: List[List[int]]) -> None:
    if is_nine_right(g):
        fill_region(out, 8, 12, 16, 21, 3)
        fill_region(out, 18, 22, 16, 21, 3)

def fill_middle_left_if_full_zero_left(g: List[List[int]], out: List[List[int]]) -> None:
    if full_zero_left(g):
        fill_region(out, 12, 18, 1, 6, 3)

def fill_middle_mid_if_one_mid(g: List[List[int]], out: List[List[int]]) -> None:
    if has_one_mid(g):
        fill_region(out, 12, 18, 6, 11, 3)

def fill_middle_right_if_seven_right(g: List[List[int]], out: List[List[int]]) -> None:
    if has_seven_right(g):
        fill_region(out, 12, 18, 11, 21, 3)

def fill_lower_left_mid_if_four_mid(g: List[List[int]], out: List[List[int]]) -> None:
    if any_four_mid(g):
        fill_region(out, 17, 23, 1, 11, 3)

def fill_lower_mid_if_two_mid(g: List[List[int]], out: List[List[int]]) -> None:
    if any_two_mid(g):
        fill_region(out, 18, 23, 6, 11, 3)

def fill_lower_far_if_two_far_and_not_one_mid(g: List[List[int]], out: List[List[int]]) -> None:
    if any_two_far(g) and not has_one_mid(g):
        fill_region(out, 23, 28, 16, 21, 3)

def program(g: List[List[int]]) -> List[List[int]]:
    out = [row[:] for row in g]
    fill_top_and_bottom_if_zero_and_one(g, out)
    fill_upper_left_if_two_left(g, out)
    fill_long_mid_if_one_mid_and_two_far(g, out)
    fill_upper_far_if_nine_right(g, out)
    fill_middle_left_if_full_zero_left(g, out)
    fill_middle_mid_if_one_mid(g, out)
    fill_middle_right_if_seven_right(g, out)
    fill_lower_left_mid_if_four_mid(g, out)
    fill_lower_mid_if_two_mid(g, out)
    fill_lower_far_if_two_far_and_not_one_mid(g, out)
    return out
```