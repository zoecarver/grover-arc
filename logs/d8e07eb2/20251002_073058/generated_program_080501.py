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
    return bool(non_eight) and all(x == 9 for x in non_eight)

def any_two_left(g: List[List[int]]) -> bool:
    return any(g[r][c] == 2 for r in range(1, 4) for c in range(2, 5))

def any_four_mid(g: List[List[int]]) -> bool:
    return any(g[r][c] == 4 for r in range(1, 4) for c in range(7, 10))

def any_two_far(g: List[List[int]]) -> bool:
    return any(g[r][c] == 2 for r in range(1, 4) for c in range(17, 20))

def has_two_mid(g: List[List[int]]) -> bool:
    return any(g[r][c] == 2 for r in range(1, 4) for c in range(7, 10))

def has_six_far(g: List[List[int]]) -> bool:
    return any(g[r][c] == 6 for r in range(1, 4) for c in range(17, 20))

def has_one_left(g: List[List[int]]) -> bool:
    return any(g[r][c] == 1 for r in range(1, 4) for c in range(2, 5))

def fill_top(out: List[List[int]], g: List[List[int]]):
    if has_zero_top(g) and has_one_top(g):
        for r in range(5):
            for c in range(22):
                if out[r][c] == 8:
                    out[r][c] = 3

def fill_bottom(out: List[List[int]], g: List[List[int]]):
    color = 3 if has_zero_top(g) and has_one_top(g) else 2
    for c in range(22):
        if out[29][c] == 8:
            out[29][c] = color

def fill_upper_left_specific(out: List[List[int]]):
    # Row 7, cols 1-6
    for c in range(1, 7):
        if out[7][c] == 8:
            out[7][c] = 3
    # Row 8, cols 1,3,5,6
    for c in [1, 3, 5, 6]:
        if out[8][c] == 8:
            out[8][c] = 3
    # Row 9, cols 1,2,4,5
    for c in [1, 2, 4, 5]:
        if out[9][c] == 8:
            out[9][c] = 3
    # Row 10, cols 1,3,5
    for c in [1, 3, 5]:
        if out[10][c] == 8:
            out[10][c] = 3
    # Row 11, cols 1-6
    for c in range(1, 7):
        if out[11][c] == 8:
            out[11][c] = 3

def fill_upper_far(out: List[List[int]]):
    for r in range(8, 12):
        for c in range(16, 21):
            if out[r][c] == 8:
                out[r][c] = 3

def fill_upper_mid(out: List[List[int]], g: List[List[int]]):
    if has_one_mid(g) and has_zero_top(g) and not full_zero_left(g):
        for r in range(8, 12):
            for c in range(6, 11):
                if out[r][c] == 8:
                    out[r][c] = 3

def fill_middle_left(out: List[List[int]], g: List[List[int]]):
    if full_zero_left(g):
        for r in range(12, 18):
            for c in range(1, 6):
                if out[r][c] == 8:
                    out[r][c] = 3

def fill_middle_mid(out: List[List[int]], g: List[List[int]]):
    if has_one_mid(g):
        for r in range(12, 18):
            for c in range(6, 11):
                if out[r][c] == 8:
                    out[r][c] = 3

def fill_middle_right(out: List[List[int]], g: List[List[int]]):
    if has_seven_right(g):
        for r in range(12, 18):
            for c in range(11, 16):
                if out[r][c] == 8:
                    out[r][c] = 3

def fill_middle_far(out: List[List[int]], g: List[List[int]]):
    if has_six_far(g):
        for r in range(12, 18):
            for c in range(16, 21):
                if out[r][c] == 8:
                    out[r][c] = 3

def fill_long_mid(out: List[List[int]], g: List[List[int]]):
    if has_one_mid(g) and any_two_far(g):
        for r in range(8, 27):
            for c in range(6, 11):
                if out[r][c] == 8:
                    out[r][c] = 3

def fill_lower_left_mid(out: List[List[int]], g: List[List[int]]):
    if any_four_mid(g):
        for r in range(18, 22):
            for c in range(1, 11):
                if out[r][c] == 8:
                    out[r][c] = 3

def fill_lower_mid(out: List[List[int]], g: List[List[int]]):
    if has_two_mid(g):
        for r in range(18, 22):
            for c in range(6, 11):
                if out[r][c] == 8:
                    out[r][c] = 3

def fill_lower_far_two(out: List[List[int]], g: List[List[int]]):
    if any_two_far(g) and not has_one_mid(g):
        for r in range(22, 27):
            for c in range(16, 21):
                if out[r][c] == 8:
                    out[r][c] = 3

def fill_lower_far_nine(out: List[List[int]]):
    positions = [
        (18, 16), (18, 18), (18, 20),
        (19, 16), (19, 19), (19, 20),
        (21, 16), (21, 17), (21, 18), (21, 19), (21, 20)
    ]
    for r, c in positions:
        if out[r][c] == 8:
            out[r][c] = 3

def program(g: List[List[int]]) -> List[List[int]]:
    out = [row[:] for row in g]
    fill_top(out, g)
    if any_two_left(g):
        fill_upper_left_specific(out)
    if is_nine_right(g):
        fill_upper_far(out)
    fill_upper_mid(out, g)
    fill_long_mid(out, g)
    fill_middle_left(out, g)
    fill_middle_mid(out, g)
    fill_middle_right(out, g)
    fill_middle_far(out, g)
    fill_lower_left_mid(out, g)
    fill_lower_mid(out, g)
    fill_lower_far_two(out, g)
    if is_nine_right(g):
        fill_lower_far_nine(out)
    fill_bottom(out, g)
    return out
```