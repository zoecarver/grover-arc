```python
from typing import List

def has_zero_top(g: List[List[int]]) -> bool:
    return any(g[r][c] == 0 for r in range(1, 4) for c in range(22))

def has_one_top(g: List[List[int]]) -> bool:
    return any(g[r][c] == 1 for r in range(1, 4) for c in range(22))

def full_zero_left(g: List[List[int]]) -> bool:
    return all(g[r][c] == 0 for r in range(1, 4) for c in range(2, 5))

def has_one_mid(g: List[List[int]]) -> bool:
    return any(g[r][c] == 1 for r in range(1, 4) for c in range(7, 10))

def has_seven_right(g: List[List[int]]) -> bool:
    return any(g[r][c] == 7 for r in range(1, 4) for c in range(12, 15))

def is_nine_right(g: List[List[int]]) -> bool:
    non_eight = [g[r][c] for r in range(1, 4) for c in range(12, 15) if g[r][c] != 8]
    return len(non_eight) > 0 and all(x == 9 for x in non_eight)

def any_two_left(g: List[List[int]]) -> bool:
    return any(g[r][c] == 2 for r in range(1, 4) for c in range(2, 5))

def any_two_far(g: List[List[int]]) -> bool:
    return any(g[r][c] == 2 for r in range(1, 4) for c in range(17, 22))

def any_two_top(g: List[List[int]]) -> bool:
    return any(g[r][c] == 2 for r in range(1, 4) for c in range(22))

def any_two_mid(g: List[List[int]]) -> bool:
    return any(g[r][c] == 2 for r in range(1, 4) for c in range(7, 10))

def has_one_left(g: List[List[int]]) -> bool:
    return any(g[r][c] == 1 for r in range(1, 4) for c in range(2, 5))

def fill_region(out: List[List[int]], r_start: int, r_end: int, c_start: int, c_end: int, val: int) -> None:
    for r in range(r_start, r_end + 1):
        for c in range(c_start, c_end + 1):
            if out[r][c] == 8:
                out[r][c] = val

def fill_top_band(out: List[List[int]], g: List[List[int]]) -> None:
    if has_zero_top(g) and has_one_top(g):
        fill_region(out, 0, 4, 0, 21, 3)

def fill_bottom_band(out: List[List[int]], g: List[List[int]]) -> None:
    if has_zero_top(g) and has_one_top(g):
        fill_region(out, 28, 29, 0, 21, 3)
    else:
        fill_region(out, 28, 29, 0, 21, 2)

def fill_upper_left(out: List[List[int]], g: List[List[int]]) -> None:
    if any_two_left(g):
        fill_region(out, 7, 11, 1, 5, 3)
        for r in range(8, 11):
            if g[r][2] == 2 and g[r][4] == 2 and out[r][6] == 8:
                out[r][6] = 3

def fill_upper_far(out: List[List[int]], g: List[List[int]]) -> None:
    if is_nine_right(g):
        fill_region(out, 7, 11, 16, 20, 3)

def fill_long_mid(out: List[List[int]], g: List[List[int]]) -> None:
    if has_one_mid(g) and any_two_far(g):
        fill_region(out, 8, 26, 6, 10, 3)

def fill_middle_left(out: List[List[int]], g: List[List[int]]) -> None:
    if full_zero_left(g):
        fill_region(out, 12, 16, 1, 5, 3)

def fill_middle_mid(out: List[List[int]], g: List[List[int]]) -> None:
    if has_one_mid(g):
        fill_region(out, 12, 16, 6, 10, 3)

def fill_middle_right(out: List[List[int]], g: List[List[int]]) -> None:
    if has_seven_right(g):
        fill_region(out, 12, 16, 11, 20, 3)

def fill_row17_mid(out: List[List[int]], g: List[List[int]]) -> None:
    if (has_one_mid(g) and not full_zero_left(g)) or any_two_mid(g):
        fill_region(out, 17, 17, 6, 10, 3)

def fill_lower_left(out: List[List[int]], g: List[List[int]]) -> None:
    if any_two_left(g):
        fill_region(out, 18, 21, 1, 5, 3)

def fill_lower_mid(out: List[List[int]], g: List[List[int]]) -> None:
    if any_two_top(g):
        fill_region(out, 18, 21, 6, 10, 3)

def fill_lower_far_early(out: List[List[int]], g: List[List[int]]) -> None:
    if has_one_left(g):
        fill_region(out, 18, 21, 16, 20, 3)

def fill_lower_far_late(out: List[List[int]], g: List[List[int]]) -> None:
    if any_two_far(g) and not has_one_mid(g):
        fill_region(out, 22, 26, 16, 20, 3)

def program(g: List[List[int]]) -> List[List[int]]:
    out = [row[:] for row in g]
    fill_top_band(out, g)
    fill_bottom_band(out, g)
    fill_upper_left(out, g)
    fill_upper_far(out, g)
    fill_long_mid(out, g)
    fill_middle_left(out, g)
    fill_middle_mid(out, g)
    fill_middle_right(out, g)
    fill_row17_mid(out, g)
    fill_lower_left(out, g)
    fill_lower_mid(out, g)
    fill_lower_far_early(out, g)
    fill_lower_far_late(out, g)
    return out
```