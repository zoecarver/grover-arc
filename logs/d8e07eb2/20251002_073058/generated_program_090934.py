```python
from typing import List

def has_zero_top(g: List[List[int]]) -> bool:
    return any(g[r][c] == 0 for r in range(1, 4) for c in range(22))

def has_one_top(g: List[List[int]]) -> bool:
    return any(g[r][c] == 1 for r in range(1, 4) for c in range(22))

def full_zero_left(g: List[List[int]]) -> bool:
    return all(g[r][c] == 0 for r in range(1, 4) for c in range(2, 5))

def has_one_mid(g: List[List[int]]) -> bool:
    return any(g[r][c] == 1 for r in range(1, 4) for c in range(7, 11))

def has_seven_right(g: List[List[int]]) -> bool:
    return any(g[r][c] == 7 for r in range(1, 4) for c in range(12, 16))

def is_nine_right(g: List[List[int]]) -> bool:
    non_eight = [g[r][c] for r in range(1, 4) for c in range(12, 16) if g[r][c] != 8]
    return bool(non_eight) and all(x == 9 for x in non_eight)

def any_two_left(g: List[List[int]]) -> bool:
    return any(g[r][c] == 2 for r in range(1, 4) for c in range(2, 5))

def any_two_far(g: List[List[int]]) -> bool:
    return any(g[r][c] == 2 for r in range(1, 4) for c in range(17, 21))

def any_four_mid(g: List[List[int]]) -> bool:
    return any(g[r][c] == 4 for r in range(1, 4) for c in range(7, 11))

def any_two_top(g: List[List[int]]) -> bool:
    return any(g[r][c] == 2 for r in range(1, 4) for c in range(22))

def fill_region(out: List[List[int]], row_range: range, col_range: range, val: int) -> None:
    for r in row_range:
        for c in col_range:
            if out[r][c] == 8:
                out[r][c] = val

def program(g: List[List[int]]) -> List[List[int]]:
    out = [row[:] for row in g]
    if has_zero_top(g) and has_one_top(g):
        fill_region(out, range(0, 5), range(22), 3)
        fill_region(out, range(28, 30), range(22), 3)
    else:
        fill_region(out, range(28, 30), range(22), 2)
    if any_two_left(g):
        fill_region(out, range(7, 12), range(1, 6), 3)
    if is_nine_right(g):
        fill_region(out, range(8, 12), range(16, 21), 3)
        fill_region(out, range(18, 22), range(16, 21), 3)
    if full_zero_left(g):
        fill_region(out, range(12, 17), range(1, 6), 3)
        fill_region(out, range(17, 18), range(1, 6), 3)
    if has_one_mid(g):
        fill_region(out, range(12, 17), range(6, 11), 3)
        fill_region(out, range(17, 18), range(6, 11), 3)
    if has_seven_right(g):
        fill_region(out, range(12, 17), range(11, 21), 3)
        fill_region(out, range(17, 18), range(11, 21), 3)
    if has_one_mid(g) and any_two_far(g):
        fill_region(out, range(7, 27), range(6, 11), 3)
    if any_four_mid(g):
        fill_region(out, range(18, 22), range(1, 6), 3)
    if any_two_top(g):
        fill_region(out, range(18, 22), range(6, 11), 3)
    if any_two_far(g) and not has_one_mid(g):
        fill_region(out, range(22, 27), range(16, 21), 3)
    return out
```