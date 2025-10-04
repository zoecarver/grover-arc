```python
from typing import List

def program(g: List[List[int]]) -> List[List[int]]:
    out = [row[:] for row in g]

    def full_zero_left() -> bool:
        return all(out[r][c] == 0 for r in range(1, 4) for c in range(2, 5))

    def has_zero_top() -> bool:
        return any(out[r][c] == 0 for r in range(1, 4) for c in range(22))

    def has_one_top() -> bool:
        return any(out[r][c] == 1 for r in range(1, 4) for c in range(22))

    def has_one_mid() -> bool:
        return any(out[r][c] == 1 for r in range(1, 4) for c in range(7, 11))

    def has_seven_right() -> bool:
        return any(out[r][c] == 7 for r in range(1, 4) for c in range(12, 16))

    def is_nine_right() -> bool:
        non_eight = [out[r][c] for r in range(1, 4) for c in range(12, 16) if out[r][c] != 8]
        return len(non_eight) > 0 and all(x == 9 for x in non_eight)

    def any_two_left() -> bool:
        return any(out[r][c] == 2 for r in range(1, 4) for c in range(2, 5))

    def any_two_far() -> bool:
        return any(out[r][c] == 2 for r in range(1, 4) for c in range(17, 21))

    def any_two_top() -> bool:
        return any(out[r][c] == 2 for r in range(1, 4) for c in range(22))

    def fill_rect(rs: int, re: int, cs: int, ce: int, val: int) -> None:
        for r in range(rs, re + 1):
            for c in range(cs, ce + 1):
                if out[r][c] == 8:
                    out[r][c] = val

    # Rule: Fill top band if zero and one in top clues
    if has_zero_top() and has_one_top():
        fill_rect(0, 4, 0, 21, 3)

    # Rule: Fill bottom band to 3 if zero and one in top clues, else to 2
    if has_zero_top() and has_one_top():
        fill_rect(28, 29, 0, 21, 3)
    else:
        fill_rect(28, 29, 0, 21, 2)

    # Rule: Upper left fill if any two left
    if any_two_left():
        fill_rect(7, 11, 1, 6, 3)

    # Rule: Upper far fill if nine right
    if is_nine_right():
        fill_rect(7, 11, 16, 20, 3)

    # Rule: Middle left fill if full zero left
    if full_zero_left():
        fill_rect(12, 17, 1, 6, 3)

    # Rule: Middle mid fill if one mid
    if has_one_mid():
        fill_rect(12, 17, 6, 10, 3)

    # Rule: Middle right fill if seven right
    if has_seven_right():
        fill_rect(12, 17, 11, 20, 3)

    # Rule: Upper mid extension if one mid and two far
    if has_one_mid() and any_two_far():
        fill_rect(7, 11, 6, 10, 3)

    # Rule: Lower left fill if any two left
    if any_two_left():
        fill_rect(18, 22, 1, 6, 3)

    # Rule: Lower mid fill if any two top
    if any_two_top():
        fill_rect(18, 22, 6, 10, 3)

    # Rule: Lower far fill if two far and not one mid
    if any_two_far() and not has_one_mid():
        fill_rect(22, 26, 16, 20, 3)

    return out
```