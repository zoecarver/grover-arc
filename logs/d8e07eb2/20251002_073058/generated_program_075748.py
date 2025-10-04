```python
import typing
List = typing.List

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
    return len(set(non_eight)) == 1 and non_eight and non_eight[0] == 9

def any_two_left(g: List[List[int]]) -> bool:
    return any(g[r][c] == 2 for r in range(1, 4) for c in range(2, 5))

def any_two_mid(g: List[List[int]]) -> bool:
    return any(g[r][c] == 2 for r in range(1, 4) for c in range(7, 10))

def any_two_right(g: List[List[int]]) -> bool:
    return any(g[r][c] == 2 for r in range(1, 4) for c in range(12, 15))

def any_two_far(g: List[List[int]]) -> bool:
    return any(g[r][c] == 2 for r in range(1, 4) for c in range(17, 21))

def any_two_top(g: List[List[int]]) -> bool:
    return any_two_left(g) or any_two_mid(g) or any_two_right(g) or any_two_far(g)

def any_four_mid(g: List[List[int]]) -> bool:
    return any(g[r][c] == 4 for r in range(1, 4) for c in range(7, 10))

def is_full_block_left(g: List[List[int]]) -> bool:
    non_eight = [g[r][c] for r in range(1, 4) for c in range(2, 5) if g[r][c] != 8]
    return len(non_eight) == 9 and len(set(non_eight)) <= 1

def fill_top(g: List[List[int]], out: List[List[int]]):
    if has_zero_top(g) and has_one_top(g):
        for r in range(5):
            for c in range(22):
                if out[r][c] == 8:
                    out[r][c] = 3

def fill_bottom(g: List[List[int]], out: List[List[int]]):
    fill_color = 3 if has_zero_top(g) and has_one_top(g) else 2
    for r in [28, 29]:
        for c in range(22):
            out[r][c] = fill_color

def fill_middle_band(g: List[List[int]], out: List[List[int]]):
    for r in range(12, 17):
        for c in range(22):
            if out[r][c] != 8:
                continue
            if full_zero_left(g) and 1 <= c <= 5:
                out[r][c] = 3
            if has_one_mid(g) and 6 <= c <= 10:
                out[r][c] = 3
            if has_seven_right(g) and 11 <= c <= 20:
                out[r][c] = 3

def vertical_middle_fill(g: List[List[int]], out: List[List[int]]):
    if has_one_mid(g) and any_two_far(g):
        for r in range(8, 27):
            for c in range(6, 11):
                if out[r][c] == 8:
                    out[r][c] = 3

def vertical_far_fill(g: List[List[int]], out: List[List[int]]):
    if is_nine_right(g):
        for r in range(8, 12):
            for c in range(16, 21):
                if out[r][c] == 8:
                    out[r][c] = 3
        for r in range(17, 22):
            for c in range(16, 21):
                if out[r][c] == 8:
                    out[r][c] = 3

def upper_left_fill(g: List[List[int]], out: List[List[int]]):
    if any_two_left(g):
        for r in range(7, 12):
            for c in range(1, 6):
                if out[r][c] == 8:
                    out[r][c] = 3

def lower_left_fill(g: List[List[int]], out: List[List[int]]):
    if any_four_mid(g):
        for r in range(18, 23):
            for c in range(1, 6):
                if out[r][c] == 8:
                    out[r][c] = 3

def lower_middle_fill(g: List[List[int]], out: List[List[int]]):
    if any_two_top(g) and not (has_one_mid(g) and any_two_far(g)):
        for r in range(18, 22):
            for c in range(6, 11):
                if out[r][c] == 8:
                    out[r][c] = 3
        if not is_full_block_left(g):
            for c in range(6, 11):
                if out[22][c] == 8:
                    out[22][c] = 3

def bottom_far_fill(g: List[List[int]], out: List[List[int]]):
    any_two_right_or_far = any_two_right(g) or any_two_far(g)
    if any_two_right_or_far and not (has_one_mid(g) and any_two_far(g)):
        for r in range(23, 27):
            for c in range(16, 21):
                if out[r][c] == 8:
                    out[r][c] = 3

def program(g: List[List[int]]) -> List[List[int]]:
    out = [row[:] for row in g]
    fill_top(g, out)
    fill_bottom(g, out)
    fill_middle_band(g, out)
    vertical_middle_fill(g, out)
    vertical_far_fill(g, out)
    upper_left_fill(g, out)
    lower_left_fill(g, out)
    lower_middle_fill(g, out)
    bottom_far_fill(g, out)
    return out
```