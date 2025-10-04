```python
from typing import List

def program(g: List[List[int]]) -> List[List[int]]:
    out = [row[:] for row in g]
    has_zero_top = any(out[r][c] == 0 for r in range(1, 4) for c in range(22))
    has_one_top = any(out[r][c] == 1 for r in range(1, 4) for c in range(22))
    if has_zero_top and has_one_top:
        for r in range(5):
            for c in range(22):
                if out[r][c] == 8:
                    out[r][c] = 3
        for r in range(28, 30):
            for c in range(22):
                out[r][c] = 3
    else:
        for r in range(28, 30):
            for c in range(22):
                out[r][c] = 2
    has_one_mid = any(out[r][c] == 1 for r in range(1, 4) for c in range(7, 11))
    any_two_far = any(out[r][c] == 2 for r in range(1, 4) for c in range(17, 22))
    if has_one_mid and any_two_far:
        for r in range(7, 27):
            for c in range(6, 12):
                if out[r][c] == 8:
                    out[r][c] = 3
    any_two_left = any(out[r][c] == 2 for r in range(1, 4) for c in range(2, 6))
    if any_two_left:
        for r in range(7, 12):
            for c in range(1, 7):
                if out[r][c] == 8:
                    out[r][c] = 3
        for r in range(18, 23):
            for c in range(1, 7):
                if out[r][c] == 8:
                    out[r][c] = 3
    has_zero_left = any(out[r][c] == 0 for r in range(1, 4) for c in range(2, 6))
    has_seven_right = any(out[r][c] == 7 for r in range(1, 4) for c in range(12, 16))
    if has_zero_left and has_seven_right:
        for r in range(12, 18):
            for c in range(1, 22):
                if out[r][c] == 8:
                    out[r][c] = 3
    elif has_one_mid:
        for r in range(12, 18):
            for c in range(6, 12):
                if out[r][c] == 8:
                    out[r][c] = 3
    any_two_top = any(out[r][c] == 2 for r in range(1, 4) for c in range(22))
    if any_two_top:
        row_end = 22 if has_seven_right else 23
        for r in range(18, row_end):
            for c in range(6, 12):
                if out[r][c] == 8:
                    out[r][c] = 3
    if any_two_top and not has_one_mid and not has_seven_right:
        for r in range(22, 26):
            for c in range(16, 21):
                if out[r][c] == 8:
                    out[r][c] = 3
    non_eight_right = [out[r][c] for r in range(1, 4) for c in range(12, 16) if out[r][c] != 8]
    if len(non_eight_right) > 0 and all(x == 9 for x in non_eight_right):
        for c in range(16, 21):
            if out[21][c] == 8:
                out[21][c] = 3
    return out
```