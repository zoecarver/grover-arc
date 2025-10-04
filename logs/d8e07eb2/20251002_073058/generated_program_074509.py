```python
from typing import List
from functools import reduce

def has_zero_left(g: List[List[int]]) -> bool:
    return any(g[r][c] == 0 for r in range(1, 4) for c in range(2, 5))

def has_one_window(g: List[List[int]]) -> bool:
    return any(g[r][c] == 1 for r in range(1, 4) for c in range(7, 10))

def solid_zero_left(g: List[List[int]]) -> bool:
    return all(g[r][c] == 0 for r in range(1, 4) for c in range(2, 5))

def has_partial_zero_left(g: List[List[int]]) -> bool:
    num_zeros = sum(1 for r in range(1, 4) for c in range(2, 5) if g[r][c] == 0)
    return 0 < num_zeros < 9

def has_two_window(g: List[List[int]]) -> bool:
    num_twos = sum(1 for r in range(1, 4) for c in range(7, 10) if g[r][c] == 2)
    return num_twos >= 5

def has_seven_middle(g: List[List[int]]) -> bool:
    return any(g[r][c] == 7 for r in range(1, 4) for c in range(12, 15))

def has_six_right(g: List[List[int]]) -> bool:
    return any(g[r][c] == 6 for r in range(1, 4) for c in range(18, 20))

def has_two_left(g: List[List[int]]) -> bool:
    return any(g[r][c] == 2 for r in range(1, 4) for c in range(2, 5))

def has_four_window(g: List[List[int]]) -> bool:
    return any(g[r][c] == 4 for r in range(1, 4) for c in range(7, 10))

def has_two_middle(g: List[List[int]]) -> bool:
    return any(g[r][c] == 2 for r in range(1, 4) for c in range(12, 15))

def has_two_right(g: List[List[int]]) -> bool:
    return any(g[r][c] == 2 for r in range(1, 4) for c in range(17, 20))

def has_nine_middle(g: List[List[int]]) -> bool:
    return any(g[r][c] == 9 for r in range(1, 4) for c in range(12, 15))

def has_one_left(g: List[List[int]]) -> bool:
    return any(g[r][c] == 1 for r in range(1, 4) for c in range(2, 5))

def fill_top_green(g: List[List[int]], out: List[List[int]]):
    if not (has_zero_left(g) and has_one_window(g)):
        return
    for r in range(5):
        out[r] = [3 if x == 8 else x for x in out[r]]

def fill_bottom_green_or_red(g: List[List[int]], out: List[List[int]]):
    color = 3 if has_zero_left(g) and has_one_window(g) else 2
    for r in range(28, 30):
        out[r] = [color for _ in out[r]]

def fill_B_full(g: List[List[int]], out: List[List[int]]):
    if not (solid_zero_left(g) and has_one_window(g) and has_seven_middle(g) and has_six_right(g)):
        return
    for r in range(13, 17):
        mid = [3 if x == 8 else x for x in out[r][1:21]]
        out[r] = out[r][0:1] + mid + out[r][21:22]

def fill_B_partial(g: List[List[int]], out: List[List[int]]):
    if not (solid_zero_left(g) and has_two_window(g) and has_seven_middle(g) and has_six_right(g)):
        return
    for r in range(12, 17):
        left_part = [3 if x == 8 else x for x in out[r][1:6]]
        mid_part = out[r][6:11]
        right_part = [3 if x == 8 else x for x in out[r][11:21]]
        out[r] = out[r][0:1] + left_part + mid_part + right_part + out[r][21:22]

def fill_middle_strip_all(g: List[List[int]], out: List[List[int]]):
    if not (has_one_window(g) and has_partial_zero_left(g)):
        return
    for r in range(7, 27):
        mid_part = [3 if x == 8 else x for x in out[r][6:11]]
        out[r] = out[r][0:6] + mid_part + out[r][11:22]

def fill_middle_strip_B(g: List[List[int]], out: List[List[int]]):
    if not (has_one_window(g) and not has_zero_left(g)):
        return
    for r in range(12, 17):
        mid_part = [3 if x == 8 else x for x in out[r][6:11]]
        out[r] = out[r][0:6] + mid_part + out[r][11:22]

def fill_left_A(g: List[List[int]], out: List[List[int]]):
    if not has_two_left(g):
        return
    for r in range(7, 12):
        left_part = [3 if x == 8 else x for x in out[r][1:6]]
        out[r] = out[r][0:1] + left_part + out[r][6:22]

def fill_left_C(g: List[List[int]], out: List[List[int]]):
    if not has_four_window(g):
        return
    for r in range(17, 22):
        left_part = [3 if x == 8 else x for x in out[r][1:6]]
        out[r] = out[r][0:1] + left_part + out[r][6:22]

def fill_middle_C(g: List[List[int]], out: List[List[int]]):
    if not has_two_middle(g):
        return
    for r in range(17, 22):
        mid_part = [3 if x == 8 else x for x in out[r][6:11]]
        out[r] = out[r][0:6] + mid_part + out[r][11:22]

def fill_right_D(g: List[List[int]], out: List[List[int]]):
    if not (has_two_right(g) and not has_one_window(g)):
        return
    for r in range(22, 27):
        right_part = [3 if x == 8 else x for x in out[r][16:21]]
        out[r] = out[r][0:16] + right_part + out[r][21:22]

def fill_right_A(g: List[List[int]], out: List[List[int]]):
    if not has_nine_middle(g):
        return
    for r in range(7, 12):
        right_part = [3 if x == 8 else x for x in out[r][16:21]]
        out[r] = out[r][0:16] + right_part + out[r][21:22]

def fill_right_C(g: List[List[int]], out: List[List[int]]):
    if not has_one_left(g):
        return
    for r in range(17, 22):
        right_part = [3 if x == 8 else x for x in out[r][16:21]]
        out[r] = out[r][0:16] + right_part + out[r][21:22]

def program(g: List[List[int]]) -> List[List[int]]:
    out = [row[:] for row in g]
    fill_B_full(g, out)
    fill_B_partial(g, out)
    fill_middle_strip_all(g, out)
    fill_middle_strip_B(g, out)
    fill_left_A(g, out)
    fill_left_C(g, out)
    fill_middle_C(g, out)
    fill_right_D(g, out)
    fill_right_A(g, out)
    fill_right_C(g, out)
    fill_top_green(g, out)
    fill_bottom_green_or_red(g, out)
    return out
```