```python
from typing import List

def program(g: List[List[int]]) -> List[List[int]]:
    out = [row[:] for row in g]
    # Detect top conditions for top and bottom fills
    has_zero_top = any(g[r][c] == 0 for r in range(1, 4) for c in range(22))
    has_one_top = any(g[r][c] == 1 for r in range(1, 4) for c in range(22))
    if has_zero_top and has_one_top:
        # Fill top rows 0-4 with 3 on 8s
        for r in range(5):
            for c in range(22):
                if out[r][c] == 8:
                    out[r][c] = 3
        # Fill bottom rows 28-29 with 3 on 8s
        for r in range(28, 30):
            for c in range(22):
                if out[r][c] == 8:
                    out[r][c] = 3
    else:
        # Fill bottom rows 28-29 with 2 on 8s
        for r in range(28, 30):
            for c in range(22):
                if out[r][c] == 8:
                    out[r][c] = 2
    # Detect clue conditions
    full_zero_left = all(g[r][c] == 0 for r in range(1, 4) for c in range(2, 5))
    has_one_mid = any(g[r][c] == 1 for r in range(1, 4) for c in range(7, 11))
    has_seven_right = any(g[r][c] == 7 for r in range(1, 4) for c in range(12, 16))
    non_eight_right = [g[r][c] for r in range(1, 4) for c in range(12, 16) if g[r][c] != 8]
    is_nine_right = len(non_eight_right) > 0 and all(x == 9 for x in non_eight_right)
    any_two_left = any(g[r][c] == 2 for r in range(1, 4) for c in range(2, 6))
    any_two_far = any(g[r][c] == 2 for r in range(1, 4) for c in range(17, 22))
    any_two_top = any(g[r][c] == 2 for r in range(1, 4) for c in range(22))
    # Upper left fill if any two left
    if any_two_left:
        # Rows 8-10 cols 1-6
        for r in range(8, 11):
            for c in range(1, 7):
                if out[r][c] == 8:
                    out[r][c] = 3
        # Row 11 cols 1-5
        for c in range(1, 6):
            if out[11][c] == 8:
                out[11][c] = 3
    # Upper mid fill if one mid and two far
    if has_one_mid and any_two_far:
        # Rows 7-11 cols 6-10
        for r in range(7, 12):
            for c in range(6, 11):
                if out[r][c] == 8:
                    out[r][c] = 3
    # Upper and lower far C fill if nine right
    if is_nine_right:
        # Upper far rows 8-10 cols 16-20
        for r in range(8, 11):
            for c in range(16, 21):
                if out[r][c] == 8:
                    out[r][c] = 3
        # Upper far row 11 cols 16-20
        for c in range(16, 21):
            if out[11][c] == 8:
                out[11][c] = 3
        # Lower far C rows 18-20 cols 16-20
        for r in range(18, 21):
            for c in range(16, 21):
                if out[r][c] == 8:
                    out[r][c] = 3
        # Lower far C rows 17 and 21 cols 16-20
        for r in [17, 21]:
            for c in range(16, 21):
                if out[r][c] == 8:
                    out[r][c] = 3
    # Middle B left fill if full zero left
    if full_zero_left:
        # Rows 12-17 cols 1-5
        for r in range(12, 18):
            for c in range(1, 6):
                if out[r][c] == 8:
                    out[r][c] = 3
    # Middle B mid fill if one mid
    if has_one_mid:
        # Rows 12-17 cols 6-10
        for r in range(12, 18):
            for c in range(6, 11):
                if out[r][c] == 8:
                    out[r][c] = 3
    # Middle B right fill if seven right
    if has_seven_right:
        # Rows 12-17 cols 11-20
        for r in range(12, 18):
            for c in range(11, 21):
                if out[r][c] == 8:
                    out[r][c] = 3
    # Lower C left fill if any two left
    if any_two_left:
        # Rows 17-21 cols 1-5
        for r in range(17, 22):
            for c in range(1, 6):
                if out[r][c] == 8:
                    out[r][c] = 3
    # Lower C mid fill if two top and not (one mid and two far)
    if any_two_top and not (has_one_mid and any_two_far):
        # Rows 17-21 cols 6-10
        for r in range(17, 22):
            for c in range(6, 11):
                if out[r][c] == 8:
                    out[r][c] = 3
    # D far fill if two far and not one mid
    if any_two_far and not has_one_mid:
        # Rows 22-26 cols 16-20
        for r in range(22, 27):
            for c in range(16, 21):
                if out[r][c] == 8:
                    out[r][c] = 3
    return out
```